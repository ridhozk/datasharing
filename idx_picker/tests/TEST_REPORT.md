# idx_picker metric library — test report

**Suite:** `idx_picker/tests/` · plain pytest · no network, no fixtures pulled from disk
except the integration module.

**Run:** `cd /home/user/datasharing && python3 -m pytest idx_picker/tests -q`

**Result:** `216 passed, 7 xfailed, 0 failed` — every xfail is a genuine defect in the
library, documented below. There are no failures caused by the tests themselves.

| Module | Tests | Passing | xfail (defects) |
|---|---|---|---|
| `test_metrics.py` | 130 | 127 | 3 |
| `test_scoring.py` | 64 | 61 | 3 |
| `test_pipeline_integration.py` | 29 | 28 | 1 |
| **Total** | **223** | **216** | **7** |

Counts include parametrised cases as separate tests. `conftest.py` carries the
`make_bundle` / `make_series` helpers and the CSV loaders; it contains no tests.

All xfails are `strict=True` except the integration one, so the suite turns red the
moment a defect is fixed without the test being updated — the defects cannot rot into
silently accepted behaviour.

---

## 1. Defects found, ranked by severity

### D1 — HIGH: annual F-Score can never evaluate CFO, so two of nine signals are blank for the entire universe

* **Where:** `metrics._piotroski_annual` (the `annual("OperatingCashFlow")` lookups).
* **Failing test:** `test_metrics.py::test_piotroski_annual_derives_cfo_from_fcf_and_capex`
  and the downstream consequence test
  `test_pipeline_integration.py::test_no_row_is_demoted_by_an_f_score_built_on_blank_signals`.
* **Input:** an annual bundle carrying `FreeCashFlow` and `CapitalExpenditure` but no
  `OperatingCashFlow` — which is exactly what Yahoo returns for every IDX name
  (`RAW_history_annual.csv` has an empty `OperatingCashFlow` column on all 50 rows while
  `FreeCashFlow` and `CapitalExpenditure` are populated).
* **Expected:** `cfo_positive` and `accruals` evaluate, via the identity
  `CFO = FCF − capex` (capex arrives negative). `build_core` already runs this identity
  in the opposite direction (`fcf = cfo + capex`), so the data and the convention are
  both already in hand.
* **Actual:** both signals are `None`. Observed in the current output:
  `F: CFO Positive` and `F: Accruals` are blank for 9 of 12 tickers, and **all 12 tickers
  run on the annual basis** — the TTM basis the docstring prefers is never reached,
  because Yahoo's free quarterly feed carries 5–6 quarters, not 8.
* **Why it matters:** `scoring.classify` sends any name with `F-Score <= 3` to WATCH.
  Two structurally unevaluable signals cap the achievable score at 7/9 and consume two
  of the three blanks `metrics._total` tolerates. On the current 12-ticker sample this
  is decisive for **ITMG**: MOS 63%, safety 87, quality 50, no red flags, F-Score 3 — a
  WATCH produced by a missing data line rather than by the business. ADRO (F=2) and
  PTBA (F=2) are in the same position. The gate is partly measuring Yahoo's coverage,
  not the company's fundamentals.

### D2 — HIGH: `classify` treats missing data as a passing grade, so a data-poor name can be promoted to BUY

* **Where:** `scoring.classify`, the four post-valuation gates.
* **Failing test:** `test_scoring.py::test_missing_quality_and_safety_data_must_not_produce_a_buy`
* **Input:** `Assessment(mos_base=0.80)` with `safety_score=None`, `quality_score=None`,
  `f_score=None`, `red_flags=[]`.
* **Expected:** `WATCH` — the docstring promises a BUY requires "a balance sheet that is
  not distressed" and "evidence of financial improvement", and blanks are neither.
* **Actual:** `BUY`, with the reason string "MOS 80%, quality and balance sheet both
  pass" — an affirmative claim about two things that were never measured.
* **Why it matters:** every gate is written `if x is not None and x < threshold`, so
  absence is indistinguishable from a pass. The universe is full of partial data (see
  D1: F-Score blanks are routine, and `score_safety` returns `None` outright when no
  balance-sheet line is computable). This is the single highest-conviction output of the
  whole system being reachable on a row where three of the four gates were never
  evaluated. The verdict text actively misleads.

### D3 — MEDIUM: the bull scenario can value a company *below* its own base case

* **Where:** `scoring.build_scenarios`, the bull spec `max(0.06, base_wacc - 0.01)`.
* **Failing test:** `test_scoring.py::test_bull_case_is_never_worse_than_the_base_case`
* **Input:** `base_wacc=0.05`, `base_terminal_growth=0.03`, `historical_growth=0.05`,
  FCF 1000, 100 shares, no net debt.
* **Expected:** bull WACC ≤ base WACC and bull IV ≥ base IV.
* **Actual:** bull WACC = `max(0.06, 0.04)` = **0.06 > 0.05**, giving IV bear 186.45,
  base 565.00, **bull 530.41** — the bull case is 6% *below* the base case.
* **Why it matters:** the 6% floor is applied against an absolute constant instead of
  against the base WACC, so it can invert the scenario ordering rather than bound it.
  `IV Bull` and `MOS Bull` are read as an upside bound; an inverted range is worse than
  no range because it looks authoritative. Triggers whenever `base_wacc < 0.06` —
  reachable through `cost_of_equity_capm`'s floor of risk-free + 300bps in any low-rate
  configuration, and through any explicit low-WACC setting.

### D4 — MEDIUM: the bear case is not pessimistic on growth for already-shrinking businesses

* **Where:** `scoring.build_scenarios`, `growth_base = max(-0.05, ...)` combined with the
  bear spec `max(-0.05, growth_base - 0.05)`.
* **Failing test:** `test_scoring.py::test_bear_growth_is_still_lower_when_the_base_is_already_at_the_floor`
* **Input:** `historical_growth=-0.30`.
* **Expected:** bear growth strictly below base growth.
* **Actual:** both clamp to `-0.05`; the bear case differs from the base only by the
  +200bp WACC add-on.
* **Why it matters:** the scenario band collapses for exactly the companies whose
  downside is most real — a business shrinking 30% a year is handed a bear case that
  assumes it shrinks only 5%. The stated contract ("the bear case is not merely lower
  growth") is silently unmet on one of its two levers.

### D5 — MEDIUM: `justified_pb_value`'s 400bp minimum-spread guard is unreachable dead code

* **Where:** `metrics.justified_pb_value`, lines computing `growth_capped` then testing
  `if spread < minimum_spread: return None`.
* **Failing test:** `test_metrics.py::test_justified_pb_rejects_growth_at_or_above_the_cost_of_equity`
* **Input:** `book_value_per_share=1000, roe=0.20, cost_of_equity=0.10, growth=0.50`.
* **Expected:** `None` — 50% perpetual growth against a 10% cost of equity is not a
  valuation the Gordon form can express.
* **Actual:** `3500.0` (3.5x book). `growth_capped = min(growth, coe - 0.04, roe*0.6)` is
  already bounded by `coe - 0.04`, so `spread` is **always** ≥ 0.04 and the guard can
  never fire. The absurd growth input is silently discarded and replaced with the
  maximum-spread assumption.
* **Why it matters:** the module documents a rejection and implements a clamp. Nothing
  downstream can tell that the growth input was thrown away, so a nonsensical input
  produces a confident-looking bank valuation instead of a blank. `justified_pb` is the
  EPV stand-in for every financial-sector name in `blended_intrinsic`, so it feeds MOS
  directly. Clamping may well be the *desired* behaviour — but then the dead branch
  should go, because as written the code claims a guard it does not have.

### D6 — LOW: `altman_z_modified`'s X4 term is unbounded and inverts at zero liabilities

* **Where:** `metrics.altman_z_modified`, `x4 = safe_div(total_equity, total_liabilities)`
  combined with `1.05 * (x4 or 0.0)`.
* **Failing test:** `test_metrics.py::test_altman_debt_free_company_is_not_penalised`
* **Input:** assets 1000, WC 500, RE 400, EBIT 200, equity 1000 — with total liabilities
  0.0 versus 1.0.
* **Expected:** the debt-free balance sheet scores at least as safe as the one carrying a
  token liability.
* **Actual:** liabilities 0.0 → **Z'' = 5.93** (X4 blanked by `safe_div`, then read as
  0.0 — the value a company with *no equity at all* would get); liabilities 1.0 →
  **Z'' = 1055.93**.
* **Why it matters:** two failure modes in one term. The `or 0.0` conflates "infinitely
  safe" with "insolvent", and the uncapped ratio lets Z'' run to four digits for any
  filer with a near-zero liabilities line. `score_safety` bands Altman at 2.6 so the
  scoring impact is muted, but the `Altman Z` column is published raw and is read
  against the documented 1.1 / 2.6 boundaries. Current output already shows Z = 10.5
  (AALI) and 6.8 (ADRO), well outside the range the score was calibrated on.

### D7 — LOW / documentation: Greenblatt ROC includes goodwill, which the docstring says it excludes

* **Not xfailed** — the arithmetic is pinned by
  `test_metrics.py::test_greenblatt_roc_uses_working_capital_plus_fixed_assets`, which
  passes.
* `return_on_capital_greenblatt` claims "Greenblatt excludes goodwill and excess cash on
  purpose". Excess cash *is* excluded (via `current_assets - cash`), but "net fixed
  assets" is computed as `total_assets - current_assets`, which includes goodwill and
  intangibles. The denominator is therefore overstated and ROC understated for any
  acquisitive name. Flagged for the owner to decide: fix the formula or fix the comment.

---

## 2. What is covered

### `metrics.py` (130 tests)

* **`ttm`** — exact 4-quarter sum; `None` at 3 quarters; `offset=4` prior-year window;
  `None` for every incomplete offset window (5, 8, 99); `None` for an absent field.
* **`growth`** — normal case; the **negative-base sign convention** (−100 → +50 gives
  **+1.5**, and −100 → −150 still gives −0.5); zero and `None` bases; `GROWTH_CAP`
  suppression with the boundary pinned at exactly 10.0 (10.0 kept, 10.01 rejected).
* **`cagr`** — compounding verified against `2**(1/3)-1` and `1.1**3`; `None` for every
  non-positive endpoint combination including both-negative; `None` for zero and
  negative years.
* **`safe_div`** — zero denominator, all `None` permutations, inf/−inf/NaN suppression,
  and the happy path including a zero numerator.
* **`piotroski_f_score`** — a hand-built **exact 9** and **exact 0** with the full
  breakdown dict asserted key by key; a **mixed 5** with each signal's arithmetic in a
  comment; TTM basis at ≥ 8 quarters and annual fallback at 7, asserted via `_basis`;
  the gate correctly also requires 8 quarters of *net income*, not just revenue; the
  ">3 unevaluable → `None`" rule and the exactly-3 boundary that still scores; the
  "no long-term debt reported = strongest leverage reading" rule.
* **`altman_z_modified`** — hand-computed Z'' = 3.998 from stated X1–X4; `None` for zero
  and missing assets; `None` when X1 or X3 is missing (X2/X4 default to zero by design);
  the debt-free inversion (D6).
* **`return_on_capital_greenblatt` vs `return_on_invested_capital`** — both formulas
  hand-computed (156/700 vs 200/750); asserted **genuinely different** and ordered as
  theory predicts; asserted that neither borrows the other's inputs when its own are
  missing (dropping `total_assets` blanks ROC but must not blank ROIC); implausible
  effective tax rate rejected in favour of the statutory 22%; `None` for negative
  invested capital.
* **`earnings_yield_greenblatt`** — EBIT/EV; `None` for zero, negative and missing EV;
  `None` for missing EBIT.
* **`ncav_per_share`** — a bundle where current liabilities (200) and total liabilities
  (800) differ, asserting the result is **20.0 (total) and explicitly not 80.0
  (current)**; negative NCAV preserved; `None` on every missing leg and on zero shares.
* **`dcf_per_share`** — full two-stage PV hand-computed to 144.6212 with all five
  discounted cash flows and the terminal value spelled out; net-debt subtraction;
  `None` for `wacc <= terminal_growth` (three variants); `None` for zero/negative/absent
  base FCF; `None` for invalid share counts; `None` when net debt exceeds EV.
* **`ddm_per_share` / `cost_of_equity_capm`** — Gordon DDM value and its guards; the
  **beta credibility band** verified at 0.168 (the real BBRI figure), 0.0, 0.49, 2.51,
  5.0, `None` and −1.2, each asserted to equal the beta-1.0 result; betas at 0.5, 1.5 and
  2.5 asserted to be *used*; the **risk-free + 300bps floor** and a custom floor; the
  **0.22 ceiling** from two directions; the leverage add-on bounded to [0, 300bps].
* **`justified_pb_value`** — residual-income identity (1500 from stated inputs); the
  **4.0x cap** binding; the 40% ROE clip; `None` for zero/negative/absent book value,
  negative ROE and non-positive cost of equity; the unreachable spread guard (D5).
* **`comparables_value`** — three lenses with one degenerate (0.3 against a median of
  3000): outlier rejected, **median of the survivors (3100)** returned; single lens
  returned unmodified; `None` when no lens applies; the EV lens skipped when net debt
  swamps enterprise value; two-lens median confirming it is not a min in disguise.
* **`normalised_ebit`** — `[100, 20, 15, 10]` → **17.5, asserted not 36.25**; the
  `years` window honoured; `OperatingIncome` fallback; rolling-TTM fallback for a
  single-year annual series; `None` with no history.
* **`epv_per_share`** — uses the pipeline-attached `_normalised_ebit` rather than TTM
  EBIT; `None` when net debt exceeds earnings power.
* **`quarters_stale`** — four fixed-reference cases (0, 0.99, 2.0, 4.0 quarters), `today`
  always passed explicitly; `None` for absent, empty, unparseable and impossible dates.
* **`build_core`** — FCF derived from CFO + capex and the reported line preferred over
  it; EBIT → OperatingIncome fallback; equity and working-capital identities; stock
  items taking the latest quarter rather than a sum; `as_of` preferring the balance
  sheet; an empty bundle producing **all `None` and no zeros**.
* **`median`** / **`days_between`** — odd, even, unsorted, empty, `None`-containing.

### `scoring.py` (64 tests)

* **`classify_business`** — financial sector wins over 30% ROIC and over a sub-NCAV
  price, across four sector spellings; sub-NCAV routes to Deep Value despite −30% ROIC;
  the compounder test parametrised over all seven combinations of high/low/exactly-at-
  threshold/unknown ROIC and CAGR, confirming **both** are required and both thresholds
  are strict; cyclical sector beats the compounder test.
* **`net_net_test`** — the 2/3 threshold at 13.32 / 13.3333 / 13.34 / 20.0 against an
  NCAV of 20.0; negative NCAV can never pass but is still reported; missing price or
  NCAV cannot pass.
* **`classify`** — the four BUY gates broken one at a time from a common passing
  baseline (safety 39, F-Score 3, quality 34, one red flag → each returns WATCH with the
  right reason); the exact boundaries (40 / 35 / 4) returning BUY; MOS below watch → SKIP;
  MOS between thresholds → WATCH; `mos_base=None` → SKIP; staleness > 3 quarters → SKIP
  even at 95% MOS, at exactly 3.0 → not skipped, and overriding the net-net branch;
  unknown staleness not blocking; net-net with safety 29 → WATCH with a going-concern
  reason, with safety 55 → DEEP VALUE, and the net-net branch correctly ignoring MOS and
  F-Score.
* **`blended_intrinsic`** — deep value anchoring on the **minimum** and refusing the DCF
  entirely; cyclical weights hand-computed (2450) against ordinary (3075) and asserted
  lower; financials excluding a 9,000,000 DCF and returning the comps/EPV mean;
  financials with only a DCF returning `None`; non-positive lenses dropped with weights
  renormalised; all-`None` inputs → `None` across all five business types.
* **`build_scenarios`** — bear lower on growth *and* higher on WACC *and* lower on
  terminal growth, bull the reverse; resulting IVs ordered bear < base < bull; MOS and
  upside using different denominators; normalised EBIT preferred over trailing FCF;
  historical growth clamped into [−5%, +15%]; all scenarios `None` for a cash-burning
  base; the two ordering defects (D3, D4).
* **`detect_red_flags`** — a clean baseline that fires nothing, then each flag tested on
  **both** sides of its trigger: earnings/cash divergence at 49 vs 51; six vs five
  negative FCF quarters; share count +16% vs +14%; net debt/EBITDA above 4x and its
  suppression for financials; gross margin −10pp vs −3pp over twelve quarters; interest
  coverage 1.33x vs 2.0x vs no interest expense at all; the peak/trough normalised-EBIT
  flags at 2.5x, 0.4x and 1.1x; an empty bundle not raising.
* **Score bands** — financials graded on ROE with gross margin skipped; `score_safety`
  returning `None` when nothing is computable (the input to D2); `_band` as a
  first-threshold-wins step function with an inclusive comparison and a floor.

### `test_pipeline_integration.py` (29 tests, against the real CSVs)

Every test skips cleanly via `conftest.load_csv` when a file is missing or has fewer
than 5 rows, and none depends on a ticker count or a ticker list.

* Verdict from the allowed set on every row; every verdict carries a reason.
* `MOS Blended` inside the clamped [−1, 1]; **MOS reconciles to `(IV − Price)/IV`** to
  1e-6 wherever both legs exist and IV > 0 (clamped rows exempted); `Upside` and `MOS`
  mutually consistent via `upside = mos/(1−mos)`; scenario IVs ordered bear ≤ base ≤ bull.
* `Net-Net Pass` = TRUE implies `Price < (2/3) × NCAV per Share` (warns when the sample
  contains no passes, so a vacuous run is visible); DEEP VALUE verdicts backed by the flag.
* Piotroski total an integer 0–9 or blank; the **nine `F:` columns sum to the total**;
  components binary or blank; the score agreeing between `RAW_scores.csv` and
  `RAW_key_statistics.csv`; per-signal blank coverage reported.
* Every `RAW_key_statistics.csv` ticker present in `RAW_scores.csv` and
  `RAW_idx_stocks.csv`; no duplicate tickers in any file.
* **Currency guard both ways**: no non-IDR filer with an FX rate of 1.0, and no IDR filer
  with a rate other than 1.0.
* Stale rows (> 3 quarters) actually carry SKIP.
* EBIT/EV and EV/EBIT reciprocal to 1e-6; Greenblatt ROC not aliased to ROIC across the
  file; five shared columns agreeing between the two output files.
* Reporting-only (warnings, never failures unless > 50% of rows are affected): PE outside
  [−1000, 1000], PB outside [0, 100], ROE outside [−10, 10]; verdict distribution;
  blended-IV coverage; F-Score signal blanks.

**Reported from the current 12-ticker sample** (all warnings, nothing failing):

* PE / PB / ROE band violations: **0 / 0 / 0**.
* Verdict distribution: `{WATCH: 6, SKIP: 5, BUY: 1}`.
* Blended IV missing for 1 of 12 rows (ABBA).
* F-Score signal blanks: `CFO Positive = 9/12`, `Accruals = 9/12`,
  `Current Ratio Improving = 3/12`, `Gross Margin Improving = 3/12`, rest 0 — see D1.
* No `Net-Net Pass` rows, so that rule's check is currently vacuous (warned).

---

## 3. What is NOT covered, and why

1. **`yahoo.py` — the HTTP client, cache, rate limiter and retry logic.** Out of scope
   (the brief is the metric library) and untestable without either a network or a mock
   HTTP layer that would test the mock more than the client. The consequence is that
   `STATEMENT_FIELDS` coverage gaps — the root cause of D1 — are invisible to unit tests
   and only surface in the integration module.
2. **`pipeline.py` end to end.** Not exercised directly: no test calls `run()`, builds a
   `Settings`, or drives the peer-group machinery. It is tested only through its
   *output* (the CSVs). Concretely uncovered: the ~956-ticker concurrency path, the cache
   TTL, `load_seeds`, `write_csv`, per-ticker failure handling, and the currency
   conversion *code* (only its result is asserted, via the FX-rate guard).
3. **`workbook/`.** Explicitly another agent's territory; not touched.
4. **Peer-group construction and the peer median columns.** The current sample has
   `Peer Count = 0` on every row, so peer PE / EV-EBIT / PB are blank and
   `comparables_value` is never exercised on real data. Its unit tests cover the maths;
   nothing covers how peers are selected. This is a real gap — `Comparables IV` is blank
   for all 12 tickers, so 1 of 3 valuation lenses is currently dead in production and no
   test would notice if it stayed that way.
5. **`score_quality` / `score_safety` / `score_value` band-by-band.** Only the routing
   decisions (ROE vs ROIC for financials, the skipped gross-margin term, the `None`
   result) and the `_band` primitive are pinned. The specific cut-offs are calibration
   choices, not contracts — pinning all ~25 of them would convert every future
   re-calibration into a test-editing exercise without catching real bugs.
6. **`composite` score weighting.** Computed in `pipeline.py`, not in the two modules
   under test.
7. **Currency conversion arithmetic itself.** No unit test converts a USD statement to
   IDR, because the conversion lives in `pipeline.py`. The integration test asserts only
   that non-IDR filers received a rate ≠ 1.0 — it cannot detect a rate applied to the
   wrong subset of columns, or applied twice.
8. **Property-based / fuzz testing.** Every test uses hand-chosen inputs. A Hypothesis
   pass over `safe_div`, `growth`, `dcf_per_share` and `build_scenarios` would likely
   find more ordering and guard defects of the D3/D4 family; it was not in scope here.
9. **Behaviour under a concurrent rewrite of the output CSVs.** The tests skip on a
   short file, but a file rewritten *between* two fixtures in the same session could in
   principle mix two runs. The fixtures are session-scoped, which narrows but does not
   eliminate the window.
10. **`Assessment.to_dict` / the scenario column flattening.** Trivial serialisation,
    covered indirectly by the CSV column assertions.
