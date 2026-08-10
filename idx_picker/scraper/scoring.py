"""Business classification, scenario valuation and the BUY / WATCH / SKIP verdict.

Implements the layered decision framework: business type first, then quality,
then balance-sheet safety, then valuation, then the four value lenses as
cross-checks, and only then a verdict. Cheapness alone never produces a BUY --
that rule is enforced structurally in `classify`, not left to the weights.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from . import metrics as M

# Sectors where enterprise-value and free-cash-flow frameworks are meaningless.
# Debt is raw material for a bank, not leverage, and EV/EBIT on a lender is
# noise. These names are routed to a book-value and returns-based track instead.
FINANCIAL_SECTORS = {
    "financials",
    "financial services",
    "banks",
    "insurance",
    "financial",
}

# Sectors whose earnings are cycle-driven, so TTM earnings are the wrong base
# for valuation and normalised (mid-cycle) earnings are used instead.
CYCLICAL_SECTORS = {
    "basic materials",
    "energy",
    "industrials",
    "properties & real estate",
    "infrastructures",
    "transportation & logistic",
}

BUSINESS_COMPOUNDER = "Compounder"
BUSINESS_CYCLICAL = "Cyclical"
BUSINESS_FINANCIAL = "Financial"
BUSINESS_DEEP_VALUE = "Deep Value"
BUSINESS_ORDINARY = "Ordinary"

VERDICT_BUY = "BUY"
VERDICT_WATCH = "WATCH"
VERDICT_SKIP = "SKIP"
VERDICT_DEEP_VALUE = "DEEP VALUE"


@dataclass
class Scenario:
    """One valuation case. `growth` and `margin` are the levers that vary."""

    name: str
    growth: float
    wacc: float
    terminal_growth: float
    intrinsic_value: float | None = None
    mos: float | None = None
    upside: float | None = None


@dataclass
class Assessment:
    ticker: str
    business_type: str = BUSINESS_ORDINARY
    quality_score: float | None = None
    safety_score: float | None = None
    value_score: float | None = None
    composite: float | None = None
    verdict: str = VERDICT_SKIP
    reasons: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    scenarios: dict[str, Scenario] = field(default_factory=dict)
    intrinsic_base: float | None = None
    mos_base: float | None = None
    upside_base: float | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reasons"] = "; ".join(self.reasons)
        data["flags"] = "; ".join(self.flags)
        data.pop("scenarios", None)
        for name, scenario in self.scenarios.items():
            data[f"iv_{name}"] = scenario.intrinsic_value
            data[f"mos_{name}"] = scenario.mos
            data[f"upside_{name}"] = scenario.upside
        return data


# ------------------------------------------------------------ classification


def classify_business(
    sector: str | None,
    core: M.CoreFinancials,
    price: float | None,
    shares: float | None,
    roic: float | None,
    revenue_cagr: float | None,
) -> str:
    """Route each name to the framework that actually fits it.

    Order matters. The net-net test runs before the quality tests because a
    company trading below liquidation value is a special situation regardless of
    how poor its ROIC looks -- that is the whole premise of the Graham lens.
    """
    sector_key = (sector or "").strip().lower()
    if sector_key in FINANCIAL_SECTORS:
        return BUSINESS_FINANCIAL

    ncav_ps = M.ncav_per_share(core, shares)
    if ncav_ps and price and price < ncav_ps:
        return BUSINESS_DEEP_VALUE

    if sector_key in CYCLICAL_SECTORS:
        return BUSINESS_CYCLICAL

    # A compounder earns above its cost of capital and keeps growing. Both
    # conditions, not either.
    if roic is not None and roic > 0.12 and revenue_cagr is not None and revenue_cagr > 0.05:
        return BUSINESS_COMPOUNDER
    return BUSINESS_ORDINARY


def net_net_test(core: M.CoreFinancials, price: float | None, shares: float | None) -> tuple[bool, float | None]:
    """Graham's classic test: price below two-thirds of NCAV per share."""
    ncav_ps = M.ncav_per_share(core, shares)
    if ncav_ps is None or price is None or ncav_ps <= 0:
        return False, ncav_ps
    return price < (2.0 / 3.0) * ncav_ps, ncav_ps


# ------------------------------------------------------------------- scoring


def score_quality(core: M.CoreFinancials, roic: float | None, roe: float | None,
                  business_type: str, revenue_cagr: float | None,
                  gross_margin: float | None) -> float | None:
    """0-100 business-economics score. Financials are graded on ROE, not ROIC."""
    points: list[float] = []

    if business_type == BUSINESS_FINANCIAL:
        if roe is not None:
            points.append(_band(roe, [(0.20, 100), (0.15, 85), (0.12, 70), (0.08, 50), (0.04, 30)], 10))
    elif roic is not None:
        points.append(_band(roic, [(0.20, 100), (0.15, 85), (0.12, 70), (0.08, 50), (0.04, 30)], 10))

    if gross_margin is not None and business_type != BUSINESS_FINANCIAL:
        points.append(_band(gross_margin, [(0.40, 100), (0.30, 80), (0.20, 60), (0.10, 40)], 20))

    if revenue_cagr is not None:
        points.append(_band(revenue_cagr, [(0.15, 100), (0.10, 85), (0.05, 70), (0.00, 45)], 20))

    # Earnings quality: cash conversion. Profits that never become cash are the
    # single most reliable early warning in this dataset.
    conversion = M.safe_div(core.cfo_ttm, core.net_income_ttm)
    if conversion is not None and core.net_income_ttm and core.net_income_ttm > 0:
        points.append(_band(conversion, [(1.2, 100), (1.0, 85), (0.8, 65), (0.5, 40)], 15))

    return round(sum(points) / len(points), 1) if points else None


def score_safety(core: M.CoreFinancials, f_score: int | None, altman: float | None,
                 business_type: str) -> float | None:
    """0-100 balance-sheet safety. Higher is safer."""
    points: list[float] = []

    if business_type != BUSINESS_FINANCIAL:
        net_debt_ebitda = M.safe_div(
            (core.total_debt or 0.0) - (core.cash or 0.0), core.ebitda_ttm
        )
        if net_debt_ebitda is not None and core.ebitda_ttm and core.ebitda_ttm > 0:
            # Lower is better, so the bands run downward.
            points.append(_band(-net_debt_ebitda, [(0.0, 100), (-1.0, 85), (-2.0, 70), (-3.0, 45)], 15))

        current_ratio = M.safe_div(core.current_assets, core.current_liabilities)
        if current_ratio is not None:
            points.append(_band(current_ratio, [(2.0, 100), (1.5, 85), (1.2, 70), (1.0, 50)], 25))

        if altman is not None:
            points.append(_band(altman, [(2.6, 100), (1.8, 75), (1.1, 50)], 20))
    else:
        equity_assets = M.safe_div(core.total_equity, core.total_assets)
        if equity_assets is not None:
            points.append(_band(equity_assets, [(0.15, 100), (0.12, 85), (0.10, 70), (0.06, 45)], 20))

    interest_cover = M.safe_div(core.ebit_ttm, abs(core.interest_expense_ttm or 0.0) or None)
    if interest_cover is not None:
        points.append(_band(interest_cover, [(8.0, 100), (4.0, 85), (2.5, 65), (1.5, 40)], 15))

    if f_score is not None:
        points.append(min(100.0, f_score / 9.0 * 100.0))

    return round(sum(points) / len(points), 1) if points else None


def score_value(earnings_yield: float | None, acquirers_multiple: float | None,
                pe: float | None, pb: float | None, fcf_yield: float | None,
                business_type: str) -> float | None:
    """0-100 cheapness score, weighted by which lens fits the business type."""
    points: list[float] = []

    if business_type == BUSINESS_FINANCIAL:
        if pb is not None and pb > 0:
            points.append(_band(-pb, [(-0.7, 100), (-1.0, 85), (-1.5, 65), (-2.0, 45)], 20))
        if pe is not None and pe > 0:
            points.append(_band(-pe, [(-6.0, 100), (-9.0, 85), (-12.0, 65), (-18.0, 40)], 15))
    else:
        if earnings_yield is not None:
            points.append(_band(earnings_yield, [(0.20, 100), (0.15, 88), (0.10, 72), (0.06, 50)], 20))
        if acquirers_multiple is not None and acquirers_multiple > 0:
            points.append(_band(-acquirers_multiple, [(-4.0, 100), (-6.0, 85), (-9.0, 65), (-13.0, 40)], 15))
        if fcf_yield is not None:
            points.append(_band(fcf_yield, [(0.12, 100), (0.08, 85), (0.05, 68), (0.02, 45)], 20))
        if pe is not None and pe > 0:
            points.append(_band(-pe, [(-8.0, 100), (-12.0, 82), (-16.0, 62), (-22.0, 40)], 20))

    return round(sum(points) / len(points), 1) if points else None


def _band(value: float, thresholds: list[tuple[float, float]], floor: float) -> float:
    """Step function: first threshold the value clears wins, else `floor`."""
    for cutoff, score in thresholds:
        if value >= cutoff:
            return float(score)
    return float(floor)


# ---------------------------------------------------------------- scenarios


def build_scenarios(
    core: M.CoreFinancials,
    normalised_ebit_value: float | None,
    shares: float | None,
    price: float | None,
    base_wacc: float,
    base_terminal_growth: float,
    historical_growth: float | None,
    tax_rate: float = 0.22,
) -> dict[str, Scenario]:
    """Bear / Base / Bull FCFF valuations off one consistent cash-flow base.

    The bear case is not merely lower growth -- it also carries a higher
    discount rate, because the scenarios that depress growth are the same ones
    that raise the risk premium. Varying growth alone understates the spread.
    """
    growth_base = historical_growth if historical_growth is not None else 0.03
    growth_base = max(-0.05, min(0.15, growth_base))

    specs = [
        ("bear", max(-0.05, growth_base - 0.05), base_wacc + 0.02, max(0.0, base_terminal_growth - 0.01)),
        ("base", growth_base, base_wacc, base_terminal_growth),
        ("bull", min(0.20, growth_base + 0.04), max(0.06, base_wacc - 0.01), base_terminal_growth + 0.005),
    ]

    # Prefer normalised EBIT converted to an unlevered cash-flow proxy over raw
    # TTM FCF, which for a cyclical is a snapshot of the wrong point in the cycle.
    if normalised_ebit_value is not None and normalised_ebit_value > 0:
        fcf_base = normalised_ebit_value * (1 - tax_rate)
        if core.capex_ttm is not None and core.ebitda_ttm and core.ebit_ttm:
            depreciation = core.ebitda_ttm - core.ebit_ttm
            fcf_base += depreciation + core.capex_ttm  # capex arrives negative
    else:
        fcf_base = core.fcf_ttm

    net_debt = (core.total_debt or 0.0) - (core.cash or 0.0)

    out: dict[str, Scenario] = {}
    for name, growth, wacc, terminal in specs:
        scenario = Scenario(name=name, growth=growth, wacc=wacc, terminal_growth=terminal)
        scenario.intrinsic_value = M.dcf_per_share(
            fcf_base=fcf_base,
            shares=shares,
            net_debt=net_debt,
            wacc=wacc,
            growth_stage1=growth,
            terminal_growth=terminal,
        )
        if scenario.intrinsic_value and price:
            # MOS is measured against intrinsic value; upside against price.
            # They are different denominators and are reported separately.
            scenario.mos = (scenario.intrinsic_value - price) / scenario.intrinsic_value
            scenario.upside = scenario.intrinsic_value / price - 1
        out[name] = scenario
    return out


def blended_intrinsic(
    scenarios: dict[str, Scenario],
    epv_value: float | None,
    comparables_value: float | None,
    ncav_ps: float | None,
    business_type: str,
) -> float | None:
    """Blend the valuation lenses appropriate to the business type.

    Deep-value names are anchored on asset value, financials on comparables and
    book, everything else on a DCF/EPV/comps blend. A single lens applied to
    every business is how a screen ends up recommending a bank on EV/EBIT.
    """
    base = scenarios.get("base")
    dcf_value = base.intrinsic_value if base else None

    if business_type == BUSINESS_DEEP_VALUE:
        candidates = [value for value in (ncav_ps, epv_value, comparables_value) if value and value > 0]
        # The conservative anchor: liquidation value, not the optimistic case.
        # Safe to take the minimum here because NCAV is an asset-based floor
        # rather than a multiple-derived estimate, so it cannot collapse toward
        # zero the way a levered EV/EBIT lens can.
        return min(candidates) if candidates else None

    if business_type == BUSINESS_FINANCIAL:
        candidates = [value for value in (comparables_value, epv_value) if value and value > 0]
        return sum(candidates) / len(candidates) if candidates else None

    weights = {"dcf": 0.4, "epv": 0.35, "comps": 0.25}
    if business_type == BUSINESS_CYCLICAL:
        # Mid-cycle earnings power outweighs a projection off a cyclical peak.
        weights = {"dcf": 0.2, "epv": 0.5, "comps": 0.3}

    pairs = [
        (dcf_value, weights["dcf"]),
        (epv_value, weights["epv"]),
        (comparables_value, weights["comps"]),
    ]
    usable = [(value, weight) for value, weight in pairs if value and value > 0]
    if not usable:
        return None
    total_weight = sum(weight for _, weight in usable)
    return sum(value * weight for value, weight in usable) / total_weight


# ------------------------------------------------------------------ verdict


def classify(
    assessment: Assessment,
    price: float | None,
    mos_buy: float,
    mos_watch: float,
    f_score: int | None,
    is_net_net: bool,
    quarters_stale: float | None,
    red_flags: list[str],
) -> str:
    """Layered verdict. Value alone is never sufficient.

    A BUY requires all four of: adequate margin of safety, a balance sheet that
    is not distressed, evidence of financial improvement, and no unresolved red
    flag. Failing any one drops the name to WATCH; failing valuation outright
    drops it to SKIP.
    """
    reasons = assessment.reasons
    mos = assessment.mos_base

    if quarters_stale is not None and quarters_stale > 3.0:
        reasons.append(f"Filings {quarters_stale:.1f} quarters stale - not screenable")
        return VERDICT_SKIP

    # Deep value is judged on asset protection, not earnings quality.
    if is_net_net:
        if assessment.safety_score is not None and assessment.safety_score < 30:
            reasons.append("Net-net but balance sheet distressed - going-concern risk")
            return VERDICT_WATCH
        reasons.append("Trades below 2/3 NCAV - Graham net-net")
        return VERDICT_DEEP_VALUE

    if mos is None:
        reasons.append("No usable intrinsic value - cannot assess margin of safety")
        return VERDICT_SKIP

    if mos < mos_watch:
        reasons.append(f"MOS {mos:.0%} below watch threshold {mos_watch:.0%}")
        return VERDICT_SKIP

    if mos < mos_buy:
        reasons.append(f"MOS {mos:.0%} attractive but short of buy threshold {mos_buy:.0%}")
        return VERDICT_WATCH

    # From here the price is right. Everything that follows tests whether the
    # business deserves it -- this is the value-trap filter.
    if assessment.safety_score is not None and assessment.safety_score < 40:
        reasons.append("Cheap but balance sheet weak - possible value trap")
        return VERDICT_WATCH

    if f_score is not None and f_score <= 3:
        reasons.append(f"Cheap but F-Score {f_score}/9 shows deteriorating fundamentals")
        return VERDICT_WATCH

    if assessment.quality_score is not None and assessment.quality_score < 35:
        reasons.append("Cheap but business economics poor - value trap risk")
        return VERDICT_WATCH

    if red_flags:
        reasons.append(f"Cheap and sound, but flagged: {red_flags[0]}")
        return VERDICT_WATCH

    reasons.append(f"MOS {mos:.0%}, quality and balance sheet both pass")
    return VERDICT_BUY


def detect_red_flags(core: M.CoreFinancials, bundle: dict[str, list[dict[str, Any]]],
                     business_type: str) -> list[str]:
    """Screen-level red flags. Each is a reason to look harder, not a rejection."""
    flags: list[str] = []

    if core.net_income_ttm and core.cfo_ttm is not None:
        if core.net_income_ttm > 0 and core.cfo_ttm < core.net_income_ttm * 0.5:
            flags.append("Earnings materially exceed cash generation")

    fcf_negative_quarters = sum(
        1 for item in (bundle.get("quarterlyFreeCashFlow") or [])[-8:] if item["value"] < 0
    )
    if fcf_negative_quarters >= 6:
        flags.append("Free cash flow negative in 6 of last 8 quarters")

    shares_now = M.latest(bundle, "DilutedAverageShares")
    shares_prior = M.nth_last(bundle, "DilutedAverageShares", 8)
    if shares_now and shares_prior and shares_now > shares_prior * 1.15:
        flags.append(f"Share count up {shares_now / shares_prior - 1:.0%} over two years")

    if business_type != BUSINESS_FINANCIAL:
        net_debt_ebitda = M.safe_div((core.total_debt or 0.0) - (core.cash or 0.0), core.ebitda_ttm)
        if net_debt_ebitda is not None and core.ebitda_ttm and core.ebitda_ttm > 0 and net_debt_ebitda > 4:
            flags.append(f"Net debt/EBITDA {net_debt_ebitda:.1f}x")

    gross_now = M.safe_div(M.ttm(bundle, "GrossProfit"), M.ttm(bundle, "TotalRevenue"))
    gross_prior = M.safe_div(M.ttm(bundle, "GrossProfit", 8), M.ttm(bundle, "TotalRevenue", 8))
    if gross_now is not None and gross_prior is not None and gross_now < gross_prior - 0.05:
        flags.append(f"Gross margin down {(gross_prior - gross_now) * 100:.0f}pp over two years")

    interest_cover = M.safe_div(core.ebit_ttm, abs(core.interest_expense_ttm or 0.0) or None)
    if interest_cover is not None and interest_cover < 1.5:
        flags.append(f"Interest coverage {interest_cover:.1f}x")

    # The peak-earnings trap, made explicit. When mid-cycle EBIT sits far above
    # the trailing figure, every normalised valuation on this row is a bet that
    # the cycle turns back up -- the user should see that assumption, not
    # inherit it silently.
    normalised = core.__dict__.get("_normalised_ebit")
    if normalised and core.ebit_ttm and core.ebit_ttm > 0:
        ratio = normalised / core.ebit_ttm
        if ratio > 2.0:
            flags.append(f"Normalised EBIT {ratio:.1f}x trailing - valuation assumes cycle recovery")
        elif ratio < 0.5:
            flags.append(f"Trailing EBIT {1 / ratio:.1f}x mid-cycle - possible peak earnings")

    return flags
