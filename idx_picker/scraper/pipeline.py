"""Orchestration: fetch every ticker, derive every metric, write the CSVs.

Output contract (all files land in ``output/``):

``RAW_idx_stocks.csv``      - listing and market data; same column order as the
                              workbook tab it feeds.
``RAW_key_statistics.csv``  - the wide per-ticker statistics table, original 70
                              columns preserved in order, new columns appended.
``RAW_analyses.csv``        - the derived composite-rank table.
``RAW_history_quarterly.csv`` - long-format quarterly history, ~5 years per
                              ticker. This is the "longer historical" input the
                              old single-snapshot scraper never produced.
``RAW_history_annual.csv``  - same, annual periods.
``RAW_scores.csv``          - business classification, scenario valuations and
                              the BUY / WATCH / SKIP verdict.

Column order in the first three files is preserved deliberately: the existing
workbook tabs reference them positionally and by table-column name.
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

from . import metrics as M
from . import scoring as S
from .yahoo import YahooClient, RateLimitError

log = logging.getLogger(__name__)

# Original RAW_key_statistics column order, preserved so existing formulas that
# reference `keyStats[...]` by name keep resolving.
LEGACY_KEYSTATS_COLUMNS = [
    "Ticker", "Current PE Ratio (Annualised)", "Current PE Ratio (TTM)", "Forward PE Ratio",
    "IHSG PE Ratio TTM (Median)", "Earnings Yield (TTM)", "Current Price to Sales(TTM)",
    "Current Price to Book Value", "Current Price To Cashflow (TTM)",
    "Current Price To Free Cashflow (TTM)", "EV to EBIT (TTM)", "EV to EBITDA (TTM)",
    "PEG Ratio", "PEG Ratio (3yr)", "PEG (Forward)", "Current EPS (TTM)",
    "Current EPS (Annualised)", "Revenue Per Share (TTM)", "Cash Per Share (Quarter)",
    "Current Book Value Per Share", "Free Cashflow Per Share (TTM)", "Current Ratio (Quarter)",
    "Quick Ratio (Quarter)", "Debt to Equity Ratio (Quarter)", "LT Debt/Equity (Quarter)",
    "Total Liabilities/Equity (Quarter)", "Total Debt/Total Assets (Quarter)",
    "Financial Leverage (Quarter)", "Interest Coverage (TTM)", "Free cash flow (Quarter)",
    "Altman Z-Score (Modified)", "Return on Assets (TTM)", "Return on Equity (TTM)",
    "Return on Capital Employed (TTM)", "Return On Invested Capital (TTM)",
    "Days Sales Outstanding (Quarter)", "Days Inventory (Quarter)",
    "Days Payables Outstanding (Quarter)", "Cash Conversion Cycle (Quarter)",
    "Receivables Turnover (Quarter)", "Asset Turnover (TTM)", "Inventory Turnover (TTM)",
    "Gross Profit Margin (Quarter)", "Operating Profit Margin (Quarter)",
    "Net Profit Margin (Quarter)", "Revenue (Quarter YoY Growth)",
    "Gross Profit (Quarter YoY Growth)", "Net Income (Quarter YoY Growth)", "Dividend",
    "Dividend (TTM)", "Payout Ratio", "Dividend Yield", "Latest Dividend Ex-Date",
    "Piotroski F-Score", "EPS Rating", "Relative Strength Rating", "Rank (Market Cap)",
    "Rank (Current PE Ratio TTM)", "Rank (Earnings Yield)", "Rank (P/S)", "Rank (P/B)",
    "Rank (Near 52 Weeks High)", "Revenue (TTM)", "Gross Profit (TTM)", "EBITDA (TTM)",
    "Net Income (TTM)", "Cash (Quarter)", "Total Assets (Quarter)",
    "Total Liabilities (Quarter)", "Working Capital (Quarter)",
]

# Appended columns. Everything here is new capability the old scraper could not
# supply -- correctly-defined Magic Formula inputs, cycle-normalised earnings,
# multi-year history-derived growth, and the staleness guard.
NEW_KEYSTATS_COLUMNS = [
    "Market Cap", "Enterprise Value", "Current Share Outstanding", "Total Equity",
    "Total Debt (Quarter)", "Net Debt (Quarter)", "Current Assets (Quarter)",
    "Current Liabilities (Quarter)", "EBIT (TTM)", "Operating Cash Flow (TTM)",
    "Capital expenditure (TTM)", "Free cash flow (TTM)", "Inventory (Quarter)",
    "Retained Earnings (Quarter)", "Beta",
    # Correctly-defined value lenses
    "Earnings Yield Greenblatt (EBIT/EV)", "ROC Greenblatt", "Acquirers Multiple (EV/EBIT)",
    "FCF Yield (TTM)", "NCAV", "NCAV per Share", "Net-Net Pass",
    # Cycle-aware inputs
    "Normalised EBIT (5Y)", "Normalised EBIT Margin", "Normalised/Trailing EBIT", "EPV per Share",
    "Working Capital Intensity", "Implied Terminal Multiple",
    # History-derived
    "Revenue CAGR 3Y", "Revenue CAGR 5Y", "EPS CAGR 3Y", "Net Income CAGR 3Y",
    "Gross Margin 5Y Avg", "EBIT Margin 5Y Avg", "ROE 5Y Avg",
    "Revenue Volatility 5Y", "Quarters of History", "Years of Annual History",
    # Piotroski breakdown
    "F: ROA Positive", "F: CFO Positive", "F: ROA Improving", "F: Accruals",
    "F: Leverage Falling", "F: Current Ratio Improving", "F: No Dilution",
    "F: Gross Margin Improving", "F: Asset Turnover Improving", "F-Score Basis",
    # Data quality
    "52W High", "52W Low", "Pct From 52W High", "1Y Price Change",
    "Price CAGR 3Y", "Price CAGR 5Y", "Price Percentile 10Y", "Max Drawdown 10Y",
    "Months of Price History",
    "Latest Filing Date", "Quarters Stale", "Statement Currency", "FX Rate Applied",
    "Share Count Source", "Reported/Implied Shares", "Minority Interest",
    "Data Source", "Fetched At",
]

KEYSTATS_COLUMNS = LEGACY_KEYSTATS_COLUMNS + NEW_KEYSTATS_COLUMNS

IDX_STOCKS_COLUMNS = [
    "Ticker", "Name", "IPO Date", "Outstanding Shares", "Note", "Price", "Volume",
    "Change", "Percentage Change", "Average", "Close Price", "High Price", "Open Price",
    "Low Price", "ARA Price", "ARB Price", "Frequency", "Frequency Sell", "Frequency Buy",
    "52W High", "52W Low", "Pct From 52W High", "1Y Price Change", "Currency", "Fetched At",
]

ANALYSES_COLUMNS = [
    "Ticker", "PBV x ROE", "Close Price", "Price to Equity Discount (%)",
    "Relative PE ratio (TTM)", "EPS Growth", "Debt to Total Assets Ratio",
    "Liquidity Differential", "CCE", "Operating Efficiency",
    "Dividend Payout Efficiency", "Yearly Price Change", "Composite Rank",
    "Net Debt to Equity",
]

HISTORY_FIELDS = [
    "TotalRevenue", "CostOfRevenue", "GrossProfit", "OperatingIncome", "EBIT", "EBITDA",
    "NetIncome", "PretaxIncome", "TaxProvision", "InterestExpense", "DilutedAverageShares",
    "TotalAssets", "TotalLiabilitiesNetMinorityInterest", "StockholdersEquity",
    "CashAndCashEquivalents", "TotalDebt", "LongTermDebt", "CurrentAssets",
    "CurrentLiabilities", "WorkingCapital", "Inventory", "AccountsReceivable",
    "AccountsPayable", "RetainedEarnings", "InvestedCapital", "OperatingCashFlow",
    "CapitalExpenditure", "FreeCashFlow",
]


@dataclass
class Settings:
    """Model-level assumptions. Mirrors the workbook's Setup sheet."""

    tax_rate: float = 0.22
    wacc: float = 0.12
    terminal_growth: float = 0.03
    risk_free_rate: float = 0.065
    equity_risk_premium: float = 0.055
    mos_buy: float = 0.30
    mos_watch: float = 0.10
    market: str = "IDX"

    @classmethod
    def for_market(cls, market: str) -> "Settings":
        """US names carry a lower risk-free rate and discount rate than IDX."""
        if market.upper() == "US":
            return cls(
                tax_rate=0.21, wacc=0.09, terminal_growth=0.025, risk_free_rate=0.042,
                equity_risk_premium=0.05, market="US",
            )
        return cls()


def _get(node: dict[str, Any] | None, *path: str) -> Any:
    """Walk Yahoo's nested `{raw: ...}` envelopes, returning None on any miss."""
    current: Any = node or {}
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    if isinstance(current, dict):
        current = current.get("raw")
    return current



def normalise_currency(
    client: YahooClient, bundle: dict[str, list[dict[str, Any]]], price_currency: str
) -> tuple[dict[str, list[dict[str, Any]]], str, float]:
    """Restate the statements into the currency the shares actually trade in.

    A material minority of IDX issuers -- the coal, energy and shipping names
    (ITMG, ADRO, INDY, MEDC among them) -- report in USD while their shares
    trade in IDR. Every per-share output built from unconverted statements is
    then wrong by the exchange rate, roughly 16,000x. In testing this valued
    ITMG at IDR 5 per share against a IDR 25,125 market price, which the screen
    read as a -100% margin of safety rather than as a unit error.

    Returns the converted bundle, the currency the statements were filed in, and
    the rate applied.
    """
    codes = [
        entry.get("currency")
        for series in bundle.values()
        for entry in series
        if entry.get("currency")
    ]
    if not codes:
        return bundle, price_currency, 1.0

    statement_currency = max(set(codes), key=codes.count)
    if statement_currency.upper() == price_currency.upper():
        return bundle, statement_currency, 1.0

    rate = client.fx_rate(statement_currency, price_currency)
    if not rate:
        log.warning(
            "no FX rate for %s->%s; leaving statements unconverted",
            statement_currency, price_currency,
        )
        return bundle, statement_currency, 1.0

    converted = {
        type_name: [
            {**entry, "value": entry["value"] * rate, "currency": price_currency}
            for entry in series
        ]
        for type_name, series in bundle.items()
    }
    # Share counts are not monetary and must not be scaled by the FX rate.
    for type_name in list(converted):
        if "Shares" in type_name:
            converted[type_name] = bundle[type_name]
    return converted, statement_currency, rate


def fetch_one(client: YahooClient, ticker: str, market: str = "IDX") -> dict[str, Any] | None:
    """Fetch and derive everything for a single ticker."""
    try:
        bundle = client.fundamentals(ticker)
        quote = client.quote_summary(ticker)
        chart = client.price_history(ticker)
        # Yahoo's free fundamentals feed holds only ~4 annual periods and ~6
        # quarters. Ten years of monthly prices is the one genuinely long series
        # available, and it carries the cycle information the fundamentals lack:
        # drawdown depth, where today's price sits in its own decade-long range,
        # and multi-year price CAGR.
        long_chart = client.price_history(ticker, range_="10y", interval="1mo")
    except RateLimitError as exc:
        log.error("%s: %s", ticker, exc)
        return None

    if not bundle and not quote:
        return None

    price_currency = _get(quote, "price", "currency") or "IDR"
    bundle, statement_currency, fx = normalise_currency(client, bundle, price_currency)

    core = M.build_core(ticker, bundle)

    price = _get(quote, "price", "regularMarketPrice")
    if price is None:
        price = _get(chart, "meta", "regularMarketPrice")
    market_cap = _get(quote, "price", "marketCap") or _get(quote, "summaryDetail", "marketCap")

    # Share count, in priority order: market cap / price, then Yahoo's reported
    # `sharesOutstanding`, then the diluted average from the filings.
    #
    # Market cap over price comes first because Yahoo's `sharesOutstanding` is
    # unreliable for IDX listings by orders of magnitude -- it reports 1,395,970
    # for LPPF against an implied 1,170,221,581 (838x), and 22,400,000 for BDMN
    # against 9,773,552,914 (436x). Both errors flow straight into book value per
    # share and every per-share valuation: BDMN was valued at IDR 1.7 million a
    # share against a IDR 4,410 price. Market cap and price come from the same
    # quote payload and are internally consistent, which is what makes the ratio
    # trustworthy where the standalone field is not.
    reported_shares = _get(quote, "defaultKeyStatistics", "sharesOutstanding")
    implied_shares = (market_cap / price) if (market_cap and price) else None

    shares = implied_shares or reported_shares or core.shares_diluted
    shares_source = (
        "market_cap/price" if implied_shares
        else "reported" if reported_shares
        else "diluted_average" if core.shares_diluted
        else None
    )

    # Record when the sources disagree materially, so a bad share count is
    # visible in the output rather than silently priced in.
    shares_disagreement = None
    if implied_shares and reported_shares:
        shares_disagreement = round(reported_shares / implied_shares, 4)

    if not market_cap and shares and price:
        market_cap = shares * price

    net_debt = (core.total_debt or 0.0) - (core.cash or 0.0)

    # Enterprise value is computed from market cap plus our own balance-sheet net
    # debt, not taken from Yahoo's `enterpriseValue`. Yahoo's figure is derived
    # from its own cash and debt snapshot, which disagrees with the statements by
    # more than 5% of market cap on 557 of 956 IDX tickers -- for ESSA it
    # recognised only IDR 345bn of a IDR 2,945bn net cash pile, overstating
    # EV/EBIT at 6.5x against a true 5.0x. Deriving it here keeps EV, net debt,
    # EPV and the Acquirer's Multiple all consistent with one balance sheet.
    # Minority interest belongs in enterprise value: EV is the cost of acquiring
    # the whole enterprise, and EBIT/EBITDA are consolidated figures that already
    # include the minorities' share of earnings. Omitting it compares a
    # parent-only numerator against a consolidated denominator and understates
    # every EV multiple. It exceeds 5% of market cap on 154 of 956 IDX tickers --
    # PNIN by 16x, BHIT by 10x -- and for INDY it lifts EV/EBIT from 9.1x to
    # 10.1x. Derived rather than read: total equity including minorities, less
    # the parent's stockholders' equity.
    minority_interest = 0.0
    if (
        core.total_assets is not None
        and core.total_liabilities is not None
        and core.total_equity is not None
    ):
        derived = (core.total_assets - core.total_liabilities) - core.total_equity
        # Rounding noise and restatements can make this mildly negative; a
        # negative minority interest is not meaningful, so it floors at zero.
        minority_interest = max(0.0, derived)

    if market_cap is not None:
        enterprise_value = market_cap + net_debt + minority_interest
    else:
        enterprise_value = _get(quote, "defaultKeyStatistics", "enterpriseValue")

    beta = _get(quote, "defaultKeyStatistics", "beta")
    currency = _get(quote, "price", "currency") or "IDR"

    return {
        "ticker": ticker, "bundle": bundle, "core": core, "quote": quote, "chart": chart,
        "price": price, "market_cap": market_cap, "shares": shares,
        "enterprise_value": enterprise_value, "net_debt": net_debt, "beta": beta,
        "currency": currency, "market": market, "long_chart": long_chart,
        "minority_interest": minority_interest,
        "statement_currency": statement_currency, "fx_rate": fx,
        "shares_source": shares_source, "shares_disagreement": shares_disagreement,
    }


def derive_rows(record: dict[str, Any], settings: Settings, seed: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Turn one fetched record into the row for each output file."""
    ticker = record["ticker"]
    bundle, core = record["bundle"], record["core"]
    price, shares = record["price"], record["shares"]
    market_cap, enterprise_value = record["market_cap"], record["enterprise_value"]
    quote = record["quote"]

    # ------------------------------------------------------------ per-share
    eps_ttm = M.safe_div(core.net_income_ttm, shares)
    eps_annualised = M.safe_div((core.net_income_q or 0) * 4, shares) if core.net_income_q is not None else None
    book_value_ps = M.safe_div(core.total_equity, shares)
    fcf_ps = M.safe_div(core.fcf_ttm, shares)
    revenue_ps = M.safe_div(core.revenue_ttm, shares)
    cash_ps = M.safe_div(core.cash, shares)

    # ---------------------------------------------------------- multiples
    pe_ttm = M.safe_div(price, eps_ttm) if eps_ttm and eps_ttm > 0 else M.safe_div(price, eps_ttm)
    pe_annualised = M.safe_div(price, eps_annualised)
    forward_eps = _get(quote, "defaultKeyStatistics", "forwardEps")
    forward_pe = M.safe_div(price, forward_eps)
    pb = M.safe_div(price, book_value_ps)
    ps = M.safe_div(market_cap, core.revenue_ttm)
    p_cf = M.safe_div(market_cap, core.cfo_ttm)
    p_fcf = M.safe_div(market_cap, core.fcf_ttm)
    ev_ebit = M.safe_div(enterprise_value, core.ebit_ttm)
    ev_ebitda = M.safe_div(enterprise_value, core.ebitda_ttm)
    earnings_yield_ni = M.safe_div(eps_ttm, price)
    earnings_yield_gb = M.earnings_yield_greenblatt(core.ebit_ttm, enterprise_value)
    fcf_yield = M.safe_div(core.fcf_ttm, market_cap)

    # -------------------------------------------------------------- returns
    roa = M.safe_div(core.net_income_ttm, core.total_assets)
    roe = M.safe_div(core.net_income_ttm, core.total_equity)
    capital_employed = None
    if core.total_assets is not None and core.current_liabilities is not None:
        capital_employed = core.total_assets - core.current_liabilities
    roce = M.safe_div(core.ebit_ttm, capital_employed)
    roic = M.return_on_invested_capital(core, settings.tax_rate)
    roc_greenblatt = M.return_on_capital_greenblatt(core)

    # -------------------------------------------------------------- margins
    gross_margin_q = M.safe_div(core.gross_profit_q, core.revenue_q)
    operating_margin_q = M.safe_div(core.operating_income_q, core.revenue_q)
    net_margin_q = M.safe_div(core.net_income_q, core.revenue_q)

    # --------------------------------------------------------------- growth
    revenue_growth = M.growth(core.revenue_q, M.nth_last(bundle, "TotalRevenue", 4))
    gross_growth = M.growth(core.gross_profit_q, M.nth_last(bundle, "GrossProfit", 4))
    ni_growth = M.growth(core.net_income_q, M.nth_last(bundle, "NetIncome", 4))

    revenue_series = bundle.get("quarterlyTotalRevenue") or []
    quarters_of_history = len(revenue_series)

    def annual_cagr(field: str, years: int) -> float | None:
        """CAGR across the annual series, which reaches back further than the
        quarterly one. Yahoo carries ~4 annual periods but only ~6 quarters, so
        a TTM-offset CAGR (needing 12 or 20 quarters) is never computable here.
        """
        series = bundle.get(f"annual{field}") or []
        if len(series) < years + 1:
            # Use whatever span is available rather than returning nothing; the
            # actual span is reported in "Years of Annual History".
            if len(series) < 2:
                return None
            return M.cagr(series[-1]["value"], series[0]["value"], len(series) - 1)
        return M.cagr(series[-1]["value"], series[-1 - years]["value"], years)

    revenue_cagr_3y = annual_cagr("TotalRevenue", 3)
    revenue_cagr_5y = annual_cagr("TotalRevenue", 5)
    ni_cagr_3y = annual_cagr("NetIncome", 3)
    eps_cagr_3y = ni_cagr_3y
    years_annual_history = len(bundle.get("annualTotalRevenue") or [])

    annual_revenue = [item["value"] for item in (bundle.get("annualTotalRevenue") or [])[-5:]]
    revenue_volatility = None
    if len(annual_revenue) >= 3:
        mean = sum(annual_revenue) / len(annual_revenue)
        if mean:
            variance = sum((value - mean) ** 2 for value in annual_revenue) / len(annual_revenue)
            revenue_volatility = (variance**0.5) / abs(mean)

    gross_margin_5y = M.median([
        M.safe_div(gross["value"], rev["value"])
        for gross, rev in zip(
            (bundle.get("annualGrossProfit") or [])[-5:],
            (bundle.get("annualTotalRevenue") or [])[-5:],
        )
        if M.safe_div(gross["value"], rev["value"]) is not None
    ])
    ebit_margin_5y = M.median([
        M.safe_div(ebit["value"], rev["value"])
        for ebit, rev in zip(
            (bundle.get("annualEBIT") or bundle.get("annualOperatingIncome") or [])[-5:],
            (bundle.get("annualTotalRevenue") or [])[-5:],
        )
        if M.safe_div(ebit["value"], rev["value"]) is not None
    ])
    roe_5y = M.median([
        M.safe_div(ni["value"], eq["value"])
        for ni, eq in zip(
            (bundle.get("annualNetIncome") or [])[-5:],
            (bundle.get("annualStockholdersEquity") or [])[-5:],
        )
        if M.safe_div(ni["value"], eq["value"]) is not None
    ])

    # ------------------------------------------------------------- liquidity
    current_ratio = M.safe_div(core.current_assets, core.current_liabilities)
    quick_assets = None
    if core.current_assets is not None:
        quick_assets = core.current_assets - (core.inventory or 0.0)
    quick_ratio = M.safe_div(quick_assets, core.current_liabilities)
    debt_equity = M.safe_div(core.total_debt, core.total_equity)
    ltd_equity = M.safe_div(core.long_term_debt, core.total_equity)
    liabilities_equity = M.safe_div(core.total_liabilities, core.total_equity)
    debt_assets = M.safe_div(core.total_debt, core.total_assets)
    financial_leverage = M.safe_div(core.total_assets, core.total_equity)
    interest_coverage = M.safe_div(core.ebit_ttm, abs(core.interest_expense_ttm or 0.0) or None)
    net_debt_equity = M.safe_div(record["net_debt"], core.total_equity)

    # ------------------------------------------------------------ efficiency
    # Cost of revenue drives days-inventory and days-payables. Derive it once,
    # and only when both inputs exist: a filer that reports inventory but no
    # revenue line (banks holding repossessed assets, newly listed shells) would
    # otherwise crash the whole row on a None minus int.
    cogs_ttm = None
    if core.revenue_ttm is not None and core.gross_profit_ttm is not None:
        cogs_ttm = core.revenue_ttm - core.gross_profit_ttm
    cogs_basis = abs(cogs_ttm) if cogs_ttm else None

    dso = M.safe_div((core.receivables or 0) * 365, core.revenue_ttm) if core.receivables else None
    dio = M.safe_div((core.inventory or 0) * 365, cogs_basis) if core.inventory else None
    dpo = M.safe_div((core.payables or 0) * 365, cogs_basis) if core.payables else None
    ccc = None
    if dso is not None and dio is not None and dpo is not None:
        ccc = dso + dio - dpo
    receivables_turnover = M.safe_div(core.revenue_ttm, core.receivables)
    asset_turnover = M.safe_div(core.revenue_ttm, core.total_assets)
    inventory_turnover = M.safe_div(cogs_ttm, core.inventory)

    # ------------------------------------------------------------- dividends
    dividend_rate = _get(quote, "summaryDetail", "dividendRate")
    dividend_yield = _get(quote, "summaryDetail", "dividendYield")
    if dividend_yield is None and dividend_rate and price:
        dividend_yield = dividend_rate / price
    # Computed from the dividend and EPS actually reported, not Yahoo's
    # `payoutRatio`, which lags a fiscal year and contradicted DPS/EPS on 49 of
    # 956 rows. ESSA's field read 0.2023 while its own DPS of IDR 52 against EPS
    # of IDR 41.9 was a 125% payout funded partly from retained earnings - the
    # difference between a covered 8% yield and a liquidating one.
    payout_ratio = None
    if dividend_rate and eps_ttm and eps_ttm > 0:
        payout_ratio = dividend_rate / eps_ttm
    if payout_ratio is None:
        payout_ratio = _get(quote, "summaryDetail", "payoutRatio")
    ex_date = _get(quote, "summaryDetail", "exDividendDate")
    ex_date_str = (
        datetime.utcfromtimestamp(ex_date).date().isoformat() if isinstance(ex_date, (int, float)) else ""
    )

    # ------------------------------------------------------- quality scores
    f_score, f_signals = M.piotroski_f_score(bundle)
    altman = M.altman_z_modified(core)
    ncav_ps = M.ncav_per_share(core, shares)
    ncav = (core.current_assets - core.total_liabilities) if (
        core.current_assets is not None and core.total_liabilities is not None
    ) else None

    normalised_ebit_value = M.normalised_ebit(bundle)
    core.__dict__["_normalised_ebit"] = normalised_ebit_value
    normalised_ebit_margin = M.safe_div(normalised_ebit_value, M.median([
        item["value"] for item in (bundle.get("annualTotalRevenue") or [])[-5:]
    ]))

    cost_of_equity = M.cost_of_equity_capm(
        settings.risk_free_rate, settings.equity_risk_premium, record["beta"], net_debt_equity
    )
    epv_ps = M.epv_per_share(core, shares, cost_of_equity, settings.tax_rate)

    # ------------------------------------------------------------- verdict
    sector = seed.get("sector")
    business_type = S.classify_business(sector, core, price, shares, roic, revenue_cagr_3y)
    is_net_net, _ = S.net_net_test(core, price, shares)

    assessment = S.Assessment(ticker=ticker, business_type=business_type)
    assessment.quality_score = S.score_quality(
        core, roic, roe, business_type, revenue_cagr_3y, gross_margin_5y or gross_margin_q
    )
    assessment.safety_score = S.score_safety(core, f_score, altman, business_type)
    assessment.value_score = S.score_value(
        earnings_yield_gb, ev_ebit, pe_ttm, pb, fcf_yield, business_type
    )
    assessment.scenarios = S.build_scenarios(
        core, normalised_ebit_value, shares, price, settings.wacc,
        settings.terminal_growth, revenue_cagr_3y, settings.tax_rate,
        normalised_capex_value=M.normalised_capex(bundle),
    )
    assessment.flags = S.detect_red_flags(core, bundle, business_type)
    if S.growth_destroys_value(assessment.scenarios):
        assessment.flags.append(
            "Growth destroys value - working capital consumed exceeds returns earned"
        )

    staleness = M.quarters_stale(core.as_of)
    scores = [s for s in (assessment.quality_score, assessment.safety_score, assessment.value_score) if s is not None]
    assessment.composite = round(sum(scores) / len(scores), 1) if scores else None

    # The blend, margin of safety and verdict need peer medians, which only
    # exist once the whole universe is loaded. `finalise_row` completes them in
    # a second pass -- see `run`.

    # --------------------------------------------------------- price context
    chart_meta = (record["chart"] or {}).get("meta") or {}
    high_52w = chart_meta.get("fiftyTwoWeekHigh") or _get(quote, "summaryDetail", "fiftyTwoWeekHigh")
    low_52w = chart_meta.get("fiftyTwoWeekLow") or _get(quote, "summaryDetail", "fiftyTwoWeekLow")
    pct_from_high = M.safe_div((price or 0) - (high_52w or 0), high_52w)
    closes = ((record["chart"] or {}).get("indicators", {}).get("quote") or [{}])[0].get("close") or []
    first_close = next((value for value in closes if value), None)
    yearly_change = M.safe_div((price or 0) - (first_close or 0), first_close)

    long_closes = [
        value
        for value in (
            ((record.get("long_chart") or {}).get("indicators", {}).get("quote") or [{}])[0].get("close") or []
        )
        if value
    ]
    price_cagr_3y = price_cagr_5y = price_percentile_10y = max_drawdown_10y = None
    if len(long_closes) >= 12 and price:
        if len(long_closes) >= 36:
            price_cagr_3y = M.cagr(price, long_closes[-36], 3)
        if len(long_closes) >= 60:
            price_cagr_5y = M.cagr(price, long_closes[-60], 5)
        # Where today sits in its own decade-long range: 0 = decade low.
        low, high = min(long_closes), max(long_closes)
        if high > low:
            price_percentile_10y = round((price - low) / (high - low), 4)
        peak = long_closes[0]
        worst = 0.0
        for close in long_closes:
            peak = max(peak, close)
            worst = min(worst, close / peak - 1)
        max_drawdown_10y = round(worst, 4)

    fetched_at = datetime.now().isoformat(timespec="seconds")

    keystats = {
        "Ticker": ticker,
        "Current PE Ratio (Annualised)": pe_annualised,
        "Current PE Ratio (TTM)": pe_ttm,
        "Forward PE Ratio": forward_pe,
        "IHSG PE Ratio TTM (Median)": None,  # filled in the cross-sectional pass
        "Earnings Yield (TTM)": earnings_yield_ni,
        "Current Price to Sales(TTM)": ps,
        "Current Price to Book Value": pb,
        "Current Price To Cashflow (TTM)": p_cf,
        "Current Price To Free Cashflow (TTM)": p_fcf,
        "EV to EBIT (TTM)": ev_ebit,
        "EV to EBITDA (TTM)": ev_ebitda,
        "PEG Ratio": M.safe_div(pe_ttm, (ni_growth or 0) * 100) if ni_growth else None,
        "PEG Ratio (3yr)": M.safe_div(pe_ttm, (ni_cagr_3y or 0) * 100) if ni_cagr_3y else None,
        "PEG (Forward)": None,
        "Current EPS (TTM)": eps_ttm,
        "Current EPS (Annualised)": eps_annualised,
        "Revenue Per Share (TTM)": revenue_ps,
        "Cash Per Share (Quarter)": cash_ps,
        "Current Book Value Per Share": book_value_ps,
        "Free Cashflow Per Share (TTM)": fcf_ps,
        "Current Ratio (Quarter)": current_ratio,
        "Quick Ratio (Quarter)": quick_ratio,
        "Debt to Equity Ratio (Quarter)": debt_equity,
        "LT Debt/Equity (Quarter)": ltd_equity,
        "Total Liabilities/Equity (Quarter)": liabilities_equity,
        "Total Debt/Total Assets (Quarter)": debt_assets,
        "Financial Leverage (Quarter)": financial_leverage,
        "Interest Coverage (TTM)": interest_coverage,
        "Free cash flow (Quarter)": M.nth_last(bundle, "FreeCashFlow", 0),
        "Altman Z-Score (Modified)": altman,
        "Return on Assets (TTM)": roa,
        "Return on Equity (TTM)": roe,
        "Return on Capital Employed (TTM)": roce,
        "Return On Invested Capital (TTM)": roic,
        "Days Sales Outstanding (Quarter)": dso,
        "Days Inventory (Quarter)": dio,
        "Days Payables Outstanding (Quarter)": dpo,
        "Cash Conversion Cycle (Quarter)": ccc,
        "Receivables Turnover (Quarter)": receivables_turnover,
        "Asset Turnover (TTM)": asset_turnover,
        "Inventory Turnover (TTM)": inventory_turnover,
        "Gross Profit Margin (Quarter)": gross_margin_q,
        "Operating Profit Margin (Quarter)": operating_margin_q,
        "Net Profit Margin (Quarter)": net_margin_q,
        "Revenue (Quarter YoY Growth)": revenue_growth,
        "Gross Profit (Quarter YoY Growth)": gross_growth,
        "Net Income (Quarter YoY Growth)": ni_growth,
        "Dividend": dividend_rate,
        "Dividend (TTM)": dividend_rate,
        "Payout Ratio": payout_ratio,
        "Dividend Yield": dividend_yield,
        "Latest Dividend Ex-Date": ex_date_str,
        "Piotroski F-Score": f_score,
        "EPS Rating": None,
        "Relative Strength Rating": None,
        "Rank (Market Cap)": None,
        "Rank (Current PE Ratio TTM)": None,
        "Rank (Earnings Yield)": None,
        "Rank (P/S)": None,
        "Rank (P/B)": None,
        "Rank (Near 52 Weeks High)": None,
        "Revenue (TTM)": core.revenue_ttm,
        "Gross Profit (TTM)": core.gross_profit_ttm,
        "EBITDA (TTM)": core.ebitda_ttm,
        "Net Income (TTM)": core.net_income_ttm,
        "Cash (Quarter)": core.cash,
        "Total Assets (Quarter)": core.total_assets,
        "Total Liabilities (Quarter)": core.total_liabilities,
        "Working Capital (Quarter)": core.working_capital,
        # --- appended
        "Market Cap": market_cap,
        "Enterprise Value": enterprise_value,
        "Current Share Outstanding": shares,
        "Total Equity": core.total_equity,
        "Total Debt (Quarter)": core.total_debt,
        "Net Debt (Quarter)": record["net_debt"],
        "Current Assets (Quarter)": core.current_assets,
        "Current Liabilities (Quarter)": core.current_liabilities,
        "EBIT (TTM)": core.ebit_ttm,
        "Operating Cash Flow (TTM)": core.cfo_ttm,
        "Capital expenditure (TTM)": core.capex_ttm,
        "Free cash flow (TTM)": core.fcf_ttm,
        "Inventory (Quarter)": core.inventory,
        "Retained Earnings (Quarter)": core.retained_earnings,
        "Beta": record["beta"],
        "Earnings Yield Greenblatt (EBIT/EV)": earnings_yield_gb,
        "ROC Greenblatt": roc_greenblatt,
        "Acquirers Multiple (EV/EBIT)": ev_ebit,
        "FCF Yield (TTM)": fcf_yield,
        "NCAV": ncav,
        "NCAV per Share": ncav_ps,
        "Net-Net Pass": is_net_net,
        "Normalised EBIT (5Y)": normalised_ebit_value,
        "Normalised EBIT Margin": normalised_ebit_margin,
        "Normalised/Trailing EBIT": M.safe_div(normalised_ebit_value, core.ebit_ttm),
        "Working Capital Intensity": M.working_capital_intensity(core),
        # 1/(WACC - g). Surfaced because it silently drives ~70% of any DCF's
        # present value: at 12% and 3% it implies an ~11x terminal cash-flow
        # multiple, well above the ~7.6x EV/EBIT Indonesian distributors
        # actually trade at. A terminal multiple far above sector norms is an
        # assumption, not a result.
        "Implied Terminal Multiple": round(1.0 / (settings.wacc - settings.terminal_growth), 2),
        "EPV per Share": epv_ps,
        "Revenue CAGR 3Y": revenue_cagr_3y,
        "Revenue CAGR 5Y": revenue_cagr_5y,
        "EPS CAGR 3Y": eps_cagr_3y,
        "Net Income CAGR 3Y": ni_cagr_3y,
        "Gross Margin 5Y Avg": gross_margin_5y,
        "EBIT Margin 5Y Avg": ebit_margin_5y,
        "ROE 5Y Avg": roe_5y,
        "Revenue Volatility 5Y": revenue_volatility,
        "Quarters of History": quarters_of_history,
        "Years of Annual History": years_annual_history,
        "F: ROA Positive": f_signals.get("roa_positive"),
        "F: CFO Positive": f_signals.get("cfo_positive"),
        "F: ROA Improving": f_signals.get("roa_improving"),
        "F: Accruals": f_signals.get("accruals"),
        "F: Leverage Falling": f_signals.get("leverage_falling"),
        "F: Current Ratio Improving": f_signals.get("current_ratio_improving"),
        "F: No Dilution": f_signals.get("no_dilution"),
        "F: Gross Margin Improving": f_signals.get("gross_margin_improving"),
        "F: Asset Turnover Improving": f_signals.get("asset_turnover_improving"),
        "F-Score Basis": f_signals.get("_basis"),
        "52W High": high_52w,
        "52W Low": low_52w,
        "Pct From 52W High": pct_from_high,
        "1Y Price Change": yearly_change,
        "Price CAGR 3Y": price_cagr_3y,
        "Price CAGR 5Y": price_cagr_5y,
        "Price Percentile 10Y": price_percentile_10y,
        "Max Drawdown 10Y": max_drawdown_10y,
        "Months of Price History": len(long_closes),
        "Latest Filing Date": core.as_of,
        "Quarters Stale": staleness,
        "Statement Currency": record["statement_currency"],
        "FX Rate Applied": record["fx_rate"],
        "Minority Interest": record["minority_interest"],
        "Share Count Source": record["shares_source"],
        "Reported/Implied Shares": record["shares_disagreement"],
        "Data Source": "Yahoo Finance",
        "Fetched At": fetched_at,
    }

    idx_row = {
        "Ticker": ticker,
        "Name": seed.get("name") or _get(quote, "price", "longName") or "",
        "IPO Date": seed.get("ipo_date") or "",
        "Outstanding Shares": shares,
        "Note": seed.get("board_note") or "",
        "Price": price,
        "Volume": _get(quote, "price", "regularMarketVolume"),
        "Change": _get(quote, "price", "regularMarketChange"),
        "Percentage Change": (_get(quote, "price", "regularMarketChangePercent") or 0) * 100
        if _get(quote, "price", "regularMarketChangePercent") is not None else None,
        "Average": _get(quote, "price", "regularMarketPreviousClose"),
        "Close Price": price,
        "High Price": _get(quote, "price", "regularMarketDayHigh"),
        "Open Price": _get(quote, "price", "regularMarketOpen"),
        "Low Price": _get(quote, "price", "regularMarketDayLow"),
        # ARA/ARB and buy/sell frequency are IDX auto-rejection mechanics that
        # only RTI publishes. Yahoo has no equivalent; columns are kept so the
        # sheet layout is unchanged, but they are intentionally blank.
        "ARA Price": None, "ARB Price": None, "Frequency": None,
        "Frequency Sell": None, "Frequency Buy": None,
        "52W High": high_52w, "52W Low": low_52w,
        "Pct From 52W High": pct_from_high, "1Y Price Change": yearly_change,
        "Currency": record["currency"], "Fetched At": fetched_at,
    }

    analyses_row = {
        "Ticker": ticker,
        "PBV x ROE": (pb * roe) if (pb is not None and roe is not None) else None,
        "Close Price": price,
        "Price to Equity Discount (%)": ((book_value_ps - price) / price * 100)
        if (book_value_ps and price) else None,
        "Relative PE ratio (TTM)": None,  # cross-sectional pass
        "EPS Growth": ni_growth,
        "Debt to Total Assets Ratio": debt_assets,
        "Liquidity Differential": current_ratio,
        "CCE": M.safe_div(core.cash, core.total_assets),
        "Operating Efficiency": operating_margin_q,
        "Dividend Payout Efficiency": payout_ratio,
        "Yearly Price Change": yearly_change,
        "Composite Rank": None,  # cross-sectional pass
        "Net Debt to Equity": net_debt_equity,
    }

    score_row = {
        "Ticker": ticker,
        "Name": idx_row["Name"],
        "Sector": sector or "",
        "Business Type": business_type,
        "Price": price,
        "Quality Score": assessment.quality_score,
        "Safety Score": assessment.safety_score,
        "Value Score": assessment.value_score,
        "Composite Score": assessment.composite,
        "F-Score": f_score,
        "Altman Z": altman,
        "Earnings Yield (EBIT/EV)": earnings_yield_gb,
        "ROC (Greenblatt)": roc_greenblatt,
        "Acquirers Multiple": ev_ebit,
        "Net-Net Pass": is_net_net,
        "NCAV per Share": ncav_ps,
        "EPV per Share": epv_ps,
        "IV Bear": assessment.scenarios["bear"].intrinsic_value,
        "IV Base": assessment.scenarios["base"].intrinsic_value,
        "IV Bull": assessment.scenarios["bull"].intrinsic_value,
        "MOS Bear": assessment.scenarios["bear"].mos,
        "MOS Base": assessment.scenarios["base"].mos,
        "MOS Bull": assessment.scenarios["bull"].mos,
        "Blended IV": assessment.intrinsic_base,
        "MOS Blended": assessment.mos_base,
        "Upside Blended": assessment.upside_base,
        "Verdict": assessment.verdict,
        "Reasons": "; ".join(assessment.reasons),
        "Red Flags": "; ".join(assessment.flags),
        "Comparables IV": None,
        "Justified PB IV": None,
        "Quarters Stale": staleness,
        "Latest Filing": core.as_of,
    }

    history_rows: list[dict[str, Any]] = []
    for period in ("quarterly", "annual"):
        dates: set[str] = set()
        for field_ in HISTORY_FIELDS:
            for item in bundle.get(f"{period}{field_}") or []:
                if item["asOfDate"]:
                    dates.add(item["asOfDate"])
        for as_of in sorted(dates):
            row = {"Ticker": ticker, "Period Type": period, "Period End": as_of}
            for field_ in HISTORY_FIELDS:
                value = next(
                    (item["value"] for item in bundle.get(f"{period}{field_}") or []
                     if item["asOfDate"] == as_of),
                    None,
                )
                row[field_] = value
            history_rows.append(row)

    return {
        "keystats": keystats, "idx": idx_row, "analyses": analyses_row,
        "scores": score_row, "history": history_rows,
        "_pending": {
            "assessment": assessment, "core": core, "price": price, "shares": shares,
            "eps_ttm": eps_ttm, "book_value_ps": book_value_ps, "roe": roe,
            "epv_ps": epv_ps, "ncav_ps": ncav_ps, "business_type": business_type,
            "f_score": f_score, "is_net_net": is_net_net, "staleness": staleness,
            "cost_of_equity": cost_of_equity, "net_debt": record["net_debt"],
            "revenue_cagr_3y": revenue_cagr_3y, "settings": settings,
        },
    }


def cross_sectional_pass(rows: list[dict[str, Any]]) -> None:
    """Fill the market-relative columns that need the whole universe present.

    Percentile ranks are computed only over rows where the metric is genuinely
    available. The original workbook ranked over blanks coerced to zero, which
    pushed every no-data name to one end of the distribution and displaced the
    real extremes.
    """
    keystats = [row["keystats"] for row in rows]

    pe_values = [
        row["Current PE Ratio (TTM)"] for row in keystats
        if row["Current PE Ratio (TTM)"] is not None and row["Current PE Ratio (TTM)"] > 0
    ]
    market_pe = M.median(pe_values)
    for row in keystats:
        row["IHSG PE Ratio TTM (Median)"] = market_pe

    def percentile_rank(column: str, target: str, ascending: bool = False) -> None:
        pairs = [(row["Ticker"], row[column]) for row in keystats if row[column] is not None]
        if not pairs:
            return
        pairs.sort(key=lambda item: item[1], reverse=not ascending)
        total = len(pairs)
        lookup = {ticker: 1 - (index / total) for index, (ticker, _) in enumerate(pairs)}
        for row in keystats:
            row[target] = round(lookup[row["Ticker"]], 4) if row["Ticker"] in lookup else None

    percentile_rank("Market Cap", "Rank (Market Cap)")
    percentile_rank("Current PE Ratio (TTM)", "Rank (Current PE Ratio TTM)", ascending=True)
    percentile_rank("Earnings Yield Greenblatt (EBIT/EV)", "Rank (Earnings Yield)")
    percentile_rank("Current Price to Sales(TTM)", "Rank (P/S)", ascending=True)
    percentile_rank("Current Price to Book Value", "Rank (P/B)", ascending=True)
    percentile_rank("Pct From 52W High", "Rank (Near 52 Weeks High)")

    for row in rows:
        pe = row["keystats"]["Current PE Ratio (TTM)"]
        row["analyses"]["Relative PE ratio (TTM)"] = (
            pe / market_pe if pe and market_pe else None
        )

    # Composite rank blends the four lenses into one 0-1 ordering.
    components = [
        ("Rank (Earnings Yield)", 0.3),
        ("Rank (P/B)", 0.2),
        ("Rank (Current PE Ratio TTM)", 0.2),
        ("Rank (Market Cap)", 0.1),
    ]
    for row in rows:
        stats = row["keystats"]
        parts = [(stats[name], weight) for name, weight in components if stats.get(name) is not None]
        f_score = stats.get("Piotroski F-Score")
        if f_score is not None:
            parts.append((f_score / 9.0, 0.2))
        if parts:
            total_weight = sum(weight for _, weight in parts)
            row["analyses"]["Composite Rank"] = round(
                sum(value * weight for value, weight in parts) / total_weight, 4
            )


def peer_medians(rows: list[dict[str, Any]], seeds: dict[str, dict[str, Any]]) -> dict[str, dict[str, float | None]]:
    """Peer-group medians with a minimum-population fallback.

    Peer groups tighten from sub-industry to sector, stepping out only when a
    level holds fewer than four *valid* observations. The original workbook
    counted group membership, not valid observations, so a five-member group
    where four had negative EBIT still produced a one-stock "median".
    """
    groups: dict[str, dict[str, list[float]]] = {}

    def keys_for(ticker: str) -> list[str]:
        seed = seeds.get(ticker, {})
        parts = [seed.get("sector"), seed.get("subsector"), seed.get("industry"), seed.get("subindustry")]
        parts = [part for part in parts if part]
        return [" | ".join(parts[: n + 1]) for n in range(len(parts))][::-1]  # tightest first

    for row in rows:
        ticker = row["keystats"]["Ticker"]
        pe = row["keystats"]["Current PE Ratio (TTM)"]
        ev_ebit = row["keystats"]["EV to EBIT (TTM)"]
        pb = row["keystats"]["Current Price to Book Value"]
        for key in keys_for(ticker):
            bucket = groups.setdefault(key, {"pe": [], "ev_ebit": [], "pb": []})
            if pe is not None and 0 < pe < 100:
                bucket["pe"].append(pe)
            if ev_ebit is not None and 0 < ev_ebit < 50:
                bucket["ev_ebit"].append(ev_ebit)
            if pb is not None and 0 < pb < 20:
                bucket["pb"].append(pb)

    out: dict[str, dict[str, float | None]] = {}
    for row in rows:
        ticker = row["keystats"]["Ticker"]
        chosen = {"pe": None, "ev_ebit": None, "pb": None, "group": None, "n": 0}
        for key in keys_for(ticker):
            bucket = groups.get(key, {})
            if len(bucket.get("pe", [])) >= 4 or len(bucket.get("ev_ebit", [])) >= 4:
                chosen = {
                    "pe": M.median(bucket.get("pe", [])),
                    "ev_ebit": M.median(bucket.get("ev_ebit", [])),
                    "pb": M.median(bucket.get("pb", [])),
                    "group": key,
                    "n": max(len(bucket.get("pe", [])), len(bucket.get("ev_ebit", []))),
                }
                break
        out[ticker] = chosen
    return out


def finalise_row(row: dict[str, Any], peer: dict[str, Any]) -> None:
    """Second pass: peer comparables, blended intrinsic value, MOS and verdict.

    Split out from `derive_rows` because peer medians are a property of the
    whole universe, not of one ticker. Doing this inline during the fetch would
    have valued every name against an incomplete peer set -- the first ticker
    processed would see no peers at all.
    """
    pending = row["_pending"]
    assessment: S.Assessment = pending["assessment"]
    core: M.CoreFinancials = pending["core"]
    settings: Settings = pending["settings"]
    price, shares = pending["price"], pending["shares"]
    business_type = pending["business_type"]

    comps_value = M.comparables_value(
        eps_ttm=pending["eps_ttm"],
        peer_pe=peer.get("pe"),
        ebit_ttm=core.ebit_ttm,
        peer_ev_ebit=peer.get("ev_ebit"),
        net_debt=pending["net_debt"],
        shares=shares,
        book_value_per_share=pending["book_value_ps"],
        peer_pb=peer.get("pb"),
    )

    # Banks and insurers get a residual-income valuation instead of the
    # cash-flow lenses, which do not apply to them.
    justified_pb = None
    if business_type == S.BUSINESS_FINANCIAL:
        justified_pb = M.justified_pb_value(
            book_value_per_share=pending["book_value_ps"],
            roe=pending["roe"],
            cost_of_equity=pending["cost_of_equity"],
            growth=min(pending["revenue_cagr_3y"] or 0.03, settings.terminal_growth + 0.02),
        )

    epv_ps = pending["epv_ps"]
    if business_type == S.BUSINESS_FINANCIAL:
        # `blended_intrinsic` averages comparables and EPV for financials; the
        # justified-P/B figure is the appropriate stand-in for EPV here.
        epv_ps = justified_pb

    assessment.intrinsic_base = S.blended_intrinsic(
        assessment.scenarios, epv_ps, comps_value, pending["ncav_ps"], business_type
    )
    if assessment.intrinsic_base and price:
        # MOS divides by intrinsic value, so an intrinsic value near zero
        # produces a meaningless four-digit negative percentage. Clamp the
        # reported figure: anything past -100% already means "worth far less
        # than the market price" and the extra precision is noise.
        raw_mos = (assessment.intrinsic_base - price) / assessment.intrinsic_base
        assessment.mos_base = max(-1.0, min(1.0, raw_mos))
        assessment.upside_base = assessment.intrinsic_base / price - 1

    assessment.verdict = S.classify(
        assessment, price, settings.mos_buy, settings.mos_watch, pending["f_score"],
        pending["is_net_net"], pending["staleness"], assessment.flags,
    )

    scores = row["scores"]
    scores["Comparables IV"] = comps_value
    scores["Justified PB IV"] = justified_pb
    scores["Blended IV"] = assessment.intrinsic_base
    scores["MOS Blended"] = assessment.mos_base
    scores["Upside Blended"] = assessment.upside_base
    scores["Verdict"] = assessment.verdict
    scores["Reasons"] = "; ".join(assessment.reasons)


def write_csv(path: Path, columns: list[str], rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def load_seeds(data_dir: Path) -> dict[str, dict[str, Any]]:
    seeds: dict[str, dict[str, Any]] = {}
    tickers_file = data_dir / "idx_tickers_seed.csv"
    if tickers_file.exists():
        with tickers_file.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                seeds[row["ticker"]] = dict(row)
    listing_file = data_dir / "idx_listing_seed.csv"
    if listing_file.exists():
        with listing_file.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                seeds.setdefault(row["ticker"], {}).update(
                    {"ipo_date": row.get("ipo_date"), "board_note": row.get("board_note")}
                )
    return seeds


def run(
    tickers: list[str],
    data_dir: Path,
    output_dir: Path,
    cache_dir: Path,
    settings: Settings,
    workers: int = 3,
    cache_ttl_hours: float = 20.0,
) -> dict[str, Any]:
    """Fetch, derive and write. Returns a run summary."""
    seeds = load_seeds(data_dir)
    client = YahooClient(cache_dir=cache_dir, cache_ttl_hours=cache_ttl_hours)
    started = time.time()

    rows: list[dict[str, Any]] = []
    failed: list[str] = []

    def work(ticker: str) -> dict[str, Any] | None:
        record = fetch_one(client, ticker, settings.market)
        if record is None:
            return None
        try:
            return derive_rows(record, settings, seeds.get(ticker, {}))
        except Exception:  # one malformed filer must not kill a 950-name run
            log.exception("derive failed for %s", ticker)
            return None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(work, ticker): ticker for ticker in tickers}
        for index, future in enumerate(as_completed(futures), 1):
            ticker = futures[future]
            try:
                result = future.result()
            except Exception:
                log.exception("fetch failed for %s", ticker)
                result = None
            if result is None:
                failed.append(ticker)
            else:
                rows.append(result)
            if index % 25 == 0 or index == len(tickers):
                elapsed = time.time() - started
                log.info(
                    "%d/%d done (%d ok, %d failed) %.0fs elapsed, cache hits %d",
                    index, len(tickers), len(rows), len(failed), elapsed,
                    client.stats["cache_hits"],
                )

    if not rows:
        raise RuntimeError("no tickers returned data")

    cross_sectional_pass(rows)
    peers = peer_medians(rows, seeds)

    for row in rows:
        ticker = row["keystats"]["Ticker"]
        peer = peers.get(ticker, {})
        row["scores"]["Peer Group"] = peer.get("group")
        row["scores"]["Peer Count"] = peer.get("n")
        row["scores"]["Peer PE Median"] = peer.get("pe")
        row["scores"]["Peer EV/EBIT Median"] = peer.get("ev_ebit")
        row["scores"]["Peer PB Median"] = peer.get("pb")
        finalise_row(row, peer)

    for row in rows:
        row.pop("_pending", None)

    rows.sort(key=lambda item: item["keystats"]["Ticker"])

    score_columns = list(rows[0]["scores"].keys())
    history_columns = ["Ticker", "Period Type", "Period End"] + HISTORY_FIELDS

    counts = {
        "RAW_idx_stocks.csv": write_csv(
            output_dir / "RAW_idx_stocks.csv", IDX_STOCKS_COLUMNS, (r["idx"] for r in rows)
        ),
        "RAW_key_statistics.csv": write_csv(
            output_dir / "RAW_key_statistics.csv", KEYSTATS_COLUMNS, (r["keystats"] for r in rows)
        ),
        "RAW_analyses.csv": write_csv(
            output_dir / "RAW_analyses.csv", ANALYSES_COLUMNS, (r["analyses"] for r in rows)
        ),
        "RAW_scores.csv": write_csv(
            output_dir / "RAW_scores.csv", score_columns, (r["scores"] for r in rows)
        ),
    }

    quarterly = [h for r in rows for h in r["history"] if h["Period Type"] == "quarterly"]
    annual = [h for r in rows for h in r["history"] if h["Period Type"] == "annual"]
    counts["RAW_history_quarterly.csv"] = write_csv(
        output_dir / "RAW_history_quarterly.csv", history_columns, quarterly
    )
    counts["RAW_history_annual.csv"] = write_csv(
        output_dir / "RAW_history_annual.csv", history_columns, annual
    )

    summary = {
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "market": settings.market,
        "tickers_requested": len(tickers),
        "tickers_ok": len(rows),
        "tickers_failed": len(failed),
        "failed": failed[:100],
        "elapsed_seconds": round(time.time() - started, 1),
        "rows_written": counts,
        "client_stats": client.stats,
    }
    (output_dir / "run_summary.json").write_text(
        __import__("json").dumps(summary, indent=2)
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refresh IDX fundamentals from Yahoo Finance")
    root = Path(__file__).resolve().parent.parent
    parser.add_argument("--tickers", help="Comma-separated tickers; default is the full seed universe")
    parser.add_argument("--limit", type=int, help="Process only the first N tickers")
    parser.add_argument("--data-dir", type=Path, default=root / "data")
    parser.add_argument("--output-dir", type=Path, default=root / "output")
    parser.add_argument("--cache-dir", type=Path, default=root / "data" / "cache")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--cache-ttl", type=float, default=20.0, help="Cache TTL in hours; -1 disables expiry")
    parser.add_argument("--market", default="IDX", choices=["IDX", "US"])
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout,
    )

    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    else:
        tickers = sorted(load_seeds(args.data_dir).keys())
    if args.limit:
        tickers = tickers[: args.limit]

    settings = Settings.for_market(args.market)
    summary = run(
        tickers, args.data_dir, args.output_dir, args.cache_dir, settings,
        workers=args.workers, cache_ttl_hours=args.cache_ttl,
    )
    print(__import__("json").dumps(summary, indent=2))
    return 0 if summary["tickers_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
