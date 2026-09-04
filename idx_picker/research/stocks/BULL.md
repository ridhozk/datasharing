# BULL — Buana Lintas Lautan Tbk.

*Screener fact sheet, **refetched live from Yahoo 2026-09-04 03:11 UTC**, on corrected
figures (EBIT from OperatingIncome; EV from balance-sheet net debt; payout from DPS/EPS;
DCF reinvestment on a normalised-capex basis; working-capital reinvestment charged;
net income attributable to common stockholders.)*

> ### ⛔ Data-currency warning — read before using any figure below
>
> **Yahoo's newest BULL filing is still period-end 2026-03-31 (Q1). Q2-2026 (June) is
> NOT in the feed** — staleness has widened to **1.72 quarters**. FACT, verified by a live
> refetch today, not a cache read.
>
> Every fundamental number on this sheet is therefore **Q1-2026 or older**. Pricing and FX
> *are* current: last close **IDR 464**, FX **17,684** (IDR firmed from 17,908 three weeks
> ago), 52W range **147 – 685**.
>
> **Agents must retrieve BULL's Q2-2026 (H1-2026) report from IDX / the company's own
> disclosure** (idx.co.id disclosure, company IR, or an Indonesian financial data source)
> and state explicitly whether it confirms or breaks the Q1 step-change described below.
> Label anything you cannot source as *"Insufficient evidence — requires further research."*

**Business:** PT Buana Lintas Lautan — an Indonesian **oil tanker owner and operator**
(crude and product carriers, plus offshore/gas), largely on time charter to Pertamina and
related counterparties. Reports in **USD**, trades in **IDR** (FX applied: 17,908). Asset-
heavy, cyclical, and financed with vessel-level debt.

⚠️ **The screener has this in the peer group "Passenger Marine Transportation."** That is
a Yahoo sector misclassification — BULL is a tanker owner, not a passenger operator. The
Comparables IV of 580 rests on a peer EV/EBIT median of **15.0x** drawn from the wrong
comparable set. Treat that lens as unreliable and rebuild it from tanker owners.

## Screener output (candidate generation only — a hypothesis to falsify)

**This is the first name in this review the screener rated negatively.** The job here is
symmetric to the others: not "is the BUY real" but **"is the SKIP real"** — is the screener
producing a false negative after the stock tripled?

| Field | Value |
|---|---|
| Sector | Transportation & Logistic |
| Business Type | **Cyclical** |
| Price | 464.0 |
| Quality Score | 66.7 |
| Safety Score | 43.9 |
| Value Score | 43.0 |
| Composite Score | 51.2 |
| F-Score | **4 / 9** (annual basis) |
| Altman Z | **−0.58** |
| Earnings Yield (EBIT/EV) | 0.0793 |
| ROC (Greenblatt) | 0.1217 |
| Acquirers Multiple (EV/EBIT) | 12.62 |
| Net-Net Pass | False |
| NCAV per Share | −133.99 |
| EPV per Share | **92.21** |
| IV Bear / Base / Bull | **(blank — DCF produced no value; see below)** |
| Comparables IV | 579.69 *(wrong peer group)* |
| Justified PB IV | (n/a — not a financial) |
| Blended IV | 275.02 |
| MOS Blended | **−0.687** |
| Upside Blended | **−0.407** |
| Verdict | **SKIP** |
| Reasons | MOS −69% below watch threshold 10% |
| Red Flags | *(none raised)* |
| Peer Count | 10 |
| Peer PE / EV-EBIT / PB Median | 18.14 / 15.02 / 1.87 |
| Quarters Stale | **1.72** (was 1.46) |
| Latest Filing | **2026-03-31 — Q2 not yet in feed** |

*Verdict, scores, F-Score, Altman Z and ROC are unchanged on the refetch; the EV/EBIT-type
ratios moved only with FX (EV/EBIT 12.62 → 12.74, EPV/share 92.21 → 91.06). The peer
medians above come from the full 956-ticker universe run; today's single-ticker refetch has
no peer set, which is why a solo run reports Comparables IV blank and MOS −100%. That is a
run-scope artifact, not new information.*

### ⚠️ Why the DCF is blank — a suspected seventh screener defect

`build_scenarios` constructs the cash-flow base as
`normalised EBIT × (1−tax) + depreciation + normalised capex`, where **depreciation is
inferred as `EBITDA_TTM − EBIT_TTM`**. For BULL, Yahoo reports EBITDA 750.0bn against
EBIT 726.5bn — an implied **D&A of just IDR 23.5bn/yr against a IDR 7,303bn asset base
and a IDR 5,628bn invested-capital line.** That is not a plausible depreciation charge for
a tanker fleet; the real figure is plainly an order of magnitude larger and sits inside
cost of revenue.

The arithmetic:

```
NOPAT              = 622.9bn × 0.78  =  +485.9bn
implied D&A        = 740.7 − 717.5   =   +23.2bn   ← should be ~500-700bn
normalised capex   = median annual   =  −623.6bn
                                        ---------
cash-flow base                       =  −113.9bn   → DCF returns None
```
*(Figures at today's FX; on the 2026-08-11 FX the same arithmetic gave −116.0bn. The sign
does not depend on the currency conversion — it depends entirely on the missing D&A.)*

So the DCF did not "decline to value" BULL — **it was silently killed by a depreciation
add-back that Yahoo did not supply.** The existing suppression rule only fires when
EBITDA equals EBIT to within IDR 1, so a 23.5bn stub slips through. The blend then fell
back on EPV (92) and a wrong-peer Comparables IV (580), which is how a −69% MOS was
produced. **Both surviving lenses in this blend are compromised. The SKIP verdict is not
yet earned — it must be re-derived, not assumed.**

*(Note this cuts in the opposite direction to ERAA's defect: there a missing term made a
fair-valued stock look 66% cheap; here a missing term may be making a cyclical look
expensive. Same root cause — a reinvestment term that does not match the earnings basis.)*

## Key statistics *(refetched 2026-09-04; IDR figures at FX 17,684)*

| Metric | Value | USD equivalent |
|---|---:|---:|
| Market Cap | IDR 7,189bn | ~USD 407m |
| Enterprise Value | IDR 9,143bn | ~USD 517m |
| Net Debt (Q) | IDR 1,907bn | ~USD 108m |
| Total Debt (Q) | IDR 2,254bn | ~USD 127m |
| Total Assets (Q) | IDR 7,211bn | ~USD 408m |
| Equity (Q) | IDR 3,800bn | ~USD 215m |
| Minority Interest | IDR 46bn | ~USD 2.6m *(immaterial)* |
| Revenue (TTM) | IDR 2,653bn | ~USD 150m |
| EBIT (TTM) | IDR 717bn | ~USD 41m |
| Net Income (TTM) | IDR 578bn | ~USD 33m |
| Capex (TTM) | IDR −1,724bn | ~USD −97m |
| Free Cash Flow (TTM) | IDR 78bn | ~USD 4m |
| Shares out | 15,494,436,935 | *(source: market cap / price)* |

*Because BULL files in USD, the IDR figures move with FX even when nothing in the business
changes: the whole three-week delta above is the rupiah firming 17,908 → 17,684. The USD
column is the one to reason about. **A weaker rupiah mechanically inflates BULL's reported
IDR earnings — the opposite of ERAA, and an FX exposure the bull case must not be allowed
to smuggle in as operating performance.***

| Ratio | Value |
|---|---:|
| PE (TTM) | 12.43 |
| **PE (Q1-2026 annualised)** | **7.16** |
| Price / Book | **1.89** |
| Price / Sales | 2.71 |
| EV / EBIT (TTM) | 12.74 |
| EV / EBITDA (TTM) | 12.34 |
| FCF Yield (TTM) | 1.1% |
| ROE (TTM) | 15.2% |
| ROIC (TTM) | 11.8% |
| ROCE (TTM) | 14.3% |
| ROA (TTM) | 8.0% |
| Book value / share | 245.26 |
| Cash / share | 22.42 |
| **Current Ratio** | **0.597** |
| **Quick Ratio** | **0.560** |
| Debt / Equity | 0.593 |
| Total Liabilities / Equity | 0.885 |
| Net Debt / Equity | 0.502 |
| Total Debt / Assets | 0.313 |
| **Interest Coverage** | **4.58x** |
| Asset Turnover | 0.368 |
| Days Sales Outstanding | 72.0 |
| Dividend | **none** (payout 0%) |
| Beta | 1.207 |
| Statement Currency | **USD** (FX 17,684) |

## Annual history (IDR bn, converted at spot — note the 2022 loss year)

| FY | Revenue | Gross Profit | **Operating Income** | Yahoo "EBIT" | Net Income | Interest Exp | Total Debt | Equity | Capex | FCF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | 2,038.8 | 439.0 | **178.8** | −82.4 | **−787.5** | 692.2 | 3,363.1 | 2,088.7 | −131.2 | −362.7 |
| 2023 | 2,654.2 | 1,141.5 | **1,054.4** | 896.5 | 500.6 | 397.2 | 2,822.5 | 2,589.6 | −502.9 | 78.3 |
| 2024 | 2,510.9 | 887.1 | **664.0** | 574.3 | 246.3 | 330.4 | 2,434.2 | 2,834.0 | −760.4 | −79.2 |
| 2025 | 2,603.5 | 721.8 | **597.6** | 619.0 | 436.7 | 182.0 | 2,046.2 | 3,594.0 | −937.4 | 159.5 |

*2022 is the clearest single illustration of the EBIT-contamination defect this project
fixed: Yahoo's "EBIT" of **−82.4bn** is `PretaxIncome + InterestExpense` and folds a
loss-making year's financing items into operating profit, against a true operating income
of **+178.8bn**. Every ratio built on Yahoo's EBIT for this name was wrong.*

**Retained earnings: −3,903bn at FY2025** (−3,637bn at Q1-2026), i.e. a large accumulated
deficit still being worked off. This is what drives Altman Z to −0.58: the X2 term
(retained earnings / total assets) alone contributes ≈ **3.26 × −0.53 = −1.74**, and
negative working capital contributes another negative X1. **Altman Z here is measuring
balance-sheet history, not current distress risk** — but the negative working capital and
0.60 current ratio are real and must be assessed on their own terms.

## Quarterly history (IDR bn)

| Quarter | Revenue | Gross Profit | Operating Income | Net Income | Interest Exp | Total Debt | Equity | Capex | FCF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-Q1 | 704.1 | 198.8 | 164.8 | 105.0 | 61.4 | 2,299.9 | 2,949.8 | −450.4 | 95.7 |
| 2025-Q2 | 548.6 | 145.7 | 118.7 | 40.2 | 57.0 | 1,886.2 | 2,959.0 | — | 86.0 |
| 2025-Q3 | 668.7 | 142.3 | 113.1 | 83.4 | 51.8 | 1,936.5 | 3,304.4 | −55.7 | 126.6 |
| 2025-Q4 | 682.1 | 235.0 | 201.1 | 207.7 | 11.8 | 2,046.2 | 3,594.0 | −881.3 | −148.8 |
| **2026-Q1** | **786.9** | **331.4** | **293.7** | **254.3** | **38.2** | 2,282.9 | 3,848.3 | −358.2 | 14.7 |

**Q1-2026 is a step change.** Revenue +11.8% YoY, gross margin **42.1%** (vs 28.2% a year
earlier), operating margin **37.3%**, net income **+142% YoY**. Interest expense has fallen
from 61.4bn to 38.2bn as debt was paid down. Annualising Q1 puts the stock on **7.1x PE**.

Two readings, and separating them is the whole job:
- **THESIS (bull):** a deleveraged tanker owner entering a strong rate cycle, re-rating off
  a depressed base, with earnings power well above the trailing twelve months.
- **THESIS (bear):** a cyclical printing peak-cycle margins after a 3x share-price run,
  where the four-year median operating income is 631bn — **not** the 1,175bn Q1 annualises
  to. *The owner's framework: never treat peak-cycle earnings as permanent earnings.*

## Price and momentum

| Metric | Value |
|---|---:|
| Price (last close, 2026-09-04) | 464 |
| Day range / volume | 456 – 478 / 676m shares |
| 52W High / Low | **685 / 147** |
| % from 52W high | **−32.3%** |
| **1Y price change** | **+203.3%** |
| Price CAGR 3Y | +63.6% |
| Price CAGR 5Y | +13.0% |
| Price percentile, 10Y | **89.5%** |
| Max drawdown, 10Y | −79.9% |
| Months of price history | 121 |

The stock **tripled and then gave back a third**. Both facts matter: the market has already
re-rated this, and something then took a third of it back out.

## Piotroski detail (4/9, annual basis)

| Signal | Pass |
|---|:--:|
| ROA positive | ✅ |
| CFO positive | ✅ |
| ROA improving | ✅ |
| Accruals (CFO > NI) | ✅ |
| Leverage falling | ❌ |
| Current ratio improving | ❌ |
| No dilution | ❌ |
| Gross margin improving | ❌ |
| Asset turnover improving | ❌ |

*Note the shape: every **profitability** signal passes, every **balance-sheet / efficiency**
signal fails. The failures are consistent with a company in a fleet-expansion phase funding
vessels with debt and equity. Whether that is value-creating is the central question, not a
detail — capex TTM of 1,746bn is **2.4x TTM EBIT** and 5.4x the FY2023 level.*

## Growth and normalisation

| Metric | Value |
|---|---:|
| Revenue CAGR 3Y / 5Y | 8.5% / 8.5% |
| Gross Margin 5Y Avg | 31.5% |
| EBIT Margin 5Y Avg | 23.3% |
| ROE 5Y Avg | **10.4%** *(vs 15.2% TTM)* |
| Revenue Volatility 5Y | 9.9% |
| **Normalised EBIT (median, 4Y)** | **630.8bn** |
| Normalised EBIT margin | 24.7% |
| Normalised / Trailing EBIT | 0.868 |
| Working Capital Intensity | 10.1% |
| Implied Terminal Multiple | 11.11x |
| Quarters of history / Years annual | 5 / 4 |

## What the screener cannot see, and the agents must establish

1. **Fleet NAV.** A tanker owner is valued on vessel values, not multiples. How many
   vessels, what type (VLCC / Aframax / MR / gas), what age, and what is second-hand value
   less debt? **P/B is 1.87** — where does that sit against NAV, and where has BULL traded
   against NAV historically? Tanker owners above ~1.3x NAV are usually late-cycle.
2. **Charter cover and counterparty.** How much of revenue is on time charter to Pertamina
   versus spot? Time charter explains stable ~25% margins and low volatility (5Y revenue
   volatility just 9.9%, unusual for tankers). What is the contract roll schedule, and are
   renewals repricing up? **Charter cover is the difference between the two readings of Q1.**
3. **Why did Q1-2026 gross margin jump 14 points?** Rate cycle, mix, a one-off, an asset
   sale gain, or FX? This single question decides whether 7.1x PE is real.
4. **What is real depreciation?** Needed both to fix the screener and to judge whether
   reported profit is economic. Take it from the cash-flow statement in the filings.
5. **The capex programme.** IDR 1,746bn TTM against a 7,189bn market cap. What is being
   bought, at what price, and what returns are underwritten? Vessels bought at cycle-peak
   asset values are the classic way shipowners destroy capital.
6. **The accumulated deficit and share count.** Retained earnings −3,903bn; the "no
   dilution" Piotroski signal fails; diluted shares moved 13,962m → 14,452m. What is the
   equity-issuance history, is there a rights-issue pattern, and is there a quasi-
   reorganisation or restructuring history behind that deficit?
7. **Debt maturity ladder and covenants.** Current liabilities 2,230bn against current
   assets 1,331bn. Which vessel loans mature when, and is refinancing arranged?
8. **Governance and related parties.** Ownership structure, related-party charters, and the
   history of the controlling shareholder. Tanker vehicles with related-party charters are
   where minority value is most often diverted.
9. **The +205% / −32% price path.** What happened, and when? An index inclusion, a
   corporate action, a large placement, a rate spike, or a broker initiation?
10. **Zero dividend.** No dividend at all despite 15.2% ROE. Is that capex discipline, debt
    covenants, or the accumulated deficit legally blocking distributions?

## Framing for the agents

The four lenses disagree, and that disagreement is the signal:

| Lens | Reads |
|---|---|
| Magic Formula | EY 7.9%, ROC 12.2% — **mediocre, not cheap** |
| Piotroski | **4/9 — fails** |
| Acquirer's Multiple | EV/EBIT 12.6x — **not cheap for a cyclical** |
| Graham Net-Net | NCAV **−134/share** — nowhere near |
| Q1-annualised PE | **7.1x** — cheap *if* the quarter is representative |
| P/B vs ROE | 1.87x P/B on 15.2% ROE, 10.4% 5Y avg ROE — **fair-to-full** |

**Every trailing lens says this is not cheap. The only cheap reading requires Q1-2026 to be
the new run-rate.** That is precisely the judgement the owner's framework says not to make
on a cyclical without evidence. The burden of proof sits with the bull case.

**Five outcomes must stay distinguishable.** For BULL the live candidates are:
*good business at a fair price* (deleveraged, charter-covered, mid-cycle) · *fairly valued
or expensive* (the screener's SKIP, correctly reached by the wrong route) · **value trap**
(peak-cycle earnings capitalised at the top of a fleet-expansion binge, with an accumulated
deficit, no dividend and negative working capital).
