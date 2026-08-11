# ERAA — Financial Forensics

## Resolving the central contradiction

The screener's reasoning ("quality and balance sheet both pass") is **not fully
supported by its own numbers**. FACT: the same row shows F-Score 4/9, Altman Z
2.68 (grey zone, 1.8–2.99), quick ratio 0.40, D/E 0.84, interest coverage 3.4x
and FCF yield −32%. INFERENCE: "balance sheet passes" over-weights the fact
that equity is still growing and leverage is not extreme in absolute terms, and
under-weights that this is a working-capital-heavy distributor whose current
assets are 63% inventory (11,644.7bn of 19,894.2bn at FY2025) — a genuinely
weak liquidity structure even if typical for the sector. THESIS: the correct
reading is "moderate-risk, cyclical/seasonal working-capital funding, not
structural insolvency risk" — worse than the screener's binary PASS, better
than the raw ratios look in isolation. See below.

## 1. Inventory — the whole risk

FACT (from fact sheet + web corroboration): Inventory rose from IDR 7,130.9bn
(FY2024) to IDR 11,644.7bn (FY2025), +63% YoY, far outpacing revenue growth of
+17.3%. Days Inventory Outstanding deteriorated from ~44.8 days (FY2024) to
~59–62 days (FY2025/quarterly), per pintarsaham.id analysis corroborating the
fact sheet's Days Inventory (Quarter) of 59.3. Inventory is now ~40% of total
assets (11,644.7/28,856.5 FY2025) and, at Q2 2026, IDR 12,480.7bn against a
market cap of IDR 7,352bn — i.e. inventory alone is 1.7x the entire equity
market value.

FACT: Inventory is financed only partially by trade credit. Accounts Payable
of IDR 5,964.9bn (FY2025) covers ~51% of inventory; the remainder is funded by
short-term bank debt and equity/cash. Quarterly total debt tracks the
inventory cycle almost exactly (Q1'25 8,638.5bn → Q2'25 12,569.0bn during the
big build → Q4'25 9,399.7bn → Q1'26 10,793.0bn → Q2'26 7,980.8bn as inventory
was drawn down) — INFERENCE: debt is being used as a revolving working-capital
swing line tied to the phone-launch/Lebaran cycle, not permanent capital.

INFERENCE: **Smartphone/electronics obsolescence risk is real but probably
moderate, not acute**, for two reasons: (a) DIO of ~59 days is roughly two
months' turnover — elevated but not extreme for the category; (b) the
inventory swings hard within the year (huge build in H1, drawn down in H2),
consistent with launch-cycle/seasonal stocking rather than stranded, aging
goods. ASSUMPTION/GAP: I could not directly read the FY2025 or 1H2026 notes to
financial statements to confirm the balance and movement of the "cadangan
penurunan nilai persediaan" (inventory impairment allowance) — **insufficient
evidence — requires reading the actual notes to financial statements (IDX
filing) to confirm whether any material write-down was taken.** No news
coverage found reporting a write-down or clearance-sale event in 2025–2026.

## 2. Where the FCF is going

FACT: Annual FCF: 2022 −365.1bn, 2023 −180.7bn, 2024 +1,316.9bn, 2025 −679.5bn.
Summed over four years this is **roughly breakeven (+91.6bn cumulative)**
despite revenue growing from 49,471.5bn to 76,606.9bn (+55% cumulative) — i.e.
FCF has not structurally deteriorated over the medium term; it has been
volatile and growth-funded.

FACT (web, pintarsaham.id + secondary corroboration): 1H2025 operating cash
flow was **negative ~IDR 4.9 trillion** (cash received from customers
Rp35.12tn vs cash paid to suppliers/employees Rp39.13tn), driven explicitly by
the inventory build described above, not by a shrinking core business — 1H2025
revenue and net income both grew YoY. CapEx was modest by comparison (~437bn
in 1H2025 combined, ~904.6bn for full-year 2025) and is **store network
expansion, not the primary driver of the cash burn** — inventory/working
capital dominates. FACT: no acquisitions of a scale visible in this data;
GAP: no M&A cash-flow line item was available to me — **insufficient evidence
on acquisition spend**, treat CFO/FCF split above as the load-bearing finding.

INFERENCE from the quarterly FCF pattern (Q1'25 −1,119.8bn, Q2'25 −4,228.6bn,
Q4'25 +563.6bn, Q1'26 −1,046.9bn, Q2'26 +2,331.0bn): this is a **seasonal
build-then-harvest cycle** (pre-Ramadan/Lebaran and new-model stocking in
H1/Q1, sell-through and destocking afterward), not a one-directional
structural cash drain. THESIS: the −32% trailing FCF yield the screener flags
is a **snapshot mid-cycle**, not the steady-state economics of the business —
directionally the "false positive" risk cuts the *other* way from what a naive
reading suggests (i.e., the ratio overstates the badness of underlying
economics), but the multi-year trend of rising DIO (44.8 → 59–62 days) still
means *more* cash is being permanently parked in inventory each cycle, which
is a genuine structural drift worth monitoring, not a one-off.

## 3. Debt structure and refinancing risk

FACT (IDX filing / Kontan, June 2026): ERAA and its subsidiaries extended and
increased credit facilities with **Bank Central Asia (BCA)** on 19 June 2026:
rupiah facilities totaling ~IDR 9.05 trillion, plus a USD175 million
Multi-Facility Loan and a USD500 million Forex Forward Line, explicitly for
working capital and FX-transaction support. Individual tranches carry
multi-year maturities (Time Loan 2 to May 2029, Time Loan 3 to May 2027, new
Time Loan 4 at 6.75% p.a.). Separately (VOI.id), a subsidiary secured Rp3
trillion + US$300 million from **Bank Mandiri**. ERAA's own disclosure stated
the BCA extension had no material adverse impact on operations/continuity.

INFERENCE: these are **long-standing, relationship-bank working-capital
facilities renewed on normal terms**, not distressed emergency financing — the
multi-year tranche maturities (2027, 2029) argue against a near-term
refinancing cliff. The **existence of a dedicated USD forex-forward line**
suggests the company hedges at least part of its USD-denominated inventory
purchases, mitigating unhedged FX risk on imports. FACT: PEFINDO affirms ERAA
at **idA / stable**, describing "moderate financial profile" — a mid-tier
domestic investment-grade rating, consistent with "leveraged but serviceable,"
not distressed.

RISK, not yet disproven: D/E 0.84 and interest coverage 3.4x mean debt service
absorbs a meaningful share of EBIT, and BI's tightening to 5.75% raises the
cost of the revolving facilities each renewal (new Time Loan 4 priced at
6.75%, above where similar facilities likely priced a year or two ago —
**insufficient evidence to confirm the prior rate for direct comparison**).
The "distributor funding inventory with short-term debt into a rate-tightening
cycle" failure mode described in the brief is a real, live risk here — it just
does not appear to be at the acute stage yet, given the ample renewed facility
headroom (facility ceilings well above amounts actually drawn).

## 4. Is the 16% ROE / 4.7x PE real?

FACT: Gross margin has been stable, 10.7%–11.2% every year 2022–2025 (5Y avg
10.87% per fact sheet) — no sign of margin manipulation or one-off gross-level
boosts. Operating margin has **compressed**: 3.04% (2022) → 2.55% (2023) →
2.57% (2024) → 2.15% (2025), even as gross margin held — INFERENCE: opex
(store network expansion, SG&A) is growing faster than gross profit, a real
and moderately concerning trend, separate from the working-capital story.

FACT: ROE 16.45% (TTM) decomposes cleanly via DuPont: ROA 5.31% (TTM) × total
assets/equity leverage of ~3.16x (28,856.5/9,141.6) ≈ 16.8%, closely matching
the reported figure — INFERENCE: the ROE is **leverage-amplified, not
manufactured** — it is arithmetically consistent with the reported balance
sheet, but it means ROE quality depends on the same debt structure discussed
in §3, not on unusually high underlying returns on assets (ROA is a modest
5.3%).

FLAG on earnings quality: Piotroski's **Accruals** component fails (0/1 in the
breakdown) — this component specifically tests whether net income is backed by
cash flow (roughly, ROA vs. CFO/Assets), and it failing is directly consistent
with the CFO story in §2: **paper profit is running ahead of cash profit**.
This is a genuine, not spurious, earnings-quality flag — it is the same
phenomenon as the FCF/CFO negativity, seen from the accrual side rather than
the cash side.

GAP: I found no specific disclosure on **supplier rebates/volume incentives**
from Apple/Samsung/other principals (common and often lumpy in distribution
businesses) — **insufficient evidence — requires reading the annual report's
revenue-recognition and "other income" notes directly** to confirm whether
rebate income is a material and volatile contributor to reported gross/net
margin. Given gross margin's *stability* across 4 years, large swings from
rebate timing seem unlikely to be a dominant factor, but this is inference
from margin stability, not direct confirmation.

## 5. Minority interests and related parties

FACT (web, corroborating multiple sources): 1H2025 consolidated net income of
Rp605.8bn split as Rp568.29bn to parent-company shareholders and Rp37.53bn to
non-controlling interests (~6.2% of consolidated profit). Non-controlling
interest on the balance sheet: Rp1,035.7bn (FY2025) vs Rp923.1bn (FY2024) and
Rp807.4bn (FY2023) — i.e. NCI is roughly ~10% of total equity but takes only
~6% of profit, a modest, not alarming, minority drag. Controlling shareholder:
PT Eralink International at 55.17% of paid-in capital (June 2026 registry).

GAP: **insufficient evidence** on related-party transaction values/terms
(e.g., transactions with affiliated distribution or property entities such as
Era Property Holding) — did not read the annual report notes directly; no
red flags surfaced in secondary sources, but this is not a substitute for
reading Note on related-party transactions in the FY2025 annual report.

## Screener false-positive assessment

The screener's BUY hinges on MOS 66% off a blended IV that itself leans on
EPV/DCF assuming normalized earnings — reasonable in isolation — plus a
"balance sheet passes" claim that this analysis only **partially** confirms.
The balance sheet is leveraged and liquidity-thin by design (distributor
model) but is **not showing acute distress signals**: renewed multi-year
credit facilities, a stable idA rating, hedged FX exposure, and a roughly
breakeven 4-year cumulative FCF despite heavy growth investment. The main
things the screener's single-line "passes" glosses over are (a) the
deteriorating DIO trend, (b) the accrual-based earnings-quality flag, and (c)
operating-margin compression — none of which are fatal on their own but
collectively argue for real caution, i.e. moving this from "quality passes
cleanly" to "quality passes with a leveraged, working-capital-fragile
balance sheet that must be monitored every quarter."

---

```
Financial Quality Score: 50/100
Earnings Quality: Gross margin stable (~10.9–11.2%, 4yr) with no evidence of
  manipulation, but operating margin compressed 3.0%→2.2% (2022–2025) as opex
  grew faster than gross profit. ROE (16.45% TTM) is arithmetically consistent
  via DuPont (ROA 5.3% × ~3.16x leverage) — leverage-amplified, not fabricated
  — but Piotroski's Accruals test fails, directly flagging that net income is
  running ahead of cash flow. No evidence found (nor evidence against) of
  supplier-rebate distortion; gross-margin stability argues against a large
  rebate effect. Insufficient evidence on one-off items / FX gains/losses
  within the P&L — not directly verified from primary filings.
Balance Sheet: Leveraged, working-capital-heavy distributor: D/E 0.84,
  interest coverage 3.4x, current ratio 1.26, quick ratio 0.40 (63% of current
  assets are inventory). Inventory (IDR 11,644.7bn FY2025, IDR 12,480.7bn Q2
  2026) is 1.7x market cap and financed roughly half by trade payables, the
  rest by short-term bank debt that swings tightly with the inventory cycle.
  DIO deteriorated from ~44.8 to ~59–62 days YoY — a real, monitorable trend,
  not yet acute. Altman Z 2.68 sits in the grey zone, consistent with a
  leveraged-but-not-distressed profile. PEFINDO rates ERAA idA/stable
  ("moderate financial profile"). Large, recently-renewed multi-year working
  capital facilities from BCA (~IDR 9.05tn + USD175m + USD500m FX forward,
  tranches to 2027/2029) and Mandiri (~IDR 3tn + USD300m) argue against a
  near-term refinancing cliff, though facility renewal at 6.75% reflects the
  higher-rate environment.
Cash Flow Quality: FCF volatile and mid-cycle negative (TTM −32% yield;
  1H2025 CFO ~−IDR 4.9tn) almost entirely explained by inventory build ahead
  of seasonal/launch demand, not by margin collapse or one-off losses; CapEx
  (~IDR 0.9–1.1tn/yr, store expansion) is a secondary driver. Quarterly FCF
  swings hard both ways within the same year (e.g. Q2'25 −4,228.6bn, Q2'26
  +2,331.0bn), consistent with a build-then-harvest seasonal pattern rather
  than structural cash loss. Over 4 years (2022–2025) cumulative FCF is
  roughly breakeven (+91.6bn) despite +55% cumulative revenue growth — i.e.
  growth has been funded without net destruction of cash over the medium
  term, but the trend in DIO shows a growing amount of cash being
  structurally parked in inventory each cycle.
Capital Allocation: Payout ratio ~25% (dividend yield ~5.4%) funded off
  reported earnings even in years with negative FCF — INFERENCE this implies
  dividends are effectively debt/working-capital-line funded in weak-FCF
  years, a moderate but not extreme capital-allocation concern. Store network
  expansion (iBox/Erafone/Urban Republic) continues; no major disclosed
  acquisitions found in the window reviewed. Insufficient evidence on
  buybacks or other capital return beyond the dividend.
Accounting Concerns: (1) No annualOperatingCashFlow line from Yahoo — CFO
  here is inferred (FCF − CapEx) per this project's known Yahoo/IDX data gap;
  cross-checked against web-reported 1H2025 CFO of ~−IDR 4.9tn, which is
  consistent with the inferred figure, raising confidence in the derived
  numbers. (2) Piotroski Accruals component fails — earnings running ahead of
  cash, a genuine (not spurious) flag. (3) Could not directly confirm the
  inventory impairment allowance / obsolescence provision from primary
  filings — insufficient evidence, a real gap given the stranding risk in
  smartphone inventory. (4) Related-party transaction detail not directly
  reviewed — insufficient evidence.
Key Positive Findings:
  1. Multi-year, recently-renewed, large working-capital credit facilities
     from BCA and Mandiri (tranches to 2027/2029) substantially reduce
     near-term refinancing risk despite short-term-debt-heavy optics.
  2. 4-year cumulative FCF is roughly breakeven despite 55% cumulative
     revenue growth — the cash story is "funding growth," not "losing money."
  3. Gross margin has been stable for 4 straight years (~10.9–11.2%),
     PEFINDO idA/stable rating, and a dedicated USD500m FX-forward facility
     suggests import FX exposure is at least partially hedged.
Key Negative Findings:
  1. Days Inventory Outstanding deteriorating (~44.8 → 59–62 days YoY) with
     inventory now 1.7x market cap and only ~51% trade-credit financed —
     the rest is short-term bank debt, into a higher-rate environment.
  2. Operating margin compression (3.0% → 2.2%, 2022–2025) despite stable
     gross margin, and Piotroski's Accruals test failing — both point to
     earnings quality that is weaker than the headline 16% ROE suggests.
  3. Quick ratio of 0.40 and Altman Z in the grey zone (2.68) mean the
     balance sheet has very little non-inventory liquidity cushion if the
     seasonal destocking phase does not materialize on schedule.
Potential Screener False Positives:
  1. "Quality and balance sheet both pass" overstates balance-sheet strength;
     the correct characterization is "serviceable but structurally thin
     liquidity, monitor every quarter," not a clean pass.
  2. FCF yield of −32% (TTM) is a mid-cycle snapshot inflated in badness by
     seasonal inventory timing; taken alone it understates that FCF nets out
     close to breakeven across a full 4-year window.
  3. F-Score 4/9 partly reflects the same seasonal/growth-funded working
     capital dynamic (Current Ratio Improving, Asset Turnover Improving,
     Gross Margin Improving all fail during a heavy build year) rather than
     purely a business-quality signal — but the Accruals failure component
     specifically should NOT be waved away, as it is a genuine cash-vs-paper
     earnings flag.
Financial Verdict: QUESTIONABLE
```
