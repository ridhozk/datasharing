"""Unit tests for `idx_picker.scraper.metrics`.

Each test pins a *contract* -- what a caller is entitled to assume -- rather than
restating the implementation. The recurring theme is that a metric which cannot
be computed must return ``None``, never a plausible-looking number, because
every one of these values feeds a BUY/WATCH/SKIP decision downstream and a
silently wrong number is far more damaging than a blank.
"""

from __future__ import annotations

from datetime import date

import pytest

from idx_picker.scraper import metrics as M

from .conftest import TODAY, make_bundle


# ============================================================== ttm / offsets


def test_ttm_sums_exactly_four_quarters():
    """TTM must be the sum of the four most recent quarters and nothing else.

    Downstream margins, yields and the Piotroski deltas all divide by this
    figure; including a fifth quarter or dropping one silently rescales every
    ratio built on it.
    """
    bundle = make_bundle(quarterly={"TotalRevenue": [90, 100, 110, 120, 130]})
    # Last four of [90,100,110,120,130] = 100+110+120+130 = 460
    assert M.ttm(bundle, "TotalRevenue") == 460.0


def test_ttm_returns_none_with_only_three_quarters():
    """Three quarters must be None, not a 3/4-scale understatement.

    A newly listed company with three filings would otherwise show a TTM revenue
    ~25% below reality, which inflates every margin and yield computed from it
    and can flip a name into the "cheap" bucket on missing data alone.
    """
    bundle = make_bundle(quarterly={"TotalRevenue": [100, 110, 120]})
    assert M.ttm(bundle, "TotalRevenue") is None


def test_ttm_offset_four_returns_prior_year_window():
    """`offset=4` must return the same four quarters one year earlier.

    This is the comparison basis for every year-over-year signal in the
    F-Score; an off-by-one here corrupts four of the nine signals at once.
    """
    bundle = make_bundle(quarterly={"TotalRevenue": [1, 2, 3, 4, 5, 6, 7, 8]})
    assert M.ttm(bundle, "TotalRevenue") == 26.0  # 5+6+7+8
    assert M.ttm(bundle, "TotalRevenue", 4) == 10.0  # 1+2+3+4


def test_ttm_offset_window_incomplete_returns_none():
    """An offset window that runs off the start of the series must be None.

    Wrapping or clamping would compare this year's TTM against a shorter,
    smaller window, manufacturing fake growth for every short-history name.
    """
    bundle = make_bundle(quarterly={"TotalRevenue": [1, 2, 3, 4, 5, 6, 7, 8]})
    assert M.ttm(bundle, "TotalRevenue", 5) is None  # only 3 quarters remain
    assert M.ttm(bundle, "TotalRevenue", 8) is None
    assert M.ttm(bundle, "TotalRevenue", 99) is None


def test_ttm_missing_field_returns_none():
    """A field Yahoo never reported must be None, not zero."""
    assert M.ttm(make_bundle(), "TotalRevenue") is None


# ==================================================================== growth


def test_growth_normal_case():
    """Ordinary positive-base growth is the familiar (cur - prior)/prior."""
    assert M.growth(120, 100) == pytest.approx(0.20)  # (120-100)/100


def test_growth_negative_base_is_a_turnaround_not_a_collapse():
    """A swing from -100 to +50 must read +150%, not -150%.

    This is the single most important sign convention in the module. Naive
    ``(cur - prior)/prior`` divides by a negative base and flips the sign, so
    every loss-making company that turns profitable is scored as if it had
    collapsed -- and the quality/growth bands would then penalise exactly the
    recoveries a value screen exists to find.
    """
    assert M.growth(50, -100) == pytest.approx(1.5)
    # And the genuinely deteriorating direction still reads negative.
    assert M.growth(-150, -100) == pytest.approx(-0.5)  # (-150 - -100)/100


def test_growth_zero_base_returns_none():
    """A zero base is undefined growth, not infinite growth."""
    assert M.growth(100, 0) is None
    assert M.growth(0, 0) is None


def test_growth_none_inputs_return_none():
    """Missing data must propagate as None rather than being read as zero."""
    assert M.growth(None, 100) is None
    assert M.growth(100, None) is None


@pytest.mark.parametrize(
    "current, prior",
    [
        (5_000, 1),      # +499,900%
        (-5_000, 1),     # -500,100%
        (1_200, 100),    # +1100%, just past the 10.0 cap
    ],
)
def test_growth_cap_suppresses_absurd_values(current, prior):
    """|growth| beyond GROWTH_CAP (10.0) must be None, not a ranking-dominating number.

    Yahoo restates tiny prior-year bases constantly. A single IDR 1mn base year
    produces a 5,000x "growth" that would sit at the top of any growth-ranked
    list forever, crowding out real compounders.
    """
    assert abs((current - prior) / abs(prior)) > M.GROWTH_CAP
    assert M.growth(current, prior) is None


def test_growth_cap_boundary_is_inclusive():
    """Exactly 10.0x is retained; the cap rejects only what exceeds it."""
    assert M.growth(1_100, 100) == pytest.approx(10.0)  # (1100-100)/100 = 10.0
    assert M.growth(1_101, 100) is None


# ====================================================================== cagr


def test_cagr_compounds_correctly():
    """CAGR must compound, not average.

    Doubling over 3 years is 25.99%/yr (2 ** (1/3) - 1), not 33%/yr. The
    difference decides whether a name clears the 5% compounder threshold in
    `classify_business`.
    """
    assert M.cagr(200.0, 100.0, 3) == pytest.approx(2 ** (1 / 3) - 1)
    assert M.cagr(133.1, 100.0, 3) == pytest.approx(0.10, abs=1e-9)  # 1.1**3 = 1.331


@pytest.mark.parametrize(
    "latest_value, earliest_value",
    [(-50.0, 100.0), (100.0, -50.0), (0.0, 100.0), (100.0, 0.0), (-50.0, -100.0)],
)
def test_cagr_none_when_either_endpoint_non_positive(latest_value, earliest_value):
    """A non-positive endpoint makes the geometric ratio meaningless.

    (-50/-100) ** (1/3) is a real number but says nothing about growth, and
    (50/-100) ** (1/3) is complex. Returning None is the only honest answer for
    a company that was or is loss-making across the window.
    """
    assert M.cagr(latest_value, earliest_value, 3) is None


def test_cagr_zero_or_negative_years_returns_none():
    """A zero-year window would be a division by zero in the exponent."""
    assert M.cagr(200.0, 100.0, 0) is None
    assert M.cagr(200.0, 100.0, -1) is None


# ================================================================== safe_div


def test_safe_div_zero_denominator():
    """Zero denominators must be None -- the workbook's classic divide-by-zero."""
    assert M.safe_div(100.0, 0.0) is None
    assert M.safe_div(0.0, 0.0) is None


def test_safe_div_none_inputs():
    """Either operand missing means the ratio is unknown, not zero."""
    assert M.safe_div(None, 10.0) is None
    assert M.safe_div(10.0, None) is None
    assert M.safe_div(None, None) is None


@pytest.mark.parametrize("numerator", [float("inf"), float("-inf"), float("nan")])
def test_safe_div_suppresses_non_finite_results(numerator):
    """inf/NaN must never escape into a CSV column or a scoring band.

    A NaN compares False against every threshold, so it would silently score at
    the band floor rather than being reported as missing data.
    """
    assert M.safe_div(numerator, 2.0) is None


def test_safe_div_normal_case_returns_the_quotient():
    """The happy path still has to work."""
    assert M.safe_div(3.0, 4.0) == pytest.approx(0.75)
    assert M.safe_div(0.0, 4.0) == pytest.approx(0.0)


# ================================================================== Piotroski


def _perfect_nine_bundle():
    """Eight quarters engineered so all nine Piotroski signals fire.

    Revenue 100x4 then 150x4; gross margin 30% -> 40%; net income 10x4 -> 25x4;
    CFO comfortably above net income; long-term debt paid down; current ratio
    1.5 -> 2.5; share count flat.
    """
    return make_bundle(
        quarterly={
            "TotalRevenue": [100, 100, 100, 100, 150, 150, 150, 150],
            "GrossProfit": [30, 30, 30, 30, 60, 60, 60, 60],
            "NetIncome": [10, 10, 10, 10, 25, 25, 25, 25],
            "OperatingCashFlow": [15, 15, 15, 15, 40, 40, 40, 40],
            # index -5 (one year ago) = 900, index -1 (now) = 1000
            "TotalAssets": [800, 850, 880, 900, 910, 930, 960, 1000],
            "LongTermDebt": [200, 200, 200, 200, 50, 50, 50, 50],
            "CurrentAssets": [300, 300, 300, 300, 500, 500, 500, 500],
            "CurrentLiabilities": [200, 200, 200, 200, 200, 200, 200, 200],
            "DilutedAverageShares": [1000] * 8,
        }
    )


def test_piotroski_perfect_nine():
    """A company improving on every axis must score exactly 9 with all signals set.

    The F-Score is a hard gate in `classify` (<= 3 forces WATCH), so both the
    total and the breakdown are part of the public contract, not diagnostics.
    """
    score, signals = M.piotroski_f_score(_perfect_nine_bundle())
    assert score == 9
    assert signals["_basis"] == "ttm"
    assert signals == {
        "_basis": "ttm",
        # TTM NI 100 / assets 1000 = 0.100 > prior 40 / 900 = 0.044
        "roa_positive": 1,
        "roa_improving": 1,
        "cfo_positive": 1,        # TTM CFO = 160
        "accruals": 1,            # CFO 160 > NI 100
        "leverage_falling": 1,    # LTD/assets 50/1000 = 0.05 <= 200/900 = 0.222
        "current_ratio_improving": 1,  # 500/200 = 2.5 > 300/200 = 1.5
        "no_dilution": 1,         # 1000 <= 1000 * 1.01
        "gross_margin_improving": 1,   # 240/600 = 0.40 > 120/400 = 0.30
        "asset_turnover_improving": 1,  # 600/1000 = 0.60 > 400/900 = 0.44
    }


def test_piotroski_zero():
    """A company deteriorating on every axis must score exactly 0, with no signal None.

    Zero and None are different verdicts: 0 means "nine signals evaluated, all
    bad", None means "not enough data to say". Conflating them is how a screen
    ends up rejecting a healthy company for having a short history.
    """
    bundle = make_bundle(
        quarterly={
            "TotalRevenue": [150, 150, 150, 150, 100, 100, 100, 100],
            "GrossProfit": [60, 60, 60, 60, 20, 20, 20, 20],
            "NetIncome": [-5, -5, -5, -5, -20, -20, -20, -20],
            "OperatingCashFlow": [-30] * 8,
            "TotalAssets": [800, 850, 880, 900, 910, 930, 960, 1000],
            "LongTermDebt": [50, 50, 50, 50, 400, 400, 400, 400],
            "CurrentAssets": [500, 500, 500, 500, 150, 150, 150, 150],
            "CurrentLiabilities": [200] * 8,
            "DilutedAverageShares": [1000, 1000, 1000, 1000, 1500, 1500, 1500, 1500],
        }
    )
    score, signals = M.piotroski_f_score(bundle)
    assert score == 0
    assert signals["_basis"] == "ttm"
    scored = {k: v for k, v in signals.items() if not k.startswith("_")}
    assert len(scored) == 9
    assert all(value == 0 for value in scored.values()), scored


def test_piotroski_intermediate_score_and_breakdown():
    """A mixed company must produce the exact partial score, signal by signal.

    Profitable and cash-generative but diluting, levering up, with a worsening
    current ratio and shrinking margin: the shape of a leveraged roll-up.
    """
    bundle = make_bundle(
        quarterly={
            "TotalRevenue": [100, 100, 100, 100, 150, 150, 150, 150],
            "GrossProfit": [40, 40, 40, 40, 45, 45, 45, 45],
            "NetIncome": [10, 10, 10, 10, 25, 25, 25, 25],
            "OperatingCashFlow": [15, 15, 15, 15, 40, 40, 40, 40],
            "TotalAssets": [800, 850, 880, 900, 910, 930, 960, 1000],
            "LongTermDebt": [50, 50, 50, 50, 400, 400, 400, 400],
            "CurrentAssets": [500, 500, 500, 500, 150, 150, 150, 150],
            "CurrentLiabilities": [200] * 8,
            "DilutedAverageShares": [1000, 1000, 1000, 1000, 1500, 1500, 1500, 1500],
        }
    )
    score, signals = M.piotroski_f_score(bundle)
    assert signals == {
        "_basis": "ttm",
        "roa_positive": 1,              # 100/1000 > 0
        "cfo_positive": 1,              # 160 > 0
        "roa_improving": 1,             # 0.100 > 40/900 = 0.044
        "accruals": 1,                  # 160 > 100
        "leverage_falling": 0,          # 400/1000 = 0.40 > 50/900 = 0.056
        "current_ratio_improving": 0,   # 0.75 < 2.5
        "no_dilution": 0,               # 1500 > 1000 * 1.01
        "gross_margin_improving": 0,    # 180/600 = 0.30 < 160/400 = 0.40
        "asset_turnover_improving": 1,  # 0.60 > 0.44
    }
    assert score == 5


def test_piotroski_uses_ttm_basis_with_eight_quarters():
    """With eight quarters the score must move on the TTM basis.

    The whole point is that the score refreshes each quarter instead of once a
    year; `_basis` is the observable proof of which comparison was used.
    """
    _, signals = M.piotroski_f_score(_perfect_nine_bundle())
    assert signals["_basis"] == "ttm"


def test_piotroski_falls_back_to_annual_with_fewer_than_eight_quarters():
    """Seven quarters is not enough for a prior-year TTM, so the annual basis applies.

    Falling back silently to a *three*-quarter comparison would be worse than
    using the annual filings Piotroski originally specified.
    """
    quarterly = {"TotalRevenue": [100] * 7, "NetIncome": [10] * 7}
    annual = {
        "TotalRevenue": [400, 600],
        "GrossProfit": [120, 240],
        "NetIncome": [40, 100],
        "OperatingCashFlow": [60, 160],
        "TotalAssets": [900, 1000],
        "LongTermDebt": [200, 50],
        "CurrentAssets": [300, 500],
        "CurrentLiabilities": [200, 200],
        "DilutedAverageShares": [1000, 1000],
    }
    score, signals = M.piotroski_f_score(make_bundle(quarterly=quarterly, annual=annual))
    assert signals["_basis"] == "annual"
    assert score == 9


def test_piotroski_annual_basis_when_net_income_history_is_short():
    """Eight revenue quarters do not license a TTM basis if net income is short.

    The gate must consider every series the comparison needs, not just the
    longest one, or the prior-year ROA silently becomes None and three signals
    vanish.
    """
    bundle = make_bundle(
        quarterly={"TotalRevenue": [100] * 8, "NetIncome": [10] * 5},
        annual={"TotalAssets": [900, 1000], "NetIncome": [40, 100],
                "TotalRevenue": [400, 600]},
    )
    _, signals = M.piotroski_f_score(bundle)
    assert signals["_basis"] == "annual"


def test_piotroski_returns_none_when_more_than_three_signals_unevaluable():
    """More than three blanks must return None, not a misleadingly low score.

    A "2/9" assembled from seven blanks reads as a distressed company to every
    downstream consumer -- including `classify`, where F-Score <= 3 forces a
    WATCH. That is a data problem being reported as a business problem.
    """
    bundle = make_bundle(annual={"TotalAssets": [900, 1000]})
    score, signals = M.piotroski_f_score(bundle)
    assert score is None
    scored = {k: v for k, v in signals.items() if not k.startswith("_")}
    assert sum(1 for value in scored.values() if value is None) > 3


def test_piotroski_scores_with_exactly_three_signals_unevaluable():
    """Exactly three blanks is still scoreable -- the cut-off is *more than* three.

    Pins the boundary so a later tightening of the rule is a deliberate change
    rather than an accident.
    """
    annual = {
        "TotalRevenue": [400, 600],
        "NetIncome": [40, 100],
        "OperatingCashFlow": [60, 160],
        "TotalAssets": [900, 1000],
        "LongTermDebt": [200, 50],
        # GrossProfit / CurrentAssets+CurrentLiabilities / DilutedAverageShares
        # omitted -> gross_margin_improving, current_ratio_improving and
        # no_dilution are exactly three blanks.
    }
    score, signals = M.piotroski_f_score(make_bundle(annual=annual))
    scored = {k: v for k, v in signals.items() if not k.startswith("_")}
    blanks = sum(1 for value in scored.values() if value is None)
    assert blanks == 3
    assert score is not None
    assert score == sum(v for v in scored.values() if v)


def test_piotroski_no_long_term_debt_reads_as_the_strongest_leverage_signal():
    """A company reporting no long-term debt scores the leverage signal, not a blank.

    Treating "no debt line" as unevaluable would spend one of only three
    permitted blanks on the single healthiest balance-sheet configuration.
    """
    annual = {
        "TotalRevenue": [400, 600], "GrossProfit": [120, 240],
        "NetIncome": [40, 100], "OperatingCashFlow": [60, 160],
        "TotalAssets": [900, 1000],
    }
    _, signals = M.piotroski_f_score(make_bundle(annual=annual))
    assert signals["leverage_falling"] == 1


@pytest.mark.xfail(
    reason="DEFECT: annual CFO is never derived from FreeCashFlow - CapitalExpenditure, "
           "so cfo_positive and accruals are permanently unevaluable on the annual "
           "basis whenever Yahoo omits annualOperatingCashFlow (it does for the whole "
           "IDX universe).",
    strict=True,
)
def test_piotroski_annual_derives_cfo_from_fcf_and_capex():
    """CFO must be reconstructable from FCF and capex on the annual basis.

    `build_core` already derives FCF as CFO + capex; the inverse identity
    CFO = FCF - capex is equally available and is exactly what the annual
    F-Score needs. Yahoo returns no `annualOperatingCashFlow` for any IDX name
    in the current output, so two of nine signals are blank for every ticker in
    the universe -- half the three-blank budget spent on missing plumbing, and
    a systematic ~2-point drag on a score that gates BUY at 3.
    """
    annual = {
        "TotalRevenue": [400, 600],
        "GrossProfit": [120, 240],
        "NetIncome": [40, 100],
        "FreeCashFlow": [20, 60],
        "CapitalExpenditure": [-40, -100],  # CFO = 60 - (-100) = 160
        "TotalAssets": [900, 1000],
    }
    _, signals = M.piotroski_f_score(make_bundle(annual=annual))
    assert signals["cfo_positive"] == 1
    assert signals["accruals"] == 1  # CFO 160 > NI 100


# ==================================================================== Altman


def test_altman_z_matches_hand_computation():
    """Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4 against known inputs.

    The absolute level matters because 1.1 and 2.6 are hard distress/safe
    boundaries used by `score_safety`; a mis-weighted term moves names across
    them.
    """
    core = M.CoreFinancials(
        ticker="T",
        total_assets=1000.0,
        working_capital=200.0,      # X1 = 0.20
        retained_earnings=300.0,    # X2 = 0.30
        ebit_ttm=150.0,             # X3 = 0.15
        total_equity=400.0,
        total_liabilities=600.0,    # X4 = 0.6667
    )
    # 6.56*0.20 + 3.26*0.30 + 6.72*0.15 + 1.05*(400/600)
    # = 1.312 + 0.978 + 1.008 + 0.700 = 3.998
    assert M.altman_z_modified(core) == pytest.approx(3.998, abs=1e-3)


@pytest.mark.parametrize("assets", [0.0, None])
def test_altman_none_without_total_assets(assets):
    """Every term divides by total assets, so a missing denominator is fatal."""
    core = M.CoreFinancials(ticker="T", total_assets=assets, working_capital=1.0,
                            ebit_ttm=1.0, retained_earnings=1.0)
    assert M.altman_z_modified(core) is None


def test_altman_none_when_working_capital_or_ebit_missing():
    """X1 and X3 are load-bearing; missing either must blank the whole score.

    Unlike X2 and X4 (which default to zero), these two carry the liquidity and
    earnings-power content -- a Z'' without them is not a Z''.
    """
    base = dict(total_assets=1000.0, retained_earnings=100.0, total_equity=500.0,
                total_liabilities=500.0)
    assert M.altman_z_modified(M.CoreFinancials("T", ebit_ttm=100.0, **base)) is None
    assert M.altman_z_modified(M.CoreFinancials("T", working_capital=100.0, **base)) is None


@pytest.mark.xfail(
    reason="DEFECT: X4 (equity/liabilities) is unbounded and collapses to 0.0 when "
           "total liabilities are zero, so a debt-free balance sheet scores *worse* "
           "than one with a token liability.",
    strict=True,
)
def test_altman_debt_free_company_is_not_penalised():
    """A company with no liabilities must not score below one with 1 unit of them.

    Zero liabilities makes X4 = equity/0, which `safe_div` blanks and the
    formula then reads as 0.0 -- the value it would take for a company with no
    equity at all. The same unbounded term gives Z'' = 1055 for one unit of
    liabilities, so the reported "Altman Z" column is meaningless at both ends
    of the range.
    """
    common = dict(total_assets=1000.0, working_capital=500.0, retained_earnings=400.0,
                  ebit_ttm=200.0, total_equity=1000.0)
    debt_free = M.altman_z_modified(M.CoreFinancials("T", total_liabilities=0.0, **common))
    token_liability = M.altman_z_modified(M.CoreFinancials("T", total_liabilities=1.0, **common))
    assert debt_free is not None
    assert debt_free >= token_liability


# =========================================================== returns on capital


def _returns_core():
    """Shared core: EBIT 200, 22% effective tax, IC not reported by Yahoo."""
    return M.CoreFinancials(
        ticker="T",
        ebit_ttm=200.0,
        tax_ttm=44.0,
        pretax_ttm=200.0,
        total_assets=1000.0,
        current_assets=400.0,
        current_liabilities=150.0,
        cash=100.0,
        total_equity=600.0,
        total_debt=200.0,
    )


def test_roic_uses_nopat_over_invested_capital():
    """ROIC = EBIT*(1-t) / (equity + debt - cash) when invested capital is absent."""
    core = _returns_core()
    # NOPAT = 200 * (1 - 0.22) = 156 ; capital = 600 + 200 - 100 = 700
    assert M.return_on_invested_capital(core) == pytest.approx(156 / 700)


def test_greenblatt_roc_uses_working_capital_plus_fixed_assets():
    """Greenblatt ROC = EBIT / (net working capital + net fixed assets), pre-tax.

    Not NOPAT, not total capital: the Magic Formula deliberately excludes excess
    cash and taxes so the ranking reflects operating economics rather than
    capital structure or a one-off tax rate.
    """
    core = _returns_core()
    # NWC = max(0, (400 - 100 cash) - 150) = 150 ; net fixed = 1000 - 400 = 600
    # 200 / 750 = 0.26667
    assert M.return_on_capital_greenblatt(core) == pytest.approx(200 / 750)


def test_greenblatt_roc_and_roic_are_genuinely_different_formulas():
    """The two return metrics must not converge or fall back to one another.

    The original workbook substituted ROIC for Greenblatt ROC, which silently
    changes the Magic Formula ranking. If these ever produce the same number for
    a normal balance sheet, one has been aliased to the other.
    """
    core = _returns_core()
    roic = M.return_on_invested_capital(core)
    roc = M.return_on_capital_greenblatt(core)
    assert roic is not None and roc is not None
    assert roc != pytest.approx(roic, rel=1e-6)
    assert roc > roic  # pre-tax numerator over a smaller, operating-only base


def test_roic_none_without_ebit_and_roc_none_without_assets():
    """Neither metric may substitute the other's inputs when its own are missing."""
    core = _returns_core()
    core.ebit_ttm = None
    assert M.return_on_invested_capital(core) is None
    assert M.return_on_capital_greenblatt(core) is None

    core = _returns_core()
    core.total_assets = None
    # ROIC does not need total assets and must still compute.
    assert M.return_on_invested_capital(core) is not None
    # Greenblatt needs fixed assets and must not silently borrow ROIC's base.
    assert M.return_on_capital_greenblatt(core) is None


def test_roic_rejects_an_implausible_effective_tax_rate():
    """A loss-making year's effective rate must not be trusted.

    Tax 100 on a pre-tax loss of -50 implies a -200% rate, which would turn
    NOPAT into 3x EBIT. The statutory 22% is used instead.
    """
    core = _returns_core()
    core.tax_ttm, core.pretax_ttm = 100.0, -50.0
    assert M.return_on_invested_capital(core) == pytest.approx(200 * 0.78 / 700)


def test_roic_none_when_invested_capital_non_positive():
    """Negative capital employed produces a sign-flipped return; blank it."""
    core = _returns_core()
    core.total_equity, core.total_debt, core.cash = 50.0, 0.0, 500.0  # -450
    assert M.return_on_invested_capital(core) is None


# ========================================================== Greenblatt yield


def test_earnings_yield_is_ebit_over_enterprise_value():
    """EBIT/EV, not E/P: the Magic Formula's capital-structure-neutral yield."""
    assert M.earnings_yield_greenblatt(200.0, 1000.0) == pytest.approx(0.20)


@pytest.mark.parametrize("ev", [0.0, -500.0, None])
def test_earnings_yield_none_for_non_positive_enterprise_value(ev):
    """A net-cash company can show a negative EV; the yield is then meaningless.

    Dividing EBIT by a negative EV yields a large *negative* yield for what is
    in fact an unusually cheap balance sheet -- exactly backwards.
    """
    assert M.earnings_yield_greenblatt(200.0, ev) is None


def test_earnings_yield_none_without_ebit():
    """Missing EBIT must blank the yield rather than read as a zero yield."""
    assert M.earnings_yield_greenblatt(None, 1000.0) is None


# ======================================================================= NCAV


def test_ncav_uses_total_liabilities_not_current_liabilities():
    """Graham's NCAV nets out *all* liabilities, including long-term debt.

    A company with IDR 1,000 of current assets, 200 of current liabilities and
    800 of total liabilities has NCAV of 200, not 800. Using current liabilities
    alone would report a 4x-too-generous liquidation value for every leveraged
    name and manufacture net-nets out of thin air.
    """
    core = M.CoreFinancials(
        ticker="T",
        current_assets=1000.0,
        current_liabilities=200.0,
        total_liabilities=800.0,
    )
    # (1000 - 800) / 10 = 20.0 ; the current-liabilities reading would be 80.0
    assert M.ncav_per_share(core, 10.0) == pytest.approx(20.0)
    assert M.ncav_per_share(core, 10.0) != pytest.approx(80.0)


def test_ncav_can_be_negative_and_is_reported_as_such():
    """A negative NCAV is information, not an error, and must survive.

    Clamping it at zero would make every over-levered company look like it had
    exactly zero asset protection rather than negative.
    """
    core = M.CoreFinancials(ticker="T", current_assets=100.0, total_liabilities=500.0)
    assert M.ncav_per_share(core, 10.0) == pytest.approx(-40.0)


@pytest.mark.parametrize(
    "current_assets, total_liabilities, shares",
    [(None, 100.0, 10.0), (100.0, None, 10.0), (100.0, 50.0, 0.0), (100.0, 50.0, None)],
)
def test_ncav_none_on_missing_inputs(current_assets, total_liabilities, shares):
    """Any missing leg means no NCAV; zero shares must not raise."""
    core = M.CoreFinancials(ticker="T", current_assets=current_assets,
                            total_liabilities=total_liabilities)
    assert M.ncav_per_share(core, shares) is None


# ======================================================================== DCF


def test_dcf_two_stage_present_value_hand_checked():
    """Two-stage FCFF DCF against a fully hand-computed example.

    FCF 100, 5% stage-1 growth for 5 years, 10% WACC, 2% terminal growth:
      CF1..CF5 = 105, 110.25, 115.7625, 121.550625, 127.62815625
      PV(CF)   = 95.4545 + 91.1157 + 86.9737 + 83.0245 + 79.2416 = 435.810
      TV       = 127.62815625 * 1.02 / (0.10 - 0.02) = 1627.259
      PV(TV)   = 1627.259 / 1.10**5 = 1010.401
      Equity   = 1446.211 - 0 net debt ; / 10 shares = 144.62
    """
    value = M.dcf_per_share(100.0, 10.0, 0.0, 0.10, 0.05, 0.02)
    assert value == pytest.approx(144.6212, abs=1e-3)


def test_dcf_subtracts_net_debt_from_enterprise_value():
    """Net debt must reduce equity value one-for-one."""
    no_debt = M.dcf_per_share(100.0, 10.0, 0.0, 0.10, 0.05, 0.02)
    with_debt = M.dcf_per_share(100.0, 10.0, 446.212, 0.10, 0.05, 0.02)
    assert with_debt == pytest.approx(no_debt - 44.6212, abs=1e-3)


@pytest.mark.parametrize("wacc, terminal", [(0.02, 0.02), (0.02, 0.05), (0.0, -0.01)])
def test_dcf_none_when_wacc_does_not_exceed_terminal_growth(wacc, terminal):
    """The Gordon guard: WACC <= g makes the terminal value infinite or negative.

    Without it the terminal denominator is zero or negative and the intrinsic
    value comes back as inf or a large *negative* number, which then propagates
    into MOS as a spuriously attractive figure. This is the failure mode that
    puts a distressed name at the top of a screen.
    """
    assert M.dcf_per_share(100.0, 10.0, 0.0, wacc, 0.05, terminal) is None


@pytest.mark.parametrize("fcf", [0.0, -50.0, None])
def test_dcf_none_for_non_positive_base_fcf(fcf):
    """Compounding a negative cash flow produces a confidently negative valuation.

    A cash-burning company has no DCF value; the honest output is a blank, which
    routes it to SKIP via "no usable intrinsic value" rather than to a fake
    negative intrinsic value.
    """
    assert M.dcf_per_share(fcf, 10.0, 0.0, 0.10, 0.05, 0.02) is None


@pytest.mark.parametrize("shares", [0.0, -10.0, None])
def test_dcf_none_for_invalid_share_count(shares):
    """Per-share output needs a positive share count."""
    assert M.dcf_per_share(100.0, shares, 0.0, 0.10, 0.05, 0.02) is None


def test_dcf_none_when_net_debt_exceeds_enterprise_value():
    """Negative equity value must be blank, not a negative price target."""
    assert M.dcf_per_share(100.0, 10.0, 1_000_000.0, 0.10, 0.05, 0.02) is None


# ======================================================== DDM and cost of equity


def test_ddm_gordon_growth():
    """DDM = D0*(1+g)/(COE - g); 100 * 1.03 / 0.07 = 1471.43."""
    assert M.ddm_per_share(100.0, 0.10, 0.03) == pytest.approx(103 / 0.07)


@pytest.mark.parametrize("dividend", [0.0, -10.0, None])
def test_ddm_none_for_non_payers(dividend):
    """A non-payer has no dividend-discount value; that is not a zero value."""
    assert M.ddm_per_share(dividend, 0.10, 0.03) is None


@pytest.mark.parametrize("coe, growth_rate", [(0.03, 0.10), (0.10, 0.10)])
def test_ddm_none_when_growth_meets_or_exceeds_cost_of_equity(coe, growth_rate):
    """Same Gordon guard as the DCF: the denominator must be strictly positive."""
    assert M.ddm_per_share(100.0, coe, growth_rate) is None


@pytest.mark.parametrize("beta", [0.168, 0.0, 0.49, 2.51, 5.0, None, -1.2])
def test_capm_falls_back_to_beta_one_outside_the_credibility_band(beta):
    """Beta outside [0.5, 2.5] must be replaced by 1.0, not used as reported.

    Yahoo reports beta 0.168 for BBRI. Accepted literally that drives the cost
    of equity to the floor, and because `justified_pb_value` divides by
    (COE - g), it inflates a bank's fair value toward the 4x book cap. The band
    is the defence against a single bad third-party field re-rating a whole
    sector.
    """
    unbanded = M.cost_of_equity_capm(0.065, 0.06, beta, 0.0)
    reference = M.cost_of_equity_capm(0.065, 0.06, 1.0, 0.0)
    assert unbanded == pytest.approx(reference)


@pytest.mark.parametrize("beta", [0.5, 1.5, 2.5])
def test_capm_trusts_beta_inside_the_band(beta):
    """Inside [0.5, 2.5] the reported beta must actually be used."""
    # 0.065 + beta * 0.06, below the 0.22 ceiling and above the 0.095 floor
    expected = max(0.065 + beta * 0.06, 0.095)
    assert M.cost_of_equity_capm(0.065, 0.06, beta, 0.0) == pytest.approx(expected)


def test_capm_floor_is_risk_free_plus_300bps():
    """No equity may be discounted at less than government debt plus 300bps.

    A regression that says otherwise is describing a data artefact, not a real
    financing cost, and a too-low discount rate inflates every valuation lens
    simultaneously.
    """
    # ERP of 0.001 would give 0.065 + 0.001 = 0.066; the floor lifts it to 0.095.
    assert M.cost_of_equity_capm(0.065, 0.001, 1.0, 0.0) == pytest.approx(0.095)
    assert M.cost_of_equity_capm(0.065, 0.001, 1.0, 0.0, floor=0.12) == pytest.approx(0.12)


def test_capm_ceiling_holds_at_22_percent():
    """The 22% ceiling caps the leverage add-on and a high beta together.

    Above ~22% the DCF terminal value collapses toward zero and every name looks
    expensive for reasons that are about the discount rate, not the business.
    """
    assert M.cost_of_equity_capm(0.10, 0.10, 2.4, 1.0) == pytest.approx(0.22)
    assert M.cost_of_equity_capm(0.15, 0.15, 2.5, 1.0) == pytest.approx(0.22)


def test_capm_leverage_add_on_is_bounded():
    """The net-debt/equity add-on contributes at most 300bps and never negative.

    Otherwise a net-cash company would be handed a *discount* to its cost of
    equity and a wildly levered one an unbounded premium.
    """
    no_leverage = M.cost_of_equity_capm(0.065, 0.06, 1.0, 0.0)
    net_cash = M.cost_of_equity_capm(0.065, 0.06, 1.0, -5.0)
    max_leverage = M.cost_of_equity_capm(0.065, 0.06, 1.0, 10.0)
    assert net_cash == pytest.approx(no_leverage)
    assert max_leverage == pytest.approx(no_leverage + 0.03)


# ============================================================== justified P/B


def test_justified_pb_matches_the_residual_income_identity():
    """Value = BVPS * (ROE - g) / (COE - g), the standard lender valuation.

    BVPS 1000, ROE 15%, COE 11%, g 3% -> 1000 * 0.12/0.08 = 1500.
    """
    assert M.justified_pb_value(1000.0, 0.15, 0.11, 0.03) == pytest.approx(1500.0)


def test_justified_pb_caps_the_multiple_at_four_times_book():
    """No bank is worth more than 4x book on this model, whatever the inputs.

    Uncapped, ROE 40% against an 9% COE and 2% growth implies 5.4x book; the cap
    is what stops a single strong year capitalising into an absurd target.
    """
    # roe capped at 0.40; g = min(0.02, 0.09-0.04, 0.24) = 0.02
    # multiple = (0.40 - 0.02) / 0.07 = 5.43 -> capped to 4.0
    assert M.justified_pb_value(1000.0, 0.60, 0.09, 0.02) == pytest.approx(4000.0)


def test_justified_pb_caps_roe_at_forty_percent():
    """Sustained ROE above 40% is treated as unsustainable and clipped."""
    high = M.justified_pb_value(1000.0, 0.40, 0.20, 0.0)
    absurd = M.justified_pb_value(1000.0, 2.00, 0.20, 0.0)
    assert high == absurd


@pytest.mark.parametrize("bvps", [0.0, -500.0, None])
def test_justified_pb_none_for_non_positive_book_value(bvps):
    """Negative book value has no justified multiple -- the model does not apply."""
    assert M.justified_pb_value(bvps, 0.15, 0.11, 0.03) is None


def test_justified_pb_none_for_negative_roe():
    """A loss-making lender cannot be valued on residual income.

    (ROE - g) is negative, so the multiple is negative and the only honest
    output is a blank rather than a negative price target.
    """
    assert M.justified_pb_value(1000.0, -0.05, 0.12, 0.03) is None


@pytest.mark.parametrize("coe", [0.0, -0.05])
def test_justified_pb_none_for_non_positive_cost_of_equity(coe):
    assert M.justified_pb_value(1000.0, 0.15, coe, 0.03) is None


@pytest.mark.xfail(
    reason="DEFECT: the 400bp minimum-spread guard is unreachable. `growth_capped` is "
           "already min(growth, coe - 0.04, ...), so `spread < minimum_spread` can "
           "never be true and an input with g >= COE is silently revalued at the "
           "maximum-spread assumption instead of being rejected.",
    strict=True,
)
def test_justified_pb_rejects_growth_at_or_above_the_cost_of_equity():
    """Growth above the cost of equity must blank the valuation, not be clamped.

    Assumed growth of 50% against an 11% cost of equity is not a valuation the
    model can express -- the Gordon form diverges. Clamping g down to COE-4%
    turns an obviously broken input into a confident 3.5x book, and nothing
    downstream can tell that the growth input was discarded.
    """
    assert M.justified_pb_value(1000.0, 0.20, 0.10, 0.50) is None
    assert M.justified_pb_value(1000.0, 0.20, 0.10, 0.10) is None


# ============================================================== comparables


def test_comparables_rejects_a_degenerate_lens_and_medians_the_survivors():
    """An order-of-magnitude outlier must be dropped before the median is taken.

    This is the ADRO/ITMG failure: a levered cyclical's `EBIT * multiple - net
    debt` lands just above zero, giving an implied price of IDR 0.33 against a
    IDR 2,540 stock. Taking the minimum -- or a plain median of two lenses --
    lets that one number produce a -769,000% margin of safety.
    """
    value = M.comparables_value(
        eps_ttm=300.0, peer_pe=10.0,           # lens 1: 3000
        ebit_ttm=1.0, peer_ev_ebit=1.0,        # lens 2: (1 - 0)/10 = 0.1  <- degenerate
        net_debt=0.0, shares=10.0,
        book_value_per_share=1600.0, peer_pb=2.0,  # lens 3: 3200
    )
    # median([0.1, 3000, 3200]) = 3000 ; keep [300, 30000] -> [3000, 3200] -> 3100
    assert value == pytest.approx(3100.0)


def test_comparables_single_lens_is_returned_unmodified():
    """One usable lens is returned as-is; outlier rejection needs a peer group."""
    assert M.comparables_value(300.0, 10.0, None, None, 0.0, 10.0) == pytest.approx(3000.0)


def test_comparables_returns_none_when_no_lens_applies():
    """Loss-making with negative book must be blank, never a negative price.

    Every lens is skipped rather than zeroed, so a blended valuation is not
    dragged down by a lens that does not apply to the business.
    """
    assert M.comparables_value(-50.0, 10.0, -200.0, 8.0, 0.0, 10.0,
                               book_value_per_share=-100.0, peer_pb=2.0) is None
    assert M.comparables_value(300.0, None, 200.0, None, 0.0, 10.0) is None


def test_comparables_skips_the_ev_lens_when_net_debt_swamps_enterprise_value():
    """A negative implied equity value must not enter the candidate set at all."""
    value = M.comparables_value(
        eps_ttm=300.0, peer_pe=10.0,
        ebit_ttm=100.0, peer_ev_ebit=5.0, net_debt=10_000.0, shares=10.0,
    )
    assert value == pytest.approx(3000.0)  # only the P/E lens survives


def test_comparables_median_of_two_close_lenses():
    """Two sane lenses average, confirming the median is not a min in disguise."""
    value = M.comparables_value(300.0, 10.0, None, None, 0.0, 10.0,
                                book_value_per_share=2000.0, peer_pb=2.0)
    assert value == pytest.approx(3500.0)  # median([3000, 4000])


# =========================================================== normalised EBIT


def test_normalised_ebit_is_the_median_not_the_mean():
    """Mid-cycle EBIT must be the median of the annual series.

    Given [100, 20, 15, 10] the median is (15 + 20)/2 = 17.5; the mean is 36.25.
    The mean is dominated by the single supercycle year -- ITMG's 2022 EBIT was
    5x its 2025 figure -- and would set "earnings power" at a level the company
    has reached exactly once.
    """
    bundle = make_bundle(annual={"EBIT": [100, 20, 15, 10]})
    assert M.normalised_ebit(bundle) == pytest.approx(17.5)
    assert M.normalised_ebit(bundle) != pytest.approx(36.25)


def test_normalised_ebit_window_is_limited_to_the_requested_years():
    """Only the last `years` fiscal years enter the median.

    A ten-year window on an IDX name spans two entirely different businesses;
    the point of normalisation is one cycle, not the whole listing history.
    """
    bundle = make_bundle(annual={"EBIT": [1000, 2000, 100, 20, 15, 10]})
    # last 4 of the series = [100, 20, 15, 10] -> 17.5
    assert M.normalised_ebit(bundle, years=4) == pytest.approx(17.5)


def test_normalised_ebit_falls_back_to_operating_income():
    """Yahoo omits EBIT for many IDX filers; OperatingIncome is the same line."""
    bundle = make_bundle(annual={"OperatingIncome": [100, 20, 15, 10]})
    assert M.normalised_ebit(bundle) == pytest.approx(17.5)


def test_normalised_ebit_falls_back_to_rolling_ttm_windows():
    """With a single annual point the quarterly history must carry the median.

    Otherwise every recently listed name loses its EPV lens entirely.
    """
    bundle = make_bundle(
        quarterly={"EBIT": [10, 10, 10, 10, 30, 30, 30, 30]},
        annual={"EBIT": [40]},
    )
    # windows: TTM now = 120, TTM offset 4 = 40 -> median = 80
    assert M.normalised_ebit(bundle) == pytest.approx(80.0)


def test_normalised_ebit_none_without_any_history():
    assert M.normalised_ebit(make_bundle()) is None


# ================================================================ EPV / staleness


def test_epv_uses_normalised_ebit_when_the_pipeline_attaches_it():
    """EPV must value mid-cycle earnings power, not the current cycle position.

    The pipeline attaches `_normalised_ebit` to the core; if EPV ignored it the
    metric would collapse into "TTM EBIT capitalised", which is just a re-priced
    snapshot wearing an intrinsic-value label.
    """
    core = M.CoreFinancials(ticker="T", ebit_ttm=1000.0, total_debt=0.0, cash=0.0)
    core._normalised_ebit = 200.0  # type: ignore[attr-defined]
    # 200 * 0.78 / 0.10 = 1560 enterprise ; no net debt ; / 10 shares = 156
    assert M.epv_per_share(core, 10.0, 0.10) == pytest.approx(156.0)


def test_epv_none_when_net_debt_exceeds_earnings_power():
    """Negative equity value is a blank, not a negative per-share number."""
    core = M.CoreFinancials(ticker="T", ebit_ttm=100.0, total_debt=1_000_000.0, cash=0.0)
    assert M.epv_per_share(core, 10.0, 0.10) is None


@pytest.mark.parametrize(
    "as_of, expected",
    [
        ("2026-03-31", 0.0),    # same day as the reference date
        ("2025-12-31", 0.99),   # 90 days / 91.31
        ("2025-09-30", 2.0),    # 182 / 91.31 = 1.993 -> 1.99
        ("2025-03-31", 4.0),    # 365 / 91.31 = 3.997 -> 4.0
    ],
)
def test_quarters_stale_arithmetic_against_a_fixed_reference(as_of, expected):
    """Staleness must be measured in quarters against an explicit reference date.

    The 3-quarter cut-off in `classify` turns this number into a hard SKIP, so
    the arithmetic has to be exact -- and the test must pass `today` explicitly
    or it silently changes meaning every day it runs.
    """
    assert M.quarters_stale(as_of, TODAY) == pytest.approx(expected, abs=0.02)


def test_quarters_stale_none_for_missing_or_malformed_dates():
    """An unparseable filing date must be None, never treated as "fresh".

    Returning 0 for a broken date would let a name with no known filing pass the
    staleness gate.
    """
    assert M.quarters_stale(None, TODAY) is None
    assert M.quarters_stale("", TODAY) is None
    assert M.quarters_stale("not-a-date", TODAY) is None
    assert M.quarters_stale("2025-13-45", TODAY) is None


def test_days_between_and_malformed_input():
    """Date arithmetic helper: correct span, None on junk."""
    assert M.days_between("2026-03-31", "2025-03-31") == 365
    assert M.days_between("2026-03-31", None) is None
    assert M.days_between("junk", "2025-03-31") is None


# ==================================================================== build_core


def test_build_core_derives_free_cash_flow_from_cfo_plus_capex():
    """Capex arrives negative, so FCF = CFO + capex reconstructs the missing line."""
    bundle = make_bundle(
        quarterly={
            "OperatingCashFlow": [100, 100, 100, 100],
            "CapitalExpenditure": [-30, -30, -30, -30],
        }
    )
    core = M.build_core("T", bundle)
    assert core.fcf_ttm == pytest.approx(400 - 120)


def test_build_core_prefers_the_reported_free_cash_flow_line():
    """A reported FCF line wins over the derived one."""
    bundle = make_bundle(
        quarterly={
            "FreeCashFlow": [50, 50, 50, 50],
            "OperatingCashFlow": [100, 100, 100, 100],
            "CapitalExpenditure": [-30, -30, -30, -30],
        }
    )
    assert M.build_core("T", bundle).fcf_ttm == pytest.approx(200.0)


def test_build_core_falls_back_from_ebit_to_operating_income():
    """Yahoo omits EBIT for many IDX filers; the fallback keeps EV/EBIT alive."""
    bundle = make_bundle(quarterly={"OperatingIncome": [25, 25, 25, 25]})
    assert M.build_core("T", bundle).ebit_ttm == pytest.approx(100.0)


def test_build_core_derives_equity_and_working_capital():
    """Balance-sheet identities fill the gaps Yahoo leaves.

    Equity = assets - liabilities and WC = CA - CL are definitional, so deriving
    them is safe; the alternative is blanking Altman Z and the safety score for
    any filer with a patchy balance sheet.
    """
    bundle = make_bundle(
        quarterly={
            "TotalAssets": [1000],
            "TotalLiabilitiesNetMinorityInterest": [600],
            "CurrentAssets": [400],
            "CurrentLiabilities": [150],
        }
    )
    core = M.build_core("T", bundle)
    assert core.total_equity == pytest.approx(400.0)
    assert core.working_capital == pytest.approx(250.0)


def test_build_core_stock_items_take_the_latest_quarter_not_a_sum():
    """Balance-sheet items must never be summed across quarters.

    Summing four quarters of total assets would quadruple the denominator of
    ROA, asset turnover and every Altman term.
    """
    bundle = make_bundle(quarterly={"TotalAssets": [700, 800, 900, 1000]})
    assert M.build_core("T", bundle).total_assets == pytest.approx(1000.0)


def test_build_core_as_of_prefers_the_balance_sheet_date():
    """Staleness is measured from the balance sheet, with revenue as a fallback."""
    bundle = make_bundle(quarterly={"TotalAssets": [1, 2], "TotalRevenue": [1, 2, 3]})
    assert M.build_core("T", bundle).as_of == "2025-12-31"
    revenue_only = make_bundle(quarterly={"TotalRevenue": [1, 2, 3]})
    assert M.build_core("T", revenue_only).as_of == "2025-12-31"


def test_build_core_on_an_empty_bundle_is_all_none():
    """A ticker Yahoo knows nothing about must produce blanks, never zeros.

    Zeros would place it in the same bucket as a genuinely unprofitable company
    and let it be scored rather than excluded.
    """
    core = M.build_core("T", make_bundle())
    assert core.ticker == "T"
    numeric = {k: v for k, v in core.__dict__.items() if k not in {"ticker", "as_of"}}
    assert all(value is None for value in numeric.values()), numeric


# ====================================================================== median


@pytest.mark.parametrize(
    "values, expected",
    [([1], 1), ([1, 2], 1.5), ([3, 1, 2], 2), ([4, 1, 3, 2], 2.5), ([], None)],
)
def test_median_helper(values, expected):
    """The median helper must sort first and average the middle pair when even."""
    assert M.median(values) == expected


def test_median_ignores_none_entries():
    """A missing lens must not shift the centre of the surviving ones."""
    assert M.median([10.0, None, 20.0, 30.0]) == 20.0
