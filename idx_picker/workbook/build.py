"""Build PERSONAL_STOCKS_PICKER.xlsx -- a value-investing screener workbook that
recalculates *identically* in Microsoft Excel and Google Sheets.

Why this file looks the way it does
-----------------------------------
The workbook it replaces was Google-Sheets-native: it leaned on ``QUERY``,
``FILTER``, ``SORT``, ``ARRAYFORMULA`` and ``TEXTJOIN``.  None of those exist in
Excel (or exist with different semantics), so the sheet was dead on arrival for
anyone opening it in Excel.  The portability rules we hold ourselves to here:

*   **Allowed vocabulary only.**  INDEX, MATCH, VLOOKUP, IF, IFERROR, AND, OR,
    NOT, SUM, SUMIF(S), COUNT, COUNTA, COUNTIF(S), AVERAGE, AVERAGEIF, MEDIAN,
    MIN, MAX, LARGE, SMALL, RANK, ABS, ROUND, PERCENTILE, TEXT, CONCATENATE/&,
    LEFT, RIGHT, MID, LEN, NA, ISNUMBER, ISBLANK, ISTEXT.  Nothing else.
*   **No dynamic arrays.**  ``SORT``/``FILTER``/``UNIQUE`` are banned, so any
    "top N" or "cheapest N" table is *ordered in Python at build time* and the
    chosen tickers are written as static text into a rank column.  Every other
    cell on that row is a live ``INDEX``/``MATCH`` against the Screener, so the
    displayed figures track the underlying data even though the membership of
    the list is a build-time snapshot.  Re-running this builder refreshes the
    membership.
*   **INDEX/MATCH, not VLOOKUP.**  VLOOKUP addresses a column by ordinal offset,
    so inserting a column in a RAW sheet silently returns the wrong field.
    INDEX/MATCH addresses ranges directly and fails loudly instead.
*   **Bounded ranges.**  Never ``A:A``.  Google Sheets recalculates whole-column
    references across all 131 statistics columns catastrophically slowly.  Every
    range stops at the real last data row, computed from the CSV at build time.
*   **One MATCH per row per source.**  A row of 30 lookups against the same RAW
    sheet would otherwise evaluate MATCH 30 times.  Each row instead carries a
    hidden helper column holding ``MATCH(ticker, keys, 0)`` once; the visible
    cells are ``INDEX(range, $HELPER<row>)``.  Same functions, a fraction of the
    work, and much shorter formulas.
*   **Blank-vs-zero.**  ``INDEX`` over an empty cell returns 0, which would
    render a missing PE as "0.0x".  Numeric pulls are therefore wrapped as
    ``IF(ISBLANK(INDEX(...)),"",INDEX(...))`` -- ISBLANK is on the allowed list
    and behaves the same in Excel, Sheets and LibreOffice.

Usage
-----
    python3 -m idx_picker.workbook.build \
        --input-dir idx_picker/output \
        --output idx_picker/output/PERSONAL_STOCKS_PICKER.xlsx
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

# --------------------------------------------------------------------------
# Style vocabulary
# --------------------------------------------------------------------------

FONT_NAME = "Arial"

CLR_INPUT = "FF0000FF"     # blue   -- hardcoded inputs / scenario levers
CLR_FORMULA = "FF000000"   # black  -- formulas within a sheet
CLR_LINK = "FF008000"      # green  -- links to another sheet
CLR_BAD = "FF9C0006"       # dark red text
CLR_MUTED = "FF7F7F7F"

FILL_INPUT = PatternFill("solid", fgColor="FFFFFF00")      # yellow: user edits here
FILL_HEADER = PatternFill("solid", fgColor="FF1F3864")     # dark navy header
FILL_BAND = PatternFill("solid", fgColor="FFD9E1F2")       # light blue section band
FILL_BUY = PatternFill("solid", fgColor="FFC6EFCE")        # green
FILL_WATCH = PatternFill("solid", fgColor="FFFFEB9C")      # amber
FILL_SKIP = PatternFill("solid", fgColor="FFE7E6E6")       # grey
FILL_DEEP = PatternFill("solid", fgColor="FFBDD7EE")       # blue
FILL_STALE = PatternFill("solid", fgColor="FFFCE4D6")

F_BASE = Font(name=FONT_NAME, size=10)
F_BOLD = Font(name=FONT_NAME, size=10, bold=True)
F_TITLE = Font(name=FONT_NAME, size=16, bold=True, color="FF1F3864")
F_SUB = Font(name=FONT_NAME, size=10, italic=True, color=CLR_MUTED)
F_SECTION = Font(name=FONT_NAME, size=11, bold=True, color="FF1F3864")
F_HEADER = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFFFF")
F_INPUT = Font(name=FONT_NAME, size=10, bold=True, color=CLR_INPUT)
F_LINK = Font(name=FONT_NAME, size=10, color=CLR_LINK)
F_NOTE = Font(name=FONT_NAME, size=9, italic=True, color=CLR_MUTED)

THIN = Side(style="thin", color="FFBFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# Number formats.  Percentages are stored as fractions (0.15 -> "15.0%").
FMT_TEXT = "@"
FMT_CUR = "#,##0;(#,##0);-"
FMT_CUR2 = "#,##0.00;(#,##0.00);-"
FMT_PCT = "0.0%"
FMT_MULT = '0.0"x"'
FMT_SCORE = "0.0"
FMT_INT = "0"

# Column-format shorthand used by the sheet specs below.
KIND_FMT = {
    "text": FMT_TEXT,
    "cur": FMT_CUR,
    "cur2": FMT_CUR2,
    "pct": FMT_PCT,
    "mult": FMT_MULT,
    "score": FMT_SCORE,
    "int": FMT_INT,
}


# --------------------------------------------------------------------------
# RAW sheet plumbing
# --------------------------------------------------------------------------


@dataclass
class RawTable:
    """A CSV dumped verbatim onto a worksheet, addressable by column name.

    Everything downstream builds its A1 ranges through this object so that a
    column moving inside the scraper's CSV output changes exactly one thing:
    the letter this class hands back.
    """

    sheet: str
    df: pd.DataFrame
    key_col: str = "Ticker"

    @property
    def nrows(self) -> int:
        return len(self.df)

    @property
    def first_row(self) -> int:
        return 2  # headers occupy row 1

    @property
    def last_row(self) -> int:
        # Guard the degenerate empty-CSV case so ranges stay syntactically legal.
        return max(2, self.nrows + 1)

    def letter(self, column: str) -> str:
        try:
            return get_column_letter(self.df.columns.get_loc(column) + 1)
        except KeyError as exc:  # pragma: no cover - surfaces a scraper contract break
            raise KeyError(
                f"{self.sheet}: expected column {column!r}; available: "
                f"{list(self.df.columns)[:10]}..."
            ) from exc

    def col_range(self, column: str) -> str:
        col = self.letter(column)
        return f"{self.sheet}!${col}${self.first_row}:${col}${self.last_row}"

    def key_range(self) -> str:
        return self.col_range(self.key_col)

    def match(self, key_expr: str) -> str:
        return f"MATCH({key_expr},{self.key_range()},0)"

    # -- formula factories -------------------------------------------------

    def row_index_formula(self, key_cell: str) -> str:
        """Helper-cell formula: the row offset of `key_cell` inside this table."""
        return f"={self.match(key_cell)}"

    def by_index(self, column: str, idx_cell: str, scale: float | None = None) -> str:
        """Pull `column` using a pre-computed row offset held in `idx_cell`.

        Blank source cells come back as "" rather than 0 -- see module docstring.
        """
        rng = self.col_range(column)
        val = f"INDEX({rng},{idx_cell})"
        if scale is not None:
            val = f"{val}/{scale:.0f}"
        return f'=IFERROR(IF(ISBLANK(INDEX({rng},{idx_cell})),"",{val}),"")'

    def by_key(self, column: str, key_cell: str, scale: float | None = None) -> str:
        """Pull `column` doing the MATCH inline (for one-off cells)."""
        rng = self.col_range(column)
        m = self.match(key_cell)
        val = f"INDEX({rng},{m})"
        if scale is not None:
            val = f"{val}/{scale:.0f}"
        return f'=IFERROR(IF(ISBLANK(INDEX({rng},{m})),"",{val}),"")'


# --------------------------------------------------------------------------
# Small writing helpers
# --------------------------------------------------------------------------


def put(
    ws: Worksheet,
    ref: str,
    value,
    font: Font | None = None,
    fill: PatternFill | None = None,
    fmt: str | None = None,
    align: str | None = None,
    wrap: bool = False,
    border: bool = False,
):
    cell = ws[ref]
    cell.value = value
    cell.font = font or F_BASE
    if fill is not None:
        cell.fill = fill
    if fmt is not None:
        cell.number_format = fmt
    if align or wrap:
        cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if border:
        cell.border = BOX
    return cell


def title_block(ws: Worksheet, title: str, subtitle: str, width: int = 12):
    put(ws, "A1", title, font=F_TITLE)
    put(ws, "A2", subtitle, font=F_SUB)


def section(ws: Worksheet, row: int, text: str, span: int):
    """A shaded band used as a visual section header."""
    for col in range(1, span + 1):
        c = ws.cell(row=row, column=col)
        c.fill = FILL_BAND
        c.font = F_SECTION
        c.border = BOX
    ws.cell(row=row, column=1).value = text


def header_row(ws: Worksheet, row: int, headers: Sequence[str], start_col: int = 1):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i)
        c.value = h
        c.font = F_HEADER
        c.fill = FILL_HEADER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX


def set_widths(ws: Worksheet, widths: dict[str, float]):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def cell_value(v):
    """Coerce a pandas value into something openpyxl will accept."""
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, (bool,)):
        # Written as text so that COUNTIF(range,"TRUE") behaves the same in
        # Excel and Sheets; a real boolean compares differently in each.
        return "TRUE" if v else "FALSE"
    if hasattr(v, "item"):  # numpy scalar
        try:
            v = v.item()
        except Exception:  # pragma: no cover
            return str(v)
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, pd.Timestamp):
        return v.strftime("%Y-%m-%d")
    return v


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------

CSV_FILES = {
    "RAW_idx_stocks": "RAW_idx_stocks.csv",
    "RAW_key_statistics": "RAW_key_statistics.csv",
    "RAW_analyses": "RAW_analyses.csv",
    "RAW_scores": "RAW_scores.csv",
    "RAW_history_quarterly": "RAW_history_quarterly.csv",
    "RAW_history_annual": "RAW_history_annual.csv",
}

HISTORY_SHEETS = ("RAW_history_quarterly", "RAW_history_annual")

KEY_COL = "Key (Ticker|Period End)"
RECENCY_COL = "Recency Key (Ticker|Rn)"


def load_inputs(input_dir: str) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for sheet, fname in CSV_FILES.items():
        path = os.path.join(input_dir, fname)
        if not os.path.exists(path):
            raise FileNotFoundError(f"missing input CSV: {path}")
        # keep_default_na leaves genuine text intact while blanks become NaN
        df = pd.read_csv(path)
        frames[sheet] = df

    for sheet in HISTORY_SHEETS:
        df = frames[sheet]
        df["Period End"] = df["Period End"].astype(str)
        # Spec-mandated composite key: two-condition lookups without array
        # formulas need a single concatenated key to MATCH against.
        df[KEY_COL] = df["Ticker"].astype(str) + "|" + df["Period End"]
        # Second key: R1 = most recent period for that ticker, R2 = next, ...
        # This lets the Company sheet ask for "the last four years" without
        # knowing how many periods any given ticker actually has.
        rank = (
            df.groupby("Ticker")["Period End"]
            .rank(method="first", ascending=False)
            .astype(int)
        )
        df[RECENCY_COL] = df["Ticker"].astype(str) + "|R" + rank.astype(str)
        frames[sheet] = df

    return frames


# --------------------------------------------------------------------------
# RAW sheets
# --------------------------------------------------------------------------


def build_raw_sheet(ws: Worksheet, df: pd.DataFrame):
    ws.append([str(c) for c in df.columns])
    for c in ws[1]:
        c.font = F_HEADER
        c.fill = FILL_HEADER
    for row in df.itertuples(index=False, name=None):
        ws.append([cell_value(v) for v in row])
    ws.freeze_panes = "B2"
    # Readable-but-not-huge widths; RAW sheets are lookup targets, not reading material.
    for i, col in enumerate(df.columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = min(
            max(11, len(str(col)) + 2), 34
        )


# --------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------

# (row, label, value, format, consumed-by note).  Row numbers are fixed because
# every other sheet hardcodes these addresses.
SETUP_ROWS = [
    (4, "Tax Rate", 0.22, FMT_PCT,
     "Company!EPV cross-check (NOPAT = Normalised EBIT x (1 - Tax Rate))"),
    (5, "WACC (discount rate)", 0.12, FMT_PCT,
     "Scenario!B13 discount rate; Sensitivity (both grids, via Scenario); Company!EPV cross-check"),
    (6, "Terminal Growth", 0.03, FMT_PCT,
     "Scenario!B12 terminal growth + growth fade; Sensitivity grid axes"),
    (7, "Risk Free Rate", 0.065, FMT_PCT,
     "Company!Cost of equity (CAPM) = RF + Beta x ERP"),
    (8, "Equity Risk Premium", 0.055, FMT_PCT,
     "Company!Cost of equity (CAPM)"),
    (9, "MOS Buy threshold", 0.30, FMT_PCT,
     "Dashboard!count above buy MOS; Company!verdict test; Scenario!verdict test"),
    (10, "MOS Watch threshold", 0.10, FMT_PCT,
     "Dashboard!count above watch MOS; Company!verdict test; Scenario!verdict test"),
]

SETUP = {
    "tax": "Setup!$B$4",
    "wacc": "Setup!$B$5",
    "tg": "Setup!$B$6",
    "rf": "Setup!$B$7",
    "erp": "Setup!$B$8",
    "mos_buy": "Setup!$B$9",
    "mos_watch": "Setup!$B$10",
}


def build_setup(ws: Worksheet):
    title_block(ws, "SETUP — Model Assumptions", "Every value below is referenced by "
                "formulas elsewhere in this workbook. Change one and the model moves.")
    header_row(ws, 3, ["Assumption", "Value", "Consumed by"])
    for row, label, value, fmt, consumers in SETUP_ROWS:
        put(ws, f"A{row}", label, font=F_BOLD, border=True)
        put(ws, f"B{row}", value, font=F_INPUT, fill=FILL_INPUT, fmt=fmt,
            align="center", border=True)
        put(ws, f"C{row}", consumers, font=F_BASE, border=True, wrap=True)

    put(ws, "A12", "Yellow cells with blue text are inputs — edit them directly.",
        font=F_NOTE)
    put(ws, "A13", "Black text = formula on the same sheet. Green text = link to "
        "another sheet in this workbook.", font=F_NOTE)
    put(ws, "A14", "Formula portability: this workbook uses only functions that "
        "behave identically in Microsoft Excel and Google Sheets "
        "(INDEX/MATCH rather than XLOOKUP/FILTER/QUERY).", font=F_NOTE)
    set_widths(ws, {"A": 28, "B": 14, "C": 96})
    ws.freeze_panes = "A4"


# --------------------------------------------------------------------------
# Screener
# --------------------------------------------------------------------------

# (header, source-table key, source column, kind, optional scale divisor)
SCREENER_SPEC: list[tuple] = [
    ("Ticker", None, None, "text", None),
    ("Name", "sc", "Name", "text", None),
    ("Sector", "sc", "Sector", "text", None),
    ("Business Type", "sc", "Business Type", "text", None),
    ("Price", "st", "Price", "cur2", None),
    ("Market Cap (IDR bn)", "ks", "Market Cap", "cur", 1_000_000_000),
    ("PE (TTM)", "ks", "Current PE Ratio (TTM)", "mult", None),
    ("PB", "ks", "Current Price to Book Value", "mult", None),
    ("EV/EBIT", "ks", "EV to EBIT (TTM)", "mult", None),
    ("EV/EBITDA", "ks", "EV to EBITDA (TTM)", "mult", None),
    ("Div Yield", "ks", "Dividend Yield", "pct", None),
    ("ROE", "ks", "Return on Equity (TTM)", "pct", None),
    ("ROIC", "ks", "Return On Invested Capital (TTM)", "pct", None),
    ("ROC (Greenblatt)", "ks", "ROC Greenblatt", "pct", None),
    ("Earnings Yield (EBIT/EV)", "ks", "Earnings Yield Greenblatt (EBIT/EV)", "pct", None),
    ("FCF Yield", "ks", "FCF Yield (TTM)", "pct", None),
    ("F-Score", "ks", "Piotroski F-Score", "int", None),
    ("Altman Z", "ks", "Altman Z-Score (Modified)", "score", None),
    ("Current Ratio", "ks", "Current Ratio (Quarter)", "mult", None),
    ("Net Debt/Equity", "an", "Net Debt to Equity", "mult", None),
    ("Rev CAGR 3Y", "ks", "Revenue CAGR 3Y", "pct", None),
    ("NCAV/share", "ks", "NCAV per Share", "cur2", None),
    ("Net-Net Pass", "ks", "Net-Net Pass", "text", None),
    ("EPV/share", "ks", "EPV per Share", "cur2", None),
    ("IV Bear", "sc", "IV Bear", "cur2", None),
    ("IV Base", "sc", "IV Base", "cur2", None),
    ("IV Bull", "sc", "IV Bull", "cur2", None),
    ("Blended IV", "sc", "Blended IV", "cur2", None),
    ("MOS", "sc", "MOS Blended", "pct", None),
    ("Upside", "sc", "Upside Blended", "pct", None),
    ("Quality", "sc", "Quality Score", "score", None),
    ("Safety", "sc", "Safety Score", "score", None),
    ("Value", "sc", "Value Score", "score", None),
    ("Composite", "sc", "Composite Score", "score", None),
    ("Verdict", "sc", "Verdict", "text", None),
    ("Quarters Stale", "sc", "Quarters Stale", "score", None),
    ("Red Flags", "sc", "Red Flags", "text", None),
]

# Hidden helper columns: one MATCH per row per RAW table (see module docstring).
HELPER_SPEC = [
    ("_row in RAW_key_statistics", "ks"),
    ("_row in RAW_scores", "sc"),
    ("_row in RAW_idx_stocks", "st"),
    ("_row in RAW_analyses", "an"),
]

SCREENER_WIDTHS = {
    "Ticker": 10, "Name": 34, "Sector": 22, "Business Type": 14, "Price": 12,
    "Market Cap (IDR bn)": 17, "PE (TTM)": 10, "PB": 9, "EV/EBIT": 10,
    "EV/EBITDA": 11, "Div Yield": 11, "ROE": 10, "ROIC": 10,
    "ROC (Greenblatt)": 16, "Earnings Yield (EBIT/EV)": 20, "FCF Yield": 11,
    "F-Score": 9, "Altman Z": 10, "Current Ratio": 13, "Net Debt/Equity": 15,
    "Rev CAGR 3Y": 12, "NCAV/share": 12, "Net-Net Pass": 12, "EPV/share": 12,
    "IV Bear": 12, "IV Base": 12, "IV Bull": 12, "Blended IV": 13, "MOS": 10,
    "Upside": 10, "Quality": 9, "Safety": 9, "Value": 9, "Composite": 11,
    "Verdict": 13, "Quarters Stale": 14, "Red Flags": 44,
}


class ScreenerMap:
    """Column letters of the Screener, so other sheets can address it by name."""

    def __init__(self, nrows: int):
        self.letters = {
            h: get_column_letter(i + 1) for i, (h, *_rest) in enumerate(SCREENER_SPEC)
        }
        self.nrows = nrows
        self.first_row = 2
        self.last_row = max(2, nrows + 1)

    def col(self, header: str) -> str:
        return self.letters[header]

    def rng(self, header: str) -> str:
        c = self.col(header)
        return f"Screener!${c}${self.first_row}:${c}${self.last_row}"

    def key_range(self) -> str:
        return self.rng("Ticker")

    def lookup(self, header: str, key_cell: str) -> str:
        rng = self.rng(header)
        m = f"MATCH({key_cell},{self.key_range()},0)"
        return f'=IFERROR(IF(ISBLANK(INDEX({rng},{m})),"",INDEX({rng},{m})),"")'


def build_screener(ws: Worksheet, raw: dict[str, RawTable], smap: ScreenerMap):
    tickers = raw["RAW_scores"].df["Ticker"].astype(str).tolist()
    src = {
        "ks": raw["RAW_key_statistics"],
        "sc": raw["RAW_scores"],
        "st": raw["RAW_idx_stocks"],
        "an": raw["RAW_analyses"],
    }

    headers = [h for h, *_ in SCREENER_SPEC]
    n_visible = len(headers)
    helper_headers = [h for h, _ in HELPER_SPEC]
    header_row(ws, 1, headers + helper_headers)

    helper_letter = {
        key: get_column_letter(n_visible + i + 1) for i, (_h, key) in enumerate(HELPER_SPEC)
    }

    for r, ticker in enumerate(tickers, start=2):
        # Static anchor: the ticker itself.  Everything else on the row is live.
        put(ws, f"A{r}", ticker, font=F_INPUT, fmt=FMT_TEXT)

        # Helper MATCHes first -- one per source table for the whole row.
        for key, table_key in HELPER_SPEC:
            table = src[table_key]
            letter = helper_letter[table_key]
            ws[f"{letter}{r}"] = f'=IFERROR({table.match(f"$A{r}")},"")'
            ws[f"{letter}{r}"].font = F_BASE

        for i, (header, table_key, column, kind, scale) in enumerate(SCREENER_SPEC):
            if table_key is None:
                continue
            col = get_column_letter(i + 1)
            table = src[table_key]
            idx_cell = f"${helper_letter[table_key]}{r}"
            cell = ws[f"{col}{r}"]
            cell.value = table.by_index(column, idx_cell, scale=scale)
            cell.font = F_LINK  # green: this value lives on another sheet
            cell.number_format = KIND_FMT[kind]

    last = smap.last_row

    # Hide the helper columns: correct but noisy.
    for key in helper_letter.values():
        ws.column_dimensions[key].hidden = True

    for header, width in SCREENER_WIDTHS.items():
        ws.column_dimensions[smap.col(header)].width = width

    ws.freeze_panes = "B2"
    ws.auto_filter.ref = f"A1:{get_column_letter(n_visible)}{last}"

    apply_verdict_formats(ws, f"{smap.col('Verdict')}2:{smap.col('Verdict')}{last}")
    ws.conditional_formatting.add(
        f"{smap.col('MOS')}2:{smap.col('MOS')}{last}",
        ColorScaleRule(
            start_type="num", start_value=-0.5, start_color="FFF8696B",
            mid_type="num", mid_value=0, mid_color="FFFFEB84",
            end_type="num", end_value=0.6, end_color="FF63BE7B",
        ),
    )
    # Red text across the row when the filings are more than 3 quarters old.
    stale_col = smap.col("Quarters Stale")
    ws.conditional_formatting.add(
        f"A2:{get_column_letter(n_visible)}{last}",
        FormulaRule(
            formula=[f"AND(ISNUMBER(${stale_col}2),${stale_col}2>3)"],
            font=Font(name=FONT_NAME, size=10, color="FFFF0000", bold=True),
        ),
    )


def apply_verdict_formats(ws: Worksheet, ref: str):
    for verdict, fill in (
        ("BUY", FILL_BUY),
        ("DEEP VALUE", FILL_DEEP),
        ("WATCH", FILL_WATCH),
        ("SKIP", FILL_SKIP),
    ):
        ws.conditional_formatting.add(
            ref,
            CellIsRule(operator="equal", formula=[f'"{verdict}"'], fill=fill),
        )


# --------------------------------------------------------------------------
# Dashboard
# --------------------------------------------------------------------------

TOP_IDEAS_COLS = [
    ("Rank", "int", 6),
    ("Ticker", "text", 10),
    ("Name", "text", 34),
    ("Sector", "text", 22),
    ("Business Type", "text", 14),
    ("Price", "cur2", 12),
    ("Blended IV", "cur2", 13),
    ("MOS", "pct", 10),
    ("Composite", "score", 11),
    ("Quality", "score", 9),
    ("Safety", "score", 9),
    ("Value", "score", 9),
    ("F-Score", "int", 9),
    ("Verdict", "text", 13),
]

CHEAP_COLS = [
    ("Rank", "int"),
    ("Ticker", "text"),
    ("Name", "text"),
    ("Sector", "text"),
    ("EV/EBIT", "mult"),
    ("Earnings Yield (EBIT/EV)", "pct"),
    ("ROC (Greenblatt)", "pct"),
    ("F-Score", "int"),
    ("Altman Z", "score"),
    ("Composite", "score"),
    ("Verdict", "text"),
]

NETNET_COLS = [
    ("Rank", "int"),
    ("Ticker", "text"),
    ("Name", "text"),
    ("Sector", "text"),
    ("Price", "cur2"),
    ("NCAV/share", "cur2"),
    ("Price / NCAV", "mult"),
    ("Market Cap (IDR bn)", "cur"),
    ("F-Score", "int"),
    ("Composite", "score"),
    ("Verdict", "text"),
]


def pick_top_ideas(scores: pd.DataFrame, n: int = 15) -> list[str]:
    """Highest Composite Score among BUY / DEEP VALUE names.

    Ordered here in Python because SORT/FILTER are banned; the result is written
    as static tickers and every displayed metric stays a live lookup.
    """
    mask = scores["Verdict"].astype(str).str.upper().isin(["BUY", "DEEP VALUE"])
    sub = scores[mask].sort_values("Composite Score", ascending=False)
    return sub["Ticker"].astype(str).head(n).tolist()


def pick_cheapest_am(key_stats: pd.DataFrame, n: int = 10) -> list[str]:
    """Lowest EV/EBIT with genuinely positive trailing EBIT."""
    df = key_stats
    mask = (
        df["EBIT (TTM)"].notna()
        & (df["EBIT (TTM)"] > 0)
        & df["Acquirers Multiple (EV/EBIT)"].notna()
        & (df["Acquirers Multiple (EV/EBIT)"] > 0)
    )
    sub = df[mask].sort_values("Acquirers Multiple (EV/EBIT)", ascending=True)
    return sub["Ticker"].astype(str).head(n).tolist()


def pick_net_nets(key_stats: pd.DataFrame, n: int = 10) -> list[str]:
    df = key_stats
    passes = df["Net-Net Pass"].astype(str).str.upper() == "TRUE"
    sub = df[passes].copy()
    if sub.empty:
        return []
    # Deepest discount to net current asset value first (largest NCAV cushion
    # per share relative to what the market is asking).
    sub = sub.sort_values("NCAV per Share", ascending=False)
    return sub["Ticker"].astype(str).head(n).tolist()


def build_dashboard(
    ws: Worksheet,
    raw: dict[str, RawTable],
    smap: ScreenerMap,
    top_ideas: list[str],
    cheapest: list[str],
    net_nets: list[str],
):
    ks = raw["RAW_key_statistics"]
    title_block(
        ws,
        "IDX VALUE SCREENER — DASHBOARD",
        "Every figure below is a live formula against the RAW_* sheets. "
        "Rebuild the workbook to refresh the membership of the ranked tables.",
    )

    fetched_ref = f"{ks.sheet}!${ks.letter('Fetched At')}$2"

    # ---- header block ----------------------------------------------------
    section(ws, 4, "DATA & UNIVERSE", 14)
    rows = [
        (5, "Last data refresh (Fetched At)", f"={fetched_ref}", FMT_TEXT),
        (6, "Tickers in universe", f"=COUNTA({smap.key_range()})", FMT_INT),
        (7, "Names at/above MOS Buy threshold",
         f'=COUNTIF({smap.rng("MOS")},">="&{SETUP["mos_buy"]})', FMT_INT),
        (8, "Names at/above MOS Watch threshold",
         f'=COUNTIF({smap.rng("MOS")},">="&{SETUP["mos_watch"]})', FMT_INT),
    ]
    for r, label, formula, fmt in rows:
        put(ws, f"A{r}", label, font=F_BOLD)
        put(ws, f"D{r}", formula, font=F_LINK, fmt=fmt, align="left")

    # ---- verdict split ---------------------------------------------------
    put(ws, "A10", "VERDICT SPLIT", font=F_SECTION)
    header_row(ws, 11, ["Verdict", "Count", "% of universe"])
    verdicts = ["BUY", "DEEP VALUE", "WATCH", "SKIP"]
    for i, verdict in enumerate(verdicts):
        r = 12 + i
        put(ws, f"A{r}", verdict, font=F_BOLD, border=True)
        put(ws, f"B{r}", f'=COUNTIF({smap.rng("Verdict")},"{verdict}")',
            font=F_LINK, fmt=FMT_INT, align="center", border=True)
        put(ws, f"C{r}", f'=IFERROR(B{r}/$D$6,"")', font=F_BASE, fmt=FMT_PCT,
            align="center", border=True)
    apply_verdict_formats(ws, f"A12:A{11 + len(verdicts)}")

    # ---- market context --------------------------------------------------
    put(ws, "F10", "MARKET CONTEXT (universe medians)", font=F_SECTION)
    header_row(ws, 11, ["Measure", "Value"], start_col=6)
    ctx = [
        ("Median PE (TTM)", f'=IFERROR(MEDIAN({smap.rng("PE (TTM)")}),"")', FMT_MULT),
        ("Median PB", f'=IFERROR(MEDIAN({smap.rng("PB")}),"")', FMT_MULT),
        ("Median EV/EBIT", f'=IFERROR(MEDIAN({smap.rng("EV/EBIT")}),"")', FMT_MULT),
        ("Names with F-Score >= 7", f'=COUNTIF({smap.rng("F-Score")},">=7")', FMT_INT),
        ("Names with Altman Z < 1.1", f'=COUNTIF({smap.rng("Altman Z")},"<1.1")', FMT_INT),
        ("Median MOS (blended)", f'=IFERROR(MEDIAN({smap.rng("MOS")}),"")', FMT_PCT),
    ]
    for i, (label, formula, fmt) in enumerate(ctx):
        r = 12 + i
        put(ws, f"F{r}", label, font=F_BOLD, border=True)
        put(ws, f"G{r}", formula, font=F_LINK, fmt=fmt, align="center", border=True)

    # ---- Top Ideas -------------------------------------------------------
    row = 20
    row = _ranked_table(
        ws, row,
        "TOP IDEAS — highest Composite Score among BUY / DEEP VALUE",
        TOP_IDEAS_COLS, top_ideas, 15, smap,
        note="Membership fixed at build time (SORT/FILTER are not portable); "
             "all displayed figures are live INDEX/MATCH lookups.",
    )

    row = _ranked_table(
        ws, row + 2,
        "CHEAPEST ON ACQUIRER'S MULTIPLE — lowest EV/EBIT, positive trailing EBIT only",
        CHEAP_COLS, cheapest, 10, smap,
    )

    row = _ranked_table(
        ws, row + 2,
        "GRAHAM NET-NETS — market cap below net current asset value",
        NETNET_COLS, net_nets, 10, smap,
        empty_note="No names currently pass the net-net test in this universe.",
    )

    widths = {get_column_letter(i + 1): w for i, (_h, _k, w) in enumerate(TOP_IDEAS_COLS)}
    set_widths(ws, widths)
    ws.freeze_panes = "A5"


def _ranked_table(
    ws: Worksheet,
    start_row: int,
    title: str,
    cols: Sequence[tuple],
    tickers: Sequence[str],
    n_rows: int,
    smap: ScreenerMap,
    note: str | None = None,
    empty_note: str | None = None,
) -> int:
    """Write a fixed-height ranked table.

    `tickers` is the build-time ordering.  Rows beyond the available names are
    written empty and their formulas short-circuit on the blank ticker, so the
    table keeps its shape whatever the universe size.
    """
    put(ws, f"A{start_row}", title, font=F_SECTION)
    if note:
        put(ws, f"A{start_row + 1}", note, font=F_NOTE)
        hdr = start_row + 2
    else:
        hdr = start_row + 1
    header_row(ws, hdr, [c[0] for c in cols])

    verdict_col = None
    mos_col = None
    for i, (header, *_rest) in enumerate(cols):
        if header == "Verdict":
            verdict_col = get_column_letter(i + 1)
        if header == "MOS":
            mos_col = get_column_letter(i + 1)

    for j in range(n_rows):
        r = hdr + 1 + j
        ticker = tickers[j] if j < len(tickers) else None
        put(ws, f"A{r}", j + 1, font=F_BASE, fmt=FMT_INT, align="center", border=True)
        put(ws, f"B{r}", ticker, font=F_INPUT, fmt=FMT_TEXT, align="center", border=True)
        for i, (header, kind, *_rest) in enumerate(cols):
            if i < 2:
                continue  # Rank + Ticker are the static anchors
            col = get_column_letter(i + 1)
            if header == "Price / NCAV":
                # Derived on the Dashboard from two cells already pulled above.
                formula = (
                    f'=IF(AND(ISNUMBER($E{r}),ISNUMBER($F{r}),$F{r}<>0),$E{r}/$F{r},"")'
                )
            else:
                formula = smap.lookup(header, f"$B{r}")
            put(ws, f"{col}{r}", formula, font=F_LINK, fmt=KIND_FMT[kind],
                align="center" if kind != "text" else "left", border=True)

    last = hdr + n_rows
    if verdict_col:
        apply_verdict_formats(ws, f"{verdict_col}{hdr + 1}:{verdict_col}{last}")
    if mos_col:
        ws.conditional_formatting.add(
            f"{mos_col}{hdr + 1}:{mos_col}{last}",
            ColorScaleRule(
                start_type="num", start_value=-0.5, start_color="FFF8696B",
                mid_type="num", mid_value=0, mid_color="FFFFEB84",
                end_type="num", end_value=0.6, end_color="FF63BE7B",
            ),
        )
    if empty_note and not tickers:
        put(ws, f"A{last + 1}", empty_note, font=F_NOTE)
        return last + 1
    return last


# --------------------------------------------------------------------------
# Company
# --------------------------------------------------------------------------

F_SIGNALS = [
    ("F: ROA Positive", "Return on assets positive"),
    ("F: CFO Positive", "Operating cash flow positive"),
    ("F: ROA Improving", "ROA improving year on year"),
    ("F: Accruals", "Operating cash flow exceeds net income (quality of earnings)"),
    ("F: Leverage Falling", "Long-term leverage falling"),
    ("F: Current Ratio Improving", "Current ratio improving"),
    ("F: No Dilution", "No share issuance"),
    ("F: Gross Margin Improving", "Gross margin improving"),
    ("F: Asset Turnover Improving", "Asset turnover improving"),
]

HISTORY_LINES = [
    ("Revenue", "TotalRevenue"),
    ("Gross Profit", "GrossProfit"),
    ("EBIT", "EBIT"),
    ("Net Income", "NetIncome"),
    ("Operating Cash Flow", "OperatingCashFlow"),
    ("Free Cash Flow", "FreeCashFlow"),
    ("Total Assets", "TotalAssets"),
    ("Shareholders' Equity", "StockholdersEquity"),
]

# Helper-cell addresses on the Company sheet (hidden columns N/O).
CO_IDX = {"ks": "$O$1", "sc": "$O$2", "st": "$O$3", "an": "$O$4"}
CO_TICKER = "$B$2"
CO_PRICE = "$B$9"


def build_company(ws: Worksheet, raw: dict[str, RawTable], default_ticker: str):
    ks = raw["RAW_key_statistics"]
    sc = raw["RAW_scores"]
    st = raw["RAW_idx_stocks"]
    an = raw["RAW_analyses"]
    ha = raw["RAW_history_annual"]

    title_block(
        ws,
        "COMPANY DRILLDOWN",
        "Type a ticker into B2. Everything else on this sheet recalculates from it.",
    )
    put(ws, "A2", "Ticker (INPUT)", font=F_BOLD)
    put(ws, "B2", default_ticker, font=F_INPUT, fill=FILL_INPUT, fmt=FMT_TEXT,
        align="center", border=True)
    put(ws, "C2", "<-- the ONLY input cell on this sheet", font=F_NOTE)

    # Hidden helper block: one MATCH per source table, reused by every lookup.
    put(ws, "N1", "helper: row in RAW_key_statistics", font=F_NOTE)
    put(ws, "N2", "helper: row in RAW_scores", font=F_NOTE)
    put(ws, "N3", "helper: row in RAW_idx_stocks", font=F_NOTE)
    put(ws, "N4", "helper: row in RAW_analyses", font=F_NOTE)
    for cell, table in (("O1", ks), ("O2", sc), ("O3", st), ("O4", an)):
        put(ws, cell, f'=IFERROR({table.match(CO_TICKER)},"")', font=F_BASE)
    ws.column_dimensions["N"].hidden = True
    ws.column_dimensions["O"].hidden = True

    def ksv(col, scale=None):
        return ks.by_index(col, CO_IDX["ks"], scale=scale)

    def scv(col, scale=None):
        return sc.by_index(col, CO_IDX["sc"], scale=scale)

    def stv(col, scale=None):
        return st.by_index(col, CO_IDX["st"], scale=scale)

    def anv(col, scale=None):
        return an.by_index(col, CO_IDX["an"], scale=scale)

    def label_value(row: int, label: str, formula: str, fmt: str):
        put(ws, f"A{row}", label, font=F_BOLD, border=True)
        put(ws, f"B{row}", formula, font=F_LINK, fmt=fmt, align="center", border=True)

    # ---- identity --------------------------------------------------------
    section(ws, 4, "IDENTITY", 8)
    label_value(5, "Name", scv("Name"), FMT_TEXT)
    label_value(6, "Sector", scv("Sector"), FMT_TEXT)
    label_value(7, "Business Type", scv("Business Type"), FMT_TEXT)
    label_value(8, "Statement currency", ksv("Statement Currency"), FMT_TEXT)
    label_value(9, "Price (IDR)", stv("Price"), FMT_CUR2)
    label_value(10, "Market cap (IDR bn)", ksv("Market Cap", scale=1_000_000_000), FMT_CUR)
    label_value(11, "Shares outstanding", ksv("Current Share Outstanding"), FMT_CUR)
    label_value(12, "Latest filing date", ksv("Latest Filing Date"), FMT_TEXT)
    label_value(13, "Quarters stale", ksv("Quarters Stale"), FMT_SCORE)
    label_value(14, "Beta", ksv("Beta"), FMT_SCORE)

    # ---- valuation lenses ------------------------------------------------
    section(ws, 16, "VALUATION — EVERY LENS SIDE BY SIDE", 8)
    header_row(ws, 17, ["Lens", "Value per share", "MOS vs price", "Upside"])
    lenses = [
        ("DCF — bear", scv("IV Bear")),
        ("DCF — base", scv("IV Base")),
        ("DCF — bull", scv("IV Bull")),
        ("Earnings Power Value (EPV)", ksv("EPV per Share")),
        ("Comparables (peer multiples)", scv("Comparables IV")),
        ("Justified P/B", scv("Justified PB IV")),
        ("Graham NCAV", ksv("NCAV per Share")),
    ]
    for i, (label, formula) in enumerate(lenses):
        r = 18 + i
        put(ws, f"A{r}", label, font=F_BOLD, border=True)
        put(ws, f"B{r}", formula, font=F_LINK, fmt=FMT_CUR2, align="center", border=True)
        # MOS = 1 - price / IV; guarded so a blank or non-positive IV shows blank
        # rather than #DIV/0! or a nonsense negative.
        put(ws, f"C{r}",
            f'=IF(AND(ISNUMBER(B{r}),B{r}>0,ISNUMBER({CO_PRICE})),1-{CO_PRICE}/B{r},"")',
            font=F_BASE, fmt=FMT_PCT, align="center", border=True)
        put(ws, f"D{r}",
            f'=IF(AND(ISNUMBER(B{r}),B{r}>0,ISNUMBER({CO_PRICE}),{CO_PRICE}>0),'
            f'B{r}/{CO_PRICE}-1,"")',
            font=F_BASE, fmt=FMT_PCT, align="center", border=True)

    put(ws, "A25", "Blended IV (scoring engine)", font=F_BOLD, border=True)
    put(ws, "B25", scv("Blended IV"), font=F_LINK, fmt=FMT_CUR2, align="center", border=True)
    put(ws, "C25", scv("MOS Blended"), font=F_LINK, fmt=FMT_PCT, align="center", border=True)
    put(ws, "D25", scv("Upside Blended"), font=F_LINK, fmt=FMT_PCT, align="center", border=True)

    put(ws, "A26", "Price test only (MOS vs Setup thresholds)", font=F_BOLD, border=True)
    put(ws, "B26",
        f'=IF(NOT(ISNUMBER($C$25)),"n/a",'
        f'IF($C$25>={SETUP["mos_buy"]},"BUY",'
        f'IF($C$25>={SETUP["mos_watch"]},"WATCH","SKIP")))',
        font=F_BASE, fmt=FMT_TEXT, align="center", border=True)
    put(ws, "C26", "Thresholds live on Setup!B9 / Setup!B10", font=F_NOTE)
    put(ws, "A27", "VERDICT (price + quality + safety + flags)", font=F_BOLD, border=True)
    put(ws, "B27", scv("Verdict"), font=F_LINK, fmt=FMT_TEXT, align="center", border=True)
    apply_verdict_formats(ws, "B26:B27")

    # ---- quality ---------------------------------------------------------
    section(ws, 29, "QUALITY", 8)
    quality = [
        ("Return on equity (TTM)", ksv("Return on Equity (TTM)"), FMT_PCT),
        ("Return on assets (TTM)", ksv("Return on Assets (TTM)"), FMT_PCT),
        ("Return on invested capital (TTM)", ksv("Return On Invested Capital (TTM)"), FMT_PCT),
        ("Return on capital (Greenblatt)", ksv("ROC Greenblatt"), FMT_PCT),
        ("Gross profit margin (quarter)", ksv("Gross Profit Margin (Quarter)"), FMT_PCT),
        ("Operating profit margin (quarter)", ksv("Operating Profit Margin (Quarter)"), FMT_PCT),
        ("Net profit margin (quarter)", ksv("Net Profit Margin (Quarter)"), FMT_PCT),
        ("Gross margin 5Y average", ksv("Gross Margin 5Y Avg"), FMT_PCT),
        ("EBIT margin 5Y average", ksv("EBIT Margin 5Y Avg"), FMT_PCT),
        ("ROE 5Y average", ksv("ROE 5Y Avg"), FMT_PCT),
        ("Revenue CAGR 3Y", ksv("Revenue CAGR 3Y"), FMT_PCT),
        ("Revenue CAGR 5Y", ksv("Revenue CAGR 5Y"), FMT_PCT),
    ]
    for i, (label, formula, fmt) in enumerate(quality):
        label_value(30 + i, label, formula, fmt)
    # Cash conversion: OCF / net income, computed here from two raw pulls.
    r = 30 + len(quality)
    put(ws, f"A{r}", "Cash conversion (OCF / net income)", font=F_BOLD, border=True)
    put(ws, f"B{r}",
        f'=IFERROR(IF(AND(ISNUMBER(INDEX({ks.col_range("Operating Cash Flow (TTM)")},{CO_IDX["ks"]})),'
        f'ISNUMBER(INDEX({ks.col_range("Net Income (TTM)")},{CO_IDX["ks"]})),'
        f'INDEX({ks.col_range("Net Income (TTM)")},{CO_IDX["ks"]})<>0),'
        f'INDEX({ks.col_range("Operating Cash Flow (TTM)")},{CO_IDX["ks"]})'
        f'/INDEX({ks.col_range("Net Income (TTM)")},{CO_IDX["ks"]}),""),"")',
        font=F_LINK, fmt=FMT_MULT, align="center", border=True)

    # ---- safety ----------------------------------------------------------
    safety_top = r + 2
    section(ws, safety_top, "SAFETY", 8)
    safety = [
        ("Current ratio", ksv("Current Ratio (Quarter)"), FMT_MULT),
        ("Working capital (IDR bn)", ksv("Working Capital (Quarter)", scale=1_000_000_000), FMT_CUR),
        ("Interest coverage (TTM)", ksv("Interest Coverage (TTM)"), FMT_MULT),
        ("Altman Z-Score (modified)", ksv("Altman Z-Score (Modified)"), FMT_SCORE),
        ("Net debt / equity", anv("Net Debt to Equity"), FMT_MULT),
        ("Total debt (IDR bn)", ksv("Total Debt (Quarter)", scale=1_000_000_000), FMT_CUR),
        ("Net debt (IDR bn)", ksv("Net Debt (Quarter)", scale=1_000_000_000), FMT_CUR),
    ]
    for i, (label, formula, fmt) in enumerate(safety):
        label_value(safety_top + 1 + i, label, formula, fmt)

    r = safety_top + 1 + len(safety)
    put(ws, f"A{r}", "Net debt / EBITDA", font=F_BOLD, border=True)
    put(ws, f"B{r}",
        f'=IFERROR(IF(AND(ISNUMBER(INDEX({ks.col_range("Net Debt (Quarter)")},{CO_IDX["ks"]})),'
        f'ISNUMBER(INDEX({ks.col_range("EBITDA (TTM)")},{CO_IDX["ks"]})),'
        f'INDEX({ks.col_range("EBITDA (TTM)")},{CO_IDX["ks"]})<>0),'
        f'INDEX({ks.col_range("Net Debt (Quarter)")},{CO_IDX["ks"]})'
        f'/INDEX({ks.col_range("EBITDA (TTM)")},{CO_IDX["ks"]}),""),"")',
        font=F_LINK, fmt=FMT_MULT, align="center", border=True)

    # Cost of equity consumes Setup risk-free rate and equity risk premium.
    r += 1
    put(ws, f"A{r}", "Cost of equity (CAPM: RF + Beta x ERP)", font=F_BOLD, border=True)
    put(ws, f"B{r}",
        f'=IFERROR(IF(ISNUMBER($B$14),{SETUP["rf"]}+$B$14*{SETUP["erp"]},'
        f'{SETUP["rf"]}+{SETUP["erp"]}),"")',
        font=F_BASE, fmt=FMT_PCT, align="center", border=True)
    put(ws, f"C{r}", "Uses Setup!B7 (risk free) and Setup!B8 (ERP); "
        "falls back to beta = 1 when beta is unavailable.", font=F_NOTE)

    # EPV cross-check consumes Setup tax rate and WACC.
    r += 1
    put(ws, f"A{r}", "EPV cross-check per share (Setup tax + WACC)", font=F_BOLD, border=True)
    put(ws, f"B{r}",
        f'=IFERROR(IF(AND(ISNUMBER(INDEX({ks.col_range("Normalised EBIT (5Y)")},{CO_IDX["ks"]})),'
        f'ISNUMBER(INDEX({ks.col_range("Current Share Outstanding")},{CO_IDX["ks"]})),'
        f'INDEX({ks.col_range("Current Share Outstanding")},{CO_IDX["ks"]})>0,'
        f'{SETUP["wacc"]}>0),'
        f'INDEX({ks.col_range("Normalised EBIT (5Y)")},{CO_IDX["ks"]})*(1-{SETUP["tax"]})'
        f'/{SETUP["wacc"]}/INDEX({ks.col_range("Current Share Outstanding")},{CO_IDX["ks"]}),""),"")',
        font=F_BASE, fmt=FMT_CUR2, align="center", border=True)
    put(ws, f"C{r}", "Normalised 5Y EBIT x (1 - Setup!B4) / Setup!B5 / shares. "
        "Compare with the EPV lens above.", font=F_NOTE)

    # ---- Piotroski -------------------------------------------------------
    f_top = r + 2
    section(ws, f_top, "PIOTROSKI F-SCORE — 9 SIGNALS", 8)
    header_row(ws, f_top + 1, ["Signal", "Raw (1/0)", "Result", "What it tests"])
    for i, (col, description) in enumerate(F_SIGNALS):
        rr = f_top + 2 + i
        put(ws, f"A{rr}", col.replace("F: ", ""), font=F_BOLD, border=True)
        put(ws, f"B{rr}", ksv(col), font=F_LINK, fmt=FMT_INT, align="center", border=True)
        put(ws, f"C{rr}", f'=IF(NOT(ISNUMBER(B{rr})),"n/a",IF(B{rr}=1,"PASS","FAIL"))',
            font=F_BASE, fmt=FMT_TEXT, align="center", border=True)
        put(ws, f"D{rr}", description, font=F_BASE, border=True)
    f_last = f_top + 1 + len(F_SIGNALS)
    put(ws, f"A{f_last + 1}", "F-Score total (0-9)", font=F_BOLD, border=True)
    put(ws, f"B{f_last + 1}", ksv("Piotroski F-Score"), font=F_LINK, fmt=FMT_INT,
        align="center", border=True)
    put(ws, f"C{f_last + 1}", f"=SUM(B{f_top + 2}:B{f_last})", font=F_BASE,
        fmt=FMT_INT, align="center", border=True)
    put(ws, f"D{f_last + 1}", "Column C re-adds the nine signals as a cross-check "
        "on the scraper's own F-Score.", font=F_NOTE)
    ws.conditional_formatting.add(
        f"C{f_top + 2}:C{f_last}",
        CellIsRule(operator="equal", formula=['"PASS"'], fill=FILL_BUY),
    )
    ws.conditional_formatting.add(
        f"C{f_top + 2}:C{f_last}",
        CellIsRule(operator="equal", formula=['"FAIL"'], fill=FILL_SKIP),
    )

    # ---- narrative -------------------------------------------------------
    narr = f_last + 3
    section(ws, narr, "VERDICT NARRATIVE", 8)
    put(ws, f"A{narr + 1}", "Reasons", font=F_BOLD, border=True)
    put(ws, f"B{narr + 1}", scv("Reasons"), font=F_LINK, fmt=FMT_TEXT, wrap=True, border=True)
    put(ws, f"A{narr + 2}", "Red flags", font=F_BOLD, border=True)
    put(ws, f"B{narr + 2}", scv("Red Flags"), font=F_LINK, fmt=FMT_TEXT, wrap=True, border=True)
    ws.row_dimensions[narr + 1].height = 30
    ws.row_dimensions[narr + 2].height = 30

    # ---- 4-year annual history ------------------------------------------
    hist = narr + 4
    section(ws, hist, "ANNUAL HISTORY — LAST 4 REPORTED YEARS (IDR bn)", 8)
    put(ws, f"A{hist + 1}", "Matched on the RAW_history_annual helper key "
        "'Ticker|Period End'; two-condition lookups need one concatenated key "
        "because array formulas are not portable.", font=F_NOTE)
    hh = hist + 2
    put(ws, f"A{hh}", "Line item", font=F_HEADER, fill=FILL_HEADER, border=True)
    # Period-end headers: R4 (oldest of the last four) .. R1 (most recent).
    for j, rk in enumerate(["R4", "R3", "R2", "R1"]):
        col = get_column_letter(2 + j)
        put(ws, f"{col}{hh}",
            f'=IFERROR(INDEX({ha.col_range("Period End")},'
            f'MATCH({CO_TICKER}&"|{rk}",{ha.col_range(RECENCY_COL)},0)),"")',
            font=F_HEADER, fill=FILL_HEADER, fmt=FMT_TEXT, align="center", border=True)

    for i, (label, column) in enumerate(HISTORY_LINES):
        rr = hh + 1 + i
        put(ws, f"A{rr}", label, font=F_BOLD, border=True)
        for j in range(4):
            col = get_column_letter(2 + j)
            put(ws, f"{col}{rr}",
                f'=IFERROR(INDEX({ha.col_range(column)},'
                f'MATCH({CO_TICKER}&"|"&{col}${hh},{ha.col_range(KEY_COL)},0))/1000000000,"")',
                font=F_LINK, fmt=FMT_CUR, align="center", border=True)

    set_widths(ws, {"A": 38, "B": 18, "C": 18, "D": 18, "E": 18, "F": 16, "G": 16, "H": 16})
    ws.freeze_panes = "A3"


# --------------------------------------------------------------------------
# Scenario (live DCF)
# --------------------------------------------------------------------------

SC_TICKER = "$B$4"
SC_PRICE = "$B$5"
SC_FCF0 = "$B$6"
SC_G = ["$B$7", "$B$8", "$B$9", "$B$10", "$B$11"]
SC_TG = "$B$12"
SC_WACC = "$B$13"
SC_NETDEBT = "$B$14"
SC_SHARES = "$B$15"
SC_PROJ_FIRST = 20          # first row of the projection grid
SC_PROJ_LAST = 24           # last projection year row
SC_FCF_COL = "C"
SC_DF_COL = "D"


def build_scenario(ws: Worksheet, raw: dict[str, RawTable], default_ticker: str):
    ks = raw["RAW_key_statistics"]
    st = raw["RAW_idx_stocks"]

    title_block(
        ws,
        "SCENARIO — LIVE DISCOUNTED CASH FLOW",
        "Yellow cells are inputs. They pre-fill from the selected ticker but you "
        "may type over any of them; nothing downstream is hardcoded.",
    )

    section(ws, 3, "INPUTS", 6)
    put(ws, "A4", "Ticker", font=F_BOLD, border=True)
    put(ws, "B4", default_ticker, font=F_INPUT, fill=FILL_INPUT, fmt=FMT_TEXT,
        align="center", border=True)
    put(ws, "C4", "Any ticker present on the Screener sheet.", font=F_NOTE)

    def inp(row, label, formula, fmt, note):
        put(ws, f"A{row}", label, font=F_BOLD, border=True)
        put(ws, f"B{row}", formula, font=F_INPUT, fill=FILL_INPUT, fmt=fmt,
            align="center", border=True)
        put(ws, f"C{row}", note, font=F_NOTE)

    put(ws, "A5", "Current price (IDR)", font=F_BOLD, border=True)
    put(ws, "B5", st.by_key("Price", SC_TICKER), font=F_LINK, fmt=FMT_CUR2,
        align="center", border=True)
    put(ws, "C5", "Live from RAW_idx_stocks — not an input.", font=F_NOTE)

    inp(6, "Base free cash flow (IDR)", ks.by_key("Free cash flow (TTM)", SC_TICKER),
        FMT_CUR, "Trailing-twelve-month FCF. Override with a normalised figure "
        "if TTM is distorted.")

    # Year-1 growth seeds off 3-year revenue CAGR, clamped to a defensible band.
    inp(7, "Growth — year 1",
        f'=IFERROR(MAX(-0.1,MIN(0.15,{ks.by_key("Revenue CAGR 3Y", SC_TICKER)[1:]})),0.05)',
        FMT_PCT, "Seeded from Revenue CAGR 3Y, clamped to -10%..+15%.")
    # Years 2-5 fade linearly from year 1 toward the terminal rate.
    for i in range(2, 6):
        inp(6 + i, f"Growth — year {i}",
            f'={SC_G[0]}+({SC_TG}-{SC_G[0]})*{i - 1}/5',
            FMT_PCT, f"Linear fade from year 1 toward terminal growth ({i - 1}/5 of the way).")

    inp(12, "Terminal growth", f'={SETUP["tg"]}', FMT_PCT,
        "Defaults to Setup!B6. Must stay below WACC.")
    inp(13, "WACC (discount rate)", f'={SETUP["wacc"]}', FMT_PCT,
        "Defaults to Setup!B5. Compare with the CAPM cost of equity on Company.")
    inp(14, "Net debt (IDR)", ks.by_key("Net Debt (Quarter)", SC_TICKER), FMT_CUR,
        "Subtracted from enterprise value. Negative = net cash.")
    inp(15, "Shares outstanding", ks.by_key("Current Share Outstanding", SC_TICKER),
        FMT_CUR, "Diluted share count would be more conservative — override if you have it.")

    # ---- projection grid -------------------------------------------------
    section(ws, 18, "5-YEAR PROJECTION (every cell a formula off the inputs above)", 6)
    header_row(ws, 19, ["Year", "Growth", "Free cash flow (IDR)",
                        "Discount factor", "PV of FCF (IDR)"])
    for i in range(5):
        r = SC_PROJ_FIRST + i
        put(ws, f"A{r}", i + 1, font=F_BASE, fmt=FMT_INT, align="center", border=True)
        put(ws, f"B{r}", f"={SC_G[i]}", font=F_BASE, fmt=FMT_PCT, align="center", border=True)
        prev = SC_FCF0 if i == 0 else f"{SC_FCF_COL}{r - 1}"
        put(ws, f"{SC_FCF_COL}{r}", f"={prev}*(1+B{r})", font=F_BASE, fmt=FMT_CUR,
            align="center", border=True)
        put(ws, f"{SC_DF_COL}{r}", f"=1/(1+{SC_WACC})^A{r}", font=F_BASE,
            fmt="0.0000", align="center", border=True)
        put(ws, f"E{r}", f"={SC_FCF_COL}{r}*{SC_DF_COL}{r}", font=F_BASE,
            fmt=FMT_CUR, align="center", border=True)

    # Gordon growth terminal value, guarded: a WACC at or below terminal growth
    # makes the perpetuity meaningless, so return #N/A rather than a huge number.
    put(ws, "A26", "Terminal value (Gordon growth)", font=F_BOLD, border=True)
    put(ws, "C26",
        f'=IF({SC_WACC}<={SC_TG},NA(),{SC_FCF_COL}{SC_PROJ_LAST}*(1+{SC_TG})'
        f'/({SC_WACC}-{SC_TG}))',
        font=F_BASE, fmt=FMT_CUR, align="center", border=True)
    put(ws, "D26", f"={SC_DF_COL}{SC_PROJ_LAST}", font=F_BASE, fmt="0.0000",
        align="center", border=True)
    put(ws, "E26", "=C26*D26", font=F_BASE, fmt=FMT_CUR, align="center", border=True)
    put(ws, "F26", "A not-available result here means WACC <= terminal growth, "
        "for which the Gordon perpetuity does not converge.", font=F_NOTE)

    # ---- outputs ---------------------------------------------------------
    section(ws, 28, "OUTPUT", 6)
    outputs = [
        (29, "Enterprise value (IDR)", f"=SUM(E{SC_PROJ_FIRST}:E{SC_PROJ_LAST})+E26", FMT_CUR),
        (30, "Less: net debt (IDR)", f"={SC_NETDEBT}", FMT_CUR),
        (31, "Equity value (IDR)", "=B29-B30", FMT_CUR),
        (32, "Shares outstanding", f"={SC_SHARES}", FMT_CUR),
        (33, "Value per share (IDR)", '=IFERROR(IF(B32>0,B31/B32,""),"")', FMT_CUR2),
        (34, "Current price (IDR)", f"={SC_PRICE}", FMT_CUR2),
        (35, "Margin of safety", '=IF(AND(ISNUMBER(B33),B33>0,ISNUMBER(B34)),1-B34/B33,"")', FMT_PCT),
        (36, "Upside to value", '=IF(AND(ISNUMBER(B33),ISNUMBER(B34),B34>0),B33/B34-1,"")', FMT_PCT),
    ]
    for r, label, formula, fmt in outputs:
        put(ws, f"A{r}", label, font=F_BOLD, border=True)
        put(ws, f"B{r}", formula, font=F_BASE, fmt=fmt, align="center", border=True)
    put(ws, "A37", "Price test only (MOS vs Setup thresholds)", font=F_BOLD, border=True)
    put(ws, "B37",
        f'=IF(NOT(ISNUMBER(B35)),"n/a",IF(B35>={SETUP["mos_buy"]},"BUY",'
        f'IF(B35>={SETUP["mos_watch"]},"WATCH","SKIP")))',
        font=F_BASE, fmt=FMT_TEXT, align="center", border=True)
    put(ws, "C37", "Thresholds live on Setup!B9 / Setup!B10.", font=F_NOTE)
    apply_verdict_formats(ws, "B37:B37")

    set_widths(ws, {"A": 34, "B": 20, "C": 24, "D": 16, "E": 22, "F": 60})
    ws.freeze_panes = "A4"


# --------------------------------------------------------------------------
# Sensitivity
# --------------------------------------------------------------------------

WACC_STEPS = 7          # rows
TG_STEPS = 5            # columns, grid 1
G_STEPS = 5             # columns, grid 2
WACC_STEP = 0.01
TG_STEP = 0.01
G_STEP = 0.02


def _sens_grid1_formula(wacc_ref: str, tg_ref: str) -> str:
    """Value per share re-derived from the Scenario inputs for (WACC, g_terminal).

    The five projected FCFs do not depend on either axis, so they are referenced
    straight off the Scenario projection column; only discounting and the
    terminal value are recomputed here.  Excel data tables are not written
    because Google Sheets has no equivalent -- every cell carries the formula.
    """
    pv = "+".join(
        f"Scenario!$C${SC_PROJ_FIRST + i}/(1+{wacc_ref})^{i + 1}" for i in range(5)
    )
    tv = (
        f"(Scenario!$C${SC_PROJ_LAST}*(1+{tg_ref})/({wacc_ref}-{tg_ref}))"
        f"/(1+{wacc_ref})^5"
    )
    return (
        f'=IF({wacc_ref}<={tg_ref},"n/m",'
        f'IFERROR(IF(Scenario!{SC_SHARES}>0,'
        f"(({pv}+{tv})-Scenario!{SC_NETDEBT})/Scenario!{SC_SHARES}"
        f',""),""))'
    )


def _sens_grid2_formula(wacc_ref: str, g_ref: str) -> str:
    """Value per share for (WACC, single stage-1 growth applied to all 5 years)."""
    pv = "+".join(
        f"Scenario!{SC_FCF0}*(1+{g_ref})^{i + 1}/(1+{wacc_ref})^{i + 1}" for i in range(5)
    )
    tv = (
        f"(Scenario!{SC_FCF0}*(1+{g_ref})^5*(1+Scenario!{SC_TG})"
        f"/({wacc_ref}-Scenario!{SC_TG}))/(1+{wacc_ref})^5"
    )
    return (
        f'=IF({wacc_ref}<=Scenario!{SC_TG},"n/m",'
        f'IFERROR(IF(Scenario!{SC_SHARES}>0,'
        f"(({pv}+{tv})-Scenario!{SC_NETDEBT})/Scenario!{SC_SHARES}"
        f',""),""))'
    )


def build_sensitivity(ws: Worksheet):
    title_block(
        ws,
        "SENSITIVITY",
        "Both grids recompute value per share cell by cell from the Scenario "
        "inputs. No Excel data tables are used — Google Sheets has no equivalent.",
    )
    put(ws, "A3", 'Cells reading "n/m" are combinations where WACC <= terminal '
        "growth, for which the Gordon perpetuity is not meaningful.", font=F_NOTE)

    # ---- grid 1: WACC x terminal growth ---------------------------------
    section(ws, 5, "VALUE PER SHARE — WACC (rows) x TERMINAL GROWTH (columns)", 7)
    hdr = 6
    put(ws, f"A{hdr}", "WACC \\ g", font=F_HEADER, fill=FILL_HEADER,
        align="center", border=True)
    for j in range(TG_STEPS):
        col = get_column_letter(2 + j)
        offset = (j - (TG_STEPS // 2)) * TG_STEP
        put(ws, f"{col}{hdr}", f"=Scenario!{SC_TG}{offset:+.4f}".replace("+0.0000", "+0"),
            font=F_HEADER, fill=FILL_HEADER, fmt=FMT_PCT, align="center", border=True)
    for i in range(WACC_STEPS):
        r = hdr + 1 + i
        offset = (i - (WACC_STEPS // 2)) * WACC_STEP
        put(ws, f"A{r}", f"=Scenario!{SC_WACC}{offset:+.4f}".replace("+0.0000", "+0"),
            font=F_HEADER, fill=FILL_HEADER, fmt=FMT_PCT, align="center", border=True)
        for j in range(TG_STEPS):
            col = get_column_letter(2 + j)
            put(ws, f"{col}{r}", _sens_grid1_formula(f"$A{r}", f"{col}${hdr}"),
                font=F_BASE, fmt=FMT_CUR2, align="center", border=True)
    g1_last = hdr + WACC_STEPS
    ws.conditional_formatting.add(
        f"B{hdr + 1}:{get_column_letter(1 + TG_STEPS)}{g1_last}",
        ColorScaleRule(
            start_type="min", start_color="FFF8696B",
            mid_type="percentile", mid_value=50, mid_color="FFFFEB84",
            end_type="max", end_color="FF63BE7B",
        ),
    )

    # ---- grid 2: WACC x stage-1 growth ----------------------------------
    top2 = g1_last + 3
    section(ws, top2, "VALUE PER SHARE — WACC (rows) x STAGE-1 GROWTH (columns, "
            "applied to all five years)", 7)
    hdr2 = top2 + 1
    put(ws, f"A{hdr2}", "WACC \\ g1-5", font=F_HEADER, fill=FILL_HEADER,
        align="center", border=True)
    base_g = f"AVERAGE(Scenario!{SC_G[0]}:Scenario!{SC_G[4]})"
    for j in range(G_STEPS):
        col = get_column_letter(2 + j)
        offset = (j - (G_STEPS // 2)) * G_STEP
        put(ws, f"{col}{hdr2}", f"={base_g}{offset:+.4f}".replace("+0.0000", "+0"),
            font=F_HEADER, fill=FILL_HEADER, fmt=FMT_PCT, align="center", border=True)
    for i in range(WACC_STEPS):
        r = hdr2 + 1 + i
        offset = (i - (WACC_STEPS // 2)) * WACC_STEP
        put(ws, f"A{r}", f"=Scenario!{SC_WACC}{offset:+.4f}".replace("+0.0000", "+0"),
            font=F_HEADER, fill=FILL_HEADER, fmt=FMT_PCT, align="center", border=True)
        for j in range(G_STEPS):
            col = get_column_letter(2 + j)
            put(ws, f"{col}{r}", _sens_grid2_formula(f"$A{r}", f"{col}${hdr2}"),
                font=F_BASE, fmt=FMT_CUR2, align="center", border=True)
    g2_last = hdr2 + WACC_STEPS
    ws.conditional_formatting.add(
        f"B{hdr2 + 1}:{get_column_letter(1 + G_STEPS)}{g2_last}",
        ColorScaleRule(
            start_type="min", start_color="FFF8696B",
            mid_type="percentile", mid_value=50, mid_color="FFFFEB84",
            end_type="max", end_color="FF63BE7B",
        ),
    )

    put(ws, f"A{g2_last + 2}", "Reference: current price", font=F_BOLD)
    put(ws, f"B{g2_last + 2}", f"=Scenario!{SC_PRICE}", font=F_LINK, fmt=FMT_CUR2,
        align="center")
    put(ws, f"A{g2_last + 3}", "Reference: Scenario value per share", font=F_BOLD)
    put(ws, f"B{g2_last + 3}", "=Scenario!$B$33", font=F_LINK, fmt=FMT_CUR2,
        align="center")

    set_widths(ws, {"A": 16, "B": 16, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16})
    ws.freeze_panes = "B7"


# --------------------------------------------------------------------------
# Journal
# --------------------------------------------------------------------------

JOURNAL_HEADERS = [
    "Date Analysed", "Ticker", "Name", "Price at Analysis", "Blended IV",
    "MOS at Analysis", "Verdict", "Thesis", "Why It Is Cheap", "Catalyst",
    "Key Risks", "What Would Invalidate", "Target Price", "Expected Return",
    "Position Taken?", "Review Date", "Outcome", "Notes",
]

JOURNAL_FORMATS = {
    "Date Analysed": FMT_TEXT, "Ticker": FMT_TEXT, "Name": FMT_TEXT,
    "Price at Analysis": FMT_CUR2, "Blended IV": FMT_CUR2, "MOS at Analysis": FMT_PCT,
    "Verdict": FMT_TEXT, "Target Price": FMT_CUR2, "Expected Return": FMT_PCT,
    "Review Date": FMT_TEXT,
}

JOURNAL_WIDTHS = {
    "Date Analysed": 20, "Ticker": 10, "Name": 28, "Price at Analysis": 15,
    "Blended IV": 13, "MOS at Analysis": 15, "Verdict": 12, "Thesis": 52,
    "Why It Is Cheap": 42, "Catalyst": 38, "Key Risks": 42,
    "What Would Invalidate": 42, "Target Price": 13, "Expected Return": 15,
    "Position Taken?": 15, "Review Date": 14, "Outcome": 26, "Notes": 40,
}

BLANK_JOURNAL_ROWS = 25


def build_journal(ws: Worksheet, example: dict[str, object]):
    title_block(
        ws,
        "JOURNAL — INVESTMENT LOG",
        "One row per decision. Write the thesis before you buy, not after.",
    )
    put(ws, "A3", "LEGEND: every cell from row 6 down is yours to fill in (yellow "
        "fill, blue text). Row 5 is a worked example — overwrite or delete it. "
        "Percentages are stored as fractions, so type 30% or 0.30, not 30.",
        font=F_NOTE)

    header_row(ws, 4, JOURNAL_HEADERS)

    for i, header in enumerate(JOURNAL_HEADERS):
        col = get_column_letter(i + 1)
        put(ws, f"{col}5", example.get(header), font=F_INPUT, fill=FILL_INPUT,
            fmt=JOURNAL_FORMATS.get(header, FMT_TEXT), border=True, wrap=True)

    for r in range(6, 6 + BLANK_JOURNAL_ROWS):
        for i in range(len(JOURNAL_HEADERS)):
            col = get_column_letter(i + 1)
            c = ws[f"{col}{r}"]
            c.font = F_INPUT
            c.fill = FILL_INPUT
            c.border = BOX
            c.number_format = JOURNAL_FORMATS.get(JOURNAL_HEADERS[i], FMT_TEXT)
            c.alignment = Alignment(vertical="top", wrap_text=True)

    ws.auto_filter.ref = f"A4:{get_column_letter(len(JOURNAL_HEADERS))}{5 + BLANK_JOURNAL_ROWS}"
    ws.freeze_panes = "D5"
    for header, width in JOURNAL_WIDTHS.items():
        ws.column_dimensions[get_column_letter(JOURNAL_HEADERS.index(header) + 1)].width = width
    ws.row_dimensions[5].height = 60


def journal_example(scores: pd.DataFrame, refresh_date: str) -> dict[str, object]:
    """A realistic worked example built from a real row so the format is obvious."""
    ranked = scores.sort_values("Composite Score", ascending=False)
    row = ranked.iloc[0]
    price = row.get("Price")
    iv = row.get("Blended IV")
    mos = row.get("MOS Blended")
    price = float(price) if pd.notna(price) else 0.0
    iv = float(iv) if pd.notna(iv) else price
    mos = float(mos) if pd.notna(mos) else 0.0
    target = iv * 0.9 if iv else price
    expected = (target / price - 1) if price else 0.0
    return {
        "Date Analysed": f"EXAMPLE — {refresh_date}",
        "Ticker": str(row["Ticker"]),
        "Name": str(row.get("Name", "")),
        "Price at Analysis": round(price, 2),
        "Blended IV": round(iv, 2),
        "MOS at Analysis": round(mos, 4),
        "Verdict": str(row.get("Verdict", "")),
        "Thesis": ("Cash-generative franchise trading below the blended intrinsic "
                   "value of every lens; balance sheet carries net cash, so the "
                   "downside is earnings normalisation rather than solvency."),
        "Why It Is Cheap": ("Cyclical earnings peak scares the market; index funds "
                            "have been sellers since the sector reweighting."),
        "Catalyst": ("Full-year results confirming margin stabilisation, plus the "
                     "declared dividend at the historical payout."),
        "Key Risks": ("Commodity price reversal, IDR depreciation on imported "
                      "input costs, minority-shareholder governance."),
        "What Would Invalidate": ("Two consecutive quarters of negative operating "
                                  "cash flow, or net debt/EBITDA above 2.0x."),
        "Target Price": round(target, 2),
        "Expected Return": round(expected, 4),
        "Position Taken?": "No — watching for a 30% MOS",
        "Review Date": "2026-11-15",
        "Outcome": "Open",
        "Notes": "Sized at 4% if entered. Revisit after Q3 filing.",
    }


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

SHEET_ORDER = [
    "Dashboard", "Screener", "Company", "Scenario", "Sensitivity", "Journal",
    "Setup", "RAW_idx_stocks", "RAW_key_statistics", "RAW_analyses",
    "RAW_scores", "RAW_history_quarterly", "RAW_history_annual",
]


def build_workbook(input_dir: str, output_path: str) -> str:
    frames = load_inputs(input_dir)

    wb = Workbook()
    wb.remove(wb.active)
    # Make Arial the workbook default so the RAW dumps (which can run to
    # >100k cells) need no per-cell styling.
    for style in wb._named_styles:
        if style.name == "Normal":
            style.font = Font(name=FONT_NAME, size=10)

    sheets = {name: wb.create_sheet(name) for name in SHEET_ORDER}

    raw = {name: RawTable(name, frames[name]) for name in CSV_FILES}
    for name in CSV_FILES:
        build_raw_sheet(sheets[name], frames[name])

    scores = frames["RAW_scores"]
    key_stats = frames["RAW_key_statistics"]
    smap = ScreenerMap(len(scores))

    default_ticker = str(
        scores.sort_values("Composite Score", ascending=False).iloc[0]["Ticker"]
    )
    refresh = str(key_stats["Fetched At"].iloc[0])[:10] if len(key_stats) else ""

    build_setup(sheets["Setup"])
    build_screener(sheets["Screener"], raw, smap)
    build_dashboard(
        sheets["Dashboard"], raw, smap,
        top_ideas=pick_top_ideas(scores),
        cheapest=pick_cheapest_am(key_stats),
        net_nets=pick_net_nets(key_stats),
    )
    build_company(sheets["Company"], raw, default_ticker)
    build_scenario(sheets["Scenario"], raw, default_ticker)
    build_sensitivity(sheets["Sensitivity"])
    build_journal(sheets["Journal"], journal_example(scores, refresh))

    wb.active = wb.sheetnames.index("Dashboard")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    wb.save(output_path)
    return output_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the dual Excel/Google-Sheets value screener workbook."
    )
    parser.add_argument("--input-dir", default="idx_picker/output",
                        help="directory holding the scraper's RAW_*.csv files")
    parser.add_argument("--output", default="idx_picker/output/PERSONAL_STOCKS_PICKER.xlsx",
                        help="path of the .xlsx to write")
    args = parser.parse_args(argv)

    path = build_workbook(args.input_dir, args.output)
    frames = load_inputs(args.input_dir)
    print(
        f"wrote {path}\n"
        f"  tickers: {len(frames['RAW_scores'])}\n"
        f"  annual history rows: {len(frames['RAW_history_annual'])}\n"
        f"  quarterly history rows: {len(frames['RAW_history_quarterly'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
