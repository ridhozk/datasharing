"""Unit tests for `idx_picker.scraper.scoring`.

The verdict layer is where a screener does damage. A metric that is 5% wrong
moves a rank; a verdict that is wrong moves money. These tests concentrate on
the *structural* guarantees of `classify` -- that cheapness alone can never
produce a BUY -- and on the routing decisions that pick which valuation
framework a company is judged by at all.
"""

from __future__ import annotations

import pytest

from idx_picker.scraper import metrics as M
from idx_picker.scraper import scoring as S

from .conftest import make_bundle


# ------------------------------------------------------------------- helpers


def core_with(**kwargs) -> M.CoreFinancials:
    return M.CoreFinancials(ticker="T", **kwargs)


def ncav_core(current_assets: float = 1000.0, total_liabilities: float = 800.0):
    """NCAV per share = (1000 - 800)/10 = 20.0 with the default arguments."""
    return core_with(current_assets=current_assets, total_liabilities=total_liabilities)


def buyable_assessment(mos: float = 0.60) -> S.Assessment:
    """An assessment that clears every gate, so each test can break exactly one."""
    assessment = S.Assessment(ticker="T")
    assessment.mos_base = mos
    assessment.safety_score = 70.0
    assessment.quality_score = 70.0
    return assessment


def verdict(assessment: S.Assessment, f_score=6, is_net_net=False,
            quarters_stale=0.5, red_flags=None) -> str:
    return S.classify(
        assessment, price=100.0, mos_buy=0.30, mos_watch=0.10,
        f_score=f_score, is_net_net=is_net_net, quarters_stale=quarters_stale,
        red_flags=red_flags or [],
    )


# ======================================================= business classification


def test_financial_sector_routes_to_financial_even_with_great_economics():
    """Sector wins over every quality signal for banks and insurers.

    EV/EBIT and FCF are noise for a lender -- debt is raw material, not leverage,
    and "capex" is loan origination. A bank with a 30% ROIC reading must still be
    routed to the book-value track, or the screen ends up recommending a bank on
    an enterprise-value multiple.
    """
    for sector in ("Financials", "financial services", "BANKS", "  Insurance  "):
        assert S.classify_business(sector, ncav_core(), price=1000.0, shares=10.0,
                                   roic=0.30, revenue_cagr=0.20) == S.BUSINESS_FINANCIAL


def test_sub_ncav_routes_to_deep_value_even_with_poor_economics():
    """Trading below liquidation value is a special situation regardless of ROIC.

    That is the entire premise of the Graham lens: the thesis is the balance
    sheet, not the income statement, so the net-net test has to run *before* the
    quality tests or every cigar butt gets filed as "Ordinary" and valued on a
    DCF it will never justify.
    """
    # NCAV per share = 20.0; price 15 is below it.
    business = S.classify_business("Consumer Cyclicals", ncav_core(), price=15.0,
                                   shares=10.0, roic=-0.30, revenue_cagr=-0.40)
    assert business == S.BUSINESS_DEEP_VALUE


def test_sub_ncav_does_not_override_the_financial_route():
    """A bank below NCAV is still a bank.

    Bank "current assets" are loans and interbank placements; a Graham
    liquidation reading of them is not meaningful, so the sector check must stay
    ahead of the NCAV check.
    """
    business = S.classify_business("Financials", ncav_core(), price=15.0, shares=10.0,
                                   roic=0.05, revenue_cagr=0.01)
    assert business == S.BUSINESS_FINANCIAL


@pytest.mark.parametrize(
    "roic, cagr, expected",
    [
        (0.30, 0.20, S.BUSINESS_COMPOUNDER),  # both high
        (0.30, 0.02, S.BUSINESS_ORDINARY),    # returns without growth
        (0.05, 0.20, S.BUSINESS_ORDINARY),    # growth without returns
        (0.12, 0.20, S.BUSINESS_ORDINARY),    # ROIC exactly at the 12% threshold
        (0.30, 0.05, S.BUSINESS_ORDINARY),    # CAGR exactly at the 5% threshold
        (None, 0.20, S.BUSINESS_ORDINARY),    # unknown returns is not a pass
        (0.30, None, S.BUSINESS_ORDINARY),    # unknown growth is not a pass
    ],
)
def test_compounder_requires_both_returns_and_growth(roic, cagr, expected):
    """A compounder earns above its cost of capital *and* keeps growing.

    Either condition alone is a different animal: high ROIC with no growth is a
    cash cow to be valued on EPV, and growth without returns is value
    destruction. Thresholds are strict (`>`), so a name sitting exactly on 12% /
    5% does not qualify.
    """
    core = ncav_core(current_assets=100.0, total_liabilities=900.0)  # NCAV negative
    assert S.classify_business("Technology", core, price=1000.0, shares=10.0,
                               roic=roic, revenue_cagr=cagr) == expected


def test_cyclical_sector_beats_the_compounder_test():
    """A cyclical with a great trailing year is still a cyclical.

    TTM returns at the top of a commodity cycle look exactly like a compounder's;
    routing on sector first is what forces the mid-cycle (EPV) valuation instead
    of capitalising the peak.
    """
    core = ncav_core(current_assets=100.0, total_liabilities=900.0)
    assert S.classify_business("Energy", core, price=1000.0, shares=10.0,
                               roic=0.40, revenue_cagr=0.30) == S.BUSINESS_CYCLICAL


# ================================================================= net-net test


@pytest.mark.parametrize(
    "price, expected",
    [
        (13.32, True),      # just below 2/3 * 20 = 13.333...
        (13.3333333, True),
        (13.34, False),     # just above
        (20.0, False),      # below NCAV but not below 2/3 of it
    ],
)
def test_net_net_threshold_is_two_thirds_of_ncav(price, expected):
    """Graham's margin is a *third* off NCAV, not merely trading below NCAV.

    The one-third discount is the buffer against the receivables and inventory
    on the books not realising their carrying value in a wind-up. A test that
    fires at 1.0x NCAV has no such buffer and is a different, much weaker
    strategy wearing the same name.
    """
    passed, ncav_ps = S.net_net_test(ncav_core(), price, shares=10.0)
    assert ncav_ps == pytest.approx(20.0)
    assert passed is expected


def test_net_net_is_false_for_negative_ncav_and_still_reports_it():
    """Negative NCAV can never pass, but the figure is still returned.

    A negative price is always below a negative threshold arithmetically, so the
    non-positive guard is what stops every over-levered company being labelled a
    net-net.
    """
    passed, ncav_ps = S.net_net_test(ncav_core(current_assets=100.0,
                                               total_liabilities=900.0), 1.0, 10.0)
    assert passed is False
    assert ncav_ps == pytest.approx(-80.0)


def test_net_net_false_on_missing_price_or_ncav():
    """Missing inputs must not accidentally pass the test."""
    assert S.net_net_test(ncav_core(), None, 10.0)[0] is False
    assert S.net_net_test(core_with(), 10.0, 10.0) == (False, None)


# ===================================================== the four BUY gates


def test_only_a_name_passing_all_four_gates_returns_buy():
    """BUY requires MOS *and* safety *and* F-Score *and* no red flag.

    This is the baseline the next four tests break one gate at a time against.
    """
    assert verdict(buyable_assessment()) == S.VERDICT_BUY


def test_huge_mos_with_a_weak_balance_sheet_is_watch_not_buy():
    """A 60% margin of safety cannot buy its way past a distressed balance sheet.

    This is the value trap in its purest form: the discount exists *because* the
    company may not survive to realise it. Cheapness is evidence about price,
    not about solvency.
    """
    assessment = buyable_assessment()
    assessment.safety_score = 39.0  # gate is < 40
    assert verdict(assessment) == S.VERDICT_WATCH
    assert "value trap" in assessment.reasons[-1]


def test_huge_mos_with_low_f_score_is_watch_not_buy():
    """F-Score <= 3 means the fundamentals are deteriorating; cheap does not fix that.

    Piotroski's own result is that low-F-Score value stocks underperform the
    market; buying them is the single most reliable way to lose money in a value
    screen.
    """
    assessment = buyable_assessment()
    assert verdict(assessment, f_score=3) == S.VERDICT_WATCH
    assert verdict(buyable_assessment(), f_score=4) == S.VERDICT_BUY


def test_huge_mos_with_poor_business_economics_is_watch_not_buy():
    """A business earning below its cost of capital destroys the discount over time.

    A 60% discount to a fair value that itself shrinks 10% a year is not a
    margin of safety, it is a slower loss.
    """
    assessment = buyable_assessment()
    assessment.quality_score = 34.0  # gate is < 35
    assert verdict(assessment) == S.VERDICT_WATCH
    assert "value trap risk" in assessment.reasons[-1]


def test_huge_mos_with_a_red_flag_is_watch_not_buy():
    """An unresolved red flag demands human work before capital is committed.

    The flag is surfaced in the reason so the user knows *which* one blocked it.
    """
    assessment = buyable_assessment()
    result = verdict(assessment, red_flags=["Net debt/EBITDA 6.2x", "Interest coverage 1.1x"])
    assert result == S.VERDICT_WATCH
    assert "Net debt/EBITDA 6.2x" in assessment.reasons[-1]


@pytest.mark.parametrize("safety, quality, f_score", [(40.0, 35.0, 4)])
def test_gate_boundaries_are_exactly_at_the_documented_thresholds(safety, quality, f_score):
    """The gates trip below 40 safety, below 35 quality and at or below F-Score 3.

    Pinning the boundary means a later change to any threshold is deliberate.
    """
    assessment = buyable_assessment()
    assessment.safety_score, assessment.quality_score = safety, quality
    assert verdict(assessment, f_score=f_score) == S.VERDICT_BUY


# ==================================================== MOS thresholds and staleness


def test_mos_below_the_watch_threshold_is_skip():
    """Not cheap enough to watch is a SKIP, not a WATCH.

    The watchlist has to stay short enough to be read; a fairly valued name
    belongs off it entirely.
    """
    assessment = buyable_assessment(mos=0.05)
    assert verdict(assessment) == S.VERDICT_SKIP


def test_mos_between_the_thresholds_is_watch():
    """Attractive but short of the buy threshold is the definition of a watchlist."""
    assessment = buyable_assessment(mos=0.20)
    assert verdict(assessment) == S.VERDICT_WATCH
    assert "short of buy threshold" in assessment.reasons[-1]


def test_no_intrinsic_value_is_skip_not_buy():
    """An unknown margin of safety must never be treated as a large one."""
    assessment = buyable_assessment()
    assessment.mos_base = None
    assert verdict(assessment) == S.VERDICT_SKIP
    assert "No usable intrinsic value" in assessment.reasons[-1]


@pytest.mark.parametrize("staleness, expected", [(3.01, S.VERDICT_SKIP), (3.0, S.VERDICT_BUY)])
def test_stale_filings_skip_regardless_of_how_cheap(staleness, expected):
    """Filings more than three quarters old make a name unscreenable, full stop.

    Every number on the row describes a company that may no longer exist in that
    form. The staleness check runs before everything else -- including the
    net-net branch -- because a cheap-looking stale name is the most dangerous
    row in the file.
    """
    assessment = buyable_assessment(mos=0.95)
    assert verdict(assessment, quarters_stale=staleness) == expected


def test_stale_filings_skip_even_a_net_net():
    """Staleness outranks the deep-value branch too.

    A liquidation thesis three quarters out of date is a thesis about a balance
    sheet that has since been spent.
    """
    assessment = buyable_assessment(mos=0.95)
    assert verdict(assessment, is_net_net=True, quarters_stale=5.0) == S.VERDICT_SKIP


def test_unknown_staleness_does_not_block_a_verdict():
    """A missing filing date must not silently SKIP the whole universe."""
    assert verdict(buyable_assessment(), quarters_stale=None) == S.VERDICT_BUY


# ========================================================== the net-net branch


def test_net_net_with_a_distressed_balance_sheet_is_watch_not_deep_value():
    """A net-net that may not survive the year is a WATCH, not a recommendation.

    NCAV is a liquidation estimate, and liquidation only pays out if the company
    is wound up rather than burning the working capital first. Safety below 30
    is the going-concern trip-wire.
    """
    assessment = buyable_assessment()
    assessment.safety_score = 29.0
    assert verdict(assessment, is_net_net=True) == S.VERDICT_WATCH
    assert "going-concern risk" in assessment.reasons[-1]


def test_healthy_net_net_is_deep_value():
    """A solvent net-net gets its own verdict, distinct from BUY.

    It is a different holding period and a different thesis, so it must not be
    collapsed into the quality-value bucket.
    """
    assessment = buyable_assessment()
    assessment.safety_score = 55.0
    assert verdict(assessment, is_net_net=True) == S.VERDICT_DEEP_VALUE


def test_net_net_branch_ignores_margin_of_safety_and_f_score():
    """Deep value is judged on asset protection, not earnings momentum.

    A net-net with no computable DCF (hence no MOS) and a collapsing F-Score is
    still a net-net -- that is usually exactly what a net-net looks like.
    """
    assessment = buyable_assessment()
    assessment.mos_base = None
    assessment.safety_score = 55.0
    assert verdict(assessment, f_score=1, is_net_net=True) == S.VERDICT_DEEP_VALUE


# Regression test for a fixed defect:
# DEFECT: missing quality/safety/F-Score data passes every BUY gate.
def test_missing_quality_and_safety_data_must_not_produce_a_buy():
    """Unknown is not the same as passing.

    The docstring promises a BUY requires "evidence of financial improvement" and
    "a balance sheet that is not distressed". A row where all three of those are
    blank has no such evidence, yet currently returns BUY -- and blanks are
    common: two of nine F-Score signals are unevaluable for the entire IDX
    universe today. The safe default for a screener that gates on data is to
    hold the name at WATCH until the data exists.
    """
    assessment = S.Assessment(ticker="T")
    assessment.mos_base = 0.80  # the only thing known about this company
    result = S.classify(assessment, price=100.0, mos_buy=0.30, mos_watch=0.10,
                        f_score=None, is_net_net=False, quarters_stale=None, red_flags=[])
    assert result == S.VERDICT_WATCH


# ========================================================== blended intrinsic


def _scenarios(base_iv: float | None) -> dict[str, S.Scenario]:
    return {"base": S.Scenario(name="base", growth=0.03, wacc=0.10,
                               terminal_growth=0.02, intrinsic_value=base_iv)}


def test_deep_value_anchors_on_the_minimum_asset_floor():
    """Deep value takes the *lowest* lens, which is the liquidation anchor.

    An optimistic DCF on a cigar butt is a fantasy about a business that is not
    working; the only number with evidence behind it is the balance sheet. The
    minimum is safe here precisely because NCAV is asset-based rather than
    multiple-derived, so it cannot collapse toward zero the way a levered
    EV/EBIT lens can.
    """
    value = S.blended_intrinsic(_scenarios(5000.0), epv_value=2000.0,
                                comparables_value=1500.0, ncav_ps=800.0,
                                business_type=S.BUSINESS_DEEP_VALUE)
    assert value == pytest.approx(800.0)


def test_deep_value_ignores_the_dcf_entirely():
    """The DCF is not even a candidate for a deep-value name.

    If it were, a name whose only usable lens is a DCF would get an asset-based
    label with an earnings-based valuation -- the worst of both frameworks.
    """
    assert S.blended_intrinsic(_scenarios(5000.0), None, None, None,
                               S.BUSINESS_DEEP_VALUE) is None


def test_cyclical_weights_epv_above_dcf():
    """Mid-cycle earnings power must outweigh a projection off the current cycle.

    Weights are DCF 0.2 / EPV 0.5 / comps 0.3, versus 0.4 / 0.35 / 0.25 for an
    ordinary name. With a DCF far above EPV, the cyclical blend must land lower.
    """
    cyclical = S.blended_intrinsic(_scenarios(5000.0), 2000.0, 1500.0, None,
                                   S.BUSINESS_CYCLICAL)
    ordinary = S.blended_intrinsic(_scenarios(5000.0), 2000.0, 1500.0, None,
                                   S.BUSINESS_ORDINARY)
    # cyclical: 5000*.2 + 2000*.5 + 1500*.3 = 2450
    # ordinary: 5000*.4 + 2000*.35 + 1500*.25 = 3075
    assert cyclical == pytest.approx(2450.0)
    assert ordinary == pytest.approx(3075.0)
    assert cyclical < ordinary


def test_financials_never_use_the_dcf_path():
    """A bank's fair value must not depend on a free-cash-flow projection.

    "Free cash flow" for a lender is an accounting artefact of deposit growth. If
    the DCF leaked into the financial blend, deposit-gathering banks would be
    valued on the wrong side of their own balance sheet.
    """
    value = S.blended_intrinsic(_scenarios(9_000_000.0), epv_value=2000.0,
                                comparables_value=1500.0, ncav_ps=800.0,
                                business_type=S.BUSINESS_FINANCIAL)
    assert value == pytest.approx(1750.0)  # mean of 1500 and 2000, DCF absent
    assert S.blended_intrinsic(_scenarios(9_000_000.0), None, None, 800.0,
                               S.BUSINESS_FINANCIAL) is None


def test_blend_drops_non_positive_lenses_and_reweights():
    """A negative or zero lens is excluded and the remaining weights renormalise.

    Otherwise one broken lens would drag the blend down by its full weight while
    contributing no information.
    """
    value = S.blended_intrinsic(_scenarios(-100.0), epv_value=2000.0,
                                comparables_value=1500.0, ncav_ps=None,
                                business_type=S.BUSINESS_ORDINARY)
    # weights renormalise over EPV 0.35 and comps 0.25 -> (2000*.35 + 1500*.25)/0.6
    assert value == pytest.approx((2000 * 0.35 + 1500 * 0.25) / 0.60)


@pytest.mark.parametrize(
    "business_type",
    [S.BUSINESS_ORDINARY, S.BUSINESS_CYCLICAL, S.BUSINESS_FINANCIAL,
     S.BUSINESS_DEEP_VALUE, S.BUSINESS_COMPOUNDER],
)
def test_blend_returns_none_when_every_lens_is_missing(business_type):
    """No lens means no intrinsic value, which routes the name to SKIP.

    Returning 0 instead would report an infinitely negative margin of safety.
    """
    assert S.blended_intrinsic({}, None, None, None, business_type) is None


# ================================================================== scenarios


def _dcf_core() -> M.CoreFinancials:
    return M.CoreFinancials(ticker="T", fcf_ttm=1000.0, total_debt=0.0, cash=0.0)


def test_bear_is_pessimistic_on_both_growth_and_discount_rate():
    """The bear case must lower growth *and* raise the WACC; the bull, the reverse.

    Varying growth alone understates the spread, because the macro states that
    depress growth are the same ones that widen risk premia. A scenario band
    that is too narrow gives false precision to the base case.
    """
    scenarios = S.build_scenarios(_dcf_core(), None, shares=100.0, price=50.0,
                                  base_wacc=0.11, base_terminal_growth=0.03,
                                  historical_growth=0.06)
    bear, base, bull = scenarios["bear"], scenarios["base"], scenarios["bull"]

    assert bear.growth < base.growth < bull.growth
    assert bear.wacc > base.wacc > bull.wacc
    assert bear.terminal_growth < base.terminal_growth < bull.terminal_growth


def test_scenario_intrinsic_values_are_ordered_bear_below_base_below_bull():
    """The resulting valuations must respect the scenario ordering.

    A bull case below the base case is not a valuation range, it is a bug, and
    it corrupts the IV Bull / MOS Bull columns users read as an upside bound.
    """
    scenarios = S.build_scenarios(_dcf_core(), None, shares=100.0, price=50.0,
                                  base_wacc=0.11, base_terminal_growth=0.03,
                                  historical_growth=0.06)
    values = {name: scenario.intrinsic_value for name, scenario in scenarios.items()}
    assert all(value is not None for value in values.values()), values
    assert values["bear"] < values["base"] < values["bull"]


def test_scenario_mos_and_upside_use_different_denominators():
    """MOS divides by intrinsic value, upside by price; they are not the same number.

    Reporting one as the other is a classic screener error: a 50% MOS is a 100%
    upside, and confusing them doubles or halves every headline figure.
    """
    scenarios = S.build_scenarios(_dcf_core(), None, shares=100.0, price=50.0,
                                  base_wacc=0.11, base_terminal_growth=0.03,
                                  historical_growth=0.06)
    base = scenarios["base"]
    assert base.mos == pytest.approx((base.intrinsic_value - 50.0) / base.intrinsic_value)
    assert base.upside == pytest.approx(base.intrinsic_value / 50.0 - 1)
    assert base.mos != pytest.approx(base.upside)


def test_scenarios_prefer_normalised_ebit_over_trailing_fcf():
    """A cyclical must be valued off mid-cycle cash flow, not the current quarter's.

    Trailing FCF at a cycle trough produces a valuation that says "this trough is
    permanent", which is the opposite of what a mid-cycle framework is for.
    """
    core = M.CoreFinancials(ticker="T", fcf_ttm=10.0, ebit_ttm=100.0, ebitda_ttm=140.0,
                            capex_ttm=-20.0, total_debt=0.0, cash=0.0)
    scenarios = S.build_scenarios(core, normalised_ebit_value=500.0, shares=100.0,
                                  price=50.0, base_wacc=0.11, base_terminal_growth=0.03,
                                  historical_growth=0.06)
    # fcf_base = 500*0.78 + (140 - 100) + (-20) = 390 + 20 = 410, far above fcf_ttm 10
    ttm_based = S.build_scenarios(core, None, 100.0, 50.0, 0.11, 0.03, 0.06)
    assert scenarios["base"].intrinsic_value > (ttm_based["base"].intrinsic_value or 0) * 10


def test_scenario_growth_is_clamped_to_a_sane_band():
    """Historical growth is clamped into [-5%, +15%] before it drives a projection.

    Extrapolating a 60% historical CAGR for five years is not a valuation, and a
    single restated base year can produce one.
    """
    hot = S.build_scenarios(_dcf_core(), None, 100.0, 50.0, 0.11, 0.03,
                            historical_growth=0.90)
    assert hot["base"].growth == pytest.approx(0.15)


def test_scenarios_are_all_none_when_the_cash_flow_base_is_unusable():
    """A cash-burning company yields no scenario values at all, not negative ones."""
    core = M.CoreFinancials(ticker="T", fcf_ttm=-500.0, total_debt=0.0, cash=0.0)
    scenarios = S.build_scenarios(core, None, 100.0, 50.0, 0.11, 0.03, 0.06)
    assert all(scenario.intrinsic_value is None for scenario in scenarios.values())
    assert all(scenario.mos is None for scenario in scenarios.values())


# Regression test for a fixed defect:
# DEFECT: with historical growth at or below -5% the base growth and the
def test_bear_growth_is_still_lower_when_the_base_is_already_at_the_floor():
    """A shrinking company must still have a bear case worse than its base case.

    `growth_base` is clamped to >= -0.05 and the bear spec is
    `max(-0.05, growth_base - 0.05)`; when the base is already at the floor both
    land on -0.05 and the scenario band silently narrows to a WACC-only spread
    for the very names whose downside is most real.
    """
    scenarios = S.build_scenarios(_dcf_core(), None, 100.0, 50.0, 0.11, 0.03,
                                  historical_growth=-0.30)
    assert scenarios["bear"].growth < scenarios["base"].growth


# Regression test for a fixed defect:
# DEFECT: the bull WACC floor of 0.06 is applied without reference to the
def test_bull_case_is_never_worse_than_the_base_case():
    """The bull scenario must never value a company below its own base case.

    With base WACC 5%, bull WACC becomes max(0.06, 0.04) = 6% -- higher than the
    base -- and the bull IV lands below the base IV (530 vs 565 per share on the
    reference fixture). Anyone reading "IV Bull" as an upper bound is misled, and
    MOS Bull becomes less attractive than MOS Base.
    """
    scenarios = S.build_scenarios(_dcf_core(), None, 100.0, 50.0, base_wacc=0.05,
                                  base_terminal_growth=0.03, historical_growth=0.05)
    assert scenarios["bull"].wacc <= scenarios["base"].wacc
    assert scenarios["bull"].intrinsic_value >= scenarios["base"].intrinsic_value


# ================================================================== red flags


def _clean_core() -> M.CoreFinancials:
    """A core that trips no flag, so each test can trip exactly one."""
    return M.CoreFinancials(
        ticker="T",
        net_income_ttm=100.0,
        cfo_ttm=150.0,
        ebit_ttm=200.0,
        ebitda_ttm=300.0,
        interest_expense_ttm=20.0,   # coverage 10x
        total_debt=300.0,
        cash=100.0,                  # net debt 200 / EBITDA 300 = 0.67x
    )


def test_no_red_flags_on_a_clean_company():
    """The baseline must be silent, or every later assertion is meaningless."""
    assert S.detect_red_flags(_clean_core(), make_bundle(), S.BUSINESS_ORDINARY) == []


def test_flags_earnings_that_outrun_cash_generation():
    """Profits that never become cash are the most reliable early warning here.

    CFO below half of net income means the reported profit lives in receivables
    and inventory. Fires at 49, silent at 51.
    """
    core = _clean_core()
    core.cfo_ttm = 49.0
    assert any("exceed cash generation" in flag
               for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_ORDINARY))
    core.cfo_ttm = 51.0
    assert not any("exceed cash generation" in flag
                   for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_ORDINARY))


def test_flags_persistently_negative_free_cash_flow():
    """Six negative FCF quarters out of eight is structural, not cyclical.

    Five of eight is a bad year; six is a business that does not fund itself.
    """
    six_bad = make_bundle(quarterly={"FreeCashFlow": [-1, -1, -1, -1, -1, -1, 5, 5]})
    five_bad = make_bundle(quarterly={"FreeCashFlow": [-1, -1, -1, -1, -1, 5, 5, 5]})
    assert any("negative in 6 of last 8" in flag
               for flag in S.detect_red_flags(_clean_core(), six_bad, S.BUSINESS_ORDINARY))
    assert not any("negative in 6 of last 8" in flag
                   for flag in S.detect_red_flags(_clean_core(), five_bad, S.BUSINESS_ORDINARY))


def test_flags_material_share_count_growth():
    """A share count up more than 15% in two years dilutes the per-share thesis.

    Every intrinsic value on the row is per share; issuance that outruns the
    business is the quietest way for an apparent bargain to evaporate. Compares
    against eight quarters back, so a nine-quarter series is required.
    """
    diluting = make_bundle(quarterly={"DilutedAverageShares": [1000] * 8 + [1160]})
    steady = make_bundle(quarterly={"DilutedAverageShares": [1000] * 8 + [1140]})
    flags = S.detect_red_flags(_clean_core(), diluting, S.BUSINESS_ORDINARY)
    assert any("Share count up" in flag for flag in flags)
    assert not any("Share count up" in flag
                   for flag in S.detect_red_flags(_clean_core(), steady, S.BUSINESS_ORDINARY))


def test_flags_high_net_debt_to_ebitda_but_not_for_financials():
    """Above 4x net debt/EBITDA is a leverage flag -- except for lenders.

    A bank's "net debt" is its funding base; applying an industrial leverage
    screen to it would flag every solvent bank in the country.
    """
    core = _clean_core()
    core.total_debt, core.cash = 1400.0, 100.0  # net debt 1300 / 300 = 4.33x
    assert any("Net debt/EBITDA" in flag
               for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_ORDINARY))
    assert not any("Net debt/EBITDA" in flag
                   for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_FINANCIAL))


def test_flags_gross_margin_erosion_over_two_years():
    """A gross margin down more than 5pp in two years signals lost pricing power.

    Needs twelve quarters (a TTM window eight quarters back), which is why the
    fixture is long. Margin structure decays slowly and is the hardest thing for
    a value thesis to recover from.
    """
    eroding = make_bundle(quarterly={
        "TotalRevenue": [100] * 12,
        # oldest TTM margin 40%, latest TTM margin 30%
        "GrossProfit": [40, 40, 40, 40, 35, 35, 35, 35, 30, 30, 30, 30],
    })
    stable = make_bundle(quarterly={
        "TotalRevenue": [100] * 12,
        "GrossProfit": [40, 40, 40, 40, 38, 38, 38, 38, 37, 37, 37, 37],
    })
    assert any("Gross margin down" in flag
               for flag in S.detect_red_flags(_clean_core(), eroding, S.BUSINESS_ORDINARY))
    assert not any("Gross margin down" in flag
                   for flag in S.detect_red_flags(_clean_core(), stable, S.BUSINESS_ORDINARY))


def test_flags_thin_interest_coverage():
    """Interest cover below 1.5x means the lenders, not the shareholders, decide.

    Silent when no interest expense is reported -- absence of debt is not thin
    coverage.
    """
    core = _clean_core()
    core.interest_expense_ttm = 150.0  # 200 / 150 = 1.33x
    assert any("Interest coverage" in flag
               for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_ORDINARY))
    core.interest_expense_ttm = 100.0  # 2.0x
    assert not any("Interest coverage" in flag
                   for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_ORDINARY))
    core.interest_expense_ttm = None
    assert not any("Interest coverage" in flag
                   for flag in S.detect_red_flags(core, make_bundle(), S.BUSINESS_ORDINARY))


def test_flags_the_peak_and_trough_earnings_assumptions():
    """When mid-cycle EBIT diverges from trailing EBIT, the bet must be made explicit.

    Normalised above 2x trailing means every valuation on the row assumes the
    cycle recovers; below 0.5x means the trailing figure is probably a peak. The
    user should see the assumption rather than inherit it silently.
    """
    recovery = _clean_core()
    recovery._normalised_ebit = 500.0  # 2.5x trailing 200
    assert any("assumes cycle recovery" in flag
               for flag in S.detect_red_flags(recovery, make_bundle(), S.BUSINESS_ORDINARY))

    peak = _clean_core()
    peak._normalised_ebit = 80.0  # trailing 200 is 2.5x mid-cycle
    assert any("possible peak earnings" in flag
               for flag in S.detect_red_flags(peak, make_bundle(), S.BUSINESS_ORDINARY))

    middling = _clean_core()
    middling._normalised_ebit = 220.0  # 1.1x, within the band
    assert not any("cycle" in flag or "peak" in flag
                   for flag in S.detect_red_flags(middling, make_bundle(), S.BUSINESS_ORDINARY))


def test_red_flags_survive_a_completely_empty_bundle():
    """A ticker with no statement history must not raise inside flag detection.

    `detect_red_flags` runs for every row; an exception here would drop the
    ticker from the output entirely rather than reporting it as data-poor.
    """
    assert S.detect_red_flags(M.CoreFinancials(ticker="T"), make_bundle(),
                              S.BUSINESS_ORDINARY) == []


# ================================================================ score bands


def test_quality_score_grades_financials_on_roe_not_roic():
    """A bank's ROIC is not meaningful; its ROE is.

    Grading a lender on ROIC would push every bank to the same band regardless
    of how well it actually deploys shareholder capital.
    """
    core = M.CoreFinancials(ticker="T")
    financial = S.score_quality(core, roic=None, roe=0.22, business_type=S.BUSINESS_FINANCIAL,
                                revenue_cagr=0.10, gross_margin=0.05)
    # ROE band 100 and revenue CAGR band 85; gross margin is skipped for financials
    assert financial == pytest.approx(92.5)


def test_safety_score_returns_none_when_nothing_is_computable():
    """No inputs means no score -- which is what makes the `classify` gate blind.

    Documented here because `classify` treats this None as a pass; see
    `test_missing_quality_and_safety_data_must_not_produce_a_buy`.
    """
    assert S.score_safety(M.CoreFinancials(ticker="T"), None, None,
                          S.BUSINESS_FINANCIAL) is None


def test_band_helper_is_a_first_threshold_wins_step_function():
    """Bands must be evaluated top-down, returning the floor when nothing clears."""
    thresholds = [(0.20, 100), (0.10, 70)]
    assert S._band(0.25, thresholds, 10) == 100.0
    assert S._band(0.20, thresholds, 10) == 100.0  # inclusive
    assert S._band(0.15, thresholds, 10) == 70.0
    assert S._band(-0.50, thresholds, 10) == 10.0
