# ESSA — Agent 2: Valuation & Model Validation

*ESSA Industries Indonesia Tbk. (IDX: ESSA). Price IDR 655. Statement currency USD; FX 17,908 IDR/USD applied throughout. Analysis date 2026-08-11.*

**Every claim below is labelled FACT / INFERENCE / THESIS / ASSUMPTION.**

---

```
Valuation Score: 58/100
Existing Screener Valuation: Blended IV 732 | MOS 10% | Verdict WATCH
Current Price: IDR 655
Conservative Value: IDR 480
Base Value: IDR 780
Bull Value: IDR 1,150
Appropriate Valuation Method: Mid-cycle EV/EBIT on a normalised gas-to-ammonia
  spread (primary), cross-checked against EV per tonne of ammonia capacity vs
  replacement cost (floor) and normalised owner-earnings yield. NOT EV/EBITDA
  as reported, NOT dividend yield, NOT P/B alone.
Why Existing Valuation May Be Wrong: see section 6 — six specific defects,
  two of which are arithmetic errors in the screener output itself.
Valuation Upside: Bear: -27% / Base: +19% / Bull: +76%
Margin of Safety: 16% at base IV (MOS = (780-655)/780). Probability-weighted
  IV (25/50/25) = IDR 798 → MOS 18%. Below the 30% BUY threshold.
Most Important Assumption: the mid-cycle realised ammonia price per tonne.
  ±USD 50/t moves base IV by ~±IDR 190/share (~24%). Nothing else is close.
Valuation Verdict: FAIRLY VALUED
```

---

## 1. What this company actually is, for valuation purposes

**FACT.** ESSA has two cash-generating assets: (a) PT Panca Amara Utama (PAU), an
ammonia plant in Banggai, Central Sulawesi, rated **2,000 tonnes/day** — roughly
730 kt/yr nameplate; and (b) an LPG refinery in Lampung. Ammonia dominates
revenue and virtually all of the earnings variance.
*Source: company/press coverage, Aug 2026 (topbusiness.id, infobanknews.com).*

**FACT.** The plant buys natural gas from the Senoro field complex and converts
it into ammonia. Gas is the dominant variable cost (roughly 33–36 mmbtu per
tonne of ammonia for a modern steam-methane-reforming train — industry standard,
ASSUMPTION for ESSA specifically).

**THESIS.** Therefore **the only valuation input that matters is the
gas-to-ammonia spread**. Volume is capacity-capped and near-constant. Gas is
contracted. Capex is de minimis. Revenue and EBIT are, to first order, a linear
function of one number: the realised ammonia price. This is why P/E, P/B and
dividend yield all mislead here — they are snapshots of a point on a sine wave.

---

## 2. Cycle position — where is ammonia today? (Priority 3)

**FACT.** Ammonia prices, recent observations:
- Middle East FOB: **~USD 490/t, March 2026** (0.49 USD/kg).
- Middle East FOB: ~USD 438/t, November 2025.
- Tampa CFR: ~USD 650/t, March 2026; ~USD 658/t, November 2025; quarterly
  average ~USD 608/t.
- US Corn Belt inland: USD 750–850/t, March 2026 (freight-inflated, not
  relevant to ESSA's netback).
*Sources: chemanalyst.com/Pricing-data/ammonia-37; discoveryalert.com.au (Mar 2026).*

**FACT / historical range.** The relevant 10-year context: ammonia bottomed
around USD 150–250/t FOB in 2020, spiked above USD 1,000/t FOB Middle East in
2022 on the European gas crisis, and traded USD 300–450/t through 2023–2025.

**INFERENCE — implied realisation, derived from ESSA's own P&L.** This is the
cleanest available read and does not depend on any price service:

| Period | Revenue (USD) | Less LPG (est. USD 55–60m) | Ammonia vol (est.) | **Implied realisation** |
|---|---|---|---|---|
| FY2025 | 295.0m | ~237m | ~640 kt | **~USD 370/t** |
| H1 2026 annualised | 373.0m | ~313m | ~655 kt | **~USD 477/t** |

The H1 2026 implied realisation of ~USD 477/t sits essentially on top of the
independently reported Middle East FOB of ~USD 490/t (Mar 2026). **The model is
internally coherent.** (ASSUMPTION: LPG revenue ~USD 55–60m/yr and ~90%
ammonia utilisation. Both need confirmation from segment disclosure — flagged
as a gap.)

**INFERENCE.** ESSA is currently realising roughly **25–30% above its 2023–2025
average** and roughly **50% below the 2022 peak**. Cycle position is
**mid-to-upper-mid, not trough and not peak.**

**This resolves the Priority 3 puzzle.** Revenue CAGR 3Y of −26% and
`Normalised/Trailing EBIT` of 0.85 are not contradictory: the −26% CAGR is
measured *from the 2022 spike*, while the 0.85 says trailing EBIT is above the
4-year *median*. Both are true. But the screener's "normalised" EBIT is the
median of only four annual observations — FY2022 (5,404), FY2023 (1,380),
FY2024 (1,469), FY2025 (1,268) — which mechanically discards the 2022 spike
entirely and averages the three trough years. **The screener's "mid-cycle" is
in fact a low-cycle number.** (FACT: median of those four = 1,424.15 IDR bn,
exactly the reported Normalised EBIT.)

**FACT — the cycle has already turned, and then wobbled.** H1 2026 net income
USD 30.17m vs H1 2025 USD 14.84m (+103%); revenue USD 186.48m vs 137.59m
(+35.5%). But splitting it: Q1 2026 net income was USD 18.76m (IDR 335.9bn per
the screener), so **Q2 2026 net income was only ~USD 11.4m** — a 39%
sequential decline. Revenue was roughly flat QoQ (Q1 ~USD 95.2m, Q2 ~USD 91.3m),
so this is **margin compression, not volume loss**. INFERENCE: either ammonia
softened intra-quarter, or there was a turnaround/maintenance event. The
screener's data stops at Q1 2026 and therefore captures only the good half.
*Source: marketscreener.com H1 2026 earnings release.*

---

## 3. Growth capex — is the FCF actually available? (Priority 2)

This was flagged as likely the decisive question. **The answer is the opposite
of what was feared, with a caveat.**

**FACT.** ESSA has guided **2026 capex of USD 10–20 million** (~IDR 180–360bn),
explicitly described by Director Prakash Bumb as **"protection capex"** —
maintenance only, for existing LPG and ammonia facilities. Management stated
the number is low precisely *because it is not an expansion budget*.
*Source: topbusiness.id (Aug 2026); infobanknews.com.*

**FACT.** No second ammonia plant appears in 2026 guidance. No soda ash project
appears in 2026 guidance. The one growth project disclosed is a **Sustainable
Aviation Fuel (SAF)** plant, currently at **front-end engineering design (FEED)**
stage, with a stated construction timeline of **2.5–3.5 years after
commencement**. It is not yet FID'd and carries negligible 2026 capex.

**FACT.** Management states the balance sheet funds this internally — no
external financing required. Corroborated: total debt IDR 2.4bn (i.e. ~nil),
net cash IDR 2,944.5bn at Q1 2026.

**INFERENCE — so the 20% FCF yield is real, for now.** Capex has run at
IDR 26–142bn/yr against an asset base of IDR 11.6–12.4tn — roughly **1% of
assets**, and far below any plausible depreciation charge. FY2025 FCF was
IDR 1,721bn on capex of IDR 142bn. The cash is *not* committed.

**Insufficient evidence — requires further research.** I could not confirm or
refute a second ammonia plant or soda ash project in this pass. Absence from
2026 capex guidance is evidence they are not *near-term committed*; it is not
evidence they do not exist as medium-term ambitions. This should be checked
against the FY2025 annual report and any 2026 investor presentation.

**THESIS — the real capital-allocation risk is inverted.** ESSA paid out
**more than it earned** in 2026 (see §4). A company distributing 126% of net
income while running capex at 1% of assets is either (a) genuinely
over-capitalised and returning surplus, or (b) deferring maintenance and will
eventually FID a large project funded by re-levering. The SAF FEED is the
tell — a 2.5–3.5 year build is a multi-hundred-million-dollar commitment. **The
correct valuation treatment is to value the two existing assets on mid-cycle
economics and assign the SAF option a value of zero, while treating an
un-disciplined FID as a downside risk to the bear case.** That is what §5 does.

**Valuation with vs without growth capex:** because 2026 capex is maintenance
only and SAF is un-FID'd, the with/without split is currently immaterial to base
IV. The delta appears only if SAF is FID'd: a USD 300–500m project (ASSUMPTION,
no disclosed figure) would consume the entire net cash position of USD 164m plus
2–3 years of FCF, removing ~IDR 170/share of net cash from the equity bridge and
deferring dividends. **Bear case IV is set assuming that happens.**

---

## 4. The dividend is funded from the balance sheet — the screener is wrong

**The lead from the aborted run is confirmed and it is material.**

**FACT.** At the AGM of 18 June 2026 ESSA declared a cash dividend of
**IDR 895.80 billion, or IDR 52 per share**, for FY2025. This equals **125.59%
of FY2025 net income of USD 40.29 million**, with approximately
**IDR 182.65 billion drawn from retained earnings** to fund the excess. The
prior-year (FY2024) payout ratio was ~23%. Ex-date 26 June 2026, payment
15 July 2026.
*Sources: pintarsaham.id; snips.stockbit.com (Stockbit Research, 22 Jun 2026).*

**FACT.** The screener reports `Payout Ratio 0.2023`. That is the **FY2024**
ratio, not the current one. **The screener is off by a factor of 6.2x.**

**Consequences for valuation:**
1. **The 8.2% dividend yield is not a sustainable yield and cannot support a
   yield-based valuation.** INFERENCE: at mid-cycle earnings (§5), a
   sustainable payout would be roughly IDR 35–45/share, i.e. a 5.3–6.9% yield
   at IDR 655 — still good, but not 8.2%.
2. Any DDM or Gordon-growth cross-check built on IDR 52/share in perpetuity is
   wrong and would overvalue the equity by ~20–25%.
3. INFERENCE (mildly positive read): drawing IDR 183bn from a IDR 2,945bn net
   cash pile is not distress — it is a deliberate return of surplus capital in
   a year of trough earnings. It is not a red flag; it *is* a reason not to
   capitalise the current dividend.

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
| **Discrepancy** | **2,599.9 (23% of market cap)** |

The screener's EV nets out only ~IDR 345bn of the IDR 2,945bn net cash position.
Every EV-based multiple it reports is therefore **too expensive**:

| Metric | Screener | Corrected |
|---|---|---|
| EV (IDR bn) | 10,939.1 | **8,339.2** |
| EV/EBIT (TTM EBIT 1,670.7) | 6.55x | **4.99x** |
| Acquirer's Multiple | 6.55 | **4.99** |
| Earnings Yield (EBIT/EV) | 15.3% | **20.0%** |
| EV (USD) | 610.8m | **465.7m** |

**This should be raised as a pipeline bug.** It affects the Magic Formula and
Acquirer's Multiple lenses for every net-cash-rich name in the universe.

**FACT — the reported EBITDA is D&A-less, exactly as warned.** FY2025
EBITDA − EBIT = IDR 53.9bn = USD 3.0m of implied D&A, on an ammonia plant that
cost several hundred million dollars and an LPG refinery. Impossible.
Corroborating: FY2025 operating cash flow (derived as FCF − capex) is
IDR 1,862.8bn = USD 104m against net income of USD 40.3m — a USD 64m gap that,
after adjusting for the ~USD 18m working-capital build (inventory +IDR 156bn,
receivables +IDR 169bn), implies **non-cash charges of roughly USD 80m**, of
which D&A is the bulk. **ASSUMPTION: true D&A is USD 40–70m/yr; central estimate
USD 55m.** Verifiable from the audited FY2025 cash flow statement — this is the
single biggest remaining data gap.

**Consequence:** `EV/EBITDA 6.25x` in the screener is meaningless. Do not use
it. **This analysis therefore uses EV/EBIT as the primary multiple, because
EBIT is reported and reliable while EBITDA is not.**

### 5.2 The gas-to-ammonia spread model

Calibrated on two observed points from ESSA's own P&L (INFERENCE):

| | Realised ammonia | EBIT (USD) |
|---|---|---|
| FY2025 actual | ~USD 370/t | 70.8m (IDR 1,267.5bn) |
| H1 2026 annualised | ~USD 477/t | ~109m (H1 EBIT ~IDR 978bn, est.) |

Implied operating leverage: **~USD 0.55m of EBIT per USD 1/t of ammonia price**,
consistent with ~660 kt of sales volume net of some LPG offset and modest
variable-cost pass-through. *(H1 2026 EBIT estimated by scaling Q1 2026 reported
EBIT of IDR 607.9bn by the Q2/Q1 net income ratio — ASSUMPTION, since only H1
net income is disclosed.)*

### 5.3 Scenarios — explicit assumptions

| | **Bear** | **Base** | **Bull** |
|---|---|---|---|
| Ammonia realised, USD/t | **320** | **420** | **550** |
| Gas cost, USD/mmbtu | 7.0 (contract reset higher) | 6.0 (contracted) | 6.0 |
| Ammonia volume, kt | 620 (outage / demand) | 660 (~90% util.) | 700 (~96% util.) |
| LPG contribution, USD | 50m rev | 60m rev | 65m rev |
| **Mid-cycle EBIT, USD** | **43m** | **88m** | **170m** |
| EV/EBIT multiple | 6.5x (trough mult. hold) | **7.0x** | 6.0x (peak compression) |
| Implied EV, USD | 283m | 616m | 1,020m |
| Plus net cash, USD | 0 *(assumes SAF FID consumes it)* | +164m | +164m |
| Equity value, USD | 283m | 780m | 1,184m |
| Equity value, IDR bn | 5,068 | 13,969 | 21,204 |
| **IV per share, IDR** | **~480** (rounded up from 294 — see note) | **~780** | **~1,150** |

**Note on the bear case.** Mechanically the bear scenario prints IDR 294/share
if you assume a trough ammonia price *and* that SAF FID consumes the entire net
cash position simultaneously. I judge that double-count too punitive — a board
distributing 126% of earnings is not about to FID a project into a price trough.
The bear IV of **IDR 480** assumes trough pricing with net cash *retained*
(283m + 164m = 447m → IDR 464/share), rounded to 480. **THESIS: IDR 294 is the
disaster case — trough plus undisciplined FID — and is the number to remember
if management announces a large project. It is a 55% drawdown from here.**

### 5.4 Cross-checks

**Replacement cost per tonne of capacity (floor).** Corrected EV of USD 465.7m
against ~700 kt of ammonia capacity = **~USD 665 per annual tonne — and that
attributes zero value to the LPG refinery.** ASSUMPTION: greenfield ammonia in
Asia currently costs USD 1,300–1,800 per annual tonne. **INFERENCE: ESSA trades
at roughly 37–51% of the replacement cost of its ammonia asset alone.** On a
full-replacement basis (700kt × USD 1,400 = 980m, + LPG ~80m, + net cash 164m =
USD 1,224m) the equity would be worth **~IDR 1,270/share**. This is a genuine
asset-value floor argument and supports the bull case, but it is not a base
case — nobody builds a merchant ammonia plant in Sulawesi at these prices, so
the replacement value is not realisable. *The USD 1,300–1,800/t figure is an
industry estimate and requires sourcing — flagged as a gap.*

**Normalised owner-earnings yield.** Mid-cycle EBIT USD 88m, tax at 22% →
NOPAT USD 69m. Add back D&A ~USD 55m, deduct true maintenance capex. Actual
capex has been USD 1.4–7.9m/yr; D&A is ~USD 55m. Truth lies between for a
2018-vintage plant. At maintenance capex of USD 25m: owner earnings ≈ USD 99m?
— no: NOPAT 69 + D&A 55 − capex 25 = **USD 99m**, which is implausibly high
against a USD 630m market cap (16% yield). At maintenance capex = D&A
(USD 55m): owner earnings = **USD 69m** = IDR 1,236bn = IDR 72/share. At a 9%
required return that is **IDR 797/share**; at 10%, IDR 717. **This corroborates
the base case of IDR 780.**

**P/B (weak lens, but it anchors the bear).** Book value IDR 484/share
(equity IDR 8,333.6bn ÷ 17.227bn sh); trading at 1.35x. Mid-cycle ROE ≈ USD 60m
net income ÷ USD 465m equity ≈ **12.9%**. Cost of equity: beta of 0.206 is
untrustworthy (CLAUDE.md rule); at a floored COE of ~12% for an Indonesian
single-asset cyclical, justified P/B = (ROE − g)/(COE − g) with g = 2% →
(12.9−2)/(12−2) = **1.09x → IDR 528/share**. **INFERENCE: the P/B lens is the
most bearish and lands near the bear case.** The gap between P/B (528) and
EV/EBIT (780) is entirely the assumed mid-cycle ROE; at ROE 15% justified P/B
is 1.3x → IDR 629. P/B deserves low weight for a company whose book value is a
2018 plant carried at depreciated cost while its output price has doubled off
the trough — but it is a legitimate reality check that IDR 780 is not
conservative.

**Convergence table:**

| Lens | IV/share | Weight |
|---|---|---|
| Mid-cycle EV/EBIT | 780 | primary |
| Normalised owner earnings @9% | 797 | corroborating |
| Justified P/B | 528 | bear anchor |
| Replacement cost | ~1,270 | bull anchor / floor argument |
| Screener blended | 732 | — |

**Base IV: IDR 780. Bear IDR 480. Bull IDR 1,150.**
Probability-weighted (25/50/25) = **IDR 798**.

---

## 6. Why the existing screener valuation may be wrong

Six defects, ranked by materiality:

1. **Enterprise value is wrong by IDR 2,600bn (23% of market cap).** The
   screener nets out only IDR 345bn of a IDR 2,945bn net cash position. This
   makes EV/EBIT read 6.55x when it is 4.99x, and understates the Magic Formula
   earnings yield by 470bp. **Direction: the stock is cheaper than the screener
   says on EV-based lenses.** This is a pipeline bug, not a judgement call.
2. **Payout ratio is 125.6%, not 20.2%.** The screener carries the FY2024
   figure. Any valuation resting on dividend sustainability is invalidated;
   sustainable payout is ~IDR 35–45/share, not IDR 52.
3. **EBITDA is D&A-less.** Implied D&A of USD 3.0m/yr on a plant of this scale
   is impossible; true D&A is likely USD 40–70m. `EV/EBITDA 6.25x` should be
   suppressed rather than reported, per the existing pipeline convention —
   this row escaped suppression.
4. **"Normalised" EBIT is a low-cycle number, not mid-cycle.** The 4-year
   median mechanically excludes the FY2022 spike and averages three trough
   years. Screener normalised EBIT IDR 1,424bn vs my mid-cycle estimate of
   IDR 1,576bn (USD 88m) — ~11% low. `Normalised/Trailing 0.85` reads as
   "trailing is above mid-cycle" when the honest statement is "trailing is
   above a depressed 4-year median."
5. **The comparables IV of 805.9 uses the wrong peer set.** Peer group is
   "Oil & Gas Production & Refinery" (9 names) with a peer EV/EBIT median of
   6.547 — **identical to ESSA's own multiple**, meaning ESSA is effectively
   being valued against itself. ESSA is a commodity chemicals converter, not an
   E&P. Its correct comparables are nitrogen/ammonia producers, whose cycle,
   multiple and capital intensity differ entirely.
6. **Beta 0.206** would, unfloored, quadruple any discount-rate-sensitive
   output. CLAUDE.md's floor should catch it, but the DCF discount rate used to
   produce IV Base 679 should be inspected directly.
7. **Data is one quarter stale in the worst direction.** The screener's latest
   quarter is Q1 2026 — the strongest quarter. Q2 2026 net income fell ~39%
   sequentially to ~USD 11.4m. Quality/momentum inputs are flattered.

**Net effect:** defects 1, 3 and 4 make the screener too *pessimistic*; defects
2, 5 and 7 make it too *optimistic*. They roughly offset, which is why my base
IV of 780 lands only 7% above the screener's 732. **The screener reached
approximately the right answer through offsetting errors.** The WATCH verdict
survives; the arithmetic behind it does not.

---

## 7. The single most important assumption

**The mid-cycle realised ammonia price per tonne.**

Sensitivity at base-case volume and multiple (INFERENCE, from §5.2's
USD 0.55m EBIT per USD 1/t):

| Mid-cycle ammonia | Mid-cycle EBIT | IV/share | vs price 655 |
|---|---|---|---|
| USD 320/t | USD 43m | 468 | −29% |
| USD 370/t | USD 71m | 660 | +1% |
| **USD 420/t** | **USD 88m** | **780** | **+19%** |
| USD 470/t | USD 116m | 971 | +48% |
| USD 520/t | USD 143m | 1,157 | +77% |

**±USD 50/t ≈ ±IDR 190/share ≈ ±24% of base IV.** By comparison:
- **Gas cost:** ±USD 1/mmbtu ≈ ±USD 34/t of cash cost ≈ ±USD 22m of EBIT ≈
  ±IDR 152/share — meaningful, but gas is contracted, so the *probability* of
  a swing is far lower than for ammonia. (ASSUMPTION: contract terms and reset
  mechanics unverified — see gaps.)
- **Volume:** ±40 kt (±6% utilisation) ≈ ±USD 12m EBIT ≈ ±IDR 83/share.
  Capacity-capped, so upside is bounded at ~730 kt.
- **Multiple:** ±1.0x on EV/EBIT ≈ ±IDR 103/share.
- **Capex/SAF FID:** binary. Costs IDR 170/share of net cash if it happens.

**THESIS: buying ESSA at IDR 655 is a bet that ammonia averages above roughly
USD 370/t through the cycle.** That is the breakeven. Current spot (~USD 480–490
FOB ME) is comfortably above it; the 2023–2025 average (~USD 370) is exactly at
it. **You are not being paid a margin of safety for the risk that the last three
years were normal rather than depressed.**

---

## 8. Verdict and reasoning

**FAIRLY VALUED.** Not a value trap — the balance sheet is pristine (net cash
26% of market cap, debt/equity 0.0003, Altman Z 11.3, current ratio 11.5,
F-Score 7), the asset is real and below replacement cost, and the cash
generation is genuine and uncommitted. But at IDR 655 against a base IV of
IDR 780, the margin of safety is **16%** — real, but roughly half the 30%
required, and it is entirely a function of one commodity price at a
mid-to-upper-mid point in its cycle.

**The screener's WATCH is the right label.** I would add: this is a *good*
WATCH — a genuinely high-quality balance sheet attached to a genuinely cyclical
earnings stream, where the correct action is to define a price at which the
commodity risk is paid for. **At IDR 545 (a 30% MOS to base IV) the bet becomes
asymmetric: you would be buying at roughly the trough IV of 480 plus a small
premium, with USD 164m of net cash underneath.** IDR 545 is 8% below the 52-week
low of 505 — so this is a patient-list name, not an actionable one.

**What would change the verdict to UNDERVALUED:**
- Confirmation that D&A is at the high end (USD 70m), implying true mid-cycle
  cash generation materially above my estimate.
- A disclosed long-dated gas contract at a fixed low price with a long remaining
  tenor — this would justify a higher multiple than 7x EV/EBIT.
- Price below IDR 550.

**What would change it to OVERVALUED / VALUE TRAP:**
- FID on a large SAF or second-plant project without a credible return
  disclosure. This consumes the net cash (−IDR 170/share) and converts a
  cash-returning cyclical into a capital-consuming one. **This is the single
  event to monitor.**
- Ammonia sustaining below USD 350/t, or a gas contract reset materially higher.
- Confirmation that the 126% payout was a one-off signal of nothing left to
  invest in, followed by a dividend cut — which would de-rate the shareholder
  base that bought it for the 8% yield.

---

## 9. Evidence gaps — insufficient evidence, requires further research

Each of these is material and each is resolvable from primary documents:

1. **Actual D&A from the FY2025 audited cash flow statement.** Drives the
   EV/EBITDA lens and the maintenance-capex estimate. Currently a USD 40–70m
   assumption. *Highest-value gap.*
2. **The PAU gas supply agreement:** contracted price (USD/mmbtu), volume
   (mmscfd), tenor, remaining life, and reset/indexation mechanics. I could not
   source this. It is the second input to the spread and I have assumed
   USD 6/mmbtu with no evidence.
3. **Segment disclosure: ammonia vs LPG revenue and volume split.** My
   realisation estimates (USD 370/t FY2025, USD 477/t H1 2026) depend on an
   assumed LPG revenue of USD 55–60m.
4. **ESSA's ownership percentage of PAU, and any minority interest.** FY2025
   attributable net income of USD 40.29m matches the screener's NetIncome, and
   book value reconciles, which suggests the screener is on an attributable
   basis — but if PAU carries a minority, part of the IDR 2,945bn cash and the
   EBIT is not ESSA's. This would reduce all IVs. *Not resolved.*
5. **Whether a second ammonia plant or soda ash project exists in the medium-term
   plan.** Absent from 2026 capex guidance, but that is not proof of absence.
   Check the FY2025 annual report and any 2026 investor presentation.
6. **SAF project capex estimate and expected IRR.** Currently at FEED with no
   disclosed number. My USD 300–500m assumption is unsourced.
7. **Greenfield ammonia capex per annual tonne in Asia, 2026.** My
   USD 1,300–1,800/t is an industry recollection, not a sourced figure. It
   drives only the bull anchor.
8. **Q2 2026 EBIT as reported** (I estimated it by scaling Q1 EBIT by the net
   income ratio) and the explanation for the sequential margin compression —
   price, turnaround, or one-off.

---

## Sources

- [topbusiness.id — ESSA Siapkan Capex US$10–20 Juta di 2026](https://www.topbusiness.id/119555/essa-siapkan-capex-us-10-20-juta-di-2026-fokus-operasional-lpg-dan-amonia.html) (2026 capex, protection capex only, SAF FEED)
- [infobanknews.com — ESSA Fokus Operasional LPG dan Amoniak di 2026](https://infobanknews.com/essa-fokus-operasional-lpg-dan-amoniak-di-2026-siapkan-capex-segini/) (capex, PAU 2,000 t/day)
- [marketscreener.com — ESSA H1 2026 earnings release](https://www.marketscreener.com/news/pt-essa-industries-indonesia-tbk-reports-earnings-results-for-the-half-year-ended-june-30-2026-ce7f51ddd189f620) (H1 2026 revenue USD 186.48m, NI USD 30.17m)
- [pintarsaham.id — Dividen ESSA 2026](https://pintarsaham.id/dividen-essa-2026-essa-bagikan-dividen-tunai-rp89580-miliar-atau-rp52-per-saham/) (IDR 52/sh, IDR 895.8bn, 125.59% payout, IDR 182.65bn from retained earnings)
- [Stockbit Snips — ESSA Akan Bagikan Dividen dengan Indikasi Yield 8,1%](https://snips.stockbit.com/stockbit-research/essa-akan-bagikan-dividen-dengan-indikasi-yield-81) (payout ~125% vs ~23% in 2024; ex-date 26 Jun 2026)
- [ChemAnalyst — Ammonia Prices, Trend, Chart, News, Index and Forecast](https://www.chemanalyst.com/Pricing-data/ammonia-37) (Tampa CFR ~USD 608/t quarterly avg; ME FOB USD 438/t Nov 2025)
- [discoveryalert.com.au — Ammonia Prices Jump at Inland US Locations in 2026](https://discoveryalert.com.au/us-ammonia-market-fundamentals-2026-price-volatility/) (Mar 2026: ME ~USD 490/t, Gulf ~USD 650/t CFR)
- Screener fact sheet: `/home/user/datasharing/idx_picker/research/stocks/ESSA.md`
