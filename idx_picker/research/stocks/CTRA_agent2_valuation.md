# CTRA — Agent 2: Valuation & Model Validation

*PT Ciputra Development Tbk. | IDX: CTRA | Price IDR 630 | Review date 2026-08-10*
*All figures IDR unless noted. Every claim labelled FACT / INFERENCE / THESIS / ASSUMPTION.*

---

```
Valuation Score: 65/100
Existing Screener Valuation:   Blended IV 1,499 (EPV 1,228 @50% / Comparables 1,783 @30% / DCF base 1,750 @20%)
Current Price:                 630
Conservative Value:            600
Base Value:                    1,000
Bull Value:                    1,400
Appropriate Valuation Method:  SOTP (recurring capitalised separately) + historical P/B band,
                               cross-checked by mid-cycle P/E and justified P/B; RNAV as a
                               ceiling and asset-backing test, NOT as a target
Why Existing Valuation May Be Wrong: the peer-comparables lens (30% weight) is the single
                               largest error, not the normalised EBIT; the screener also omitted
                               justified P/B entirely and credited 100% of net cash to the parent
Valuation Upside:              Bear: −4.8% / Base: +58.7% / Bull: +122.2%
Margin of Safety:              37.0% at base (screener claimed 58%)
Most Important Assumption:     the exit multiple — that CTRA re-rates to ~0.75x book, its 3-to-5
                               year average, which is a call on the Indonesian 10-year yield.
                               Worth ±14% of the valuation per 100bp of cost of equity, roughly
                               double the sensitivity to the entire presales re-normalisation.
Valuation Verdict:             UNDERVALUED (materially, but ~37% MOS, not 58% — and the discount
                               is compensation for duration, not a mispricing waiting to close)
```

---

## 1. Framework — and why EPV and DCF are the wrong primary lenses here

**THESIS.** Three characteristics make CTRA a P/B-and-SOTP name, not an EPV-and-DCF name:

1. **FACT.** Land sits in inventory (Rp13,059.6bn) and Land for Development (Rp9,906.2bn) at
   **historical cost**, some of it a Surabaya/Tangerang basis decades old (Agent 3, AR 2025).
   Book therefore understates assets, and any lens that ignores the balance sheet ignores
   most of what you are buying.
2. **FACT.** Revenue is recognised on **handover**, not on sale. Reported earnings are a
   1–2 year lagged echo of presales. A DCF built off trailing earnings is a DCF of the past.
3. **FACT.** ~61% of presales run through joint operations (KSO) and NCI is Rp2,879bn
   (10.5% of total equity, Q2-26). Consolidated EBIT and consolidated cash are not the parent's.
   EPV, which capitalises consolidated EBIT and adds 100% of net cash, systematically
   over-credits the parent.

**FACT — the screener never ran the one lens most suited to this business.** `Justified PB IV`
in `CTRA.md` is **blank**. `scoring.py` reserves justified-P/B for financials, so the blend for
a property developer is built entirely from EPV, an EV/EBIT-and-PE comparables median, and a
DCF — three lenses that share one input (normalised EBIT) and no asset lens at all. That is a
structural gap in the pipeline, not a CTRA-specific misfire.

**The central conceptual point of this report, and the thing that reconciles the bulls and the
bears:**

> **THESIS — RNAV and earnings value are not additive. They are the same value counted twice.**
> CTRA's 48–49% gross margin is *precisely the mechanism* by which the historic-cost land
> discount is released into the P&L. Capitalise the earnings and you have already valued the
> land bank — at the pace at which it can actually be monetised. BRIDS' RNAV of Rp4,469/share
> values the identical asset as though it could be monetised now, at no discount rate. The
> difference between Rp4,469 and Rp630 is not a mispricing; it is 15–20 years of duration
> discounted at ~13%. Anyone who adds "0.48x book" and "86% discount to RNAV" together as two
> reasons to buy is double-counting one fact.

That is why the base case below is built from earnings-and-multiple lenses with RNAV used only
as a **ceiling and an impairment test on book value** — never as a target.

---

## 2. Re-normalising EBIT — the presales-to-revenue transfer function

The task set by the committee: the screener anchored every lens on normalised EBIT of
Rp3,401bn, recording `Normalised/Trailing EBIT = 0.998`. What is the forward base once the
2025–26 presales vintages flow through?

**FACT — presales history** (KBVS Research Exhibits 4–5, 4 Nov 2025; Agent 3 from AR 2025):

| Year | Presales (Rp bn) | YoY |
|---|---|---|
| 2020 | 5,493 | — |
| 2021 | 7,427 | +35.2% |
| 2022 | 8,244 | +11.0% |
| 2023 | 10,242 | +24.2% |
| 2024 | 11,017 | +7.6% |
| 2025 | 9,461 | **−14.1%** |
| 2026 target | 9,500 | +0.4% (H1 actual 4,690, **−18%**) |

**FACT — segment revenue split, FY2025** (AR 2025 p.39, via Agent 3): residential development
Rp10,259.5bn (81.3%), commercial/recurring Rp2,357.2bn (18.7%, gross margin 42.8%).

**INFERENCE — the transfer function is a one-year lag at ~0.89x, and it is remarkably stable.**
Development revenue in year *t* against presales in year *t−1*:

| | Dev revenue (Rp bn) | Presales t−1 | Ratio |
|---|---|---|---|
| 2023 | ~7,095 | 8,244 | 0.86 |
| 2024 | ~8,911 | 10,242 | 0.87 |
| 2025 | 10,259.5 | 11,017 | 0.93 |

(Recurring revenue estimated at ~2,150 / ~2,277 / 2,357 for 2023/24/25; the 2025 figure is a
disclosed FACT, the earlier two are INFERENCE from KBVS's +5.4% recurring growth forecast.)
A one-year lag fits a landed-house developer — 84% of presales are landed residential and the
build cycle is 12–18 months. The two-year-lag ratios (0.96 / 1.08 / 1.00) are noisier.

**Forward build (INFERENCE, with ASSUMPTIONS flagged):**

| | Presales driver | Dev revenue @0.89 | Recurring | Total revenue |
|---|---|---|---|---|
| FY2026E | 9,461 (FY25 actual) | 8,420 | 2,450 | **10,870** |
| FY2027E | 8,700 (ASSUMPTION: FY26 lands −8%) | 7,743 | 2,550 | **10,293** |
| FY2028E | 9,100 (ASSUMPTION: FY27 +5%, cycle turns) | 8,100 | 2,650 | **10,750** |

**Validation of FY2026E.** FACT: H1-26 revenue was Rp5,194.1bn. The 2025 H2/H1 ratio was 1.145
(6,735/5,882). Annualising gives ~Rp11,141bn. My model gives 10,870 — a 2.4% gap. Management
guided FY2026 revenue −5 to −10%, i.e. Rp11,355–11,986. **My model is slightly below both
management and the run-rate, which is the right side to err on.** Call FY2026 ~Rp11.0tn.

**Mid-cycle EBIT.** Average 2026–28E revenue = Rp10,638bn. EBIT margin: FY2025 actual 30.0%
(3,781.2/12,616.7); 5Y average 33.5%; KBVS models 26.9%, BRIDS 30.9%. Agent 5's cost-inflation
mechanism is real and directional (**FACT:** construction WPI +8.1% YoY Apr-2026 vs house
prices +0.6% Q1-26, and handover accounting means today's COGS was locked 2–3 years ago), so a
drift down is the base case, not the bear case.

| Scenario | Revenue | EBIT margin | **Mid-cycle EBIT** |
|---|---|---|---|
| Bear | 10,200 | 26.0% | **2,652** |
| **Base** | **10,638** | **28.5%** | **3,032 → call it 3,044** |
| Bull | 11,200 | 30.0% | 3,360 |

### Adjudication of the central dispute

**The screener's Rp3,401bn is too high — but by ~10%, not by the 14–18% the presales decline
suggests.** Two mechanisms cushion it, and both are FACTs the bear case under-weights:

1. **~19–21% of revenue is recurring and is not presales-driven.** A 14% presales decline
   passes through to only ~11% of total revenue.
2. **The record 2024 presales vintage (Rp11,017bn) is still being handed over through FY2026.**
   The earnings trough is FY2027, not FY2026.

`Normalised/Trailing EBIT` should read **~0.81** (3,044 / 3,781), not 0.998. That is a genuine
screener error and the framework's named error — *never treat peak-cycle earnings as permanent*.
But it is worth roughly **Rp80–120 per share of the Rp500 valuation gap, not Rp500.** Agent 5
identified the right direction and over-attributed the magnitude. The bigger error is elsewhere
(§5).

---

## 3. The historical P/B band — the decisive empirical test

BVPS = equity attributable to owners of the parent ÷ shares. Sources: FY2016/17/18 from the
**audited consolidated statements** (CTRA 3M18 and 9M19 filings, ciputradevelopment.com —
FACT); FY2021–25 from stockanalysis.com, independently corroborated for FY2023 (1,081.5) and
FY2024 (1,179.4) by **BRIDS Exhibit "Key Financials"** — two independent sources agree to the
decimal, so I treat these as FACT. FY2019–20 are INFERENCE (interpolated from the audited
Sep-2019 figure of Rp14,654.1bn and a secondary source for FY2020). Prices are month-end
closes from the pipeline's own 10-year series.

| Year | BVPS | Price low–high | **P/B low–high** | P/B on year avg |
|---|---|---|---|---|
| 2016 | 819.7 † | 1,320–1,590 | 1.61–1.94 | 1.75 |
| 2017 | 720.7 | 1,035–1,370 | 1.44–1.90 | 1.68 |
| 2018 | 774.4 | 820–1,290 | 1.06–1.67 | 1.31 |
| 2019 | ~804 ‡ | 875–1,235 | 1.09–1.54 | 1.30 |
| 2020 | ~827 ‡ | 444–985 | **0.54**–1.19 | 0.89 |
| 2021 | 915.6 | 865–1,155 | 0.94–1.26 | 1.10 |
| 2022 | 1,000.2 | 860–1,065 | 0.86–1.06 | 0.96 |
| 2023 | 1,081.5 | 990–1,250 | 0.92–1.16 | 1.01 |
| 2024 | 1,179.4 | 980–1,340 | 0.83–1.14 | 1.01 |
| 2025 | 1,298.5 | 750–1,015 | 0.58–0.78 | 0.69 |
| 2026 YTD | 1,321.6 | 555–770 | **0.42**–0.58 | **0.49** |

† pre-merger share base of 15,425.3m; ‡ INFERENCE.
**Spot: 630 / 1,321.6 = 0.477x. 52-week low 510 = 0.386x.**

**Means:** 10-year (2016–26) **1.11x** · last 5 years **0.83x** · last 3 years **0.73x**.

**Three findings, and they cut in different directions:**

**FACT (bullish).** **0.48x is the cheapest CTRA has been on month-end closes in at least a
decade — cheaper than the COVID crash, which bottomed at 0.54x on a month-end basis.** In every
year from 2021 to 2024 the stock traded in a 0.83–1.26x band on essentially the same ~10% ROE.
The market's own revealed mid-cycle multiple for this exact business, this exact management and
this exact return profile was ~1.0x.

**FACT (bearish, and the more important one).** The de-rating is **monotonic**: 1.75 → 1.68 →
1.31 → 1.30 → 0.89 → 1.10 → 0.96 → 1.01 → 1.01 → 0.69 → 0.49. This is not a cyclical
oscillation around a stable mean. It is a ten-year secular compression, and mean-reverting to
the 10-year average of 1.11x is therefore **not a defensible base-case assumption.**
Anchoring on the 3-to-5-year mean of **0.73–0.83x** is defensible; anchoring on 1.0x is a
bull case.

**INFERENCE (the explanation, which decides which of the two above matters).** The compression
tracks the widening gap between ROE and cost of equity. **FACT:** CTRA's 10-year average ROE is
**9.08%** (2016 9.39, 2017 6.69, 2018 8.25, 2019 7.54, 2020 8.61, 2021 10.23, 2022 10.10,
2023 9.21, 2024 9.73, 2025 11.06 — wisesheets.io). **FACT:** the Indonesia 10-year government
bond yielded **7.276% on 6 Aug 2026** (BRIDS Daily, via Agent 5). A ~9% through-cycle ROE
against a ~12.8% cost of equity is *rationally* worth well under book — permanently, absent a
change in either term. Agent 3 reached the same conclusion from the business side.

So the answer to the committee's question — *"if 0.4–0.5x is the trough and it has re-rated to
1x before, that is an argument; if the last decade averaged 0.6x, the upside is much smaller"* —
is: **both are true, and the honest reading is in between.** It has re-rated to 1x, repeatedly,
as recently as 2024. But the trend line through those re-ratings points down, and 0.75x is the
right base, not 1.0x.

---

## 4. The five lenses, built

### Lens A — SOTP (primary)

**Recurring portfolio** (malls, hotels, offices, hospitals, golf). FACT: FY2025 revenue
Rp2,357.2bn at 42.8% gross margin → gross profit Rp1,009bn. INFERENCE: allocate ~10% of
recurring revenue in opex (recurring carries almost no selling expense) and add back D&A
embedded in COGS (~Rp330bn of the ~Rp380bn total, per BRIDS/KBVS D&A of 350–395bn) →
**recurring EBITDA ≈ Rp1,000bn.**

*Cross-check against BRIDS' own DCF of the same assets (Exhibit 4, 9 May 2025): malls 3,675 +
office leased 578 + hotels 3,743 + hospitals 3,749 = **Rp11,744bn**. That is 11.7x my EBITDA
estimate — inside a sensible range for Indonesian mall/hotel/hospital real estate, which
independently validates both numbers.*

**Development business.** Mid-cycle total EBITDA = EBIT 3,044 + D&A 380 = 3,424; less recurring
1,000 → **development EBITDA ≈ Rp2,424bn.** A business with 706 days of inventory, a 662-day
cash conversion cycle and sub-COE returns does not earn a high exit multiple.

| Rp bn | Bear | Base | Bull |
|---|---|---|---|
| Recurring EBITDA × multiple | 900 × 8.0 = 7,200 | 1,000 × 10.0 = **10,000** | 1,100 × 12.0 = 13,200 |
| Development EBITDA × multiple | 2,132 × 4.0 = 8,528 | 2,424 × 5.5 = **13,332** | 2,640 × 7.0 = 18,480 |
| Net cash (Rp662bn) credited | 0% = 0 | 50% = **331** | 100% = 662 |
| Less NCI (book Rp2,879bn) | ×1.2 = (3,455) | ×1.0 = **(2,879)** | ×0.8 = (2,303) |
| **Equity value** | **12,273** | **20,784** | **30,039** |
| **Per share** | **662** | **1,121** | **1,621** |

The net-cash haircut and the NCI multiplier answer Agent 5's "biggest hidden risk" directly:
consolidated cash sits across dozens of KSO project entities and is not freely distributable.
I credit half of it in the base and none in the bear. **FACT:** the screener credits 100%.

**INFERENCE worth stating plainly:** at Rp630 the market cap is Rp11,677bn. The base-case
recurring portfolio alone is Rp10,000bn — **86% of the market cap.** You are buying 90 projects
across 34 cities, Rp23.0tn of land and inventory at historic cost, and a net-cash balance sheet
for roughly 14% of the price. That is the real bull case, and it is stronger than the screener's.

### Lens B — Historical P/B band

Forward BVPS: 1,321.6 today, plus retained earnings of ~Rp85–90/share/yr (NI ~2,100–2,400,
26% payout) → **~1,400 by end-2026, ~1,490 by end-2027.**

| | Multiple | Basis | Value |
|---|---|---|---|
| Bear | 0.42x | the 2026 low print itself | 1,360 → **571** |
| Base | 0.75x | between the 3-yr (0.73) and 5-yr (0.83) means | 1,400 → **1,050** |
| Bull | 1.00x | the 2021–24 revealed mid-cycle multiple | 1,450 → **1,450** |

### Lens C — Mid-cycle P/E

FACT: FY2025 NI/EBIT = 2,663.1/3,781.2 = 0.704 (Indonesian property pays a low final tax, so
the conversion is high). Use 0.69 forward for slightly higher interest expense.
Mid-cycle NI = 0.69 × 3,044 = **Rp2,100bn → EPS 113.3.**

| | P/E | EPS | Value |
|---|---|---|---|
| Bear | 5.5x | 98.7 | **543** |
| Base | 8.0x | 113.3 | **906** |
| Bull | 11.0x | 125.1 | **1,376** |

(2021–24 trailing P/E ran ~9–12x. 8x on mid-cycle earnings is deliberately below that.)

### Lens D — Justified P/B (the honest bear lens)

`Justified P/B = (ROE − g) / (COE − g)`. COE = 7.28% (IDGB10Y) + 5.5% ERP × β 1.0 = **12.78%**.
(FACT: Yahoo's β of 0.118 is outside the project's own [0.5, 2.5] trust band and is forced to
1.0.) Mid-cycle ROE = NI 2,100 / average equity ~25,900 = **8.1%**; I use 8.5% to avoid
under-shooting a trough.

| | ROE | COE | g | Justified P/B | Value |
|---|---|---|---|---|---|
| Bear | 7.5% | 13.75% | 4.0% | 0.359 | **495** |
| Base | 8.5% | 12.75% | 5.0% | 0.452 | **633** |
| Bull | 10.0% | 11.75% | 5.5% | 0.720 | **1,030** |

**This lens says CTRA is roughly fairly valued at 630, and I report that without softening it —
it is the strongest single argument against the screener.** But I weight it lightly and the
reason is mechanical, not convenient: with COE − g = 7.75pp, the output swings from 0.41x
(g = 5.5%) to 0.51x (g = 4.0%) on a 150bp change in an unobservable terminal growth rate. The
project's own memory records exactly this hazard — *"Justified P/B divides by (COE − g), so a
bad input silently quadruples fair value."* It is a valid sanity check and a poor anchor.

### Lens E — EPV, rebuilt (upper bound, low weight)

Screener EPV of 1,228 = 3,401 × (1 − 0.22) / 0.12 + 662 net cash, all shares. Rebuilt with
mid-cycle EBIT 3,044, CTRA's *actual* low effective tax (~3–8%; use 5%), COE 12.75%, **less
NCI**: 3,044 × 0.95 / 0.1275 = 22,682 + 662 − 2,879 = 20,465 → **Rp1,104/share.**

Note that a properly re-normalised EPV lands *above* my base. I still discount it, because EPV
assumes the land bank replenishes itself at constant margin, forever, at zero cost — and
**FACT:** FY2025 free cash flow was −Rp642bn while EBIT was Rp3,781bn, and land acquisition was
cut 72% to Rp628.3bn. Over 2022–25 cumulative FCF (Rp7,954bn) was 94% of cumulative net income
(Rp8,497bn), so the drag is real but not catastrophic. EPV is a ceiling, not a base.

### Lens F — Replacement / marked NAV (asset-backing test, not a target)

Two independent routes, deliberately more conservative than any broker RNAV:

1. **Transaction-comparable.** FACT: CTRA contracted ~165 ha from EMDE at Rp750k/sqm
   (Rp1,236.4bn) — an arm's-length current market price for raw peripheral township land
   (Agent 3, AR 2025). ASSUMPTION: ~2,300 ha of raw land bank (Agent 5 flagged this figure as
   unverified — **insufficient evidence, requires further research**). 23m sqm × Rp750k =
   Rp17.25tn vs Land-for-Development book of Rp9,906.2bn → pre-tax embedded gain Rp7.35tn,
   ~Rp310/share after notional tax → **adjusted NAV ≈ Rp1,630/share.**
2. **Margin-implied.** A 48–49% gross margin against a replacement-cost developer's ~32–35%
   implies ~14–16pp of margin is release of legacy land gain. On Rp22,966bn of inventory plus
   land for development, PV'd over a ~10-year average monetisation life at 12.75% →
   ~Rp345/share of embedded gain → **adjusted NAV ≈ Rp1,667/share.**

Two routes, ~Rp1,650. **INFERENCE: book value is not impaired — it is understated by roughly
25%.** That underwrites the P/B floor and rules out the terminal-value-trap case. It does *not*
justify BRIDS' Rp4,469, which values the same land as if it monetised instantly.

**FACT — for calibration:** BRIDS (9 May 2025) built RNAV of Rp4,469/share (landbank 65,920 +
apartments 1,683 + strata office 779 + recurring 11,744 = 80,126, plus net cash 2,712) and then
applied a **65% discount (its own 5-year mean)** to reach TP Rp1,600, noting the market was
already at a 79% discount and the sector at 82%. At Rp630 today the discount is **~86%** —
roughly −2SD on BRIDS' own five-year band. That is the single most bullish datapoint in this
report, and it is why the verdict is UNDERVALUED rather than FAIRLY VALUED.

---

## 5. Bear / base / bull, and why the screener is wrong

Framework rule — bear and bull are **offsets from the base**, not independent clamps; and take
the **median** across lenses, never the minimum.

| Lens | Bear | Base | Bull |
|---|---|---|---|
| A — SOTP | 662 | 1,121 | 1,621 |
| B — Historical P/B | 571 | 1,050 | 1,450 |
| C — Mid-cycle P/E | 543 | 906 | 1,376 |
| D — Justified P/B | 495 | 633 | 1,030 |
| E — EPV rebuilt | 751 | 1,104 | 1,377 |
| **Median** | **571** | **1,050** | **1,377** |
| **Adopted (rounded, symmetric offsets)** | **600** | **1,000** | **1,400** |

*Ceiling checks, not blended in: marked NAV ~1,650; BRIDS RNAV at its own 5-yr mean discount
1,564; consensus TP 1,243–1,327 (Investing.com / MarketScreener); KBVS TP 1,400; BRIDS TP 1,600.*

- **Bear (−40% from base): Rp600.** FY2026 presales land at Rp8.3tn, FY2027 revenue ~Rp10.2tn,
  EBIT margin compresses to 26% on construction cost pass-through failure, COE 13.75%, no credit
  for consolidated net cash, NCI marked above book. Price implication −4.8%.
- **Base (Rp1,000).** Presales trough in 2026 at ~Rp8.7tn and recover modestly; mid-cycle EBIT
  Rp3,044bn; the stock re-rates to ~0.75x book — its 3-to-5-year average, not its 10-year one.
  **MOS 37.0%, upside +58.7%.**
- **Bull (+40% from base): Rp1,400.** BI eases through 2027, presales inflect in 2027, EBIT
  margin holds at 30%, and CTRA re-rates to 1.0x book — the multiple the market actually paid in
  2021–2024 on the same ROE. Upside +122.2%.

Probability-weighted at 30 / 45 / 25 → **Rp980**, consistent with the Rp1,000 base.

### Decomposition of the screener's Rp499 error

The blend is exactly reproducible: 0.5 × 1,228.45 + 0.3 × 1,783.15 + 0.2 × 1,750.49 = 1,499.27
(FACT). Substituting my rebuilt lenses one at a time:

| Substitution | Blend impact | Share of error |
|---|---|---|
| Comparables 1,783 → mid-cycle P/E 906 | **−263** | **53%** |
| DCF base 1,750 → SOTP 1,121 | −126 | 25% |
| EPV 1,228 → rebuilt EPV 1,104 | −62 | 12% |
| Residual / rounding to my adopted base | −48 | 10% |
| **Total: 1,499 → 1,000** | **−499** | |

Within those, the EBIT re-normalisation from 3,401 to 3,044 accounts for only ~Rp80–120.

**Why the comparables lens is the biggest error (INFERENCE, high confidence).** `Comparables IV`
of 1,783 rests on a 35-name "Real Estate Development" cohort with a median PE of **12.4x** and
median EV/EBIT of **9.5x** — applied to CTRA's *trailing peak* earnings. Two independent
falsifications: (i) the **same peer set has a median P/B of 0.77x**, which prices CTRA at 1,018,
not 1,783 — the peer group contradicts itself, which is the signature of a median drawn from
near-zero-earnings micro-caps; (ii) **FACT (BRIDS Exhibit 9):** the actual large-cap Indonesian
developer cohort trades at a **median 2026F P/E of 7.0x and P/BV of 0.6x** (CTRA 7.2/0.7,
BSDE 4.4/0.3, PWON 8.5/0.8, SMRA 6.7/0.6). The true peer multiple is roughly *half* the
screener's. My 8x mid-cycle P/E is, correctly, a premium to that — but on lower earnings.

**Two further screener defects I confirm** (both raised by Agent 5, both verified here):
`risk_free_rate = 0.065` against a live IDGB10Y of 7.276%; and 100% of consolidated net cash
credited to the parent despite Rp2,879bn of NCI and ~61% of presales running through KSO.

---

## 6. Most important assumption

Sensitivity of the base value, holding all else constant:

| Assumption moved | Move | Base value impact |
|---|---|---|
| **Cost of equity / exit multiples** | **±100bp COE** (and the ~±1x EV/EBITDA and ±0.10x P/B that follow) | **±Rp138 (±14.4%)** |
| Mid-cycle EBIT | ±10% (2,740 ↔ 3,348) | ±Rp76 (±7.9%) |
| Recurring portfolio multiple | ±2x EV/EBITDA | ±Rp32 (±3.4%) |
| Net cash / NCI treatment | 0% ↔ 100% credit | ±Rp18 (±1.8%) |

**The exit multiple dominates the earnings level by roughly 1.8 : 1.** Stated as a single
sentence: **the base case assumes CTRA re-rates from 0.48x book to ~0.75x book — its own
three-to-five-year average — and that assumption is a call on the Indonesian 10-year yield, not
on CTRA's presales.**

This is a partial rebuttal of Agent 5, whose "most fragile assumption" was the normalised EBIT.
He is right that Rp3,401bn is wrong, and right about the direction. But correcting it costs
~Rp100 of the ~Rp500 error. **The screener's larger sin is not that it mis-measured CTRA's
earnings; it is that it paid a healthy-market multiple for them.** If BI holds or eases and the
IDGB10Y falls back below ~6.75%, the base is Rp1,150–1,250 with the same earnings. If the
sovereign yield goes to 8%, the base is Rp850 with the same earnings.

---

## 7. Verdict and how I differ from the other agents

**Valuation Verdict: UNDERVALUED.** Base Rp1,000 vs price Rp630 — **MOS 37%, upside +59%**, with
downside to a fully specified bear of only −4.8% and a marked-NAV asset backing of ~Rp1,650 that
rules out the balance-sheet trap. The asymmetry (−5% / +59% / +122%) is genuinely favourable.

**But 37% is not 58%, and the distinction matters under this framework.** For an average-quality
cyclical whose lead indicator is still falling, in the fourth month of a rate-hiking cycle, the
required MOS should be 40–50%. **At Rp630 CTRA clears the "undervalued" bar and fails the
"sufficiently large discount" bar by roughly one notch.** Rp560–580 — a 0.42–0.44x P/B, which
the stock printed earlier this year — would clear both.

**Where I agree with Agent 5 (Thesis Killer):** the direction and most of the magnitude. He
argued the realistic base is Rp900–1,100; I arrive independently at Rp1,000 from a different
lens set. His veto of the 58% MOS is correct and I endorse it. His condition (1) — re-underwrite
with forward EBIT, Rf ≥ 7.25%, and drop `Comparables IV` — is what this report does; the result
is 37% MOS, short of his 40% reinstatement threshold, but not by much.

**Where I differ from Agent 5, on three specifics:**
1. He treats the EBIT re-normalisation as the dominant error. It is worth ~20–25% of the error;
   the comparables multiple is worth ~53%. The recurring segment and the record 2024 presales
   vintage cushion the earnings decline to ~10%, not the 14–18% headline.
2. His P/B floor of 0.35–0.40x has no historical precedent — the decade's lowest month-end print
   is 0.42x and the COVID crash bottomed at 0.54x. 0.42x is the defensible floor, giving Rp571,
   not Rp463.
3. He treats the 84–86% RNAV discount as evidence the discount never closes. It is better read
   as a *level*: BRIDS' own five-year mean discount is 65% and the current 86% is ~2SD wide.
   Both readings can be true — the mean can drift wider *and* 86% can be an extreme.

**Where I differ from the screener:** on everything except the direction. Blended IV 1,499 → my
1,000; MOS 58% → 37%; `Normalised/Trailing EBIT` 0.998 → 0.81.

**Pipeline fixes this analysis implies** (beyond Agent 5's list):
- Extend `Justified PB IV` beyond financials to asset-heavy real estate. Omitting it left CTRA
  valued with no asset lens at all.
- Suppress or floor `Comparables IV` when the peer PE median and the peer P/B median imply
  values more than ~1.5x apart — that divergence is a reliable marker of a junk peer cohort, and
  here it was a 1.75x divergence (1,783 vs 1,018).
- Deduct non-controlling interests before dividing by parent shares in EPV and DCF. CTRA's NCI
  is 10.5% of total equity.

---

*Prepared as Agent 2 (Valuation & Model Validation). Primary sources: CTRA audited consolidated
financial statements (3M18, 9M19 filings); CTRA Annual Report 2025 via Agent 3; KB Valbury
Sekuritas company report 4 Nov 2025; BRI Danareksa Sekuritas company update 9 May 2025
(RNAV build, Exhibit 4; peer comparison, Exhibit 9); stockanalysis.com; wisesheets.io; the
idx_picker 10-year monthly price cache. The land-bank hectarage underlying the replacement-value
lens remains unverified against the FY2025 annual report — insufficient evidence, requires
further research.*
