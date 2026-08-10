# Project memory — IDX value-investing system

Personal value-investing operating system for the Indonesian Stock Exchange
(works for US equities too). Two stages: a quantitative screener that generates
candidates, and a multi-agent research pipeline that underwrites them.

**The screener is candidate generation only. Its BUY / DEEP VALUE verdict is a
hypothesis, not a conclusion.** Stage 2 exists to falsify it.

---

## Owner's investment framework

Practical target: 3-4 companies per week, ~40-50 minutes each. A repeatable
process, not a precision forecasting exercise. The question every time:

> Is this a sufficiently good business, or a sufficiently attractive deep-value
> situation, trading at a sufficiently large discount to reasonable intrinsic
> value, with risks I understand and can accept?

Five outcomes must stay distinguishable: good business at a fair price; average
business very cheap; deep value / special situation; **value trap**; fairly
valued or expensive.

Non-negotiable rules:
- **Cheapness alone never produces a BUY.** Enforced structurally in
  `scoring.classify`, not by weighting.
- **MOS and Upside are different numbers.** `MOS = (IV − Price) / IV`;
  `Upside = IV / Price − 1`. Always show both.
- **Never value a bank on EV/EBIT or FCF.** Financials go to ROE / P-B /
  justified-P/B.
- **Never treat peak-cycle earnings as permanent earnings.**
- **Never fabricate.** Where evidence is missing, write
  *"Insufficient evidence — requires further research."*
- Label every claim **FACT / INFERENCE / THESIS / ASSUMPTION**.

The four quantitative lenses are different views of one investment, not four
independent reasons to buy: Magic Formula, Piotroski F-Score, Acquirer's
Multiple, Graham Net-Net.

---

## Repository layout

```
idx_picker/
├── scraper/
│   ├── yahoo.py      Yahoo client: crumb auth, adaptive rate limiting, disk cache
│   ├── metrics.py    Pure functions: TTM, ratios, Piotroski, Altman, DCF, EPV, comps
│   ├── scoring.py    Business classification, scenarios, red flags, verdict
│   └── pipeline.py   Orchestration, cross-sectional ranks, peer groups, CSV output
├── workbook/build.py Generates the dual Excel/Sheets workbook
├── research/         Stage 2 multi-agent research outputs
├── data/             Ticker seeds + HTTP cache (cache is gitignored, ~79MB)
├── output/           Generated CSVs + PERSONAL_STOCKS_PICKER.xlsx
├── tests/            pytest suite (223 tests, no network)
└── docs/             LOGIC_AUDIT.md, FIXES.md, WORKBOOK_GUIDE.md
```

`metrics.py` and `scoring.py` are pure and network-free. That is deliberate —
every number the screener produces is reproducible from a hand-built fixture,
which is what makes the test suite meaningful.

---

## Commands

```bash
./idx_picker/refresh.sh                          # fetch + rebuild + test
python3 -m idx_picker.scraper.pipeline --workers 4          # full universe, 60-90 min
python3 -m idx_picker.scraper.pipeline --cache-ttl -1       # rebuild from cache, ~5 sec
python3 -m idx_picker.scraper.pipeline --tickers BBCA,AALI  # a few names
python3 -m idx_picker.scraper.pipeline --market US --tickers AAPL
python3 -m idx_picker.workbook.build                        # rebuild workbook
python3 -m pytest idx_picker/tests -q                       # 223 tests
python3 /root/.claude/skills/xlsx/scripts/recalc.py idx_picker/output/PERSONAL_STOCKS_PICKER.xlsx
```

Refresh cadence: quarterly, about a month after quarter end. Cached rebuilds are
free, so iterate on logic without re-fetching.

---

## Hard-won knowledge — do not regress these

Each of these was a real bug that produced confidently wrong numbers.

**Yahoo's `sharesOutstanding` is wrong for 42 of 956 IDX tickers**, by up to
1000x (LPPF: 1,395,970 reported vs 1,170,221,581 implied). Always derive share
count from `market cap / price`; fall back to the reported field only when price
or market cap is missing. `Share Count Source` records which was used.

**Some IDX issuers file in USD but trade in IDR** (ITMG, ADRO, INDY, coal and
shipping generally). Unconverted, per-share figures are wrong by ~16,000x.
`normalise_currency` converts at spot and never scales share counts.

**Yahoo's beta is untrustworthy for illiquid names** — 0.168 for BBCA. Trust it
only inside [0.5, 2.5]; cost of equity floors at risk-free + 300bp. Justified
P/B divides by (COE − g), so a bad beta silently quadruples a bank's fair value.

**Yahoo publishes no `annualOperatingCashFlow` for IDX at all.** Derive it as
`FreeCashFlow − CapitalExpenditure` (capex arrives negative).

**Yahoo's free feed carries only ~4 annual periods and ~5-6 quarters.** Piotroski
therefore runs on the annual basis for most names (`F-Score Basis` records it).
Ten years of *monthly prices* is available and is used. The HTTP cache is
append-only, so fundamental history deepens each quarter from here forward.

**Missing data is not passing data.** Every verdict gate must test
`is None` separately from `< threshold`, or a data-poor row reaches BUY on
margin of safety alone.

**Normalise EBIT with the median, never the mean.** One commodity supercycle
year dominates a 4-year mean (ITMG's 2022 EBIT was 5x its 2025).

**Never take the minimum across valuation lenses.** For a levered cyclical,
`EBIT × multiple − net debt` can land just above zero and swamp two sensible
lenses. Reject outliers beyond 10x from the median, then take the median.

**Bear/base/bull must be offsets from the base**, never independent absolute
clamps, or the bull case can price below the base.

---

## Formula portability (the workbook)

The workbook must recalculate identically in Excel **and** Google Sheets.

**Banned:** `XLOOKUP`, `XMATCH`, `FILTER`, `SORT`, `UNIQUE`, `SEQUENCE`, `LET`,
`LAMBDA`, `MAP`, `BYCOL`, `TEXTJOIN`, `IFS`, `SWITCH`, `MAXIFS`, `MINIFS`,
`REGEXEXTRACT`, `GEMINI`, `ARRAYFORMULA`, `QUERY`, structured table refs
(`keyStats[Ticker]`).

**Use:** `INDEX`/`MATCH` (preferred over `VLOOKUP`), `IF`, `IFERROR`, `SUMIFS`,
`COUNTIFS`, `MEDIAN`, `LARGE`, `RANK`, `NA`, `&`.

Ranges must be bounded (`$A$2:$A$957`), never whole-column. Sorting and
filtering are precomputed in Python; the sheet then pulls fields live via
`INDEX`/`MATCH` so values stay reactive.

The predecessor workbook failed this: 16 of 97 columns were
`__xludf.DUMMYFUNCTION` stubs — dead in Excel, showing frozen cached values.

Verify every build: `recalc.py` must report `total_errors: 0`. A clean recalc
proves formulas *evaluate*, not that they are *right* — always spot-check values
against the source CSVs too.

---

## Two-stage workflow

**Stage 1 — screener** (`idx_picker/`). Produces `RAW_scores.csv` with
BUY / WATCH / SKIP / DEEP VALUE for ~956 tickers, plus the workbook.

**Stage 2 — research** (`idx_picker/research/`). Takes the BUY and DEEP VALUE
names and underwrites them: five specialist agents per stock (Financial
Forensics, Valuation, Business/Industry, Macro/Catalyst, Thesis Killer), then
per-stock synthesis, cross-stock ranking, elimination, Top 10, and an
IDR 100M portfolio.

The Thesis Killer has veto power. Be especially skeptical of DEEP VALUE names.

Because 5 agents × every candidate is a very large workload, Stage 2 runs a
deterministic pre-screen first to eliminate names on evidence already in hand,
then spends agent time only on survivors. Record the pre-screen reasoning — it
is part of the elimination table, not a shortcut around it.

---

## Style

Code comments explain *why*, especially where a line encodes a hard-won
correction. Match surrounding density. Financial-model conventions in the
workbook: blue font = input, black = formula, green = cross-sheet link, yellow
fill = user-editable.
