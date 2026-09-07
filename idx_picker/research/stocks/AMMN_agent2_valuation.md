# AMMN — Agent 2: Valuation & Model Validation

*Ticker: AMMN (Amman Mineral Internasional Tbk.), IDX copper/gold miner. Price IDR 4,470,
mkt cap ~IDR 324tn (~US$18.1bn). Screener: SKIP, "Cyclical", composite 46.*

> **Process note:** first pass completed after ~10 searches/fetches, written immediately
> per instructions. Gaps are marked "Insufficient evidence — requires further research."
> A second, deeper pass was not required to reach a defensible verdict, but see Gaps
> section for what would sharpen the numbers further.

---

## 1. Reconciling the screener's number

The screener fact sheet (`AMMN.md`) shows: IV Base **IDR 136.0**, IV Bull **IDR 742.8**,
Comparables IV **IDR 1,787.5**, Blended IV **IDR 1,126.9**, MOS Blended **-100%** (floored),
Upside Blended **-74.8%**. **FACT**, read directly from the fact sheet.

Note: the task brief cites a blended IV of "865" — this does not match the fact sheet's
1,126.9. **INFERENCE**: likely a different snapshot/rounding in an upstream step not shown
in the regenerated fact sheet. I treat the fact sheet's 1,126.9 as the source of truth below
and flag the discrepancy rather than silently picking one.

## 2. What kind of year is trailing data measuring? (FACTs from company filings)

FY2025 was explicitly a transition trough:
- Concentrate production 446,563 dmt (-41% YoY), containing 209 Mlb Cu (-47% YoY) and
  102,758 oz Au (-87% YoY) — "mill feed during transition period primarily comprised
  stockpiles and low-grade Phase 8 fresh ore."
- Net sales $1,847m (-31% YoY), EBITDA $1,057m/57% margin (-26% YoY), net income
  $258m/14% margin (-60% YoY). Capex $1,372m (-23% YoY, "nearing completion of major
  expansion projects").
- Net debt grew from $3,531m (Dec-24) to $5,756m (Dec-25) funding the buildout.
- Source: AMMAN FY2025 Earnings Release (amman.co.id, 26-Mar-2026).

The recovery is **already visible** in the most recent quarter: Q1 2026 net income
**$163m (20% margin)** vs a **$138m net loss** in Q1 2025; EBITDA **$508m (63% margin)**
vs **-$42m** in Q1 2025. Cathode output ~27,700t and refined gold ~66,200oz in 1Q26.
**FACT** (Amman Q1 2026 press release / discoveryalert.com.au summary).

Processed grade inflection, 1Q26 vs prior: copper grade 0.31%→0.53%, gold grade
0.17→0.54 g/t (**FACT**, NH Korindo Sekuritas "New Smelters Unlocking Value" report,
citing AMMAN 1Q26 data).

**INFERENCE**: the screener's TTM window spans exactly the trough-to-recovery transition
(the trailing four quarters mix a large Q1-2025 loss with a record Q4-2025 and a strong
Q1-2026). Reconstructing TTM EBIT from the quarterly table in `AMMN.md`
(Q2'25 1,234.8 + Q3'25 ≈1,000.9 implied + Q4'25 11,603.0 + Q1'26 5,630.6, IDR bn) gives
≈IDR 19,533bn (~$1.09bn), broadly consistent with the screener's own implied TTM EBIT
(EV 425,075 / EV-EBIT 25.46 ≈ IDR 16,693bn, ~$0.93bn). **Even including the two strong
recovery quarters, EV/EBIT is still ~21-25x** — so the "trailing multiple is too low
because of one bad year" story is only half right; see §5.

## 3. Reserves, resources, and mine plan (FACTs, AMMAN FY2025 Earnings Release,
JORC estimate as of 31-Dec-2024, Competent Person: AMC Consultants Pty Ltd)

| Asset | Tonnage (Mt) | Cu grade | Au grade | Contained Cu | Contained Au |
|---|---|---|---|---|---|
| Batu Hijau — Stockpiles | 254 | 0.32% | 0.11 g/t | 1.78 Blb | 0.92 Moz |
| Batu Hijau — Phase 7 (remnant) | 9 | 0.62% | 0.97 g/t | 0.13 Blb | 0.29 Moz |
| Batu Hijau — Phase 8 | 442 | 0.38% | 0.36 g/t | 3.70 Blb | 5.11 Moz |
| **Batu Hijau total ore reserves** | **705** | **0.36%** | **0.28 g/t** | **5.61 Blb** | **6.32 Moz** |
| Batu Hijau mineral resources (excl. reserves) | 2,052 | 0.24% | 0.10 g/t | 10.85 Blb | 6.70 Moz |
| **Elang total ore reserves** | **2,526** | **0.32%** | **0.33 g/t** | **17.78 Blb** | **26.44 Moz** |
| Elang mineral resources (excl. reserves) | 1,294 | 0.26% | 0.21 g/t | 7.35 Blb | 8.66 Moz |

Elang reserves grew 79% in tonnage and ~71-76% in contained metal vs the 2023 estimate
(**FACT**, amman.co.id). The 2025 Feasibility Study for Elang is complete; it plans to
reuse existing Batu Hijau infrastructure (mill, power, Benete port, smelter, primary
access road) via a 54km overland conveyor — a materially lower capital-intensity path
than a standalone greenfield project of this size. **FACT** for the infrastructure-sharing
design; **INFERENCE** that this meaningfully lowers unit development capex vs a standalone
comparable.

Mine-life sequencing (**FACT**, multiple broker/company sources): Batu Hijau Phase 8
mining to ~2030, stockpile processing to ~2033; Elang mining planned to commence after
Batu Hijau closes, running to ~2046 (~13-year Elang life). Elang development capex is
**not company-confirmed** in the sources I reached — a broker estimate (Verdhana, via
search snippet) puts it at **~US$3bn, assumed to begin expensing ~2028**. **INFERENCE /
broker estimate, not FACT.**

## 4. Costs and the smelter (FACTs unless noted)

- Adjusted C1 cash cost: **-$0.54/lb** (2025) vs **-$3.37/lb** (2024) — negative because
  gold/silver/sulfuric-acid by-product credits exceed the cost of producing the copper.
  Even in the worst grade/ramp year on record, cash costs stayed net-negative. Company
  states it expects Batu Hijau to remain "among the lowest-cost copper producers globally"
  over the long term on this metric.
- New royalty regime (April 2025, **FACT**, material and permanent): copper concentrate
  7-10% (was 4%), copper cathode 4-7% (was 2%), gold 7-16% (was 3.75-10%), silver 5%
  (was 3.25%). Plus a new gold export duty (Dec-2025) of 10-15% depending on form/price.
  These are genuine forward margin headwinds not fully visible in FY2025's blended numbers
  and should be built into any forward model — a reason valuations should NOT simply
  extrapolate FY2024's fatter margins forward either.
- Smelter/PMR: 900,000 dmt/yr concentrate input capacity, designed for 220,000t copper
  cathode/yr + 830,000t sulfuric acid/yr; PMR designed for ~579 koz refined gold, 1.8 Moz
  refined silver, 77t selenium/yr. First cathode Mar-2025, first refined gold Jul-2025;
  temporary outages Jul-Aug 2025 (furnace/acid plant repairs); Completion & Project
  Acceptance Certificate signed with contractor NFC on **18-Jul-2026**, confirming
  construction/commissioning/performance-guarantee tests complete.
- Total capex for smelter+PMR+CCPP power plant is cited around **~$3bn** in aggregate
  across press sources (smelter itself ~$1bn per Kontan/Katadata, mill/processing
  expansion ~$1.6bn) — figures vary by source/scope; treat as **approximate, not a single
  reconciled company figure**. FY2025 total capex was $1,372m, described as "nearing
  completion of major expansion projects" — i.e. the heavy growth-capex phase that
  suppressed FCF (and confused trailing multiples) is largely behind the Batu Hijau/smelter
  buildout; the next capital wave is Elang (~$3bn, not yet started).
- Processing/mill expansion to 85 Mtpa (>2x prior capacity): targeted complete Q3 2026,
  first ore into new mill Jul 2026. 450MW CCPP + LNG regas facility under construction to
  cut fuel costs (Block 1 already powering the smelter; Block 2 in hot commissioning as of
  Dec-2025).
- FY2026 **official mining-level guidance** (unchanged per the FY2025 release): 900,000 dmt
  concentrate containing 485 Mlb (220,000t) Cu and 579,000 oz Au — vs FY2025 actual
  446,563 dmt / 209 Mlb Cu / 102,758 oz Au (+101% / +132% / +463% YoY guided). **The
  company explicitly declined to give official 2026 cathode/refined-gold guidance**,
  stating the priority is stable smelter performance. The widely cited 162,662t cathode
  target (2x 2025) is a **broker/press figure, not the company's formal guidance table** —
  treat as INFERENCE. Analyst consensus is more conservative, ~121,800-122,000t (~65%
  smelter utilization).

## 5. NPV sanity check (base/bear/bull) — labeled ASSUMPTION-heavy

**This is a rough, order-of-magnitude sum-of-parts check built from the public
reserve/grade/cost disclosures above — not an engineered technical-report-grade NPV.**
I did not have access to AMMN's own year-by-year mine schedule, a defensible AMMN-specific
WACC, or a full technical report, so recovery rates, margins, and the 10% discount rate
below are industry-typical placeholders, explicitly flagged as ASSUMPTION.

**Commodity price context (FACT, Aug-2026):** Copper ~$6.60/lb (record high, +49% YoY,
driven by AI/data-center electrification demand and supply disruptions). Gold ~$4,325/oz
(near record highs after a Jan-2026 peak of $5,596, with JPMorgan/Deutsche
Bank/UBS/SocGen consensus targets of $6,000-6,300 by end-2026). **Both metals are at or
near all-time highs right now** — a critical fact for interpreting any valuation built on
current spot.

| Case | Copper | Gold | Method sketch | Rough per-share IV |
|---|---|---|---|---|
| Bear | $3.50/lb | $2,500/oz | Reversion toward historical norms; Elang value haircut ~50% for execution/permitting/funding risk; Batu Hijau reserves only at full value | **~IDR 1,850** |
| Base | $4.50/lb | $3,200/oz | Partial reversion from record spot; both segments at industry-typical recovery (Cu 85-88%, Au 65-70%) and ~55% EBITDA margin (in line with FY2025's 57%, achieved even in the worst operating year), 10% discount rate, less sustaining/Elang capex and ~25% tax/PNBP burden | **~IDR 3,900** |
| Bull | $6.00/lb | $4,000/oz | Near-spot prices hold; full Phase 8 ramp + smelter margin capture; Elang de-risked and captured at base recovery assumptions | **~IDR 7,500** |

Mechanically: Batu Hijau's 705Mt reserve (recoverable ~4.9 Blb Cu / ~4.4 Moz Au) produces
most of its cash flow 2026-2033 and is only lightly discounted; Elang's 2,526Mt reserve
(recoverable ~15.1 Blb Cu / ~17.2 Moz Au) doesn't start producing until ~2033 and is
heavily discounted — its PV is the single most assumption-sensitive number in the model
(pre-construction, no confirmed capex figure, permitting/funding/execution risk over a
7+ year horizon all unresolved). Net debt (~$5.8bn and still growing) is subtracted to get
equity value, then divided by ~72.4bn shares at FX 17,908.

**Cross-check via EV/EBITDA on normalized-grade earnings** (Priority 1 ask): broker 2026
revenue estimates cited in the search results run ~$5.0-5.2bn; at a 55-57% EBITDA margin
that implies FY2026E EBITDA of roughly **$2.7-2.9bn**. Against EV of ~$23.7bn (screener
figure, consistent with the FY2025 balance sheet), that's **EV/EBITDA ≈ 8.2-8.8x** — a far
more reasonable multiple for a low-cost, long-life copper-gold asset than the **trailing
EV/EBIT of 25.5x**, and broadly in line with where major low-cost copper producers trade
mid-cycle. This is the strongest evidence for Priority 1's thesis that the trailing
multiple overstates how expensive AMMN looks.

## 6. The other direction (Priority 3) — it is not obviously cheap either

- Even after reconstructing TTM EBIT including the two strong recovery quarters
  (Q4-2025, Q1-2026), EV/EBIT is still **~21-25x**, not obviously cheap.
- Annualizing only the single strongest quarter (Q4-2025, EBIT run-rate ~$648m/quarter)
  gives EV/EBIT ~9x; annualizing only the most recent quarter (Q1-2026, ~$314m/quarter)
  gives ~19x. **That 9x-19x-25x spread depending on which quarter you pick is itself the
  finding**: AMMN is still mid-ramp, not at a stabilized run-rate, so nobody — including
  this analysis — can currently pin down one "normalized" multiple with confidence.
- P/B of 3.3x (market cap $18.1bn vs Dec-2025 book equity $5.43bn) is a real premium that
  must be earned by growth not yet visible in a full clean year of numbers.
- The base-case NPV above (~IDR 3,900) sits close to, and slightly below, the current
  price of IDR 4,470 — i.e. even crediting the company's own reserve base and grade-recovery
  guidance at only moderately-reverted commodity prices, the stock is not a screaming
  bargain. To be comfortably undervalued at today's price requires commodity prices to
  stay near their current record levels, which is the single largest identified risk.

## 7. Most important assumption

**Copper price.** It is the larger share of revenue (FY2025 net sales split roughly
$1,160m copper-related vs $687m gold-related by my reconstruction of the disclosed
product-line revenues — **INFERENCE**, exact split not separately disclosed), it prices
both segments' 23.4 Blb of combined copper reserves, and it is currently at an all-time
high (+49% YoY) that the bear/base/bull cases treat very differently — a reversion to the
$3.50-4.00/lb historical-average band pushes the base case toward the bear case and makes
the stock look overvalued; sustained $5.50-6.50/lb supports prices above the bull-case NPV.
**Gold price is a close second**: it is what makes AMMN's C1 cash cost structurally
negative, so a gold price collapse would flip cash costs sharply positive and compress
margins materially even if copper holds up.

## 8. Gaps — insufficient evidence, would sharpen the model further

- Insufficient evidence — requires further research: year-by-year mine schedule /
  grade-by-year production profile beyond the single 1Q26 data point and FY2026 guidance
  (would need the full JORC technical report or a detailed investor-presentation deck,
  neither of which I could retrieve as readable text — two source PDFs (kbvalbury
  initiation report, Verdhana research note) returned binary/inaccessible content).
- Insufficient evidence — requires further research: a confirmed, company-sourced Elang
  development capex figure (used a ~$3bn broker estimate).
- Insufficient evidence — requires further research: AMMN-specific WACC/discount rate
  derivation (I used a round 10% placeholder); AMMN-specific metallurgical recovery rates
  (I used industry-typical porphyry Cu/Au recovery assumptions, not disclosed AMMN figures).
- Insufficient evidence — requires further research: Q2 2026 results (not yet published /
  not found in search as of the task date); a reconciled, single AISC (all-in sustaining
  cost) figure — only the C1 cash cost was found.

---

```
Valuation Score: 52/100
Existing Screener Valuation: IDR 1,127 blended (IV Base 136 / IV Bull 743 / Comparables 1,788) — task brief cites 865, does not match fact sheet; flagged, not reconciled
Current Price: IDR 4,470
Conservative Value: ~IDR 1,850 (Bear: Cu $3.50/lb, Au $2,500/oz, Elang haircut 50%)
Base Value: ~IDR 3,900 (Base: Cu $4.50/lb, Au $3,200/oz, both segments at industry-typical recovery/margin)
Bull Value: ~IDR 7,500 (Bull: Cu $6.00/lb, Au $4,000/oz, near-spot prices hold, full ramp + Elang captured)
Appropriate Valuation Method: NPV/sum-of-parts of the ore body (Batu Hijau reserves + Elang reserves, phased by mine-life timing), cross-checked against EV/EBITDA on a normalized (post-ramp) earnings year — NOT a DCF/EPV/comps blend anchored to trailing or near-term EBIT, which is contaminated by the Phase 7→8 transition trough and concurrent smelter-ramp capex
Why Existing Valuation May Be Wrong: Screener's DCF/EPV are anchored to trailing/near-term EBIT during a company-disclosed transition trough (lowest grades, smelter losses, temporary export limits); IV Base of IDR 136 and IV Bull of IDR 743 imply almost no going-concern value for a $1.85bn-revenue, deeply-negative-C1-cash-cost producer with 705Mt of Batu Hijau reserves plus a de-risked, feasibility-complete Elang project — those are static-earnings artifacts, not a mine valuation
Valuation Upside: Bear: -58.6% / Base: -12.8% / Bull: +67.8%
Margin of Safety: Bear: -141.6% / Base: -14.6% / Bull: +40.4%
Most Important Assumption: Copper price (larger revenue share than gold and prices both reserve bodies), with gold price a close second because it is what keeps C1 cash cost negative
Valuation Verdict: FAIRLY VALUED
```
