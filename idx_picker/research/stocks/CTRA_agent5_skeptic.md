# CTRA — Agent 5: Thesis Killer / Skeptical Investment Committee

*PT Ciputra Development Tbk. | IDX: CTRA | Price IDR 630 | Screener verdict: BUY, MOS 58%*
*Review date: 2026-08-10. All figures IDR unless noted. Every claim labelled FACT / INFERENCE / THESIS / ASSUMPTION.*

**Scoring convention:** Skeptic Score runs 0–100 where **higher = more concern**. 0 = I found nothing to worry about; 100 = uninvestable.

---

## Skeptic Score: 72 / 100

Not a fraud. Not a balance-sheet blow-up. But the screener's 58% margin of safety is
built on four separable errors — a lagging operating indicator, a stale discount rate, a
corrupted safety metric, and an unreliable peer anchor — and correcting all four
compresses the MOS to roughly 20–30%. That is not enough cushion for a cyclical whose
lead indicator is still falling into a central-bank tightening cycle.

---

## Executive summary — the one thing that kills this

**FACT.** An Indonesian developer recognises revenue only on **handover**, not on sale.
CTRA's Corporate Secretary Aditya Ciputra Sastrawinata said so explicitly in June 2026:
*"If pre-sales decline in 2025, revenue will inevitably decline in 2026 as well"* — because
the company can only recognise revenue after units are handed over.
([IDNFinancials, 29 Jun 2026](https://www.idnfinancials.com/news/65276/ctra-forecasts-10-drop-in-profits-in-2026-why))

**FACT.** Marketing sales (pre-sales), the true lead indicator, have been falling for two
years:

| Period | Marketing sales | YoY |
|---|---|---|
| FY2025 | Rp 9.5tr (95% of guidance) | **−14%** |
| Q1 2026 | Rp 2.44tr (26% of FY target) | **−23%** |
| H1 2026 | Rp 4.69tr (49% of FY target) | **−18%** |

Sources: [BRIDS/IPOT sector update](https://www.ipotnews.com/module/newsDetail.php?jdl=Property___In_line_FY25_presales__FY26F_presales_to_rely_on_mid_up_upper_products&news_id=214588&group_news=IPOTNEWS&taging_subtype=INSTIRESEARCH&name=&search=y_general&q=Sector+Update,+Property,+(BSDE),+(SMRA),+(CTRA),+(PWON),&halaman=1);
[Bisnis, 27 Jul 2026](https://market.bisnis.com/read/20260727/189/1991150/marketing-sales-turun-begini-prospek-saham-ciputra-ctra-semester-ii2026);
[KabarBursa, 24 Jun 2026](https://www.kabarbursa.com/market-hari-ini/bi-rate-naik-ctra-buka-peluang-revisi-market-sales)

**INFERENCE (high confidence).** Every valuation lens the screener used — EPV, DCF base,
comparables — is anchored to **Normalised EBIT (5Y) of Rp 3,401bn**, with the screener
itself recording *Normalised/Trailing EBIT = 0.998*, i.e. "trailing earnings are normal
earnings." Those trailing earnings were produced by handovers of the **2022–2024
pre-sales vintage**. The 2025 and 2026 vintages are 14% and ~18% smaller. Capitalising
this EBIT into perpetuity is precisely the error the framework forbids: *never treat
peak-cycle earnings as permanent earnings.*

**FACT.** Management has already conceded the point. On 28–29 June 2026 CTRA guided
**revenue and net profit down ~10% in FY2026**
([Kontan](https://investasi.kontan.co.id/news/ciputra-development-ctra-proyeksikan-laba-turun-10-pada-2026),
[Bisnis](https://market.bisnis.com/read/20260629/192/1984067/ciputra-ctra-proyeksikan-pendapatan-laba-turun-10-pada-2026-ini-alasannya)).
H1 2026 delivered exactly that: revenue Rp 5.19tr (−11.7% YoY), net income Rp 1.10tr
(−11.2% YoY), EPS Rp 59 vs Rp 67
([Kontan](https://investasi.kontan.co.id/news/pendapatan-ciputra-development-ctra-tergerus-laba-ikut-turun-11-di-semester-i)).

**THESIS.** The screener bought the *price decline* as value while the *cause* of the
decline is still intensifying. FY2027 faces a **second** consecutive earnings decline
driven by the FY2026 pre-sales shortfall — and FY2028 too, if H2 2026 does not turn.

---

## Data-integrity defects in the screener output itself

Before arguing the business, three of the screener's own numbers are wrong. These are
mechanical, verifiable, and they all push the verdict toward BUY.

**1. FACT — the quarterly YoY growth figures compare the wrong quarters.**
The quarterly table in `CTRA.md` is missing **2025-09-30**. The five columns present are
Q1-25, Q2-25, Q4-25, Q1-26, Q2-26. Stepping back "four columns" therefore lands on Q1-25,
not Q2-25.

- Screener reports `Revenue (Quarter YoY Growth) = −3.48%`. That is 2,636.6 / 2,731.7 − 1 =
  −3.48% — Q2-26 vs **Q1-25**.
- True Q2-26 vs Q2-25 = 2,636.6 / 3,150.1 − 1 = **−16.3%**.
- Same defect on net income (`−12.38%` = Q2-26 vs Q1-25).

The screener understated the revenue contraction by a factor of ~4.7x. This is a real
pipeline bug, not just a CTRA issue — it will misfire on any ticker with a gap in the
quarterly series.

**2. FACT — Interest Coverage of 45.4x is an artifact and inflates the Safety Score.**
The quarterly table shows `InterestExpense = −331.6` for 2025-12-31 — a negative interest
expense, which is a Yahoo Q4 derived plug (FY less nine months). Working from the audited
annual line instead: FY2025 EBIT 3,781.2 / interest expense 579.5 = **6.5x coverage**, not
45.4x. Reconstructing TTM the same way gives ≈3,573 / 559 ≈ **6.4x**. Safety Score 95.6
and Altman Z 4.99 both lean on the corrupted figure. 6.4x is still adequate; it is not
"bulletproof."

**3. INFERENCE — the risk-free rate is stale and the Comparables IV is anchored on junk.**
- The pipeline uses `risk_free_rate = 0.065`, `wacc = 0.12`
  (`/home/user/datasharing/idx_picker/scraper/pipeline.py:132-135`). **FACT:** the Indonesia
  10-year government bond yielded **7.276% on 6 Aug 2026**
  ([BRIDS Daily, 7 Aug 2026](https://www.brights.id/en/research-and-news/research-report/brids-daily-economic-fixed-income-update-friday-august-7-2026)).
  The screener is discounting an illiquid, land-heavy, cyclical developer at 12% while the
  sovereign pays 7.3%. A ~470bp equity risk premium over IDR govvies for a property
  developer is not defensible.
- `Comparables IV = 1,783` (2.8x the current price) rests on a 35-name peer group with a
  **median PE of 12.4x** and **median EV/EBIT of 9.5x**. **INFERENCE:** the IDX "Real Estate
  Development" cohort contains many micro-cap, near-zero-earnings shells whose PE medians
  are numerically meaningless. Anchoring CTRA's fair value to that median imports noise as
  signal. Note the internal contradiction: the same peer set has a **median P/B of 0.77x**,
  which prices CTRA at 1,018 — not 1,783.
- **FACT:** `Beta = 0.118`. Per the project's own rule this is outside [0.5, 2.5] and is
  forced to 1.0 — a defensible fallback, but it means the discount rate carries **no
  company-specific risk information at all** for a stock with a **−72% max 10Y drawdown**.

---

## Strongest Bull Argument

*(Stated as strongly as I can, because a bear case that has not steelmanned the bull is worthless.)*

**FACT.** CTRA is a 45-year-old, genuinely national developer trading at **0.48x book**
with **11.1% ROE**, **net cash of Rp 662bn**, D/E of 0.32x, current ratio 2.29x,
F-Score 7, a **5.8% dividend yield on a 26% payout**, and a price at the **16th percentile
of its own 10-year range**, −43% from the 52-week high and −37% over one year.

**THESIS (bull).** Bank Indonesia's 100bp of hikes since May 2026 were **defensive** —
taken to arrest rupiah weakness and capital outflow, not to fight domestic inflation
([TradingEconomics](https://tradingeconomics.com/indonesia/interest-rate/news/559986),
[GlobalSource](https://www.globalsourcepartners.com/posts/indonesia-surprise-rate-hike/teaser)).
Defensive hikes reverse fast once the currency stabilises. **FACT:** the VAT subsidy
(PPN DTP) has been signalled to run to **December 2027** for landed houses up to Rp 5bn.
**FACT:** Indonesia's housing backlog is ~9.6mn households. If BI cuts 100bp through 2027,
pre-sales trough in 2026, earnings trough in 2027, and you are buying a structurally
demanded asset at trough multiples with a covered-ish dividend paying you to wait.
Consensus TP is **Rp 1,190** (+89%); BRI Danareksa had CTRA as sector top pick with TP
Rp 1,700.

That is a respectable bull case. My problem with it is entirely one of **sequencing and
price of admission**, plus the fact that the sell-side has been making that exact argument
for 18 months while the stock fell 28%.

---

## Strongest Bear Argument

**The lead indicator, the macro, and the product mix are all pointing the same way, and
the reported P&L is the only thing that looks good — because it is 12–24 months stale.**

**FACT — Macro is tightening, not easing.** BI has raised the BI-Rate by **100bp since
May 2026**: +50bp to 5.25% (20 May), +25bp to 5.50% (9 Jun), +25bp to 5.75% (18 Jun) — the
highest since April 2025, driven by rupiah pressure and foreign capital outflow, with the
currency near Rp 18,000/USD. The August meeting was expected to hold at 5.75%.
([BI](https://www.bi.go.id/en/publikasi/ruang-media/news-release/Pages/sp_2810726.aspx),
[TradingEconomics](https://tradingeconomics.com/indonesia/interest-rate/news/559986))

**FACT — CTRA is the most rate-exposed of the large developers.** Director Harun Hajadi,
24 June 2026: **~70% of CTRA's transactions are mortgage-financed (KPR)** and **>80% of
buyers are end-users** buying for personal occupation — the segment most sensitive to
rates. He opened the door to **revising the FY2026 marketing sales target**, citing
financing cost rather than demand.
([KabarBursa](https://www.kabarbursa.com/market-hari-ini/bi-rate-naik-ctra-buka-peluang-revisi-market-sales))

**FACT — the transmission is already measurable.** Mortgage lending growth decelerated from
8.7% YoY (Apr 2025) to **5.1% (Apr 2026)**; mortgage **NPLs rose to 3.2%** from 3.0%;
national home sales across 18 cities fell **−25.7% YoY in Q1 2026**. A 1pp rise in the
mortgage prime rate is estimated to slow mortgage growth by 2pp.
([Jakarta Post, 30 Jun 2026](https://www.thejakartapost.com/business/2026/06/30/a-tougher-road-ahead-for-the-property-sector),
[Indonesia Investments](https://www.indonesia-investments.com/news/todays-headlines/evaluating-indonesia-s-property-recovery-amid-2026-macro-winds/item9961))

**FACT — the contraction is concentrated exactly where CTRA sells.** Demand for homes
below Rp 2bn fell **−22% YoY**; Rp 2–5bn fell −9%; only **>Rp 5bn grew (+36%)**. CTRA's
FY2025 units below Rp 2bn fell **−29% YoY**. Per BRI Danareksa's 9M24 mix, CTRA's pre-sales
were **16% <Rp1bn + 42% Rp1–2bn = ~58% in the collapsing bucket**, and only ~10% above
Rp 5bn — the only growing bucket. **84% of CTRA's pre-sales are landed residential** and
**61% sit outside Greater Jakarta**, in secondary cities where middle-income stress is
worst (INFERENCE on the last clause).

**FACT — a margin squeeze is already in the pipeline.** The wholesale price index for
property construction rose **+8.1% YoY in April 2026** (vs +0.8% a year earlier) while
house prices rose only **+0.6% in Q1 2026**, and developers have "not yet fully passed on"
the cost. **INFERENCE:** because revenue is recognised on handover, today's 49.6% gross
margin reflects land and construction costs locked in 2–3 years ago. The cost inflation
now embedded in work-in-progress arrives in reported COGS in 2027–2028. Gross margin
normalising from 49.6% toward the 5Y average of 48.4% is the *optimistic* path; the
mechanism points lower.

**FACT — the "premium pivot" is a crowded trade.** CTRA's stated FY2026 fix is to focus on
units above Rp 1.5bn. So is BSDE (Nava Park II, targeting Rp 1tr vs Rp 528.5bn prior). So
is SMRA ("more mid-up/upper products"). So is PWON (Kota Kasablanka extension, "higher
segments"). **INFERENCE:** four large developers simultaneously redirecting supply into
the one segment that is still growing is a recipe for the premium segment's margin and
absorption to deteriorate too.

**FACT — cash generation has broken down.** FY2025 free cash flow was **−Rp 642bn** (vs
+3,400 / +3,100 / +2,096 in 2022/23/24). TTM FCF is Rp 418bn = **Rp 22.6/share**, against a
dividend of ~**Rp 36.3/share**. **The dividend is currently covered only 0.62x by free cash
flow.** The screener's own Piotroski breakdown flags this: **Accruals = 0** (CFO < net
income). A 5.8% yield you are relying on to "get paid to wait" is presently being funded
from the balance sheet.

**FACT — the earnings yield is a mirage.** EBIT/EV of **24.7%** looks spectacular. FCF
yield is **3.6%**. The gap is land replenishment: for a developer, maintenance investment
flows through **inventory**, not capex. Inventory rose from Rp 11,641bn (2022) to
Rp 13,060bn (Q2-26); days inventory is **706** and the cash conversion cycle is **662
days**. Capitalising EBIT at a 12% WACC (the screener's EPV of Rp 1,228) implicitly assumes
the land bank replenishes itself at constant margin, forever, for free. It does not — and
FY2025's negative FCF is the proof.

---

## Why The Stock Could Be A Value Trap

**The value trap test — why has the market NOT already recognised this? Concretely: it
has. Fully. For a decade. And it was right.**

**FACT — the cheapness is the persistent state, not a new opportunity.**

| Evidence | Value |
|---|---|
| Price CAGR 3Y | **−17.2% p.a.** |
| Price CAGR 5Y | **−10.1% p.a.** |
| Price percentile, 10Y | **16.2** |
| Max drawdown 10Y | **−72.1%** |
| Current P/B | **0.48x** |
| Peer median P/B (35 IDX developers) | **0.77x** |

**FACT.** Indonesia's property sector trades at an **84% discount to RNAV, ~2 standard
deviations below its long-term mean**. The discount has been *widening*, not closing.

**FACT.** In February 2025, BRI Danareksa rated CTRA **BUY, TP Rp 1,700**, called it the
**sector top pick ranking highest across all metrics**, and modelled FY2026F **P/BV of
0.6x on 10.7% ROE** — i.e. sub-book was the *forecast base case*, not an anomaly. Market cap
then: Rp 16,126bn. Today: **Rp 11,677bn**. The most bullish, best-informed local house had
the thesis right in every particular and lost 28% holding it.

**Four structural reasons the discount does not close — each is a mechanism, not a mood:**

1. **THESIS — there is no agent who can force realisation.** **FACT:** PT Sang Pelopor, the
   Ciputra family vehicle, holds **53.31%** (as at end-May 2026), and the family occupies
   the operating seats: **Candra Ciputra is President Director, Cakra Ciputra is a
   Director, Rina Ciputra Sastrawinata and Junita Ciputra are Commissioners**
   ([StockWatch](https://stockwatch.id/investor-publik-kuasai-865-miliar-saham-ciputra-development-ctra-ini-pengendalinya/)).
   Public float below 5% per holder is 46.69% across 43,835 holders. **INFERENCE:** with an
   outright majority *and* board control, no takeover, no proxy contest, no activist, no
   liquidation and no forced buyback is possible. NAV can only be realised at the family's
   chosen pace, by selling houses one at a time, for 15–20 years. **A discount that only a
   controlling family can close is not a margin of safety; it is a permanent feature.**

2. **THESIS — the "NAV" is a very long-dated, price-assumption-dependent DCF, not an asset
   with a bid.** CTRA's land bank is reported at **>2,300 hectares** (ASSUMPTION: this
   figure appears in secondary sources; I did not verify it against the FY2025 annual
   report — *insufficient evidence, requires further research*). Land bank is carried in
   **inventory at cost**, monetised over decades. There is no liquid market in which a
   minority holder's claim on it can be converted to cash. An 84% sector discount to RNAV
   is arguably the market applying a correct, high discount rate to a 20-year monetisation
   stream in a currency that just went to 18,000/USD — not a mispricing.

3. **THESIS — the trailing P/E of 4.3x is a cyclical top signal, not a bargain.** The
   correct time to buy a cyclical is on a *high* multiple of *trough* earnings. CTRA trades
   at a *low* multiple of earnings that management has already guided down 10%, off a
   pre-sales book down 14% then 18%. Screener `Business Type` correctly says **Cyclical**,
   yet `Normalised/Trailing EBIT = 0.998` treats the peak as the norm.

4. **THESIS — the four "independent" lenses are one bet.** Magic Formula (EBIT/EV 24.7%),
   Acquirer's Multiple (4.05x), EPV (1,228) and the DCF base (1,750) are all the *same*
   assumption — that Rp 3,401bn of normalised EBIT is durable — dressed four ways. Net-Net
   already **fails** (NCAV Rp 343 vs price 630), which is the one lens that does not depend
   on it. When the single shared input breaks, all four break together.

---

## Biggest Hidden Risk

**Consolidated cash and land are not the parent shareholder's cash and land.**

**FACT.** At Q2-2026: total assets 46,623.5, total liabilities 19,246.1 ⇒ total equity
27,377.4, of which **StockholdersEquity (parent) is 24,498.5**. Non-controlling interests
are therefore **Rp 2,879bn, ~10.5% of total equity**. **FACT.** CTRA's own description of its
model is that it *"works with landowners and partners in some projects"* — i.e. KSO (kerja
sama operasi) joint operations and partly-owned project SPVs.

**INFERENCE.** The Rp 8,602bn of consolidated cash and the net-cash position are aggregated
across dozens of project entities and joint operations. Cash sitting in a project SPV with
a landowner partner, or ring-fenced against customer advances and construction obligations,
is not distributable to CTRA minorities without partner and lender consent. The
screener's net cash of −662 (i.e. net cash) is being credited to equity holders at 100%.

**This is the single largest unverified item in the thesis.** I could not obtain the
FY2025 audited notes on restricted cash ("kas dibatasi penggunaannya"), customer advances,
or KSO accounting. **Insufficient evidence — requires further research.** Anyone
underwriting this must read Notes on cash, inventory, and related-party/KSO balances in the
FY2025 audited statements before crediting the balance sheet.

**Secondary hidden risk (FACT).** Morgan Stanley reported to OJK on 7 July 2026 a holding
of **3.41bn shares = 18.40%**, up from 2.22%. **INFERENCE:** at that scale this is almost
certainly custodial/prime-brokerage nominee registration rather than a proprietary
conviction stake — note it is arithmetically hard to reconcile with the end-May disclosure
that all sub-5% holders together own 46.69%. Do **not** read this as smart-money
accumulation. **Insufficient evidence — requires further research.** If it *is* aggregated
synthetic/swap exposure, an unwind is a meaningful overhang on a stock with 2.4mn shares of
daily volume.

**Governance note (honest framing).** I searched for OJK sanctions, affiliated-transaction
disputes and conflict-of-interest findings against CTRA and **found none**. Absence of
found evidence is not evidence of absence. My governance objection is **structural, not
behavioural**: majority family ownership plus family occupancy of the CEO, a directorship
and two commissioner seats means minorities have no mechanism to compel value realisation.
The 2017 CTRP/CTRS merger was executed with dissenting-shareholder buybacks of only
Rp 33.3bn, i.e. it went through essentially unopposed — evidence of control, not of abuse.

---

## Most Fragile Assumption

**That Normalised EBIT of Rp 3,401bn is the mid-cycle number.**

`Normalised/Trailing EBIT = 0.998` says the screener believes today *is* mid-cycle. But the
5-year median is drawn from FY2022–FY2025 — a window whose handovers reflect the
2020–2024 pre-sales boom, including the post-COVID VAT-incentive surge. The pre-sales that
will become 2027–2028 revenue are **−14% then −18%**.

Every headline output moves with this one number, and it moves further when the discount
rate is corrected to the 7.28% sovereign yield:

**EPV per share (Rp) — sensitivity to EBIT and WACC**

| Normalised EBIT (Rp bn) | 12% (screener) | 13% | 14% | 15% | 16% |
|---|---|---|---|---|---|
| 3,781 (FY25 actual) | 1,362 | 1,260 | 1,172 | 1,096 | 1,030 |
| **3,400 (screener)** | **1,228** | 1,136 | 1,058 | 990 | 930 |
| 3,100 (−10%, mgmt guide) | 1,123 | 1,039 | 968 | 905 | 851 |
| 2,800 (2027, second leg) | 1,018 | 942 | 877 | 821 | 772 |
| 2,500 (margin squeeze too) | 912 | 845 | 787 | 737 | 693 |

Move two cells — from (3,400 @ 12%) to (2,800 @ 14%) — and intrinsic value falls from
1,228 to **877**. The margin of safety falls from 49% to **28%**. Neither move is
aggressive: 2,800 is management's own guided decline plus one more year of the pre-sales
shortfall, and 14% is the sovereign yield plus ~670bp for an illiquid cyclical developer.

---

## Most Important Thesis-Breaker

**A second and third consecutive year of earnings decline — 2027 and 2028 — because the
pre-sales that generate them have already been missed and cannot be recovered
retroactively.**

The screener's BUY rests on "MOS 58%, quality and balance sheet both pass." The MOS is
computed against earnings power that is contractually already impaired. This is not a
forecast; it is arithmetic on a backlog:

- FY2025 pre-sales −14% ⇒ FY2026 revenue/profit −10% (**already confirmed**: H1-26 revenue
  −11.7%, NI −11.2%).
- H1 2026 pre-sales −18%, tracking 49% of an unrevised Rp 9.5tr target ⇒ **FY2027 revenue
  and profit decline again**, magnitude depending on H2.
- Management has publicly opened the door to cutting the FY2026 target. **A formal guidance
  cut is the specific event that breaks the thesis in the market's eyes.**

Compounding it: gross margin faces its own delayed hit from +8.1% construction cost
inflation against +0.6% house price inflation, and the dividend is presently 0.62x covered
by free cash flow.

**Stress test — bear case, fully specified.**

| Driver | Bear assumption | Basis |
|---|---|---|
| FY2026 pre-sales | Rp 8.3tr (−13%) | H1 at Rp 4.69tr, target unrevised and unmet |
| FY2027 revenue | ~Rp 10.5tr (−12% on FY26) | Handover lag on FY26 pre-sales |
| EBIT margin | 26% (from ~30%) | Construction cost pass-through gap |
| FY2027 EBIT | **~Rp 2,700bn** | Above |
| Discount rate | 14–15% | IDGB10Y 7.28% + illiquid cyclical premium |
| FY2027 net income | ~Rp 1,900–2,150bn | Margin + rate on tightening debt |
| **EPV-derived value** | **Rp 790–880** | Grid above |
| **Multiple-derived value** | **Rp 580–720** (5–6x on Rp 102–116 EPS) | Cyclicals trough at low multiples |
| **P/B-derived value** | **Rp 463–530** (0.35–0.40x book) | Sector already 2 SD below RNAV mean |

**Bear range: Rp 460–790 against a price of 630.** Note the consensus low target is
**Rp 530** and the 52-week low is **Rp 510** — the market has already traded inside my bear
range this year. **Downside to a genuine bear is −18% to −27%; the realistic base is
Rp 900–1,100, not Rp 1,499.** Risk/reward is roughly 1 : 1.5, not the 1 : 2.4 the screener
implies.

**Catalyst-failure test.** The named catalysts are (a) the PPN DTP VAT subsidy and (b) BI
easing. **FACT:** BRIDS judged the VAT extension to provide *"limited near-term demand
support."* The incentive has been running through the entire period in which pre-sales fell
14% then 18% — it is not a new catalyst, it is an existing subsidy that has already failed
to stop the decline. And BI is **hiking**, not easing.

---

## Contrarian Test

**What is the consensus, and am I actually differentiated?**

The consensus is *bullish*: mean TP **Rp 1,190** (+89%), range Rp 530–1,330; BRIDS
Overweight with CTRA as top pick, TP Rp 1,700. So the bear case here **is** the contrarian
position — with one caveat that cuts against me: **the price already reflects the bear
case more than the analysts do.** At 0.48x book and 4.3x trailing earnings, the market is
not asleep; it is pricing a multi-year earnings decline and a permanently unrealisable NAV.

So I must be honest about which mistake I might be making. **If I am wrong, it is because
I am extrapolating a trough.** The rate shock is 3 months old. BI's hikes were currency-
defensive and could reverse within four quarters. CTRA has net cash, 6.4x interest cover
and no refinancing wall, so it can survive a two-year air pocket without dilution — and
survival plus a cyclical recovery from 0.48x book is how the biggest returns in this asset
class are made. That is a real possibility and I do not dismiss it.

**But it is a call on the Indonesian rate cycle and the middle-class income cycle, not on
CTRA's intrinsic value.** The framework's question is whether this is *"a sufficiently good
business, or a sufficiently attractive deep-value situation, at a sufficiently large
discount, with risks I understand and can accept."* It is a decent business at a real
discount — but the discount, correctly computed, is 20–30%, not 58%, and the risk I would
be accepting is a macro call I have no edge on.

**Correct classification of the five outcomes:** not "good business at a fair price," not
"deep value / special situation," and not a terminal value trap either. This is
**average-quality cyclical business, genuinely cheap, mid-way through a deteriorating
cycle, with no mechanism to force value realisation.** The screener's error is not the
direction; it is the *magnitude* and, decisively, the *timing*.

---

## What Evidence Would Change My Mind

**Toward a BUY (I need three of these five):**

1. **Pre-sales inflect.** Q3 2026 marketing sales ≥ Rp 2.4tr and Q4 ≥ Rp 2.6tr — i.e. FY2026
   lands ≥ Rp 8.5tr — showing sequential stabilisation rather than a target that is missed
   and quietly abandoned.
2. **BI turns.** A hold-then-cut sequence, rupiah back below ~16,500/USD, and the IDGB10Y
   below ~6.75%. This is the single highest-leverage variable: 70% of CTRA's sales are
   mortgage-financed.
3. **Mix pivot proves real, not aspirational.** Two consecutive quarters where units above
   Rp 2bn grow in absolute rupiah, not just as a share of a shrinking total.
4. **Cash quality verified.** From the **FY2025 audited notes**: restricted cash, customer
   advances, cash held at partly-owned SPVs and KSO balances, plus the related-party
   transaction schedule. If ≥80% of the Rp 8,602bn cash is genuinely available at the
   parent and related-party dealing is immaterial, the balance-sheet leg of the bull case
   stands and I would raise the score.
5. **Dividend coverage restored.** FY2026 operating cash flow that covers the dividend
   more than 1.5x without land-bank liquidation.

**Toward a hard REJECT:**

1. A **formal cut to the FY2026 marketing sales target** (management has already signalled
   this is under consideration).
2. Gross margin printing **below 45%** in any quarter — confirming construction cost
   pass-through failure.
3. Any **inventory (land bank) impairment**, which would attack book value itself and
   destroy the 0.48x P/B floor.
4. **BI hiking again** beyond 5.75%, or the rupiah breaking decisively through 18,000.
5. Discovery of **material related-party asset transfers** between CTRA and family vehicles
   at non-arm's-length prices.
6. Dividend cut or suspension.

**Housekeeping (required regardless of verdict):** fix the pipeline's quarterly-YoY offset
bug on gapped series; source interest coverage from the annual line when the quarterly plug
is negative; refresh `risk_free_rate` toward the live IDGB10Y; and suppress `Comparables IV`
where the peer PE median is drawn from a cohort with negligible earnings.

---

## Probability Thesis Is Fundamentally Correct: **30%**

Decomposed, because a single number hides the disagreement:

| Proposition | Probability | Note |
|---|---|---|
| CTRA's intrinsic value exceeds Rp 630 | **~65%** | Net cash, 11% ROE, 0.48x book — genuinely cheap |
| Intrinsic value is ≥ Rp 1,499 (the screener's IV) | **~20%** | Requires normalised EBIT to hold *and* a 12% WACC |
| A 58% MOS is realised within 3–5 years | **~30%** | Requires the discount to close, which needs BI easing *and* an agent to force it |
| **Thesis as written by the screener is correct** | **30%** | |

---

## Investment Committee Verdict: **CONDITIONAL**

I exercise the veto **against the BUY at a 58% margin of safety**. I do **not** veto the
name.

**Rationale.** The balance sheet is real and I could not break it: net cash, D/E 0.32x,
6.4x true interest coverage, current ratio 2.29x, no dilution, no refinancing wall, no
governance abuse found. That is not a value trap in the terminal sense — CTRA will still be
here in 2030. But the screener's BUY rests on four correctable errors that all point the
same direction, and correcting them takes the MOS from 58% to **20–30%** — with the lead
indicator still falling, management already guiding down, and Bank Indonesia tightening.
Buying a cyclical at a low multiple of peak earnings, in the fourth month of a rate-hiking
cycle, into a −18% pre-sales print, is the framework's own named error.

**Conditions for reinstatement to BUY — all four must be met:**

1. **Re-underwrite the valuation** using forward EBIT (not the 5Y median), a risk-free rate
   of ≥7.25%, a WACC of ≥14%, and drop `Comparables IV` from the blend. If the result still
   shows ≥40% MOS, bring it back.
2. **Evidence of a pre-sales trough** — FY2026 marketing sales ≥ Rp 8.5tr, or two
   consecutive quarters of sequential growth.
3. **Bank Indonesia on hold or easing**, with the rupiah stable.
4. **Verification of cash and KSO/related-party structure** from the FY2025 audited notes
   (Agent 1, Financial Forensics, should own this).

**If the committee overrules me and buys anyway:** treat this as a **macro-timing cyclical
position, not a value position**. Cap at **half a normal weight**, stage entry across the
next two quarterly pre-sales prints, and set a hard review trigger on a formal FY2026
guidance cut. Do not size it on the 58% MOS — that number is not real.

---

*Prepared as Agent 5 (Thesis Killer). Written adversarially by design: the bull case
deserves an equally rigorous defence from Agents 2 and 3, and the cash-quality and
related-party questions raised here are unresolved and belong to Agent 1.*
