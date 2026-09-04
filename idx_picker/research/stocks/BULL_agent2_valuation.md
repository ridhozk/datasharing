# BULL — Agent 2: Valuation & Model Validation

*Status: IN PROGRESS — being written incrementally. Last updated: see bottom.*

Target: PT Buana Lintas Lautan Tbk (IDX: BULL), oil tanker owner/operator.
Price IDR 464, mkt cap ~IDR 7,189bn (~USD 407m), EV ~IDR 9,143bn (~USD 517m).
Reports in USD, trades in IDR (FX 17,684).

Screener verdict under test: **SKIP, MOS −69%.** This is the first name in the
review the screener rates negatively — the job is symmetric to the usual:
test whether the SKIP is earned, i.e. whether the screener has produced a
**false negative**.

Labeling convention used throughout: **FACT** (verifiable from source code,
cached data, or a cited filing/URL) / **INFERENCE** (derived by me from facts,
shown with arithmetic) / **THESIS** (an interpretive judgment) / **ASSUMPTION**
(an input I chose because the real figure is unavailable) / **Insufficient
evidence** (flagged explicitly, not glossed over).

---

## 1. Reproducing the screener's arithmetic (Task 1 + 2)

### 1a. Why Blended IV = 275.02 (universe run)

**FACT**, reproduced by hand from `scoring.py::blended_intrinsic` and the
fact-sheet inputs. For a `BUSINESS_CYCLICAL` name, lens weights are
`{dcf: 0.2, epv: 0.5, comps: 0.3}`. The DCF lens is unusable (see §1b), so it
drops out and the remaining two weights renormalise:

```
Blended IV = (EPV×0.5 + Comps×0.3) / (0.5+0.3)
           = (92.21×0.5 + 579.69×0.3) / 0.8
           = (46.105 + 173.907) / 0.8
           = 220.012 / 0.8
           = 275.02   ✓ matches screener output exactly
```

`MOS = (275.02 − 464)/275.02 = −0.687` ✓. `Upside = 275.02/464 − 1 = −0.407` ✓.
Both surviving inputs are independently compromised (EPV built on the same
broken D&A logic that kills DCF is *not* the case — EPV doesn't need D&A, see
§1c — but Comps uses the wrong peer group, §3). So the 275.02 blend rests on
one lens that's defensible (EPV) and one that's wrong (Comps, wrong sector).

### 1b. Confirming the suspected DCF defect — VERIFIED IN CODE AND DATA

**FACT.** In `scoring.py::build_scenarios` (lines ~274-288):

```python
if normalised_ebit_value is not None and normalised_ebit_value > 0:
    fcf_base = normalised_ebit_value * (1 - tax_rate)
    capex = normalised_capex_value if normalised_capex_value is not None else core.capex_ttm
    if capex is not None and core.ebitda_ttm and core.ebit_ttm:
        depreciation = core.ebitda_ttm - core.ebit_ttm
        fcf_base += depreciation + capex   # capex arrives negative
```

Depreciation is **inferred as `EBITDA_TTM − EBIT_TTM`** — there is no direct
D&A field at all. Confirmed in `yahoo.py::STATEMENT_FIELDS` (lines 52-95): the
scraper never requests `DepreciationAndAmortization` / `DepreciationAmortizationDepletion`
from Yahoo's timeseries API. The only D&A information the pipeline has is the
gap between two *other* reported lines.

I reproduced the exact numbers from the raw cached Yahoo timeseries
(`idx_picker/data/cache/ts_BULL_0.json` and `ts_BULL_4.json`, all figures raw
USD as reported by Yahoo — BULL is a USD filer):

**TTM EBITDA and EBIT (quarters 2025-Q2 through 2026-Q1, USD):**
| Field | Q2'25 | Q3'25 | Q4'25 | Q1'26 | TTM sum |
|---|---:|---:|---:|---:|---:|
| EBITDA | 5,418,411 | 7,573,631 | 12,492,833 | 16,398,064 | **41,882,939** |
| OperatingIncome (=ebit_ttm) | 6,625,707 | 6,317,585 | 11,226,917 | 16,400,779 | **40,570,988** |

Implied D&A = 41,882,939 − 40,570,988 = **1,311,951 USD ≈ IDR 23.2bn** at FX
17,684 — this **exactly** matches the fact sheet's "implied D&A ~23.2bn/yr."
The suppression guard in `metrics.py::build_core` (`if abs(ebitda_ttm - ebit_ttm)
< 1.0`) only fires on a difference under 1 IDR *unit* (i.e., under one rupiah),
so a 23bn-rupiah stub sails straight through it untouched.

**Normalised EBIT (median of 4 annual OperatingIncome, USD):** 2022: 9.99m,
2023: 58.88m, 2024: 37.08m, 2025: 33.37m → median = (33.37+37.08)/2 = **35.225m
USD = IDR 622.9bn** at FX 17,684. Matches fact sheet's NOPAT base exactly
(622.9 × 0.78 = 485.9bn).

**Normalised capex (median of 4 annual CapitalExpenditure, USD, Yahoo-negative):**
2022: −7.33m, 2023: −28.08m, 2024: −42.46m, 2025: −52.35m → median =
(−28.08−42.46)/2 = **−35.27m USD = IDR −623.6bn**. Matches exactly.

**Full reproduction:**
```
fcf_base = 622.9 × (1−0.22) + 23.2 + (−623.6)
         = 485.9 + 23.2 − 623.6
         = −114.5bn   (fact sheet: −113.9bn, small FX-snapshot rounding)
```
`dcf_per_share` has `if fcf_base <= 0: return None` (metrics.py line ~750) —
**every one of Bear/Base/Bull inherits the same negative base** (only wacc/
growth/terminal vary, not the D&A defect), so all three scenarios return
`None`. **Confirmed: the DCF is not "declining to value" BULL, it is being
silently killed by an add-back Yahoo never supplied the ingredient for.**

### 1c. Does this defect touch EPV too?

**FACT, checked in code.** `metrics.py::epv_per_share` does **not** use D&A at
all — `enterprise_value = normalised_ebit*(1-tax)/WACC`, no add-back. So EPV
(92.21) is unaffected by the D&A bug. It is, however, still built on
`normalised_ebit` — see §5 for whether that normalisation is itself
defensible for BULL.

---

## 2. What would the DCF produce with a plausible D&A?

*(being filled in — see live doc; placeholder while I source real D&A)*

---

## 3. Peer group rebuild

*(pending — web research in progress)*

---

## 4. NAV lens

*(pending — web research in progress)*

---

## 5. Normalised earnings power / charter cover

*(pending)*

---

## 6. Sell-side cross-check

*(pending)*

---

## 7. Adopted valuation and verdict

*(pending — will state bear/base/bull IV in IDR/share, MOS and Upside
separately, and rule the SKIP CORRECT / CORRECT-BY-ACCIDENT / FALSE NEGATIVE)*
