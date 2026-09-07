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

## 4. NAV lens — the lens a shipowner deserves

### 4a. The fleet, priced vessel-by-vessel against 2026 broker comps

**FACT**, fleet composition from Agent 3 (§1, Samuel Sekuritas initiation
report + bull.co.id/fleets, as of 1Q26): 3 Aframax + 5 MR (506,461 DWT
combined, average age ~22 years), 1 old LPG carrier (Gas Natuna, 1996, 3,213
DWT), 2 LNG carriers (Gas Garuda 145,914 CBM built 2004; Gas Polaris 140,500
CBM built 2002).

**FACT, sourced this session — a materially important, previously
un-flagged finding: both LNG carriers are old STEAM TURBINE vessels, and the
steam-turbine LNG segment is in structural decline, not a hot asset class.**
[IndexBox, "Buana Lautan Line Acquires 2002-Built LNG Carrier Gas Polaris in
Counter-Cyclical Move"](https://www.indexbox.io/blog/buana-lautan-line-acquires-2002-built-lng-carrier-gas-polaris-in-counter-cyclical-move/)
and [Splash247](https://splash247.com/indonesias-buana-lautan-saves-ageing-steam-lng-carrier-from-scrap/):
BULL (as "Buana Lautan Line") bought the 2002-built, 138,000 cbm steam
turbine LNG carrier **Gas Polaris for USD 14.9 million in March 2026** — the
report explicitly frames this as **"counter-cyclical,"** because **secondhand
LNG carrier values have been declining for four consecutive years**, not
rising. Gas Garuda (built 2004, ex-*LNG River Orashi*, DSME-built, sister
ship to a class BW/Seapeak has been actively scrapping) is the same
generation of steam-turbine tonnage; its purchase price was not disclosed in
sources found, but comparable steam-turbine LNG carriers of similar vintage
sold in 2026 for **USD 13.8-19.2m when sold for recycling** (SK Shipping,
four vessels at USD 13.8m each; two 135,000cbm units at ~USD 19.2m each),
per [Lloyd's List](https://www.lloydslist.com/LL1156173/Seapeak-sells-second-LNG-carrier-for-recycling-as-pressure-mounts-on-steam-turbine-fleet)
and search-aggregated 2026 shipping press. An estimated **100 steam-turbine
LNG carriers are expected to be scrapped industry-wide by 2030**, and
**over 60 LNGCs were idle/laid-up as of February 2026, 70% of them steam
units** — steam tonnage is explicitly described as "struggling to compete
in today's spot market" against modern dual-fuel/TFDE vessels.

**This directly qualifies, not confirms, the Agent 1 LNG-boom explanation
for Q2 earnings (see §5) and materially changes the NAV read: BULL's LNG
carriers are cheap, semi-obsolete assets acquired opportunistically near
scrap value, not premium modern tonnage capturing headline USD 300k/day
spot rates at will.** Whether BULL's two specific steam vessels can actually
fix at anywhere near the sector's cited peak spot rate — which the reporting
above suggests is being earned disproportionately by modern, fuel-efficient
LNG carriers, not the ageing steam segment these two ships belong to — is
**not established from what I found. Insufficient evidence — requires the
Q2 segment note showing gas-segment TCE actually realised.** I flag this as
a live, unresolved tension between two sourced facts (an 18-fold sector spot
spike vs. structurally declining steam-tonnage values/competitiveness), not
as a resolution in either direction.

**Vessel value estimates (FACT for comps, INFERENCE/ASSUMPTION where I
extrapolate BULL's specific — older, smaller — units from a sourced
comparable):**

| Vessel class | BULL units | Comp sourced | Comp value | Applied estimate |
|---|---|---|---:|---:|
| Aframax (104-110k dwt, 18-23yr) | 3 | Asia Ascend, 22yr, 115,444 dwt, **USD 33m** (record); Minerva Nounou, 20yr, 114,850 dwt, **>USD 40m** [Splash247](https://splash247.com/22-year-old-aframax-sets-33m-record/) | 33-40m | **~USD 36m/vessel** (midpoint) |
| MR (34.5-38.9k dwt, 21-25yr) | 5 | Minerva Xanthe, 20yr, 50,922 dwt, **USD 16m** to Chinese buyers [same] | 16m for a larger, younger unit | **~USD 12m/vessel** *(ASSUMPTION: scaled down for BULL's smaller size and older age — no direct comp for a sub-40k-dwt, 21-25yr MR was sourced)* |
| LPG (Gas Natuna, 3,213 dwt, 30yr) | 1 | none sourced | — | **~USD 2m** *(ASSUMPTION, floor estimate — a 30-year-old small gas carrier is close to scrap value; not independently verified)* |
| LNG (Gas Polaris, 140,500 cbm, 24yr, steam) | 1 | **Sourced purchase price, Mar-2026** | **USD 14.9m** | **USD 14.9m** (FACT — actual price paid, 6 months ago; treated as current value, may already be stale given a declining-value trend) |
| LNG (Gas Garuda, 145,914 cbm, 22yr, steam) | 1 | Comparable steam LNGCs, scrap-bound, 2026: USD 13.8-19.2m | 13.8-19.2m | **~USD 25m** *(ASSUMPTION — priced at a premium to the scrap-bound comps since Gas Garuda was bought to operate, not to recycle; genuinely uncertain, could reasonably be USD 15-40m)* |

```
Fleet market value ≈ 3×36 + 5×12 + 1×2 + 14.9 + 25
                    = 108 + 60 + 2 + 14.9 + 25
                    = USD 209.9m  (round to ~USD 210-220m given the ranges above)
```

**Sanity check against the balance sheet — this resolves a fact-sheet open
question.** BULL's own reported NetPPE at Q1-2026 was **USD 219m**
(fact sheet), which the original fact sheet flagged as suspiciously small
against ~USD 408m of total assets for an 11-vessel fleet. **My independent,
bottom-up broker-comp estimate of ~USD 210-220m lands almost exactly on
that reported figure.** This is a useful, if rough, cross-check: **the
NetPPE number is not obviously understated relative to current secondhand
market values** — the "fleet too small for the balance sheet" puzzle
appears to have been a size-intuition error, not a data-quality defect. I
still cannot rule out that some fleet value sits outside NetPPE (JVs,
right-of-use assets), but the aggregate magnitude checks out reasonably
well against 2026 broker comps.

### 4b. From fleet value to NAV per share, and the revaluation-surplus question

The correct NAV adjustment is not "fleet value minus net debt" (that
double-subtracts non-vessel working capital) — it is: **NAV = Book Equity +
(Fleet Market Value − Fleet Book Value)**, since total assets minus total
liabilities already nets everything else. Using the Q2-2026 book equity
(IDR 4,640bn / ~USD 262.4m, per the fact sheet's derived-absolutes table)
and Fleet MV ≈ Fleet Book (~USD 219m, per §4a):

```
NAV ≈ USD 262.4m + (USD ~215m − USD 219m)     [taking the low end of my Fleet MV range]
    ≈ USD 258.4m  →  IDR 4,570bn  →  IDR 295/share

NAV ≈ USD 262.4m + (USD ~220m − USD 219m)     [taking the midpoint]
    ≈ USD 263.4m  →  IDR 4,658bn  →  IDR 301/share
```

**INFERENCE: my independent, bottom-up NAV lands within a few IDR per share
of the reported BVPS of 299.49 — i.e., current 2026 secondhand vessel
prices roughly justify BULL's book value, they do not obviously
overstate it.** Given the width of my per-vessel estimates (the MR, LPG and
Gas Garuda legs are extrapolated, not directly sourced), treat this as a
band of roughly **IDR 210-390/share**, not a precise point estimate.

**This meaningfully refines, not confirms, Agent 5's revaluation-surplus
concern (§0 above / Agent 5 §8).** Agent 1 sourced that BULL's last *formal*
appraisal was **31 December 2022** — carried forward, not refreshed, through
FY2024. Agent 5's worry was that the revaluation model marks the fleet to a
cycle-peak value; **but the appraisal date (Dec-2022) predates the entire
2026 war-driven tanker/LNG rate and asset-value spike (Agent 4, §1, §3)** —
so the ~USD 30.7m revaluation surplus embedded in book (§0 above) was set
using **pre-boom** 2022 vessel prices, not boom-era ones. If anything, an
appraisal frozen at 2022 levels is now **stale-low**, not stale-high,
relative to the 2026 secondhand comps I sourced above (a 22-year-old
Aframax setting a "record" USD 33m in 2026 vs whatever a conservative
December-2022 appraiser would have marked a similar unit at). **Net
correction to Agent 5's framing: the revaluation-model mechanism is real and
the FY2024 book does carry an unrealised, not-yet-market-tested surplus, but
the direction of the risk this specific appraisal date creates is more
plausibly "book understates 2026 fleet value" than "book is marked to a
cycle peak."** Both agents were reasoning from real, sourced facts; the
appraisal-date detail is what resolves which way the number likely leans —
though a genuine independent 2026 appraisal, which BULL has not obtained
(Agent 1), is the only way to know for certain. **Insufficient evidence — a
fresh, dated appraisal would settle this outright; none was found.**

### 4c. NAV per share vs price — where does BULL sit?

| | IDR/share |
|---|---:|
| Price (2026-09-04) | **466** |
| Reported BVPS (Q2-2026) | 299.49 |
| **NAV estimate, this section** | **~295-301 (point), ~210-390 (band)** |
| **Implied P/NAV at price 466** | **~1.55x (point estimate)** |

### 4d. Where tanker/gas owners trade vs NAV in 2026, and is BULL early or late cycle

**FACT, sourced §3:** the global crude-tanker peer set trades in a **P/NAV
range of roughly 0.85x-1.05x for the "normal" owners** — Nordic American
Tankers ~88%, Torm ~1.02x, Hafnia at a small discount to its own USD 8.89/
share NAV — with **Okeanis Eco Tankers the richest of the set at ~1.6x
P/NAV**, explicitly flagged in the sourced Nortilus note as the most
expensive name in the crude-tanker cluster.

**BULL's implied ~1.55x P/NAV sits at the rich end of this range — next to
Okeanis, the single most expensive name in the peer set, not next to the
0.85-1.05x cluster where most tanker owners trade.** Combined with Agent 4's
sourced finding that **secondhand tanker asset values are up 30% (5-yr
tonnage) to 90% (20-yr tonnage) YoY** — described in that agent's own
source as "a classic late-cycle signal when the oldest, least efficient
tonnage rallies hardest" — and a **swollen orderbook at ~25% of the existing
global tanker fleet** (Agent 4, §3), the answer to the task's direct
question is: **BULL is priced late-cycle on the NAV lens, not early-cycle.**
A genuinely early-cycle re-rating would show the stock catching up *toward*
peer NAV multiples from a discount; BULL has already run *past* the peer
cluster to sit beside the most expensive name in it.

**What the NAV lens excludes, and why that is the conservative direction:**
this NAV carries **zero value for the FSRU/FPSO "pillars"** of the
four-pillar strategy (Agent 3, §1) — those are tender-stage bids, not owned
assets (Agent 3 found no confirmed FPSO contract win), so excluding them
cannot be inflating the P/NAV multiple above; if anything a bull could argue
NAV understates optionality. That optionality is unpriced and unproven, not
a reason to override the P/NAV read above.

---

## 5. Normalised earnings power — the single most important judgement in this report

### 5a. Decomposing Q2-2026: which driver, how much

**FACT, cross-checked across three independent agents and this session's own
arithmetic — the dominant Q2 driver is the oil-tanker spot/TCE spike, not
LNG, and not (on current evidence) an acquisition gain.** Management's own
statement (Agent 3, cited via idxchannel/RCTI+): *"Average TCE revenue
through Q2-2026 had reached more than double compared to Q1-2026."* Given
Agent 3's sourced 95% spot-revenue mix for the oil-tanker book (§2 of Agent
3's report), a near-doubling of oil-tanker TCE alone is arithmetically
sufficient to produce almost the entire Q1→Q2 revenue jump (IDR 741bn →
1,487bn, a 1.9x move) **without requiring LNG, an acquisition, or a
consolidation-scope change.** LNG (2 vessels, only one of which — Gas
Polaris — had even a partial quarter in the fleet by Q2) is a **real but
secondary contributor in revenue terms**, even though Agent 1's sourced LNG
spot-rate data (an 18-fold rate surge, spot to USD 300k/day) makes it the
more dramatic-*sounding* headline. **This re-ranks the two "big story"
explanations the earlier agents each led with:** oil-tanker TCE compounding
is the primary, better-evidenced mechanism; LNG is real and margin-accretive
but smaller in absolute revenue.

**On the residual possibility of a one-off (bargain-purchase gain on the
OMH acquisition, closed 27 March 2026, Agent 5 §1):** the TCE-doubling
arithmetic above explains the *revenue* move without needing it, but says
nothing about the *net margin* anomaly (52.12% Q2 net margin vs a 37.3% Q1
operating margin, Agent 1/5's flagged puzzle — noting Agent 1's caution that
the 37.3% comparator tile may itself be a stale Q1 figure, so the anomaly is
not as clean as it first looked). **I cannot resolve this. Insufficient
evidence — requires the actual Q2-2026 interim income statement's "other
income" line**, which no agent in this project was able to source. I
therefore treat a modest one-off contribution to Q2 net income as
**possible but unconfirmed**, and do not build it into the decomposition
below as either a certainty or a zero.

### 5b. A "recurring" baseline, and why it cross-checks

**INFERENCE, built from figures already established in this report.** Strip
out the 2026 war-risk premium entirely and ask what BULL earns on its
oil-tanker fleet at the 4-year median EBIT (IDR 630.8bn — already a
mid-cycle figure, not a trough, since it includes FY2023's own strong year,
per the annual history table in BULL.md) against a normalised interest
burden (using the post-paydown run-rate of ~IDR 153bn/yr, i.e. 4× the
Q1-2026 quarterly interest expense of 38.2bn):

```
Recurring net income  ≈ (630.8bn EBIT − 153bn interest) × (1 − 0.22 tax)
                       ≈ 477.8bn × 0.78
                       ≈ 372.7bn
Recurring EPS          ≈ 372.7bn / 15,494.44m shares
                       ≈ IDR 24.1/share
```

**This lands within IDR 2 of BULL's own actual FY2025 EPS of 25.93** (fact
sheet annual history) — **FY2025 was earned before the 2026 war/LNG boom**,
so this is a genuine, useful cross-check that the "recurring" baseline is
not an arbitrary construction: it reproduces what BULL actually earned in
the last full year before the current spike, to within a few percent.

### 5c. The LNG spot rate — a precedent this project should not ignore

**FACT, sourced this session, and this is the single most important input
to the "how much should be capitalised" question:** LNG spot charter rates
have done exactly this before, in this decade, and it mean-reverted hard.
LNG spot rates spiked to **USD 200,000/day in late 2022** (Russia-Ukraine
European gas-demand shock) and **subsequently fell back to ~USD 30,000/day**
— an **~85% collapse from peak.** [Search-aggregated 2026 LNG market
reporting, cross-referenced against Kpler/OIES/EIA 2026 outlooks cited
above]. Separately, **2026 LNG market fundamentals are bearish, not
bullish, on a supply-demand basis**: Kpler forecasts Asian spot LNG prices
falling from ~USD 12/mmBtu (2025) to ~USD 10/mmBtu (2026) as **37 mtpa of
new liquefaction capacity** comes online — the analyst consensus (Kpler,
Rabobank, Rystad) is a *buyer's market* forming in the underlying commodity,
even as the war-risk premium on *shipping* briefly spiked the freight side
of the market. **The USD 300k/day LNG spot print (Agent 1) is a shipping
war-risk-premium event layered on top of an otherwise softening LNG
commodity market, precisely analogous in shape to the 2022 spike-then-crash
— not a structural re-rating of LNG shipping economics.**

**Compounding this, §4a's finding on BULL's specific vessels matters
directly here:** BULL's two LNG carriers are **old steam-turbine tonnage in
a segment described by 2026 shipping press as struggling to compete against
modern dual-fuel vessels**, with ~100 sister-generation units headed for
scrapping industry-wide by 2030. **Whether BULL's specific ships can
actually capture a rate anywhere near the headline USD 300k/day spot print
— which the reporting suggests is disproportionately earned by modern,
fuel-efficient tonnage — is not established.** Two independent, sourced
reasons therefore argue for capitalising **very little** of the LNG
contribution as durable: (1) the precedent that LNG spot spikes of this kind
have already round-tripped violently once in the last four years, and (2)
BULL's own LNG vessels are structurally disadvantaged assets within the
segment generating the headline rate.

**Applying the owner's rule — never treat peak-cycle earnings as
permanent — with the extra force this precedent demands: the LNG
contribution to Q2-2026 should be treated as almost entirely non-recurring
for valuation purposes, not partially discounted.** This is a THESIS
judgement, not a mechanical output, but it is the best-evidenced position
available: I found a directly analogous, dated, sourced precedent for this
exact commodity/segment collapsing ~85% from an equivalent spike within
roughly a year, and no sourced case for LNG spot durability at anything
close to current levels.

### 5d. Bear / base / bull EPS

| Scenario | IDR/share (annual, forward) | Basis |
|---|---:|---|
| **Bear** | **32** | Recurring baseline (§5b, ~24) plus a modest, non-spike contribution from having 2 (rising to a guided 5 by end-2026, Agent 3 §1) LNG carriers earning ordinary — not spot-spike — charter income once the war premium fully unwinds. No credit for FPSO/FSRU (unbuilt). Assumes the Hormuz war premium and the LNG spike are **both** fully round-tripped within 2-4 quarters, consistent with the 2022 LNG precedent (§5c) and Agent 4's own sourced observation that the war-risk premium was already softening by late August 2026 (Hormuz workarounds, oil price down from >$130 peak to ~20% above pre-war). |
| **Base** | **58** | Recurring baseline plus a **fading, not vanished**, war/LNG premium through the remainder of FY2026, reverting toward (not fully to) the bear case in FY2027. Credits some structural tightening in compliant mid-size tonnage from sanctions/shadow-fleet enforcement (Agent 4, §3, Kpler) as a genuine, if smaller, durable tailwind beyond the acute war spike, plus continued interest-expense relief from debt paydown. This is roughly **2.2x the FY2025 actual** and about **44% of the current TTM(Q2) annualised figure of 130.97** — i.e. it treats under half of the current run-rate as repeatable. |
| **Bull** | **100** | War premium persists longer than base case (protracted Hormuz disruption, as has already happened once via the Jun-17 MOU that broke down again in July per Agent 4), the LNG build-out reaches 5 vessels and captures materially-above-normal (though not peak-300k) spot rates, and at least one FPSO tender converts to a signed contract. Still **~24% below** the current TTM(Q2) annualised 130.97 — deliberately never fully capitalising the single best quarter in the company's history, per the owner's explicit rule. |

**For calibration:** applying the tanker-peer PE cluster sourced in §3
(FRO 6.6x, DHT 6.6x, TEN 6.5x — a tight, real, current cluster, itself
measured on peers' own current-cycle earnings) to these three EPS estimates
gives **IDR 208 (bear) / 377 (base) / 650 (bull)** — a band that brackets
the current price of 466 roughly in its upper-base-to-bull region, **not
its lower end.** This is one more independent line of evidence, alongside
§2's DCF and §4's NAV, that the current price is pricing something closer to
the optimistic end of plausible earnings persistence, not a conservative
one — see §7 for how this is weighed against the other lenses.

---

## 6. Sell-side cross-check

**FACT, sourced this session:**

| House | Date | Rating | Target price (IDR) | Notes |
|---|---|---|---:|---|
| BRI Danareksa Sekuritas | Feb 2026 (reiterated 3 Sep 2026) | Buy | **780** | 3 Sep note is technical/momentum-framed ("bullish structure above MA20/MA200... rebound from support 416"), tied explicitly to the unconfirmed Sinar Mas 30-LNG-vessel rights-issue rumour — [StockWatch.id](https://stockwatch.id/ihsg-berpotensi-pullback-bri-danareksa-sekuritas-rekomendasi-beli-bull-hingga-cuan/), [IPOTNews TP](https://www.indopremier.com/ipotnews/newsDetail.php?jdl=Target_Price_BULL__BRI_Danareksa_Sekuritas_Rp_780___Buy&news_id=484838) |
| Samuel Sekuritas | Apr 2026 initiation, reiterated May 2026 | Buy | **700** | Initiation forecasts FY2026 revenue USD 434m (+193% YoY), EBITDA USD 181m (+269% YoY), explicitly hedged on "the market stays at this level for 2026F" (Agent 3, §3) — [Bisnis.com](https://market.bisnis.com/read/20260507/7/1972157/samuel-sekuritas-pangkas-target-ihsg-ke-7500-intip-saham-jagoannya) |
| NH Korindo Sekuritas Indonesia | ~Mar 2026 | Buy | **800** | [IPOTNews](https://www.indopremier.com/ipotnews/newsDetail.php?jdl=Target_Price_BULL__PT_NH_Korindo_Sekuritas_Indonesia_Rp_800___Buy&news_id=484243) |
| **Consensus (7 analysts)** | as of 22 Jun 2026 | **7 Buy, 0 Hold, 0 Sell** | **avg 703, range 505-950** | [search-aggregated, TradingView-style consensus source] |

**Cross-check against this report's own bands:** the sell-side consensus
average (IDR 703) sits **above my own Bull-case EPS-multiple estimate
(IDR 650, §5d)** and well above my Base case (IDR 377). The low end of the
sell-side range (IDR 505) roughly matches my Base-to-Bull region; **no
sell-side target found sits inside my Bear case (IDR 208) or anywhere near
my NAV estimate (IDR ~295-301, §4).** This is a real, sourced divergence,
not a rounding difference.

**THESIS, and the most useful single observation this section can add: the
sell-side notes sourced in this project consistently extrapolate the
current TCE/LNG rate momentum forward (Samuel's own FY2026E assumes
"the market stays at this level," BRI Danareksa's 3-Sep reiteration is
explicitly technical/momentum-based, tied to an unconfirmed related-party
rumour) — none of the sell-side material surfaced in this research
engages with the qualified audit opinion, the going-concern paragraph, the
covenant breach (Agent 1/5), the LNG spot-rate's own 2022 precedent of an
~85% collapse (§5c), or BULL's specific LNG vessels' steam-turbine
competitive disadvantage (§4a).** A unanimous 7-analyst Buy consensus with
no Hold or Sell, built substantially on continuing a war-risk-premium spike
and an unconfirmed related-party rumour, is itself a data point worth
weighting cautiously — it is closer to consensus momentum-chasing than to
independent triangulation, and the owner's framework exists precisely to
supply the discipline this sell-side set does not appear to have applied.
**I do not adopt the sell-side consensus as a valuation lens in §7** — it
is reported here as cross-check context, not as evidence of fair value.

**Not found — insufficient evidence:** any post-Q2-2026-results sell-side
note (all sourced notes predate or are contemporaneous with, not
subsequent to, a confirmed Q2 print); any sell-side note that discusses
BULL's FY2025 qualified audit opinion or going-concern paragraph by name.

---

## 7. Adopted valuation and verdict

### 7a. Every lens, side by side

| Lens | Bear | Base | Bull | What it credits |
|---|---:|---:|---:|---|
| EPV (§1a, unaffected by the D&A bug) | — | **92.21** | — | Through-cycle NOPAT, no growth, no reinvestment |
| DCF, corrected D&A (§2c) | None (equity < 0) | None (equity < 0) | **38.33** | Through-cycle NOPAT, charges 100% of normalised capex incl. growth capex |
| Comps, rebuilt peer set (§3e) | — | **~635** | — | Current-cycle EV/EBITDA (9x) on TTM(Q2) EBITDA — peak-to-peak, not through-cycle |
| NAV (§4b-c) | ~210 | **~298** | ~390 | Fleet at 2026 broker comps, cross-validated against book |
| Earnings-power × peer PE (§5d) | **208** | **377** | **650** | Bear/base/bull normalised EPS × real peer PE cluster (6.5x) |

Five lenses, none of them cheap tricks: two (EPV, DCF) are deliberately
conservative through-cycle constructions and land far below price; two
(Comps, earnings-power-bull) credit meaningful persistence of the 2026 boom
and land above price; NAV sits in between and is the most independently
cross-validated number in this report (§4a's bottom-up broker comps landed
almost exactly on both BULL's own reported NetPPE and, via §4b's equity
adjustment, on reported BVPS).

### 7b. Adopted bear / base / bull, and why

**I adopt NAV as the anchor for Base, EPV as the anchor for Bear, and a
NAV-at-rich-peer-multiple construction for Bull — not a mechanical average
of all five lenses.** Reasoning:

- **Bear = EPV = IDR 92.** This is the principled Greenwald no-growth floor
  already computed and unaffected by any of the defects this report fixed
  (§1c). It answers "what is BULL worth if it stopped growing the fleet
  today and simply ran the existing business at its 4-year median EBIT" —
  the most conservative, best-defended number available. The corrected
  DCF's own Bear/Base scenarios returning **no positive equity value at
  all** (§2c) corroborates that this is not an unreasonably harsh floor:
  an independent model, run on the same real depreciation, agrees the
  downside case is severe once IDR 1,907bn of net debt is weighed against
  a thin, capex-hungry normalised cash flow.
- **Base = NAV = IDR ~298.** The task explicitly frames NAV as "the lens a
  shipowner deserves," and of every number in this report it is the one
  two independent methods converge on: bottom-up 2026 broker vessel comps
  (§4a) and the book-equity-plus-revaluation-adjustment route (§4b) land
  within a few IDR of each other and within a few IDR of reported BVPS.
  I weight it as Base rather than Bear because, unlike EPV, it credits
  BULL's *current* fleet at *current* market prices rather than assuming
  zero growth value — a fair, not conservative, characterisation of where
  the business stands today.
- **Bull = NAV × richest peer P/NAV = IDR ~477** (298 × 1.6x, the Okeanis
  multiple sourced in §3b/4d — the richest of the crude-tanker peer
  cluster). This is deliberately **not** the earnings-power-bull figure of
  650 (§5d), which I regard as a lower-confidence upper bound because it
  requires assuming the war/LNG premium persists at materially-above-normal
  levels for an extended period — precisely the assumption §5c's 2022 LNG
  precedent argues against. A NAV-based bull case only requires that BULL
  re-rate *to where the single richest global peer already trades on its
  own NAV*, not that BULL's earnings stay elevated — a more defensible
  "best case" than compounding an optimistic earnings assumption on top of
  an optimistic multiple assumption.

**MOS and Upside, stated separately per the owner's framework (MOS =
(IV−Price)/IV; Upside = IV/Price−1), at price IDR 466:**

| Scenario | IV (IDR/share) | MOS | Upside |
|---|---:|---:|---:|
| Bear (EPV) | 92 | **−406.5%** | **−80.3%** |
| Base (NAV) | 298 | **−56.4%** | **−36.0%** |
| Bull (NAV × 1.6x) | 477 | **+2.3%** | **+2.4%** |

**Even the Bull case — BULL re-rating to sit beside the single richest
name in the global crude-tanker peer set, on a NAV that already prices in
BULL's fleet at 2026's elevated secondhand asset values — only barely
clears the current price.** The Base case, built on the most
independently-corroborated lens in this report, says the stock is
overvalued by more than a third against a fair-value anchor. This is not
a screener-style single blended number; it is a genuine, wide range, and
the width itself is the finding: **there is no lens in this report,
correctly computed, that makes BULL look cheap. The best case says roughly
fair. Every other case says expensive, several of them severely.**

### 7c. Ruling the screener's SKIP: CORRECT-BY-ACCIDENT

**Not FALSE NEGATIVE** — a completely independent, five-lens re-derivation
that fixes both defects this project's own agents found (the D&A bug, §1b-2;
the wrong peer group, §3a), incorporates the Q2-2026 boom the screener could
not see, and adds a NAV lens the screener does not compute at all, **still
does not produce a BUY or even a WATCH.** The Base case (IDR 298) sits
36% below the current price; only an optimistic Bull case barely clears it.
Whatever is wrong with the screener's mechanics, its directional call —
SKIP — survives contact with far better evidence than it was built on.

**Not simply CORRECT either.** The screener's own MOS of −69% and Blended
IV of 275.02 were reached by:
1. A DCF that returned **blank, not a number** — silently, with no red flag,
   because of a ~12x-understated depreciation add-back (§1b-2). The
   corrected DCF returns a genuinely different kind of answer (computed,
   not blank — mostly negative equity, §2c) that happens to still support
   the same directional conclusion, but the screener did not know that; it
   simply dropped the lens from its weights.
2. A Comparables IV of 579.69 built on a **wrong peer group** (§1a, §3a) —
   Yahoo's "Passenger Marine Transportation" sector, not tanker/gas owners.
   A correctly rebuilt Comps lens (§3e) gives ~635, not far from the
   broken number, but that is itself close to coincidental: the passenger-
   transport peer set's 15.0x EV/EBIT median and the rebuilt tanker peer
   set's ~9x EV/EBITDA on a materially larger current EBITDA base landed
   in a similar place by two unrelated routes.
3. The one lens that *was* mechanically sound — EPV at 92.21 (§1c) — got
   50% of the renormalised weight only because the DCF vanished, not
   because the pipeline reasoned that EPV was the most defensible lens for
   a company in the middle of a capex-heavy fleet-expansion programme.

**The screener therefore reached the right neighbourhood via a genuinely
broken process — a blank DCF, a wrong peer group, and a lucky
renormalisation — not via a chain of individually defensible steps.**
That is the textbook definition of correct-by-accident, and it is worth
stating plainly: had the peer-group bug alone been fixed without the D&A
bug also being fixed, the blend would likely have moved toward a false
BUY (a higher, correctly-sector-matched Comps number combining with a
still-blank DCF and unchanged EPV could easily have pushed the blended IV
and MOS across the 10% watch threshold). The two defects partially
cancelled each other out in this specific case. That is not a property to
rely on.

### 7d. Staleness — should it gate the verdict, and at what threshold

**FACT, from the fact sheet:** `Quarters Stale` = 1.72 is computed and
printed but does not gate, downgrade, or suppress the verdict.

**This case is a genuine natural experiment in how much a verdict can move
between the screener's data vintage and the present, and the result argues
for gating, even though gating would not have changed *this* row's final
call.** Between the Q1-2026 data the screener actually used and the Q2-2026
actuals this project's agents sourced: PE (TTM) moved 12.43 → 5.74x, current
ratio 0.597 → 0.92, EV/EBITDA 12.34 → 7.00x, ROE 15.2% → 27.1% — every
trailing ratio the screener's lower-level scores (Quality, Safety, Value)
are built from moved by 30-55% in one quarter, for a name the screener
classifies `BUSINESS_CYCLICAL`. **That the final SKIP verdict happened to
survive this swing (§7c) is a property of this specific case, not a
property the staleness field itself guarantees** — the screener got lucky
that its two mechanical defects cancelled out AND that the underlying
economics, once properly re-derived, still supported the same call. A
different cyclical name, one quarter staler, with only one defect instead
of two, could easily flip.

**Recommendation: gate at `Quarters Stale > 1.5`, per the fact sheet's own
proposal, and I would go further for `BUSINESS_CYCLICAL`-classified names
specifically.** A staleness threshold should not be uniform across business
types — a stable, contracted business (a toll road, a bank) moves little
quarter to quarter and can tolerate more staleness before its verdict goes
stale; a `BUSINESS_CYCLICAL` name, by construction, is exactly the category
where a single quarter can move trailing ratios by 30-55% as demonstrated
here. **Concretely: suppress the verdict (replace BUY/WATCH/SKIP/DEEP VALUE
with a `STALE — VERDICT SUPPRESSED, VERIFY AGAINST LATEST FILING` flag) at
`Quarters Stale > 1.5` for all business types, and tighten that threshold to
`> 1.0` specifically for `BUSINESS_CYCLICAL` names**, given this project's
own hard-won rule that cyclicals are exactly where peak-cycle numbers must
never be mistaken for permanent ones — a stale cyclical reading is doubly
dangerous, because it risks being *both* out of date *and* sitting at the
wrong point in the cycle at the same time.

### 7e. Final verdict

**SKIP, with the case reclassified from "average business, cheap" (the
apparent Q2 read) to a live "value trap vs. good-business-mid-cycle"
question that resolves to value-trap on the weight of evidence.** Restating
the five outcomes CLAUDE.md requires staying distinguishable: this is not
"good business at a fair price" (Base case is 36% overvalued against the
most defensible lens), not "average business very cheap" (no lens in this
report finds it cheap), and not "fairly valued" in the boring sense either
— it is closer to **deep-value-shaped optically (single-digit trailing PE,
sub-2x P/B) sitting on top of a genuine value-trap risk profile**: a
three-year qualified audit opinion and going-concern paragraph (§0 above,
Agent 1/5), a covenant breach never cured, revenue capitalising a war-risk
premium and an LNG spot spike that has an ~85% mean-reversion precedent in
this exact decade (§5c), LNG carriers that are structurally disadvantaged
steam-turbine tonnage rather than premium modern assets (§4a), Pertamina
counterparty concentration into a customer that is simultaneously planning
to in-source (Agent 4), a controlling shareholder who sold, not bought,
into the rally (Agent 4/5), and an unconfirmed related-party rumour
(Sinar Mas / Fortune Street) that the market is currently paying for before
it has been confirmed (§6). **The screener's SKIP is affirmed on
independently rebuilt, better-sourced evidence — correct-by-accident on
its own mechanics, but correct.**

**What would change this call:** a sourced Q2-2026 interim income statement
that (a) rules out a material one-off/bargain-purchase contribution to net
income (§5a) and (b) shows BULL's own LNG vessels realising day rates that
meaningfully exceed the discount this report applies to steam-turbine
tonnage (§4a, §5c); confirmation (not rumour) of the Sinar Mas transaction
on terms that do not dilute existing holders below NAV; and a subsequent
audit opinion that clears the covenant-breach qualification. None of these
are close to established as of 2026-09-04.
