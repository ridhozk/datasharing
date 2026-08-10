# Bug register → resolution map

Every finding in [`LOGIC_AUDIT.md`](./LOGIC_AUDIT.md) mapped to what the rebuilt
system does about it. Bug IDs are the audit's.

The audit's headline conclusion shaped the whole rebuild: **the model was not
primarily broken by its formulas — it was broken by the data feed underneath
them.** The old feed delivered every money column as an unsigned absolute value.
No amount of formula repair fixes that; the source had to change.

---

## Critical

### B-01 — Source feed strips the sign off every money column
*289 of 956 rows had a positive Net Income recorded for a company the same feed
priced at a negative P/E.*

**Resolved at the source.** Yahoo Finance returns signed values, verified
end-to-end: ABBA now reports a negative EBIT (−17.1bn normalised) and a negative
ROE (−1.04) consistently across every derived column, where the old feed showed
Net Income +6,000 mio against a P/E of −37.99.

The pipeline never takes an absolute value of a statement line. `metrics.py`
propagates sign throughout, and the integration tests assert that a company with
negative earnings carries a negative earnings yield rather than a positive one.

### B-02 — Net cash subtracted instead of added
*AALI holds 4,929,000 mio cash against 90,000 mio debt; the feed recorded "Net
Debt = +4,839,000" and the EPV formula subtracted it, turning a +19.6% upside
into a −45.9% margin of safety.*

**Resolved.** Net debt is computed as `total_debt − cash`, signed, in exactly one
place (`pipeline.fetch_one`), and every valuation consumes that single value.
AALI now shows net debt of −5,149,236 mio (negative = net cash) and an EPV that
adds the cash back. The current AALI verdict is BUY at a 29% margin of safety.

### B-03 — "Magic Formula Earnings Yield" was 1÷PE
*Identical to 1/PE on 853 of 897 rows. AALI: 0.0956 against the correct
1/4.65 = 0.2151.*

**Resolved.** `metrics.earnings_yield_greenblatt` computes `EBIT / Enterprise
Value`. AALI's now reads 0.299. The net-income-based figure is retained
separately as `Earnings Yield (TTM)` so both are visible and neither is
mislabelled.

### B-04 — "ROC" was vendor ROIC
*Identical to ROIC on 956 of 956 rows.*

**Resolved.** `metrics.return_on_capital_greenblatt` implements
`EBIT / (net working capital + net fixed assets)`, excluding excess cash and
goodwill as Greenblatt specifies. ROIC is computed independently in
`return_on_invested_capital` and reported alongside. A unit test asserts the two
are genuinely different formulas and that neither silently falls back to the
other.

### B-05 — EPV capitalised TTM EBIT at the cost of equity with a hardcoded tax rate
**Resolved on all three counts.**
- *Cycle-average earnings*: `normalised_ebit` uses the **median** of available
  annual EBIT. The median rather than the mean specifically because a four-year
  window containing one commodity supercycle is dominated by it — ITMG's 2022
  EBIT was 5x its 2025 figure, and the mean produced an earnings power the
  company has hit exactly once.
- *Discount rate*: EPV capitalises unlevered after-tax EBIT, so it takes a
  cost of capital, not a cost of equity.
- *Tax rate*: read from `Settings.tax_rate`, wired to the Setup sheet, with the
  effective rate used instead when it is credible (0–60%).

Where mid-cycle EBIT still exceeds trailing EBIT by more than 2x, a red flag
states that the valuation assumes a cycle recovery.

### B-06 — All six Setup parameters referenced by zero formulas
*Including their named ranges. The real drivers were literals buried in
formulas: `BJ1=0.07`, `BL1=0.12`, `0.22` inside `BZ4`.*

**Resolved.** `Settings` is the single source of these values in the pipeline,
and the rebuilt Setup sheet carries a column naming which sheets consume each
parameter. Terminal Growth, Risk Free Rate, MOS Buy and MOS Watch — which
previously appeared in no formula anywhere — now drive the scenario valuations
and the verdict thresholds.

### B-07 — `""` coerces to 0, manufacturing values
*BBCA's NCAV read −1,261,870,000 mio, exactly minus total liabilities, because
Current Assets was `""`. 290 blank comparables prices each displayed as a −100%
margin of safety.*

**Resolved structurally.** Every metric returns `None` rather than `0` or `""`
when it cannot be computed, and `None` never enters arithmetic — `safe_div`
returns `None` on a missing operand rather than propagating a zero. Blank
valuations produce a blank margin of safety and the verdict "No usable intrinsic
value", not a −100% one.

### B-08 — No classification engine, no DCF, no DEEP VALUE bucket
*`Shortlist?` was hand-typed on 48 of 956 rows.*

**Resolved.** `scoring.classify` produces BUY / WATCH / SKIP / DEEP VALUE for
every row, from a layered rule set rather than a weighted average.
`metrics.dcf_per_share` implements a two-stage FCFF DCF, run in bear, base and
bull cases with both growth and discount rate varying together.

### B-09 — No sector gate; banks run through EV/EBIT, EPV, NCAV and FCF
*122 financial rows, including BBNI showing a +137.8% comparables margin of
safety, and 13 financials inside the Magic Formula top 100.*

**Resolved.** `classify_business` routes financials to a separate track before
any other test. They are valued on justified P/B — `BVPS × (ROE − g) / (COE − g)`
— and comparables; the EV/EBIT, FCF and NCAV lenses are never applied to them.
Their quality score is graded on ROE rather than ROIC and their safety score on
the equity/assets ratio rather than net debt/EBITDA.

---

## High

### B-10 — All three "MOS" columns computed upside, not margin of safety
**Resolved.** `MOS = (IV − Price) / IV` and `Upside = IV / Price − 1` are
computed separately and both reported, for every scenario and for the blend.

### B-11 — Graham's 2/3 test absent; flag fired at Price < 1.0 × NCAV
*47 flagged, only 27 actually passed — 20 false positives.*

**Resolved.** `scoring.net_net_test` applies `Price < (2/3) × NCAV per share`.
An integration test re-derives the inequality for every row flagged TRUE.

### B-12 — Two contradictory EBIT estimates arithmetically averaged
*117 rows where the two had opposite signs; median disagreement 34.9%.*

**Resolved by removal.** EBIT comes from the reported statement line
(`EBIT`, falling back to `OperatingIncome`), summed over four quarters. There is
no second estimate to average, and no back-solving from a vendor multiple.

### B-13 — Peer groups keyed on the resolved label, comparing companies to themselves
*43 rows in groups smaller than 4; three groups of exactly 1.*

**Resolved.** `pipeline.peer_medians` walks from sub-industry outward to sector
and stops at the first level holding **four or more valid observations** —
counting observations with a usable metric, not group membership. Negative-EBIT
and negative-PE names are excluded from the medians rather than contributing.
The chosen level and its population are reported per ticker as `Peer Group` and
`Peer Count`.

### B-14 — AI scoring read the volatile column, not the hardcoded one
*78 refusals, 417 blanks, two prompt versions, and at least one row displaying
another ticker's review.*

**Resolved by removal.** The `GEMINI()` layer is gone — it is Google-Sheets-only,
non-deterministic, unauditable, and not reproducible in Excel. Its role is taken
by `scoring.detect_red_flags`, which produces deterministic, explainable flags
from the financial data: cash conversion, persistent negative FCF, dilution,
leverage, margin erosion, interest coverage and cycle position.

### B-15 — Piotroski imported whole, unverifiable
**Resolved.** Computed in `metrics.piotroski_f_score` from the statements, with
each of the nine signals exposed as its own column so a score can be
interrogated. An integration test asserts the components sum to the total.
`F-Score Basis` records whether the TTM or annual basis was used.

---

## Medium and Low

| ID | Finding | Resolution |
|---|---|---|
| B-16 | `<1` sign hack made "Match?" always FALSE for 290 rows | Current assets and current liabilities are read directly; no back-solving from the current ratio |
| B-17 | DDM used D₀ not D₁; k−g floor only safe by accident | `ddm_per_share` uses `D₀ × (1+g)`; returns None when `g >= COE`. Justified P/B enforces a 400bp minimum spread and a 4x multiple cap |
| B-18 | "min of both" mixed equity and EV multiples, degraded silently | `comparables_value` rejects outliers beyond 10x from the median, then takes the median of survivors — not the minimum, which one degenerate lens could dominate |
| B-19 | "Free Cashflows per Share" held total FCF | Separate `Free cash flow (TTM)` and `Free Cashflow Per Share (TTM)` columns, each matching its header |
| B-20 | "Discount Percentage" computed upside vs price | Renamed and recomputed as a genuine discount to NCAV |
| B-21 | Feed quantised to 1bn IDR; genuine zeros became `""` | Yahoo returns full precision; zero and missing are distinct |
| B-22 | Negative-EY and negative-ROC names occupied rank slots | Percentile ranks are computed only over rows where the metric is genuinely available |
| B-23 | 16 of 97 columns dead in Excel (14,754 frozen cells) | Rebuilt with INDEX/MATCH and a restricted function set that evaluates identically in Excel and Sheets |
| B-24 | Duplicate earnings-yield columns | Two distinct, correctly-labelled metrics |
| B-25 | `Active?` hardcoded TRUE on all 956 rows | Replaced by `Quarters Stale`, which actually varies and drives a SKIP above 3 |
| B-26 | Dead TradingView_Scrap sheet, referenced 0 times | Dropped |

---

## Defects found during the rebuild

Not in the original audit — these surfaced while testing the new pipeline
against live data, and are recorded because they were real and are now fixed.

**USD-reporting issuers valued in IDR.** ITMG, ADRO and other coal, energy and
shipping names file in USD while trading in IDR. Unconverted, ITMG's book value
read 1.72 against a market price of 25,125 — a unit error of roughly 16,000x that
the screen interpreted as a −100% margin of safety. `pipeline.normalise_currency`
detects the statement currency and converts at spot, excluding share counts,
which are not monetary. `Statement Currency` and `FX Rate Applied` record what
happened on every row.

**One degenerate comparables lens dominating the blend.** For a levered cyclical,
`EBIT × peer multiple − net debt` can land just above zero. Taking the minimum of
the lenses — the intuitively conservative choice — let that swamp two sensible
ones: ADRO, a 2,540 stock, was valued at 0.33 per share, reported as a
−769,000% margin of safety. Now outliers beyond an order of magnitude from the
median are rejected before the median is taken, and the reported margin of safety
is clamped to [−100%, +100%].

**An implausible beta collapsing the cost of equity.** Yahoo reports a beta of
0.168 for BBCA — one of the largest banks in Indonesia. Because justified P/B
divides by `(COE − g)`, that pushed the cost of equity to the floor and valued
the bank at four times book. Beta is now trusted only inside [0.5, 2.5], and the
cost of equity carries a floor of risk-free + 300bps.

**Piotroski unevaluable across the whole universe.** The TTM-versus-prior-TTM
basis needs eight consecutive quarters; Yahoo supplies five or six, so every row
returned blank. An annual-basis fallback — Piotroski's original construction —
now applies where quarterly history is too short.
