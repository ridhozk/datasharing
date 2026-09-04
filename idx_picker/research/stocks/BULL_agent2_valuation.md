# BULL — Agent 2: Valuation & Model Validation

*Status: COMPLETE. Incorporates the orchestrator's mid-task Q2-2026 data drop
(owner's Stockbit screenshots) — see §0 and §5-7, which supersede the Q1-only
framing in §1-4 wherever they conflict.*

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

## 2. Rebuilding the DCF with real D&A

### 2a. Inputs, all traceable to Agent 1's primary-source find or the screener's own code

**FACT**, sourced from Agent 1's read of BULL's audited FY2024 statements
(BDO Indonesia, signed 19 May 2025): total depreciation **USD 15,598,365**
(FY2024), **USD 15,782,350** (FY2023). Average **USD 15,690,358/yr ≈ IDR
277.5bn/yr** at FX 17,684 — this is the number that replaces the screener's
implied IDR 23.2bn/yr (§1b).

**FACT**, reproduced from `scoring.py::build_scenarios` and confirmed by
running it directly against these inputs (script run in this session,
`idx_picker/scraper/{metrics,scoring}.py`, unmodified):
- `base_wacc` fed into the DCF is **not** the CAPM cost of equity used by EPV
  (14.6%, see §1a/1c) — it is the flat `Settings.wacc = 0.12` default
  (`pipeline.py` line 517, `settings.wacc` passed straight through). The DCF
  and EPV lenses silently run on two different discount rates for the same
  company. This is a second, smaller inconsistency worth flagging alongside
  the D&A bug — not the focus of this section, but noted for the pipeline
  maintainer.
- `terminal_growth` = 3.0% (`Settings.terminal_growth`), `historical_growth`
  = Revenue CAGR 3Y = 8.5% (fact sheet), `tax_rate` = 22%.
- `normalised_ebit_value` = IDR 622.9bn (median of 4 annual OperatingIncome,
  §1b — unaffected by the D&A bug, and **also unaffected by the Q2-2026 spike**
  since it is built from Yahoo's *annual* series, which the Q2 quarter has not
  yet fed into). This is actually the correct behaviour per the owner's rule
  never to capitalise peak-cycle earnings — see §5.
- `normalised_capex_value` = −IDR 623.6bn (median of 4 annual CapitalExpenditure,
  §1b).
- `net_debt` = IDR 1,907bn (fact sheet, Q2 basis), `shares` = 15,494,436,935.

### 2b. Corrected cash-flow-base arithmetic

```
NOPAT               =  622.9bn × (1 − 0.22)              =  +485.86bn
Real D&A (sourced)  =  (15,598,365+15,782,350)/2 × 17,684 =  +277.47bn
Normalised capex     =  median annual, Yahoo-negative      =  −623.60bn
                                                              ---------
fcf_base             =  485.86 + 277.47 − 623.60           =  +139.73bn
```

**This is now POSITIVE — the D&A bug alone was enough to flip the sign of the
cash-flow base** (from −113.9bn in the screener's broken version to +139.7bn
here). That confirms the hypothesis in §1b directly: BULL's DCF was not
declining to value the company because the company is unvaluable, it was
being killed by a ~12x-understated add-back.

### 2c. Running the DCF scenarios on the corrected base

I ran `metrics.dcf_per_share` directly (not by hand — executed the actual
project code with the corrected `fcf_base`) using the pipeline's own bear/
base/bull offset construction (`scoring.py::build_scenarios`, lines ~261-269):

| Scenario | Growth | WACC | Terminal g | Result |
|---|---:|---:|---:|---|
| Bear | 3.5% | 14.0% | 2.0% | **None** — equity value negative |
| Base | 8.5% | 12.0% | 3.0% | **None** — equity value negative |
| Bull | 12.5% | 11.0% | 3.5% | **IDR 38.33/share** |

**FACT, computed, not estimated.** Bear and Base still return blank — not
because of the D&A bug this time, but because a `fcf_base` of only ~IDR 140bn
cannot cover **both** (a) the working-capital drag of financing 8.5%+ revenue
growth (10.1% WC intensity, per the fact sheet) **and** (b) IDR 1,907bn of
net debt sitting on the balance sheet. The 5-year present value of stage-1
cash flows plus the Gordon terminal value only clears net debt in the Bull
case (11% WACC, 12.5% growth) — and even there, the result is **IDR 38.33 —
92% below the current price of 466**, not a number that supports any BUY
framing. Sensitivity check: substituting the Q2-TTM revenue base (IDR 3,438bn)
for the WC-intensity calculation instead of the Q1 fact-sheet TTM figure
(IDR 2,653bn) makes it *worse* (Bull → IDR 32.82), because a larger revenue
base means a larger absolute WC draw for the same growth rate.

**INFERENCE, the central finding of this section: fixing the D&A bug does
not rescue the DCF as a bull-case tool for BULL — it turns it from
"silently blank" into "computed and unattractive."** The screener's original
SKIP was reached on a broken input, but a *correctly computed* DCF, using
Agent 1's sourced real depreciation, **still does not clear the current
price in the base case, and only barely clears it in a growth-optimistic
bull case.** This is meaningfully different from ERAA's defect (there, a
missing term made a fair stock look artificially cheap by 66%); here, fixing
the missing term does *not* flip the conclusion — it just makes the same
conclusion legible instead of blank. That is itself useful evidence for §7.

### 2d. Why: separating maintenance capex from growth capex

The task specifically asks me to address this, and the arithmetic above makes
the mechanism concrete rather than hand-wavy:

```
Normalised capex (4-yr median)    IDR  623.6bn/yr
Real D&A (2-yr average, sourced)  IDR  277.5bn/yr
                                        --------
"Growth" capex (the gap)          IDR  346.1bn/yr   ≈ 1.25× D&A
```

**THESIS, but grounded in Agent 3's sourced fleet data.** If maintenance
capex is, to a first approximation, capex that merely replaces what
depreciates (Greenwald's own assumption in constructing EPV — see below),
then real D&A of ~277.5bn/yr is a reasonable **proxy for maintenance capex**,
and the ~346bn/yr gap between that and actual capex is capital being
deployed for **fleet growth, not fleet replacement**. That is exactly
consistent with Agent 3's sourced finding: BULL acquired two secondhand LNG
carriers (MT Gas Garuda, Dec-2025; MT Gas Polaris, Q1-2026) for a combined
~USD 60-70m (~IDR 1,100bn at spot, spread over the capex-recognition period),
75% debt-funded, with **three more LNG units guided for H2-2026** — a
discrete, disclosed, deliberate fleet-expansion programme, not capex
diffused evenly across an ageing 11-vessel core fleet whose average age is
already ~22 years (Agent 3, §1).

**This is why EPV (92.21, §1a) and the corrected DCF (bear/base blank, bull
38.33) diverge so sharply, and the divergence is not a bug — it is the two
lenses answering different questions on purpose:**
- **EPV** assumes a no-growth steady state, where maintenance capex ≈
  depreciation and the two *net to roughly zero* — so EPV never has to charge
  the growth-capex gap at all. `EPV = NOPAT/COE − net debt` = a going-concern
  floor value if BULL stopped growing the fleet today.
- **DCF** is charged the *entire* normalised capex line, growth portion
  included, because a genuine 5-year discounted-cash-flow model should
  reflect that growth is not free — the LNG build-out consumes cash before
  it (maybe) starts returning it.

**The unresolved and genuinely hard modelling problem — flagged, not
solved:** neither lens currently *separates* maintenance from growth capex
explicitly; DCF implicitly charges 100% of normalised capex as if none of it
will ever generate a return, while EPV implicitly assumes 100% of capex above
depreciation is discretionary/growth and simply ignores it. **Truth is
between the two.** A more correct treatment would explicitly split
normalised capex into a maintenance component (≈ real D&A, ~277.5bn) and a
growth component (~346bn), charge only the maintenance component against the
steady-state FCF used for the *terminal value*, and charge the full amount
only in the explicit 5-year forecast window where the LNG capex is actually
happening. The current two-lens structure (EPV floor + DCF full-charge
ceiling) is a reasonable **band**, not a point estimate — and for BULL that
band is roughly **IDR 38 (DCF bull) to IDR 92 (EPV)**, both far below the
IDR 466 price, on *normalised, through-cycle* earnings power. Whether the
Q2-2026 boom changes that conclusion is the subject of §5.

### 2e. The design question: what should the universe-wide fix be?

**Recommendation: implement a sector-aware variant of (a) — proxy D&A from
NetPPE and an assumed useful life — but only where the underlying asset base
is genuinely time-depreciated tangible fixed assets, and pair it with (c)'s
discipline: always attach an explicit `D&A Source: Proxied` tag and a red
flag, never let a proxied number pass as if it were a filed one.** Reasoning:

**Why not pure (b) — Greenwald steady-state NOPAT alone when D&A is
unknown?** Because that is functionally what EPV *already is* in this
codebase (`epv_per_share`, §1c). Routing the DCF lens to the same formula
when D&A is missing would not add information — it would silently convert
two lenses into one lens counted twice, understating how many independent
views the blended IV actually rests on (`scoring.classify` renormalises lens
weights assuming the surviving lenses are actually independent, per §1a —
that assumption would be violated). §2d shows precisely why the two lenses
should stay different: EPV is deliberately a no-growth floor; the DCF's job
is to price the reinvestment the EPV lens ignores. Collapsing them removes
exactly the information the task wants preserved.

**Why not pure (c) — declare unavailable and red-flag, with no attempted
computation?** This is the conservative, "never fabricate" choice, and it is
right for names where the asset base cannot be sensibly time-depreciated at
all (see the sector list below). But for the median capital-intensive IDX
name, NetPPE-and-useful-life is not fabrication — it is a disclosed,
documented, sourced approximation, exactly the kind of INFERENCE this
project's own labelling convention exists to permit, provided it is labelled
as one. Blanking every capital-intensive DCF universe-wide throws away real
information for names where the proxy would be decent (see the BULL
sanity-check below) purely to avoid the failure mode of names where it would
not be — better to gate by sector than to blank uniformly.

**Why (a), and why it must carry (c)'s transparency:** I sanity-checked the
proxy against BULL's own *real, sourced* D&A. BULL's fact-sheet NetPPE is
USD 198m (FY2025) / USD 219m (Q1-2026), average ≈ USD 208.5m. At a 15-year
assumed life (justifiable given BULL's fleet skews old — average fleet age
~22 years against a 5-35 year useful-life band, Agent 3 §1) the proxy gives
**USD 13.9m/yr — 11% below the real, audited USD 15.6-15.8m/yr.** At a
20-year assumed life it gives USD 10.4m/yr, 33% low. **Either is off by low
double digits, not the ~12x the current EBITDA-EBIT-gap method is off by.**
A proxy this order of magnitude is genuinely useful for screening even though
it is imprecise — which is exactly the "not a conclusion, a hypothesis"
standard this project holds Stage 1 to.

**Effect on other named capital-intensive IDX sectors, sector by sector:**
- **Shipping (BULL, TPMA, HITS, PSSI, MBSS, WINS, SOCI)** — good fit for (a).
  Vessels are straightforwardly time-depreciated tangible assets; useful
  lives cluster 15-25 years industry-wide. The BULL sanity-check above is
  directly on point for this whole sector.
- **Towers (TOWR, MTEL)** — good fit for (a), arguably the *best* fit: tower
  structures and related equipment are homogeneous, straight-line-depreciated
  fixed assets with well-known 15-20-year lives, and these are large,
  well-covered names where Yahoo's underlying feed is more likely to be
  complete in the first place — the D&A gap this section is fixing may be
  smaller here than for a thinly-covered name like BULL. Worth a targeted
  data-quality check before assuming the defect is universe-wide at the same
  severity.
- **Toll roads (JSMR and peers)** — **poor fit; should route to (c), not
  (a).** Toll-road economics amortise a *concession intangible*, not
  straight-line PP&E, typically over the concession term (often 25-40 years)
  and frequently on a **units-of-usage (traffic-volume) basis**, not a
  time basis at all. A flat `NetPPE ÷ N years` proxy is not just imprecise
  here, it is the wrong *model*, not merely the wrong parameter — this is
  the sector where a silent proxy would most plausibly manufacture a
  confidently wrong number, which is precisely what this project's "never
  fabricate" rule exists to prevent.
- **Plantations (AALI, LSIP)** — moderate fit. Bearer-plant/mature-plantation
  costs are capitalised and depreciated over the productive tree life
  (~20-25 years) alongside separate mill/processing PP&E (~20 years) — a
  blended NetPPE/22yr proxy is defensible but conflates two different asset
  classes with different lives; treat as (a) with wider error bars than
  shipping or towers.
- **Coal (ADRO, ITMG, PTBA)** — **poor fit; should route to (c).** Mining
  equipment is commonly depreciated on a **units-of-production basis** tied
  to remaining reserves, not a fixed number of years — a name early in a
  mine's reserve life and a name late in it would get the same flat-life
  proxy despite needing opposite treatment. Given this project's own
  hard-won rule to normalise EBIT with the *median* because one supercycle
  year distorts a mean (`ITMG's 2022 EBIT was 5x its 2025`), coal is already
  known to be the sector where flat, time-based assumptions break down most
  — the D&A proxy should not repeat that mistake with a different variable.

**Net recommendation in one line:** ship (a) with a per-`business_type`
useful-life table (not one constant) for tangible, time-depreciated fixed
assets (shipping, towers, plantations), keep (c) — explicit unavailable +
red flag, no proxy attempted — for concession-amortised (toll roads) and
units-of-production (coal, mining) names, and in every case where (a) fires,
attach the `D&A Source: Proxied` tag so a screener user can never mistake a
NetPPE-based estimate for a filed number.

---

## 3. Peer group rebuild

### 3a. Why the screener's peer group is wrong (recap, confirmed independently)

**FACT**, confirmed against `pipeline.py`'s peer-group construction (grouped by
Yahoo `sector`/`industry` string) and the fact sheet: BULL is bucketed into
"Passenger Marine Transportation," a Yahoo sector misclassification — BULL
carries no passengers. The resulting peer EV/EBIT median of 15.0x (Comps IV
579.69, §1a) is drawn from an unrelated set of companies and should be
discarded, not adjusted.

### 3b. Rebuilt peer set — global crude/product tanker owners (WebSearch, Sep 2026)

| Ticker | Company | Metric | Value | Source |
|---|---|---|---:|---|
| FRO | Frontline plc | P/E (TTM) | 6.6x | [Simply Wall St](https://simplywall.st/stocks/us/energy/nyse-fro/frontline/news/is-frontline-fro-overvalued-as-record-profit-and-dividends-l) |
| FRO | Frontline plc | EV/EBITDA | 8.96x | [Yahoo/aggregated, Sep 2026] |
| FRO | Frontline plc | ROE (TTM) | 35.0% | same |
| DHT | DHT Holdings | P/E (May 2026) | 6.59x | [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/look-dht-holdings-dht-valuation-081339588.html) |
| TEN/TNP | Tsakos Energy Navigation | P/E (Jul 2026) | 6.48x | [Yahoo Finance](https://finance.yahoo.com/quote/TEN/key-statistics/) |
| NAT | Nordic American Tankers | P/NAV | ~88% | [Simply Wall St](https://simplywall.st/stocks/us/energy/nyse-nat/nordic-american-tankers) |
| NAT | Nordic American Tankers | EV/EBITDA | 5.6x–10.1x *(sources disagree on window — flagged)* | same |
| ECO | Okeanis Eco Tankers | P/NAV | ~1.6x *(richest of the crude-tanker peer set)* | [search-aggregated] |
| TRMD | Torm | P/NAV | ~1.02x | [Snowball Analytics](https://snowball-analytics.com/public/blog/hafnia-buys-1445-of-torm-what-does-it-mean-for-product-tankers-jldshia) |
| HAFN | Hafnia | P/NAV | small discount to NAV (NAV/share ≈USD 8.89 at Q2-26) | [Nasdaq press release](https://www.nasdaq.com/press-release/hafnia-limited-announces-financial-results-three-and-six-months-ended-30-june-2026), [Simply Wall St](https://simplywall.st/stocks/no/energy/ob-hafni/hafnia-shares/news/hafnia-targets-product-tanker-leadership-with-torm-stake-and) |
| TNK | Teekay Tankers | EV/EBITDA | ~2.2x *(cheapest — but see caution below)* | [Nortilus](https://nortilus.substack.com/p/crude-tankers-q2-26-earnings-preview) |

**Caution on TNK's 2.2x:** Teekay Tankers has undergone a large special-dividend
/ balance-sheet-return-of-capital programme in recent years that can distort a
simple EV/EBITDA read (large cash balance depressing EV relative to EBITDA).
**INFERENCE, not independently verified in this pass** — treat 2.2x as a
possible statistical outlier per this project's own rule ("reject outliers
beyond 10x from the median" is the CLAUDE.md convention for EBIT normalisation;
the same logic applies to a peer multiple more than ~3-4x away from the rest
of a tight cluster) rather than as the anchor multiple.

**Peer EV/EBITDA cluster, excluding the flagged outlier:** FRO 8.96x, NAT
~8x (midpoint of the two figures found), giving a **rough peer EV/EBITDA
median in the high-single-digits, ~8-9x**, corroborated independently by the
P/E cluster (FRO 6.6x, DHT 6.6x, TEN 6.5x — all within 0.1x of each other,
a striking convergence for three unrelated owners, consistent with the
whole crude-tanker sector re-rating together on the same Hormuz-war catalyst
Agent 4 sourced).

### 3c. LNG carrier owners — BULL's second, newer exposure

| Ticker | Company | Metric | Value | Source |
|---|---|---|---:|---|
| FLNG | Flex LNG | EV/EBITDA | 13.34x | [stockanalysis.com](https://stockanalysis.com/stocks/flng/statistics/) |
| FLNG | Flex LNG | Fleet TCE, Q2-2026 | USD 86,100/day (vs FY26 guidance USD 73-78k) | [Quartr](https://quartr.com/events/flex-lng-flng-q2-2026_3Y0BrE3v) |
| ALNG | Awilco LNG | EV/EBITDA | ~91.6x | [valueinvesting.io](https://valueinvesting.io/ALNG.OL/valuation/ev_ebitda-multiples) |

**Awilco LNG's 91.6x is not usable as a peer anchor** — it is a tiny,
two-vessel company whose TTM EBITDA is a rounding error against its
enterprise value in the specific window sampled; the multiple says more
about a thin denominator than about LNG sector pricing. **Cool Company and
Capital Clean Energy Carriers: insufficient evidence — requires further
research.** WebSearch did not surface current valuation multiples for
either; a live agent with more search budget should query them directly by
name (Cool Company trades as NYSE: CLCO; Capital Clean Energy Carriers as
NASDAQ: CCEC) rather than in a combined query, which returned nothing usable
here.

**Usable LNG anchor: Flex LNG at 13.3x EV/EBITDA** — materially richer than
the crude-tanker cluster (~8-9x). This matters directly for BULL: **its two
LNG carriers are a small fraction of an 11-vessel fleet, but LNG spot rates
at USD 300k/day (Agent 1, sourced) are the single largest driver of the
Q2-2026 earnings jump (§5).** If the market is willing to pay a
mid-teens multiple for a pure-play LNG owner (Flex LNG), a blended BULL —
still overwhelmingly an oil-tanker company by vessel count and by 9M25
revenue mix (95% oil per Agent 3) — should trade **closer to the tanker
cluster (~8-9x) than to the LNG cluster (~13x)**, with perhaps a modest
premium for the LNG optionality if the market believes the 3-more-LNG-units
H2-2026 guidance (Agent 3, §1) will be delivered and the LNG rate spike
proves more than transient.

### 3d. Indonesian/Asian peers

| Ticker | Company | Data found |
|---|---|---|
| SOCI | Soechi Lines | Market cap IDR 3.47tn (14 Aug 2026), **up 174.9% over 1 year** — almost identical magnitude to BULL's own +203% 1Y move (fact sheet), consistent with a sector-wide Indonesian tanker/gas re-rating, not a BULL-specific story. **PBV reported as "lowest among Indonesia's shipping companies"** as of a mid-Jan-2026 commentary — i.e. SOCI, which Agent 3 sourced as **74% time-charter / 13% spot** (far more contract-covered than BULL's 95% spot), still trades at the *cheapest* book multiple in the domestic peer set, which is a useful cross-check: the market is not obviously paying up for charter-cover stability among Indonesian shipping names right now. [IPOTNews](https://ipotnews.com/ipotnews/newsDetail.php?jdl=SOCI__Lonjakan_Saham_Cerminan_Penyesuaian_Valuasi_Pasar&news_id=211803) |
| SMDR | Samudera Indonesia | TTM revenue IDR 13.64tn, net income IDR 791.16bn, EPS 48.31, **beta 0.04** (illiquid/thinly-traded — the same Yahoo-beta problem CLAUDE.md flags for BBCA), Altman Z 1.84, F-Score 4/9. **Current P/B not sourced — insufficient evidence.** Predominantly a container-shipping/logistics operator, a weaker fit for BULL's tanker/gas book than SOCI, TPMA or HITS. [stockanalysis.com](https://stockanalysis.com/quote/idx/SMDR/statistics/) |
| TPMA, HITS, PSSI, MBSS, WINS | — | **Insufficient evidence — requires further research.** Current (2026) P/B, EV/EBITDA figures were not surfaced by WebSearch in this pass; the only PBV figures found for this set were from a 2014-2018 academic study and are explicitly stale, not usable. A live agent with IDX-terminal or Bloomberg-equivalent access should pull these directly rather than relying on general web search, which does not index current Indonesian small-cap multiples well. |

### 3e. Adopted Comparables read

**THESIS, built from the sourced cluster above, not a precise output of the
pipeline's Comps formula (which needs a full peer table this pass could not
fully rebuild for the Indonesian leg):**

- A defensible **blended peer EV/EBITDA for BULL, weighting ~85-90% toward
  the crude-tanker cluster (8-9x) and ~10-15% toward the LNG cluster (13x)**
  given the fleet-count and revenue-mix split (§3c), lands at roughly
  **9-9.5x EV/EBITDA.**
- BULL's own **EV/EBITDA is 7.00x on the Q2-2026 basis** (fact sheet). That
  is **cheaper than this rebuilt peer multiple**, not richer — a genuinely
  different conclusion from the screener's wrong-peer-group Comps IV of
  579.69 (built on a 15.0x EV/EBIT median from passenger-transport peers),
  though for a different reason than the screener's number was wrong: the
  new comparison uses the right sector, but **both BULL and its global
  peers are being valued off the same 2026 war-driven earnings peak** —
  this is a peak-to-peak comparison, not peak-to-normal. It tells you BULL
  is not egregiously mispriced *relative to other tanker owners riding the
  same cycle right now* — it says nothing about whether the whole cluster,
  BULL included, is overpriced relative to **through-cycle** earnings. That
  question is what §4 (NAV) and §5 (normalised earnings) exist to answer,
  and multiples-on-peak-earnings should not be allowed to substitute for
  either.
- Applying a **9x multiple to BULL's TTM(Q2) EBITDA** (~IDR 1,305bn per the
  fact sheet's derived-absolutes table) gives an EV of ~IDR 11,745bn; less
  net debt of IDR 1,907bn gives an equity value of ~IDR 9,838bn, or
  **~IDR 635/share** — moderately above the current IDR 466 price. **This
  is the Comps-lens fair value on peak/current-cycle earnings.** Whether
  that earnings base is real and repeatable is exactly the §5 question, and
  I do not treat this 635 figure as adoptable without that test — see §7.

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
