"""Derived fundamentals: TTM roll-ups, ratios, Piotroski, Altman, valuation.

Everything here is a pure function of the statement series returned by
`yahoo.YahooClient.fundamentals` plus the point-in-time market data from
`quote_summary`, so each metric is independently testable without a network.

Conventions
-----------
* Money is IDR *units* (not millions). The workbook divides by 1e6 at the sheet
  boundary, matching the original RAW_key_statistics contract.
* Flow items (revenue, net income, cash flow) are summed over the trailing four
  quarters. Stock items (assets, equity, debt) take the most recent quarter.
* Margins and growth rates are fractions, not percentages: 0.1323 = 13.23%.
* A metric that cannot be computed returns ``None`` rather than 0. The
  distinction matters -- the original workbook conflated "no data" with "zero",
  which silently dragged genuinely unprofitable names into the same bucket as
  names with a missing filing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Mapping, Sequence

Series = list[dict[str, Any]]
Bundle = Mapping[str, Series]

# Any |growth| beyond this is reported as None. Yahoo restates tiny bases
# (a IDR 1mn prior-year profit) and produces 5000x "growth" that would
# otherwise dominate every ranking built on top of it.
GROWTH_CAP = 10.0


# --------------------------------------------------------------------- helpers


def _q(bundle: Bundle, field: str, period: str = "quarterly") -> Series:
    return bundle.get(f"{period}{field}") or []


def latest(bundle: Bundle, field: str, period: str = "quarterly") -> float | None:
    """Most recent reported value for a stock (balance-sheet) item."""
    series = _q(bundle, field, period)
    return series[-1]["value"] if series else None


def latest_date(bundle: Bundle, field: str, period: str = "quarterly") -> str | None:
    series = _q(bundle, field, period)
    return series[-1]["asOfDate"] if series else None


def nth_last(bundle: Bundle, field: str, n: int, period: str = "quarterly") -> float | None:
    """`n=0` is the latest, `n=4` is the same quarter one year earlier."""
    series = _q(bundle, field, period)
    return series[-1 - n]["value"] if len(series) > n else None


def ttm(bundle: Bundle, field: str, offset: int = 0) -> float | None:
    """Trailing-twelve-month sum of a flow item.

    ``offset=4`` gives the prior-year TTM, which is what the year-over-year
    comparisons and the Piotroski deltas need. Returns None unless four
    consecutive quarters are present -- a three-quarter sum silently understates
    the metric by ~25% and is worse than an honest blank.
    """
    series = _q(bundle, field)
    end = len(series) - offset
    if end < 4:
        return None
    window = series[end - 4 : end]
    return sum(item["value"] for item in window)


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    try:
        value = numerator / denominator
    except (ZeroDivisionError, TypeError):
        return None
    return None if math.isinf(value) or math.isnan(value) else value


def growth(current: float | None, prior: float | None) -> float | None:
    """Year-over-year growth with a sign-aware, capped denominator.

    A negative base makes naive ``(cur - prior) / prior`` flip sign: swinging
    from -100 to +50 yields -1.5, which reads as a 150% *decline* for what is
    actually a turnaround. Using |prior| keeps the sign meaningful.
    """
    if current is None or prior is None or prior == 0:
        return None
    value = (current - prior) / abs(prior)
    return None if abs(value) > GROWTH_CAP else value


def cagr(latest_value: float | None, earliest_value: float | None, years: float) -> float | None:
    """Compound annual growth rate; undefined when either end is non-positive."""
    if not latest_value or not earliest_value or years <= 0:
        return None
    if latest_value <= 0 or earliest_value <= 0:
        return None
    return (latest_value / earliest_value) ** (1.0 / years) - 1.0


def median(values: Sequence[float]) -> float | None:
    clean = sorted(v for v in values if v is not None)
    if not clean:
        return None
    mid = len(clean) // 2
    if len(clean) % 2:
        return clean[mid]
    return (clean[mid - 1] + clean[mid]) / 2.0


# ------------------------------------------------------------------ core block


@dataclass
class CoreFinancials:
    """The statement figures every downstream metric is built from."""

    ticker: str
    as_of: str | None = None
    # Flows (TTM)
    revenue_ttm: float | None = None
    gross_profit_ttm: float | None = None
    ebit_ttm: float | None = None
    ebitda_ttm: float | None = None
    net_income_ttm: float | None = None
    cfo_ttm: float | None = None
    capex_ttm: float | None = None
    fcf_ttm: float | None = None
    interest_expense_ttm: float | None = None
    tax_ttm: float | None = None
    pretax_ttm: float | None = None
    # Flows (latest quarter)
    revenue_q: float | None = None
    gross_profit_q: float | None = None
    operating_income_q: float | None = None
    net_income_q: float | None = None
    # Stocks (latest quarter)
    total_assets: float | None = None
    total_liabilities: float | None = None
    total_equity: float | None = None
    cash: float | None = None
    total_debt: float | None = None
    long_term_debt: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    working_capital: float | None = None
    inventory: float | None = None
    receivables: float | None = None
    payables: float | None = None
    retained_earnings: float | None = None
    invested_capital: float | None = None
    shares_diluted: float | None = None


def build_core(ticker: str, bundle: Bundle) -> CoreFinancials:
    """Collapse the raw Yahoo series into the figures the model consumes.

    Falls back across near-equivalent lines where Yahoo's coverage is patchy:
    EBIT from OperatingIncome, cash including short-term investments, working
    capital derived from current assets less current liabilities.
    """
    core = CoreFinancials(ticker=ticker)
    core.as_of = latest_date(bundle, "TotalAssets") or latest_date(bundle, "TotalRevenue")

    core.revenue_ttm = ttm(bundle, "TotalRevenue")
    core.gross_profit_ttm = ttm(bundle, "GrossProfit")

    # OperatingIncome first, EBIT only as a fallback. Yahoo computes its "EBIT"
    # line as PretaxIncome + InterestExpense, which for a company with a large
    # cash pile silently folds interest *income* into operating profit: LSIP's
    # Yahoo EBIT is 2,232bn against a true operating profit of 1,851bn (+20.6%),
    # ASII's is 46,289bn against 34,641bn (+33.6%). That contaminates EV/EBIT,
    # the Acquirer's Multiple, EPV, ROC and earnings yield -- every Magic Formula
    # input -- and it flatters exactly the cash-rich, apparently-cheap names the
    # screen is built to surface.
    core.ebit_ttm = ttm(bundle, "OperatingIncome")
    if core.ebit_ttm is None:
        core.ebit_ttm = ttm(bundle, "EBIT")

    core.ebitda_ttm = ttm(bundle, "EBITDA")
    # Yahoo returns EBITDA identical to its EBIT for a minority of IDX filers,
    # meaning depreciation was never added back. A D&A-less "EBITDA" is not a
    # conservative estimate, it is a wrong one, so it is reported as missing
    # rather than as a number that would understate EV/EBITDA.
    if (
        core.ebitda_ttm is not None
        and ttm(bundle, "EBIT") is not None
        and abs(core.ebitda_ttm - ttm(bundle, "EBIT")) < 1.0
    ):
        core.ebitda_ttm = None
    # Attributable profit first: earnings that belong to minority shareholders
    # of subsidiaries are not the parent shareholder's to value. Falls back to
    # the consolidated line where Yahoo does not publish the split.
    core.net_income_ttm = ttm(bundle, "NetIncomeCommonStockholders")
    if core.net_income_ttm is None:
        core.net_income_ttm = ttm(bundle, "NetIncome")
    core.cfo_ttm = ttm(bundle, "OperatingCashFlow")
    core.capex_ttm = ttm(bundle, "CapitalExpenditure")
    core.fcf_ttm = ttm(bundle, "FreeCashFlow")
    if core.fcf_ttm is None and core.cfo_ttm is not None and core.capex_ttm is not None:
        # Yahoo reports capex as a negative number; adding it subtracts spend.
        core.fcf_ttm = core.cfo_ttm + core.capex_ttm
    core.interest_expense_ttm = ttm(bundle, "InterestExpense")
    core.tax_ttm = ttm(bundle, "TaxProvision")
    core.pretax_ttm = ttm(bundle, "PretaxIncome")

    core.revenue_q = nth_last(bundle, "TotalRevenue", 0)
    core.gross_profit_q = nth_last(bundle, "GrossProfit", 0)
    core.operating_income_q = nth_last(bundle, "OperatingIncome", 0) or nth_last(bundle, "EBIT", 0)
    core.net_income_q = nth_last(bundle, "NetIncomeCommonStockholders", 0)
    if core.net_income_q is None:
        core.net_income_q = nth_last(bundle, "NetIncome", 0)

    core.total_assets = latest(bundle, "TotalAssets")
    core.total_liabilities = latest(bundle, "TotalLiabilitiesNetMinorityInterest")
    core.total_equity = latest(bundle, "StockholdersEquity")
    core.cash = latest(bundle, "CashAndCashEquivalents")
    if core.cash is None:
        core.cash = latest(bundle, "CashCashEquivalentsAndShortTermInvestments")
    core.total_debt = latest(bundle, "TotalDebt")
    core.long_term_debt = latest(bundle, "LongTermDebt")
    core.current_assets = latest(bundle, "CurrentAssets")
    core.current_liabilities = latest(bundle, "CurrentLiabilities")
    core.working_capital = latest(bundle, "WorkingCapital")
    if core.working_capital is None and core.current_assets is not None and core.current_liabilities is not None:
        core.working_capital = core.current_assets - core.current_liabilities
    core.inventory = latest(bundle, "Inventory")
    core.receivables = latest(bundle, "AccountsReceivable")
    core.payables = latest(bundle, "AccountsPayable")
    core.retained_earnings = latest(bundle, "RetainedEarnings")
    core.invested_capital = latest(bundle, "InvestedCapital")
    core.shares_diluted = latest(bundle, "DilutedAverageShares")

    if core.total_equity is None and core.total_assets is not None and core.total_liabilities is not None:
        core.total_equity = core.total_assets - core.total_liabilities
    return core


# ------------------------------------------------------------------ Piotroski


def piotroski_f_score(bundle: Bundle) -> tuple[int | None, dict[str, int | None]]:
    """Piotroski F-Score (0-9) with the per-signal breakdown.

    Prefers a TTM-versus-prior-TTM basis so the score moves with each quarterly
    filing. That needs eight consecutive quarters, and Yahoo's free feed only
    carries five or six, so when the prior-year TTM window is unavailable the
    calculation falls back to annual-versus-prior-annual -- the basis Piotroski
    originally specified. `_fscore_basis` records which was used.

    Signals that cannot be evaluated score 0 but are reported as None in the
    breakdown, and the total is returned as None when more than three signals
    are unevaluable -- a "3/9" built from six blanks is noise, not a weak
    company.
    """
    # Eight quarters are needed for a TTM-vs-prior-TTM comparison.
    if len(_q(bundle, "TotalRevenue")) >= 8 and ttm(bundle, "NetIncome", 4) is not None:
        return _piotroski_ttm(bundle)
    return _piotroski_annual(bundle)


def _piotroski_ttm(bundle: Bundle) -> tuple[int | None, dict[str, int | None]]:
    signals: dict[str, int | None] = {"_basis": None}

    assets_now = latest(bundle, "TotalAssets")
    assets_prior = nth_last(bundle, "TotalAssets", 4)
    ni_now, ni_prior = ttm(bundle, "NetIncome"), ttm(bundle, "NetIncome", 4)
    cfo_now = ttm(bundle, "OperatingCashFlow")

    roa_now = safe_div(ni_now, assets_now)
    roa_prior = safe_div(ni_prior, assets_prior)

    # 1. Profitability
    signals["roa_positive"] = int(roa_now > 0) if roa_now is not None else None
    signals["cfo_positive"] = int(cfo_now > 0) if cfo_now is not None else None
    signals["roa_improving"] = (
        int(roa_now > roa_prior) if roa_now is not None and roa_prior is not None else None
    )
    signals["accruals"] = (
        int(cfo_now > ni_now) if cfo_now is not None and ni_now is not None else None
    )

    # 2. Leverage, liquidity and source of funds
    ltd_ratio_now = safe_div(latest(bundle, "LongTermDebt"), assets_now)
    ltd_ratio_prior = safe_div(nth_last(bundle, "LongTermDebt", 4), assets_prior)
    if ltd_ratio_now is not None and ltd_ratio_prior is not None:
        signals["leverage_falling"] = int(ltd_ratio_now <= ltd_ratio_prior)
    elif latest(bundle, "LongTermDebt") is None and assets_now is not None:
        # No long-term debt reported at all is the strongest possible reading of
        # this signal, not a missing one.
        signals["leverage_falling"] = 1
    else:
        signals["leverage_falling"] = None

    cr_now = safe_div(latest(bundle, "CurrentAssets"), latest(bundle, "CurrentLiabilities"))
    cr_prior = safe_div(nth_last(bundle, "CurrentAssets", 4), nth_last(bundle, "CurrentLiabilities", 4))
    signals["current_ratio_improving"] = (
        int(cr_now > cr_prior) if cr_now is not None and cr_prior is not None else None
    )

    shares_now = latest(bundle, "DilutedAverageShares")
    shares_prior = nth_last(bundle, "DilutedAverageShares", 4)
    if shares_now is not None and shares_prior is not None:
        # A 1% tolerance keeps routine option vesting from failing the signal.
        signals["no_dilution"] = int(shares_now <= shares_prior * 1.01)
    else:
        signals["no_dilution"] = None

    # 3. Operating efficiency
    gm_now = safe_div(ttm(bundle, "GrossProfit"), ttm(bundle, "TotalRevenue"))
    gm_prior = safe_div(ttm(bundle, "GrossProfit", 4), ttm(bundle, "TotalRevenue", 4))
    signals["gross_margin_improving"] = (
        int(gm_now > gm_prior) if gm_now is not None and gm_prior is not None else None
    )

    turnover_now = safe_div(ttm(bundle, "TotalRevenue"), assets_now)
    turnover_prior = safe_div(ttm(bundle, "TotalRevenue", 4), assets_prior)
    signals["asset_turnover_improving"] = (
        int(turnover_now > turnover_prior)
        if turnover_now is not None and turnover_prior is not None
        else None
    )

    signals["_basis"] = "ttm"
    return _total(signals)


def _total(signals: dict[str, int | None]) -> tuple[int | None, dict[str, int | None]]:
    scored = {key: value for key, value in signals.items() if not key.startswith("_")}
    unevaluable = sum(1 for value in scored.values() if value is None)
    if unevaluable > 3:
        return None, signals
    return sum(value for value in scored.values() if value), signals


def _piotroski_annual(bundle: Bundle) -> tuple[int | None, dict[str, int | None]]:
    """Annual-basis F-Score, used when quarterly history is too short.

    Piotroski's original construction: compare the latest fiscal year against
    the one before it.
    """
    signals: dict[str, int | None] = {"_basis": None}

    def annual(field: str, back: int = 0) -> float | None:
        series = _q(bundle, field, "annual")
        return series[-1 - back]["value"] if len(series) > back else None

    def annual_cfo(back: int = 0) -> float | None:
        """Operating cash flow, falling back to the FCF identity.

        Yahoo returns no `annualOperatingCashFlow` for the IDX universe at all,
        while `annualFreeCashFlow` and `annualCapitalExpenditure` are both
        populated. Without this fallback the `cfo_positive` and `accruals`
        signals are permanently unevaluable, which caps every annual-basis score
        at 7/9 and consumes two of the three blanks the total tolerates -- ITMG,
        ADRO and PTBA were all demoted to WATCH by a missing data line rather
        than by anything about the businesses.

        Capex arrives negative, so CFO = FCF - capex.
        """
        direct = annual("OperatingCashFlow", back)
        if direct is not None:
            return direct
        fcf, capex = annual("FreeCashFlow", back), annual("CapitalExpenditure", back)
        if fcf is None or capex is None:
            return None
        return fcf - capex

    assets_now, assets_prior = annual("TotalAssets"), annual("TotalAssets", 1)
    ni_now, ni_prior = annual("NetIncome"), annual("NetIncome", 1)
    cfo_now = annual_cfo()

    roa_now = safe_div(ni_now, assets_now)
    roa_prior = safe_div(ni_prior, assets_prior)

    signals["roa_positive"] = int(roa_now > 0) if roa_now is not None else None
    signals["cfo_positive"] = int(cfo_now > 0) if cfo_now is not None else None
    signals["roa_improving"] = (
        int(roa_now > roa_prior) if roa_now is not None and roa_prior is not None else None
    )
    signals["accruals"] = int(cfo_now > ni_now) if cfo_now is not None and ni_now is not None else None

    ltd_now = safe_div(annual("LongTermDebt"), assets_now)
    ltd_prior = safe_div(annual("LongTermDebt", 1), assets_prior)
    if ltd_now is not None and ltd_prior is not None:
        signals["leverage_falling"] = int(ltd_now <= ltd_prior)
    elif annual("LongTermDebt") is None and assets_now is not None:
        signals["leverage_falling"] = 1
    else:
        signals["leverage_falling"] = None

    cr_now = safe_div(annual("CurrentAssets"), annual("CurrentLiabilities"))
    cr_prior = safe_div(annual("CurrentAssets", 1), annual("CurrentLiabilities", 1))
    signals["current_ratio_improving"] = (
        int(cr_now > cr_prior) if cr_now is not None and cr_prior is not None else None
    )

    shares_now, shares_prior = annual("DilutedAverageShares"), annual("DilutedAverageShares", 1)
    signals["no_dilution"] = (
        int(shares_now <= shares_prior * 1.01)
        if shares_now is not None and shares_prior is not None
        else None
    )

    gm_now = safe_div(annual("GrossProfit"), annual("TotalRevenue"))
    gm_prior = safe_div(annual("GrossProfit", 1), annual("TotalRevenue", 1))
    signals["gross_margin_improving"] = (
        int(gm_now > gm_prior) if gm_now is not None and gm_prior is not None else None
    )

    turnover_now = safe_div(annual("TotalRevenue"), assets_now)
    turnover_prior = safe_div(annual("TotalRevenue", 1), assets_prior)
    signals["asset_turnover_improving"] = (
        int(turnover_now > turnover_prior)
        if turnover_now is not None and turnover_prior is not None
        else None
    )

    signals["_basis"] = "annual"
    return _total(signals)


def justified_pb_value(
    book_value_per_share: float | None,
    roe: float | None,
    cost_of_equity: float,
    growth: float,
) -> float | None:
    """Justified P/B valuation for banks and insurers.

    Value = BVPS x (ROE - g) / (COE - g). This is the residual-income identity
    and the standard way to value a lender: EV/EBIT and FCF are meaningless when
    debt is raw material and 'capex' is loan origination.

    Growth is capped below the cost of equity, and sustained ROE above 40% is
    treated as unsustainable and clipped -- otherwise one outlier year
    capitalises into an absurd target.
    """
    if not book_value_per_share or book_value_per_share <= 0 or roe is None:
        return None
    if cost_of_equity <= 0:
        return None
    roe_capped = min(roe, 0.40)

    # The Gordon form explodes as the spread (COE - g) narrows: at a 3% spread a
    # 100bp error in either input moves fair value by a third. Requiring a 400bp
    # minimum spread and capping the multiple at 4x book keeps the output inside
    # the range where the model carries information.
    minimum_spread = 0.04
    # Reject before clamping, not after. Capping growth at `COE - minimum_spread`
    # and *then* testing the spread makes the test unreachable: the clamp
    # guarantees it passes, so an input with growth at or above the cost of
    # equity was silently revalued at the most generous spread the model allows
    # instead of being refused.
    if cost_of_equity - growth < minimum_spread:
        return None
    growth_capped = min(growth, roe_capped * 0.6)
    spread = cost_of_equity - growth_capped
    multiple = (roe_capped - growth_capped) / spread
    if multiple <= 0:
        return None
    return book_value_per_share * min(multiple, 4.0)


def comparables_value(
    eps_ttm: float | None,
    peer_pe: float | None,
    ebit_ttm: float | None,
    peer_ev_ebit: float | None,
    net_debt: float,
    shares: float | None,
    book_value_per_share: float | None = None,
    peer_pb: float | None = None,
) -> float | None:
    """Relative valuation across the P/E, EV/EBIT and P/B lenses.

    Each lens is skipped rather than zeroed when its input is negative or
    missing, so a loss-making company does not receive a negative "implied
    price" that then drags a blended valuation downward.

    The surviving lenses are combined by *median after outlier rejection*, not
    by minimum. Taking the minimum looks conservative but is unstable: for a
    levered cyclical, `EBIT x peer multiple - net debt` can land just above zero,
    producing an implied price near nil that then swamps two perfectly sensible
    lenses. ADRO and ITMG both did exactly that in testing -- a IDR 2,540 stock
    valued at IDR 0.33, which reads as a -769,000% margin of safety. Candidates
    more than an order of magnitude away from the median of the set are dropped
    as degenerate before the median is taken.
    """
    candidates: list[float] = []

    if eps_ttm is not None and eps_ttm > 0 and peer_pe and peer_pe > 0:
        candidates.append(eps_ttm * peer_pe)

    if ebit_ttm is not None and ebit_ttm > 0 and peer_ev_ebit and peer_ev_ebit > 0 and shares:
        equity_value = ebit_ttm * peer_ev_ebit - net_debt
        if equity_value > 0:
            candidates.append(equity_value / shares)

    if book_value_per_share and book_value_per_share > 0 and peer_pb and peer_pb > 0:
        candidates.append(book_value_per_share * peer_pb)

    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    centre = median(candidates)
    if centre and centre > 0:
        kept = [value for value in candidates if 0.1 * centre <= value <= 10 * centre]
        if kept:
            candidates = kept
    return median(candidates)


def altman_z_modified(core: CoreFinancials) -> float | None:
    """Altman Z''-score, the emerging-market / non-manufacturer variant.

    Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4. Distress below 1.1, safe above
    2.6. The sales/assets term of the original Z is dropped because it makes the
    score industry-dependent, which is exactly wrong for a cross-sector screen.
    """
    assets = core.total_assets
    if not assets:
        return None
    x1 = safe_div(core.working_capital, assets)
    x2 = safe_div(core.retained_earnings, assets)
    x3 = safe_div(core.ebit_ttm, assets)
    if x1 is None or x3 is None:
        return None

    # X4 is equity/liabilities. A company with no liabilities at all divides by
    # zero, and treating that as 0.0 scores a debt-free balance sheet *worse*
    # than one carrying a token payable -- the opposite of what the ratio
    # measures. Zero liabilities is the strongest possible reading, so it takes
    # the cap rather than the floor. The cap also stops a near-debt-free filer
    # from contributing an unbounded term that swamps the other three.
    if core.total_liabilities is not None and core.total_liabilities <= 0:
        x4 = 10.0
    else:
        x4 = min(safe_div(core.total_equity, core.total_liabilities) or 0.0, 10.0)

    return 6.56 * x1 + 3.26 * (x2 or 0.0) + 6.72 * x3 + 1.05 * x4


# ------------------------------------------------------- returns and valuation


def return_on_invested_capital(core: CoreFinancials, tax_rate: float = 0.22) -> float | None:
    """NOPAT / invested capital, with a debt+equity-less-cash fallback.

    The effective tax rate is used when it is credible (0-60%); otherwise the
    Indonesian statutory 22% applies. A loss-making year produces a meaningless
    effective rate, which is why the guard is needed.
    """
    if core.ebit_ttm is None:
        return None
    effective = safe_div(core.tax_ttm, core.pretax_ttm)
    rate = effective if effective is not None and 0.0 <= effective <= 0.6 else tax_rate
    nopat = core.ebit_ttm * (1 - rate)

    capital = core.invested_capital
    if not capital:
        equity = core.total_equity or 0.0
        debt = core.total_debt or 0.0
        cash = core.cash or 0.0
        capital = equity + debt - cash
    if not capital or capital <= 0:
        return None
    return nopat / capital


def return_on_capital_greenblatt(core: CoreFinancials) -> float | None:
    """Greenblatt's ROC: EBIT / (net working capital + net fixed assets).

    This is the Magic Formula definition and is deliberately *not* ROIC. The
    original workbook substituted ROIC (and fell back to ROCE), which changes
    the ranking: Greenblatt excludes goodwill and excess cash on purpose.
    """
    if core.ebit_ttm is None:
        return None
    net_working_capital = None
    if core.current_assets is not None and core.current_liabilities is not None:
        # Excess cash is excluded; operating cash needs are already in receivables
        # and inventory.
        net_working_capital = max(0.0, (core.current_assets - (core.cash or 0.0)) - core.current_liabilities)
    net_fixed = core.total_assets
    if net_fixed is None:
        return None
    if net_working_capital is None:
        net_working_capital = core.working_capital or 0.0
    denominator = net_working_capital + (net_fixed - (core.current_assets or 0.0))
    if denominator <= 0:
        return None
    return core.ebit_ttm / denominator


def earnings_yield_greenblatt(ebit_ttm: float | None, enterprise_value: float | None) -> float | None:
    """EBIT / EV -- the Magic Formula's earnings yield.

    The original workbook used Yahoo-style net-income-based earnings yield
    (E/P), which double-counts capital structure: a heavily indebted name looks
    cheap on E/P and expensive on EBIT/EV, and the whole point of the Magic
    Formula is the latter.
    """
    if enterprise_value is None or enterprise_value <= 0:
        return None
    return safe_div(ebit_ttm, enterprise_value)


def ncav_per_share(core: CoreFinancials, shares: float | None) -> float | None:
    """Graham net current asset value per share: (CA - total liabilities) / shares.

    Total liabilities -- not just current liabilities -- is the Graham
    definition; using current liabilities alone overstates NCAV for any company
    carrying long-term debt.
    """
    if core.current_assets is None or core.total_liabilities is None or not shares:
        return None
    return (core.current_assets - core.total_liabilities) / shares


def epv_per_share(
    core: CoreFinancials,
    shares: float | None,
    cost_of_capital: float,
    tax_rate: float = 0.22,
    normalisation_years: int = 5,
) -> float | None:
    """Greenwald earnings power value, normalised over the available history.

    EPV = (normalised EBIT x (1 - tax)) / WACC - net debt, per share. Normalising
    EBIT across a full cycle is the entire purpose of EPV; valuing a single TTM
    EBIT (as the original workbook did) just re-prices the current cycle
    position and calls it intrinsic value.
    """
    if not shares or cost_of_capital <= 0:
        return None
    normalised_ebit = core.__dict__.get("_normalised_ebit", core.ebit_ttm)
    if normalised_ebit is None or normalised_ebit <= 0:
        return None
    enterprise_value = normalised_ebit * (1 - tax_rate) / cost_of_capital
    net_debt = (core.total_debt or 0.0) - (core.cash or 0.0)
    equity_value = enterprise_value - net_debt
    if equity_value <= 0:
        return None
    return equity_value / shares


def normalised_ebit(bundle: Bundle, years: int = 5) -> float | None:
    """Mid-cycle EBIT: the *median* annual EBIT over the last `years` years.

    The median, not the mean. A four-year window that happens to contain one
    commodity supercycle year is dominated by it under a mean: ITMG's 2022 EBIT
    was 5x its 2025 figure, and averaging produced a "mid-cycle" earnings power
    the company has hit exactly once. The median discounts a single extreme year
    without discarding it.

    Falls back to rolling TTM windows when the annual series is too thin.
    """
    # Same preference as `build_core`: the reported operating line, not Yahoo's
    # interest-contaminated EBIT. Normalising a contaminated series just
    # produces a contaminated mid-cycle figure -- LSIP's normalised EBIT was
    # 26.8% too high for exactly this reason.
    annual = _q(bundle, "OperatingIncome", "annual") or _q(bundle, "EBIT", "annual")
    values = [item["value"] for item in annual[-years:]]
    if len(values) >= 2:
        return median(values)
    windows = []
    for offset in range(0, years * 4, 4):
        value = ttm(bundle, "OperatingIncome", offset) or ttm(bundle, "EBIT", offset)
        if value is None:
            break
        windows.append(value)
    return median(windows) if windows else None


def normalised_capex(bundle: Bundle, years: int = 5) -> float | None:
    """Median annual capital expenditure, returned negative as Yahoo reports it.

    Exists so the DCF deducts reinvestment on the same time basis as the
    earnings it is deducting from. Netting a five-year median EBIT against a
    single trailing-twelve-month capex figure mixes a cycle-normalised numerator
    with a point-in-time denominator, and one lumpy growth-capex quarter then
    destroys the valuation: MOLI's Q1 2026 carried a IDR 43.8bn expansion outlay
    that pushed TTM capex to 2x its annual median and collapsed the cash-flow
    base from a NOPAT of IDR 71.4bn to IDR 1.7bn, making ~90% of the resulting
    intrinsic value nothing but the per-share cash pile passing through.
    """
    annual = _q(bundle, "CapitalExpenditure", "annual")
    values = [item["value"] for item in annual[-years:]]
    if values:
        return median(values)
    return ttm(bundle, "CapitalExpenditure")


def dcf_per_share(
    fcf_base: float | None,
    shares: float | None,
    net_debt: float,
    wacc: float,
    growth_stage1: float,
    terminal_growth: float,
    years: int = 5,
) -> float | None:
    """Two-stage FCFF DCF returning intrinsic value per share.

    Guards the terminal value against `wacc <= terminal_growth`, which the
    original workbook did not: a Gordon denominator of zero or a negative one
    produces an infinite or sign-flipped valuation that then propagates into the
    margin-of-safety column as a spuriously attractive number.
    """
    if not fcf_base or not shares or shares <= 0:
        return None
    if wacc <= 0 or wacc <= terminal_growth:
        return None
    if fcf_base <= 0:
        return None

    present_value = 0.0
    cash_flow = fcf_base
    for year in range(1, years + 1):
        cash_flow *= 1 + growth_stage1
        present_value += cash_flow / (1 + wacc) ** year

    terminal_value = cash_flow * (1 + terminal_growth) / (wacc - terminal_growth)
    present_value += terminal_value / (1 + wacc) ** years

    equity_value = present_value - net_debt
    if equity_value <= 0:
        return None
    return equity_value / shares


def ddm_per_share(
    dividend_ttm: float | None,
    cost_of_equity: float,
    growth_rate: float,
) -> float | None:
    """Gordon growth DDM. None for non-payers and when g >= cost of equity."""
    if not dividend_ttm or dividend_ttm <= 0:
        return None
    if cost_of_equity <= growth_rate:
        return None
    return dividend_ttm * (1 + growth_rate) / (cost_of_equity - growth_rate)


def cost_of_equity_capm(
    risk_free: float,
    equity_risk_premium: float,
    beta: float | None,
    net_debt_to_equity: float | None,
    floor: float | None = None,
    ceiling: float = 0.22,
) -> float:
    """CAPM cost of equity with a leverage add-on, clamped to a credible band.

    Beta is only trusted inside [0.5, 2.5]. Yahoo's beta for thinly traded IDX
    names is frequently computed against a mismatched index or window and comes
    back implausibly low -- it reports 0.168 for BBRI, one of the largest banks
    in the country. Accepting that pushed the cost of equity to the floor and,
    because justified P/B divides by (COE - g), inflated the bank's fair value
    to four times book. Anything outside the band falls back to 1.0.

    The floor defaults to risk-free + 300bps: no equity is cheaper to finance
    than government debt plus a real premium, whatever a regression says.
    """
    effective_floor = floor if floor is not None else risk_free + 0.03
    beta_value = beta if beta and 0.5 <= beta <= 2.5 else 1.0
    leverage = min(max(net_debt_to_equity or 0.0, 0.0), 1.0)
    value = risk_free + beta_value * equity_risk_premium + 0.03 * leverage
    return min(max(value, effective_floor), ceiling)


def days_between(later: str | None, earlier: str | None) -> int | None:
    if not later or not earlier:
        return None
    try:
        return (datetime.fromisoformat(later).date() - datetime.fromisoformat(earlier).date()).days
    except ValueError:
        return None


def quarters_stale(as_of: str | None, today: date | None = None) -> float | None:
    """How many quarters old the newest filing is -- the staleness guard.

    IDX filers routinely miss deadlines, and a screen that ranks a company on
    figures three quarters old is ranking history. Surfaced as its own column so
    stale names can be excluded rather than silently trusted.
    """
    if not as_of:
        return None
    try:
        reported = datetime.fromisoformat(as_of).date()
    except ValueError:
        return None
    reference = today or date.today()
    return round((reference - reported).days / 91.31, 2)
