# ESSA — Agent 2: Valuation & Model Validation

*ESSA Industries Indonesia Tbk. (IDX: ESSA). Price IDR 655. Statement currency USD; FX 17,908 IDR/USD applied throughout. Analysis date 2026-08-11.*

**Every claim below is labelled FACT / INFERENCE / THESIS / ASSUMPTION.**

---

```
Valuation Score: 64/100
Existing Screener Valuation: Blended IV 732 | MOS 10% | Verdict WATCH
Current Price: IDR 655
Conservative Value: IDR 440
Base Value: IDR 830
Bull Value: IDR 1,250
Appropriate Valuation Method: Mid-cycle EV/EBIT built bottom-up from the
  gas-to-ammonia spread, where gas is CONTRACTUALLY INDEXED TO THE AMMONIA
  PRICE (primary). Cross-checked against EV per annual tonne of ammonia
  capacity vs actual build cost (floor) and normalised owner-earnings yield.
  NOT EV/EBITDA as reported, NOT dividend yield, NOT P/B alone.
Why Existing Valuation May Be Wrong: see section 7 — seven defects, two of
  which are arithmetic errors in the screener output itself.
Valuation Upside: Bear: -33% / Base: +27% / Bull: +91%
Margin of Safety: 21% at base IV (MOS = (830-655)/830). Probability-weighted
  IV (25/50/25) = IDR 838 → MOS 22%. Below the 30% BUY threshold.
  Price at which 30% MOS is achieved: IDR 581.
Most Important Assumption: the mid-cycle realised ammonia price per tonne.
  ±USD 50/t moves base IV by ~±IDR 154/share (~19%). It is the largest single
  driver — but the ammonia-indexed gas contract cuts its dominance roughly in
  half versus a fixed-gas-cost ammonia producer. Second: the durability of that
  gas contract, which expires ~2027-28.
Valuation Verdict: FAIRLY VALUED (at the undervalued end; a close call)
```

---

## 1. The right framework: this is a spread business with a built-in hedge

**FACT.** ESSA owns two cash-generating assets: (a) PT Panca Amara Utama (PAU),
the Banggai Ammonia Plant in Batui, Banggai Regency, Central Sulawesi —
**700,000 tonnes/year nameplate**, ~2,000 t/day, built for a total project cost
of **USD 800 million** (USD 509m of syndicated debt led by IFC with ANZ, HSBC,
KDB, OCBC, SMBC, StanChart and UOB; agreement dated 5 Sep 2014); and (b) an LPG
refinery in Lampung. Ammonia dominates revenue and essentially all earnings
variance.
*Sources: essa.id IFC syndication release; pau.co.id; topbusiness.id (Aug 2026).*

**FACT — and this is the single most important structural fact about ESSA.**
PAU's gas is supplied by JOB Pertamina-Medco Tomori Sulawesi (JOBPMTS) from the
Senoro-Toili working area, allocation **up to 55 MMSCFD**, under a **13-year
contract running from 2015 to ~2027, extendable**. **The gas price is indexed to
the ammonia price.** The disclosed reference point: **at ammonia USD 730/t, PAU
buys gas at USD 8.60/MMBTU.**
*Sources: essa.id — MEMR gas price approval release; essa.id — JOBPMTS Heads of
Agreement; ewsdata.rightsindevelopment.org (IFC project record, contract tenor).*

**THESIS — the ammonia-indexed gas contract is the thing every generic screener
misses about this company.** ESSA is not a naked long position on ammonia. Its
principal input cost rises and falls *with* its output price by contract. This
has three valuation consequences that run in opposite directions:

1. **It compresses operating leverage in both directions.** A fixed-gas ammonia
   producer sees ~100% of a price move drop to the spread. ESSA sees ~66% (see
   §4.1). The bull case is capped and the bear case is cushioned.
2. **It makes ESSA a better business than "Cyclical" implies** — lower earnings
   volatility, near-zero risk of a negative-spread shutdown, which is exactly
   what killed European ammonia producers in 2022. It arguably justifies a
   higher multiple than a merchant ammonia producer.
3. **It concentrates the risk into a single event: contract renewal, due
   ~2027-28.** That is one to two years away. If the renewal reprices gas
   materially higher or drops the ammonia linkage, the business changes
   character. **This is the largest un-analysable risk in the name.**

INFERENCE: the correct valuation approach is therefore a **normalised spread
model**, not a multiple of trailing earnings, and it must carry an explicit
haircut for the 2027-28 contract renewal.

---

## 2. Cycle position — where is ammonia today? (Priority 3)

**FACT — external price marks:**
- Middle East FOB **~USD 490/t, March 2026** (0.49 USD/kg); ~USD 438/t Nov 2025.
- Tampa CFR ~USD 650/t Mar 2026; ~USD 658/t Nov 2025; quarterly avg ~USD 608/t.
- US Corn Belt inland USD 750–850/t Mar 2026 (freight-inflated; irrelevant to
  ESSA's netback).
*Sources: chemanalyst.com/Pricing-data/ammonia-37; discoveryalert.com.au (Mar 2026).*

**FACT — ESSA's own realised price.** Q1 2026 realised ammonia was
**USD 455/MT, up 34% YoY**, on revenue of USD 95m (+37% YoY), net profit +131%
YoY, ammonia production +16% YoY at **121% factory utilisation**.
*Source: sahamdaily.com ESSA update, 24 Jul 2026.*

This is a hard, company-specific mark and it is the anchor for everything below.
My independently derived estimate from the P&L (revenue less an assumed
USD 55–60m LPG contribution, divided by volume) gave ~USD 477/t — within 5% of
the disclosed USD 455/t. **The spread model is calibrated against a verified
number, not a guess.**

**FACT / historical range.** Ammonia bottomed around USD 150–250/t FOB in 2020,
spiked above USD 1,000/t FOB Middle East in 2022 on the European gas crisis, and
traded USD 300–450/t through 2023–2025.

**INFERENCE — cycle position.** At USD 455–490/t, ESSA is realising roughly
**25–30% above its 2023–2025 average** and roughly **50–55% below the 2022
peak**. **Mid-to-upper-mid cycle. Not trough, not peak.** You are not buying
distressed earnings, and you are not paying for peak earnings either.

**This resolves the Priority 3 puzzle.** Revenue CAGR 3Y of −26% and
`Normalised/Trailing EBIT` of 0.85 are not in conflict. The −26% is measured
*from the 2022 spike*; the 0.85 says trailing EBIT sits above the 4-year
*median*. Both are true. The problem is the median itself: it is taken over
FY2022 (5,404), FY2023 (1,380), FY2024 (1,469), FY2025 (1,268) IDR bn, so it
**mechanically discards the 2022 spike and averages three consecutive trough
years**. Median = 1,424.15 — exactly the screener's Normalised EBIT (FACT).
**The screener's "mid-cycle" is a low-cycle number.** My bottom-up mid-cycle
EBIT is USD 97m = IDR 1,737bn, ~22% above it.

**FACT — Q2 2026 weakness has a benign explanation, and I initially misread it.**
H1 2026 net income was USD 30.17m (revenue USD 186.48m) versus H1 2025
USD 14.84m (USD 137.59m). Since Q1 2026 net income was USD 18.76m (IDR 335.9bn
per the screener), **Q2 2026 net income was only ~USD 11.4m — a 39% sequential
fall.** The cause: **the Banggai Ammonia Plant was shut down from 21 April to
8 June 2026 for a scheduled inspection and turnaround**, returning to full
operations at 23:00 WITA on 8 June. That is **~48 days of a 91-day quarter with
the plant down.**
*Source: sahamdaily.com, 24 Jul 2026.*

**INFERENCE — this is a positive, not a negative.** Earning USD 11.4m with the
principal asset offline for half the quarter is a good result, and it explains
the pattern precisely: **revenue held roughly flat QoQ (USD 95.2m → ~USD 91.3m)
while margin collapsed** — the signature of selling from inventory at full price
while absorbing fixed costs with no production. Corroborating: inventory built
to IDR 725.6bn at Q1 2026 from IDR 508.8bn a year earlier (FACT, screener).
**H2 2026 should be materially stronger with the plant fully operational into a
USD 450–490/t price. Do not extrapolate Q2.**

---

## 3. Growth capex — is the FCF actually available? (Priority 2)

The task flagged this as likely decisive. **The evidence is genuinely
contradictory and the contradiction is itself the finding.**

**FACT — what management guided in August 2026.** ESSA guided **2026 capex of
USD 10–20 million** (~IDR 180–360bn), described by Director Prakash Bumb as
**"protection capex"** — maintenance only, for existing LPG and ammonia
facilities. He stated new construction projects receive minimal 2026 allocation
because they remain at early development stage. The **Sustainable Aviation Fuel
(SAF)** project is at front-end engineering design, with a **2.5–3.5 year build
after commencement**. Management states the balance sheet funds everything
internally, no external financing needed.
*Sources: topbusiness.id; infobanknews.com (Aug 2026).*

**FACT — what was previously announced for Phase 2.** A **second-phase blue
ammonia plant** of **700,000 tpa**, estimated capex **USD 100–150 million
(~IDR 2.37 trillion)**, with a stated timeline of feasibility study Q4 2024,
**FID Q1 2025, construction start Q3 2025, commercial commissioning H1 2027**.
Market sources described ESSA as "certain to proceed." Rationale: Japanese
demand for low-carbon ammonia, committed at **2 Mt/yr by 2027 rising to 3 Mt/yr
by 2030**.
*Sources: bloombergtechnoz.com; insight.kontan.co.id.*

**INFERENCE — Phase 2 has slipped and is not under construction.** The two
disclosures cannot both be current. A project that took FID in Q1 2025 and broke
ground in Q3 2025 for H1 2027 commissioning would be consuming most of its
USD 100–150m budget *during 2026* — not USD 10–20m of protection capex. Actual
capex confirms management's version: **IDR 26–142bn per year, roughly 1% of a
IDR 11.6–12.4tn asset base** (FACT, screener). **Nothing is being built.**

**THESIS — so the answer to Priority 2 is: the FCF is currently uncommitted, but
this is a reprieve, not a resolution.** The 20% FCF yield is real cash today.
FY2025 FCF was IDR 1,721bn on capex of IDR 142bn; total debt is IDR 2.4bn
(i.e. nil); net cash is IDR 2,944.5bn = **IDR 171/share, 26% of the share
price**. But two 700 ktpa-scale ambitions (blue ammonia Phase 2, SAF) sit in the
pipeline with real strategic logic behind them (Japanese offtake). **The correct
treatment is to value the two existing assets on mid-cycle economics, assign
Phase 2 and SAF a value of zero in the base case, and treat an FID as the
principal downside event.** That is what §5 does.

**Valuation with vs without growth capex:**
- **Without** (base case, as modelled): net cash of USD 164m is added to EV in
  full → IDR 830/share.
- **With** an FID that consumes the net cash: **remove IDR 171/share
  immediately**, and expect dividends to be cut from the current IDR 52. Base IV
  falls to ~IDR 660 — i.e. **the stock is worth roughly the current price if
  management commits the balance sheet**, before crediting any project returns.
- The **USD 100–150m** Phase 2 figure is, notably, only **USD 143–214 per annual
  tonne** for 700 ktpa — versus the **USD 1,143/t** it actually cost to build
  Phase 1. ASSUMPTION: that figure is either a brownfield duplicate-train /
  debottleneck using existing jetty, utilities and gas infrastructure, or it is
  an equity contribution rather than total project cost. **If USD 100–150m is
  genuinely the all-in cost for 700 ktpa, the project is extraordinarily
  value-accretive and the bull case is far too low. This single question is
  worth more research than anything else in this report.**

---

## 4. The dividend is funded from the balance sheet — the screener is wrong

**The lead from the aborted run is confirmed and it is material.**

**FACT.** At the AGM of **18 June 2026**, ESSA declared a cash dividend of
**IDR 895.80 billion / IDR 52 per share** for FY2025 — equal to **125.59% of
FY2025 net income of USD 40.29 million**, with approximately **IDR 182.65
billion drawn from retained earnings** to fund the excess. FY2024 payout was
~23%. The per-share dividend is **5x the IDR 10 paid for 2024** and is the
**highest since the 2012 IPO**. Ex-date 26 June 2026; payment 15 July 2026.
Yield ~8.1% at IDR 645–650.
*Sources: pintarsaham.id; snips.stockbit.com (Stockbit Research, 22 Jun 2026);
sahamdaily.com.*

**FACT.** The screener reports `Payout Ratio 0.2023` — the **FY2024** figure.
**It is off by a factor of 6.2x.**

**Consequences:**
1. **The 8.2% yield cannot support a yield-based valuation.** INFERENCE: at
   mid-cycle earnings a sustainable payout is roughly **IDR 35–45/share**
   (5.3–6.9% at IDR 655) — still attractive, but not 8.2%. A DDM built on
   IDR 52 in perpetuity overvalues the equity by ~20–25%.
2. **The 5x jump from IDR 10 marks this as a special distribution**, not a new
   policy. Anyone underwriting ESSA on dividend growth is extrapolating a
   one-off.
3. INFERENCE (mildly positive): drawing IDR 183bn from a IDR 2,945bn net cash
   pile in a trough-earnings year is a deliberate return of surplus capital, not
   distress. It is **not** a red flag. It is a reason not to capitalise the
   current dividend — and, read alongside §3, weak evidence that management does
   *not* currently intend to fund Phase 2 from cash.

---

## 5. The valuation

### 5.1 Corrected starting point

**FACT — arithmetic error in the screener's enterprise value.**

| | IDR bn |
|---|---|
| Market cap (17,226,975,060 sh × 655) | 11,283.7 |
| Less: cash (Q1 2026) | (2,946.9) |
| Plus: total debt (Q1 2026) | 2.4 |
| **Correct EV** | **8,339.2** |
| Screener's reported EV | 10,939.1 |
| **Discrepancy** | **2,599.9 — 23% of market cap** |

The screener nets out only ~IDR 345bn of a IDR 2,945bn net cash position. Every
EV-based multiple it reports is therefore **too expensive**:

| Metric | Screener | Corrected |
|---|---|---|
| EV (IDR bn) | 10,939.1 | **8,339.2** |
| EV/EBIT (TTM EBIT 1,670.7) | 6.55x | **4.99x** |
| Acquirer's Multiple | 6.55 | **4.99** |
| Earnings Yield (EBIT/EV) | 15.3% | **20.0%** |
| EV (USD) | 610.8m | **465.7m** |

**This should be raised as a pipeline bug — it affects the Magic Formula and
Acquirer's Multiple for every net-cash-rich name in the universe.**

**FACT — the reported EBITDA is D&A-less, exactly as the task anticipated.**
FY2025 EBITDA − EBIT = IDR 53.9bn = **USD 3.0m of implied D&A** on a USD 800m
plant plus a refinery. Impossible. Corroborating: FY2025 operating cash flow
(derived as FCF − capex per the house convention) is IDR 1,862.8bn = USD 104m
against net income of USD 40.3m — a USD 64m gap which, after adjusting for the
~USD 18m working-capital build (inventory +IDR 156bn, receivables +IDR 169bn),
implies **non-cash charges of roughly USD 80m**. ASSUMPTION: true D&A is
**USD 40–70m/yr, central USD 55m** — consistent with USD 800m of plant over a
20–25 year life plus the LPG refinery.

**Consequence: `EV/EBITDA 6.25x` is meaningless. Do not use it. This analysis
uses EV/EBIT throughout, because EBIT is reported and reliable while EBITDA is
not.** (Note: the screener's suppression rule for D&A-less EBITDA did not fire
on this ticker — worth checking.)

### 5.2 The gas-to-ammonia spread model

**Structure (FACT where sourced, ASSUMPTION where derived):**
- Gas price (USD/MMBTU) is indexed to ammonia. Reference point: **USD 8.60/MMBTU
  at ammonia USD 730/t** (FACT). ASSUMPTION: approximately proportional
  indexation, i.e. gas ≈ ammonia × 0.01178.
- Gas intensity: 55 MMSCFD supporting 700 ktpa ≈ **29 MMBTU per tonne** of
  ammonia (ASSUMPTION, derived; consistent with a modern, efficient SMR train,
  and the plant is described as among the world's most efficient).
- Fixed costs (cash opex + SG&A + D&A, net of the LPG contribution): plugged at
  **USD 85m/yr** from FY2025 actuals (ASSUMPTION).

**Resulting spread ladder (INFERENCE):**

| Ammonia USD/t | Implied gas USD/MMBTU | Gas cost USD/t | **Spread USD/t** |
|---|---|---|---|
| 320 | 3.77 | 109 | 211 |
| 370 | 4.36 | 126 | 244 |
| 420 | 4.95 | 143 | 277 |
| 455 | 5.36 | 155 | 300 |
| 550 | 6.48 | 188 | 362 |
| 730 (disclosed ref.) | **8.60** | 249 | 481 |

**Flow-through: ~66% of any ammonia price move reaches the spread.**

**Model validation against two observed points (this is the test that matters):**

| | Ammonia | Volume | Gross spread | − fixed 85 | **Model EBIT** | **Actual EBIT** |
|---|---|---|---|---|---|---|
| FY2025 | ~370 | 640 kt | 156m | | **71m** | **70.8m** (IDR 1,267.5bn) |
| Q1 2026 ann. | 455 (FACT) | ~760 kt (121% util.) | 228m | | **143m** | **~136m** (IDR 607.9bn ×4) |

**The model reproduces both a trough year and a peak quarter to within ~5%.**
That is the basis for trusting the scenarios below.

### 5.3 Scenarios — explicit assumptions

| | **Bear** | **Base** | **Bull** |
|---|---|---|---|
| Ammonia realised, USD/t | **320** | **420** | **550** |
| Implied contracted gas, USD/MMBTU | 3.77 | 4.95 | 6.48 |
| Gas cost, USD/t | 109 | 143 | 188 |
| **Spread, USD/t** | **211** | **277** | **362** |
| Volume, kt | 620 (outage/demand) | 690 (~99% util.) | 720 (~103% util.) |
| Gross spread, USD | 131m | 191m | 261m |
| Less fixed costs, USD | (85m) | (85m) | (85m) |
| EBIT pre-contract-risk | 46m | 106m | 176m |
| 2027-28 gas renewal haircut | (6m) *bad renewal* | (9m) *modest reset* | 0 *renews on terms* |
| **Durable mid-cycle EBIT, USD** | **40m** | **97m** | **176m** |
| EV/EBIT multiple | 6.0x | **6.5x** | 6.0x *(peak compression)* |
| Implied EV, USD | 240m | 631m | 1,056m |
| Plus net cash, USD | +164m | +164m | +164m |
| Equity value, USD | 404m | 795m | 1,220m |
| Equity value, IDR bn | 7,236 | 14,238 | 21,847 |
| **IV per share, IDR** | **~440** | **~830** | **~1,250** |
| Upside vs 655 | **−33%** | **+27%** | **+91%** |

**Disaster case (not the bear case).** Trough ammonia *and* an FID that consumes
the net cash: 240m equity = **IDR 279/share, a 57% drawdown**. THESIS: this
requires management to commit the balance sheet into a price trough, which a
board distributing 126% of earnings is unlikely to do. But it is the number to
remember if an FID is announced.

**Multiple justification.** 6.5x EV/EBIT for a single-asset commodity chemicals
producer in Indonesia is neither generous nor punitive. Two offsetting
adjustments: **upward** for the ammonia-indexed gas contract (a genuine
structural hedge that lowers earnings volatility and eliminates negative-spread
shutdown risk) and a fortress balance sheet; **downward** for single-asset
concentration, single-field gas dependence, and the ~2027-28 contract cliff. I
have taken the contract risk as an explicit EBIT haircut rather than burying it
in the multiple.

### 5.4 Cross-checks

**Replacement cost per annual tonne (floor).** Corrected EV of **USD 465.7m**
against 700 kt of ammonia capacity = **USD 665 per annual tonne — attributing
zero value to the LPG refinery.** Against the **actual, verified build cost of
USD 800m / 700 kt = USD 1,143/t** in 2014-18 dollars (FACT, IFC syndication
release). Escalated at ~3%/yr to 2026, replacement cost is roughly
**USD 1,450–1,550/t**.

> **INFERENCE: ESSA trades at ~58% of the nominal historical cost of its own
> plant, and ~43–46% of estimated current replacement cost — before crediting
> the LPG business or the net cash.** At full replacement (700kt × USD 1,450 =
> 1,015m, + LPG ~80m, + net cash 164m = USD 1,259m), the equity would be
> **~IDR 1,309/share**.

This is a real asset-value floor argument and it underwrites the bull case. It
is not the base case, because nobody is building a merchant ammonia plant in
Sulawesi at these prices, so replacement value is not realisable near-term.

**Normalised owner-earnings yield.** Mid-cycle EBIT USD 97m, tax at 22% → NOPAT
USD 76m. Add back D&A ~USD 55m; deduct true maintenance capex. Actual capex has
run USD 1.4–7.9m/yr against D&A of ~USD 55m — implausibly low as a permanent
run-rate, but the plant is 2018-vintage and was just turned around. At
maintenance capex = D&A (the conservative treatment), owner earnings =
**USD 76m** = IDR 1,361bn = **IDR 79/share**. At a 9% required return that is
**IDR 878/share**; at 10%, IDR 790. **Corroborates the base case of IDR 830.**

**P/B (weak lens, but it anchors the bear).** Book value **IDR 484/share**
(equity IDR 8,333.6bn ÷ 17.227bn sh); trading at 1.35x. Mid-cycle ROE ≈ USD 68m
net income ÷ USD 465m equity ≈ **14.6%**. Beta of 0.206 is untrustworthy
(CLAUDE.md rule); at a floored COE of ~12% for an Indonesian single-asset
cyclical, justified P/B = (ROE − g)/(COE − g) with g = 2% → (14.6−2)/(12−2) =
**1.26x → IDR 610/share**. **INFERENCE: P/B is the most bearish lens and lands
just below the current price.** The gap to the EV/EBIT lens is entirely the
assumed mid-cycle ROE. P/B deserves low weight for a company whose book carries
a 2018 plant at depreciated cost while its output price has risen ~35% off the
trough — but it is a legitimate check that IDR 830 is not conservative.

**Convergence:**

| Lens | IV/share | Role |
|---|---|---|
| Mid-cycle EV/EBIT on the spread model | **830** | primary |
| Normalised owner earnings @9% | 878 | corroborating |
| Justified P/B | 610 | bear anchor |
| Replacement cost | ~1,309 | bull anchor / floor |
| Screener blended | 732 | — |

**Base IV: IDR 830. Bear IDR 440. Bull IDR 1,250.
Probability-weighted (25/50/25) = IDR 838.**

---

## 6. The single most important assumption

**The mid-cycle realised ammonia price per tonne** — but by a narrower margin
than a naive read of this business would suggest.

**Sensitivity at base volume (690kt) and multiple (6.5x):**

| Mid-cycle ammonia | Spread USD/t | Durable EBIT | IV/share | vs 655 |
|---|---|---|---|---|
| USD 320/t | 211 | 40m | 440 | −33% |
| USD 370/t | 244 | 63m | 618 | −6% |
| **USD 420/t** | **277** | **97m** | **830** | **+27%** |
| USD 470/t | 310 | 129m | 1,038 | +58% |
| USD 520/t | 343 | 152m | 1,187 | +81% |

**±USD 50/t ≈ ±IDR 154/share ≈ ±19% of base IV.** Ranked against everything
else:

| Driver | Swing tested | Impact on IV |
|---|---|---|
| **Mid-cycle ammonia price** | **±USD 50/t** | **±IDR 154** |
| Fixed cost base (the USD 85m plug) | ±USD 15m | ±IDR 114 |
| Gas contract renewal 2027-28 | ±15% on gas cost | ±IDR 113 |
| EV/EBIT multiple | ±1.0x | ±IDR 113 |
| Volume / utilisation | ±40 kt | ±IDR 84 |
| **Phase 2 / SAF FID** | **binary** | **−IDR 171 (net cash) if it happens** |

**THESIS — the breakeven.** At the current price of IDR 655, you are paying for
a mid-cycle ammonia price of roughly **USD 385/t**. Spot is USD 455–490. The
2023–2025 average was ~USD 370. **You are being asked to bet that the last three
years were a depressed period rather than the new normal — and today's price
gives you only a modest cushion if you are wrong.**

**The critical nuance the screener cannot see:** because gas is ammonia-indexed,
ESSA's earnings fall only ~66% as fast as the ammonia price. A naive spread
model with fixed gas would put the bear case near zero EBIT and the bull case
near USD 300m. The contract truncates both tails. **This is why the "Cyclical"
classification, while technically correct, overstates the risk — and it is the
best argument for owning this name.**

---

## 7. Why the existing screener valuation may be wrong

Seven defects, ranked by materiality:

1. **Enterprise value is wrong by IDR 2,600bn (23% of market cap).** Only
   IDR 345bn of a IDR 2,945bn net cash position is netted out. EV/EBIT reads
   6.55x when it is 4.99x; the Magic Formula earnings yield is understated by
   470bp. **Direction: the stock is cheaper than the screener says.** A pipeline
   bug, not a judgement call.
2. **Payout ratio is 125.6%, not 20.2%** — the screener carries the FY2024
   figure, a 6.2x error. Any dividend-sustainability logic is invalidated;
   sustainable payout is ~IDR 35–45/share, not IDR 52.
3. **The model is missing the defining feature of the business.** Gas is
   contractually indexed to ammonia. No generic screener can see this, and it
   changes the risk profile more than any single line item: it is why ESSA
   should not be valued like a merchant ammonia producer.
4. **EBITDA is D&A-less.** Implied D&A of USD 3.0m/yr is impossible; true D&A is
   ~USD 40–70m. `EV/EBITDA 6.25x` should have been suppressed and was not.
5. **"Normalised" EBIT is a low-cycle number, not mid-cycle.** The 4-year median
   discards the FY2022 spike and averages three trough years: IDR 1,424bn vs my
   bottom-up IDR 1,737bn (USD 97m) — 22% low. `Normalised/Trailing 0.85` reads
   as "trailing is above mid-cycle" when the honest statement is "trailing is
   above a depressed 4-year median."
6. **Comparables IV 805.9 uses the wrong peer set.** Peer group is "Oil & Gas
   Production & Refinery" (9 names) with a peer EV/EBIT median of 6.547 —
   **identical to ESSA's own multiple**, i.e. ESSA is effectively valued against
   itself. ESSA is a gas-to-chemicals converter, not an E&P; its correct
   comparables are nitrogen/ammonia producers, whose cycle, capital intensity
   and multiple all differ.
7. **Beta 0.206** would, unfloored, badly distort any discount-rate-sensitive
   output; and **the data stops at Q1 2026**, the strongest quarter, missing
   both the Q2 turnaround shutdown and the record dividend.

**Net effect:** defects 1, 3, 4 and 5 make the screener too *pessimistic*;
defects 2, 6 and 7 make it too *optimistic*. The pessimistic errors are larger,
which is why my base IV of 830 sits 13% above the screener's 732. **The screener
reached approximately the right verdict through substantially offsetting errors.
The WATCH label survives; the arithmetic behind it does not.**

---

## 8. Verdict and reasoning

**FAIRLY VALUED — at the undervalued end. A close call, and the closest thing to
a genuine opportunity in this analysis is the gap between what the business is
and what the screener thinks it is.**

**Not a value trap.** The balance sheet is pristine (net cash 26% of market cap,
debt/equity 0.0003, Altman Z 11.3, current ratio 11.5, F-Score 7). The asset is
real, running above nameplate, and trades at ~58% of what it cost to build. The
cash generation is genuine and currently uncommitted. The gas contract is a
structural hedge, not a liability. **Four of the five outcomes in the framework
are excluded: this is not a value trap, not a deep-value special situation, and
not expensive. It is a decent business at a modestly attractive price.**

At IDR 655 against a base IV of IDR 830, the margin of safety is **21%** — real,
but short of the 30% required, and it rests on one commodity price at a
mid-to-upper-mid point in its cycle with a contract cliff 12–24 months out.

**Price discipline: at IDR 581 the MOS reaches 30%.** That is 15% below spot and
15% above the 52-week low of 505 — **reachable, unlike most WATCH names.** This
is an actionable limit, not a theoretical one.

**What would change the verdict to UNDERVALUED:**
- **Confirmation that the gas contract is extended beyond 2027-28 on
  ammonia-indexed terms.** This alone is worth ~IDR 110/share and removes the
  largest un-analysable risk. *Highest-value catalyst.*
- Confirmation that Phase 2's USD 100–150m for 700 ktpa is a genuine all-in
  brownfield cost. At that capital intensity the project would roughly double
  capacity for ~15% of market cap and the bull case is far too low.
- H2 2026 confirming the post-turnaround run-rate at USD 450+/t ammonia.
- Price below IDR 581.

**What would change it to OVERVALUED / VALUE TRAP:**
- **FID on Phase 2 or SAF without a disclosed return.** Removes IDR 171/share of
  net cash, cuts the dividend, and converts a cash-returning cyclical into a
  capital-consuming one. **This is the single event to monitor.**
- **An adverse gas contract renewal**, or loss of the ammonia linkage. This
  would remove the structural hedge and justify a lower multiple as well as
  lower earnings — a double hit not captured in the bear case above.
- Ammonia sustaining below USD 350/t.
- Senoro field deliverability decline — single-field dependence on a 2015-vintage
  gas contract is an unhedged concentration.

---

## 9. Evidence gaps — insufficient evidence, requires further research

Each is material and each is resolvable from primary documents:

1. **The exact gas price formula and, above all, the contract expiry date and
   renewal status.** I have one reference point (USD 8.60/MMBTU at USD 730/t
   ammonia) and a tenor of "13 years from 2015, extendable." But the plant
   commissioned in late 2018, two years behind the original schedule — so
   whether the tenor runs from signing or from commercial operation date changes
   the expiry from ~2027 to ~2031. **This is the highest-value open question in
   the entire analysis** and it is worth ~IDR 110/share.
2. **Actual D&A from the FY2025 audited cash flow statement.** Currently a
   USD 40–70m assumption; drives the maintenance-capex charge in the
   owner-earnings cross-check.
3. **The true scope and status of blue ammonia Phase 2.** Is USD 100–150m the
   all-in cost for 700 ktpa, or an equity slice / debottleneck? Has FID been
   taken, deferred, or abandoned? The Aug 2026 capex guidance and the earlier
   project announcement are irreconcilable as stated.
4. **Segment disclosure: ammonia vs LPG revenue and volume split.** My fixed-cost
   plug of USD 85m nets out the LPG contribution and is the second-largest
   sensitivity (±IDR 114/share).
5. **ESSA's ownership percentage of PAU and any minority interest.** FY2025
   attributable net income of USD 40.29m matches the screener's NetIncome and
   book value reconciles, which suggests an attributable basis — but if PAU
   carries a minority, part of the IDR 2,945bn cash and the EBIT is not ESSA's,
   and all IVs fall. *Not resolved.*
6. **Whether a soda ash project exists.** No evidence found in any 2026 source.
   The projects that do appear are blue ammonia Phase 2 and SAF. INFERENCE: the
   soda ash lead in the task brief may be a misattribution — but absence of
   evidence from press coverage is not proof; check the FY2025 annual report.
7. **Senoro field reserve life and deliverability**, given 55 MMSCFD is
   effectively the plant's entire feedstock.
8. **SAF project capex and expected IRR** — at FEED with no disclosed figure.

---

## Sources

- [essa.id — PAU signs Syndication Agreement with IFC](https://essa.id/pt-panca-amara-utama-signs-syndication-agreement-to-build-greenfield-ammonia-plant-and-support-indonesias-manufacturing-sector-with-ifc/) — USD 800m project cost, 700 ktpa, USD 509m debt, IFC-led syndicate, 55 MMSCFD Senoro-Toili, 5 Sep 2014
- [essa.id — PAU receives MEMR approval for its gas price](https://essa.id/pt-surya-esa-perkasa-tbk-s-subsidiary-pt-panca-amara-utama-receives-approval-from-ministry-of-energy-mineral-resources-for-its-gas-price/) — **gas price indexed to ammonia; USD 8.60/MMBTU at ammonia USD 730/t**; JOBPMTS counterparty
- [ewsdata.rightsindevelopment.org — PT Panca Amara Utama (IFC-32198)](https://ewsdata.rightsindevelopment.org/projects/32198-pt-panca-amara-utama/) — 13-year gas contract 2015–2027 extendable, 55 MMSCFD, 700 ktpa, Batui/Banggai
- [sahamdaily.com — ESSA update 24 Juli 2026](https://www.sahamdaily.com/essa-update-24-juli-2026/) — **Q1 2026 realised ammonia USD 455/MT (+34% YoY), 121% utilisation; BAP turnaround 21 Apr – 8 Jun 2026**; dividend IDR 52 vs IDR 10 in 2024
- [topbusiness.id — ESSA Siapkan Capex US$10–20 Juta di 2026](https://www.topbusiness.id/119555/essa-siapkan-capex-us-10-20-juta-di-2026-fokus-operasional-lpg-dan-amonia.html) — 2026 protection capex only; SAF at FEED, 2.5–3.5 yr build
- [infobanknews.com — ESSA Fokus Operasional LPG dan Amoniak di 2026](https://infobanknews.com/essa-fokus-operasional-lpg-dan-amoniak-di-2026-siapkan-capex-segini/) — capex ~USD 20m; PAU 2,000 t/day
- [bloombergtechnoz.com — ESSA Dikabarkan Lanjutkan Proyek Pabrik Amonia Fase Kedua](https://www.bloombergtechnoz.com/detail-news/57392/essa-dikabarkan-lanjutkan-proyek-pabrik-amonia-fase-kedua) — Phase 2 blue ammonia 700 ktpa, capex USD 100–150m, FID Q1 2025 / construction Q3 2025 / commissioning H1 2027 (as announced)
- [marketscreener.com — ESSA H1 2026 earnings release](https://www.marketscreener.com/news/pt-essa-industries-indonesia-tbk-reports-earnings-results-for-the-half-year-ended-june-30-2026-ce7f51ddd189f620) — H1 2026 revenue USD 186.48m, net income USD 30.17m
- [pintarsaham.id — Dividen ESSA 2026](https://pintarsaham.id/dividen-essa-2026-essa-bagikan-dividen-tunai-rp89580-miliar-atau-rp52-per-saham/) — **IDR 52/sh, IDR 895.8bn, 125.59% payout, IDR 182.65bn from retained earnings**, AGM 18 Jun 2026
- [Stockbit Snips — ESSA Akan Bagikan Dividen dengan Indikasi Yield 8,1%](https://snips.stockbit.com/stockbit-research/essa-akan-bagikan-dividen-dengan-indikasi-yield-81) — payout ~125% vs ~23% in 2024; ex-date 26 Jun 2026
- [ChemAnalyst — Ammonia Prices, Trend, Chart, Index and Forecast](https://www.chemanalyst.com/Pricing-data/ammonia-37) — Tampa CFR ~USD 608/t quarterly avg; ME FOB USD 438/t Nov 2025
- [discoveryalert.com.au — Ammonia Prices Jump at Inland US Locations in 2026](https://discoveryalert.com.au/us-ammonia-market-fundamentals-2026-price-volatility/) — Mar 2026: ME FOB ~USD 490/t, Gulf ~USD 650/t CFR
- [insight.kontan.co.id — Harga Amonia serta Proyek SAF dan Blue Amonia](https://insight.kontan.co.id/news/harga-amonia-serta-proyek-saf-dan-blue-amonia-menyengat-saham-essa) — Japanese low-carbon ammonia demand 2 Mt/yr by 2027, 3 Mt/yr by 2030
- Screener fact sheet: `/home/user/datasharing/idx_picker/research/stocks/ESSA.md`
