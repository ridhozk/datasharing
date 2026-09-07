# BULL — Agent 1: Financial Forensics

*Status: IN PROGRESS — skeleton, being filled in incrementally.*

## URGENT — Q2-2026 (owner-supplied Stockbit data): the revenue-doubling / margin puzzle

**The orchestrator supplied Q2-2026 per-share data from the owner's Stockbit terminal
(2026-09-04) that Yahoo/our pipeline does not carry.** Key reported figures: Q2-2026 revenue
≈ IDR 1,487bn (vs Q1-2026's IDR 741bn — **revenue nearly doubled QoQ**), Q2-2026 EPS IDR
50.04 (vs Q1's IDR 15.45), **net margin (Quarter) 52.12%**. Derived (INFERENCE, per-share ×
15.494bn shares, NOT independently confirmed against a primary filing): Q2 net income
≈ IDR 775bn (~USD 44m); TTM net income ≈ IDR 1,257bn; equity rose only ≈ IDR 840bn QoQ, i.e.
**roughly equal to the quarter's own earnings — INFERENCE: this is consistent with the
equity increase being retained profit, not a fresh capital injection, though I could not
verify this against the actual balance sheet.**

**FACT — found the most plausible driver, and it is NOT a hidden one-off gain: an LNG
spot-rate spike.** [Pasardana.id, 12 March 2026](https://pasardana.id/news/2026/3/12/buana-lintas-lautan-tbk-perkuat-armada-kapal-lng/)
reports that **LNG tanker charter rates "surged nearly 18-fold since late February 2026,
with spot rates reaching US$300,000/day"**, and that BULL took delivery of its **second LNG
tanker (78,000 DWT, ~280m)** in Q1 2026, on top of its first LNG vessel secured December
2025, with **three more LNG units planned for H2 2026**. LNG is explicitly framed as the
company's "second pillar" alongside oil tankers (four pillars: oil tanker / LNG / FSRU /
FPSO-FSO). **INFERENCE, moderately high confidence:** a single 78,000 DWT LNG carrier
earning even a fraction of a $300,000/day spot rate for part of Q2 could plausibly
contribute tens of millions of USD to revenue in one quarter — this is large enough,
relative to BULL's ~USD 42m Q1 total revenue, to explain most of the revenue near-doubling
without needing a change in consolidation scope or a vessel-sale-through-revenue
mechanism. **Voyage costs (fuel, port charges) do not scale anywhere near proportionately
with an extreme spot-rate spike, so the incremental margin on LNG spot cargoes at
$300k/day would be very high — plausibly explaining a blended net margin materially above
BULL's historical (oil-tanker-driven) operating margin, without requiring a hidden
below-the-line gain.** This is my best-sourced hypothesis, not a confirmed reconciliation
of the P&L — I could not obtain the actual Q2-2026 income statement to quantify the LNG
segment's contribution directly (see the unresolved items below).

**IMPORTANT METHODOLOGICAL CAUTION on the "net margin exceeds operating margin" framing
itself.** The orchestrator's own screenshot notes flag that the Gross Profit Margin
(Quarter) 42.11% and Operating Profit Margin (Quarter) 37.32% tiles are **byte-identical to
the Q1-2026 values**, with no "updated" marker — i.e. **these are very likely stale Q1
figures the terminal is carrying forward, not real Q2 figures.** If that is correct, then
"Q2 net margin 52.12% > Q2 operating margin" **is not actually a same-quarter comparison at
all** — it compares a real Q2 net-margin figure against a stale Q1 operating-margin figure.
**This substantially weakens (does not eliminate) the inference that a large non-operating
item is required to explain the margin.** If Q2's true operating margin is itself elevated
(plausible, given the LNG spot-rate spike above), net margin exceeding it would need no
below-the-line gain at all. **I flag this explicitly rather than asserting a hidden gain I
cannot source — treating a stale-tile artifact as a forensic red flag would itself be a
fabrication risk under this project's rules.**

**What I could NOT resolve — insufficient evidence, requires further research with primary
filings:**
- The actual Q2-2026 (or H1-2026) income statement — gross profit, operating income, "other
  income/expense," and finance-cost lines — to test directly for a bargain-purchase gain,
  FX gain, debt-extinguishment gain, or deconsolidation gain. **I could not locate or fetch
  BULL's Q2-2026 filing anywhere** (see Section 1 above and the repeated attempts there);
  this is the single biggest gap preventing a definitive answer to the orchestrator's
  question.
- Whether the **Sinarmas Group investment process** (see below) or the **Hadleigh
  Investment Pte Ltd share-purchase agreement** (Note 31c of the FY2024 audited statements —
  still "in due diligence process" as of the 19 May 2025 report date) closed during H1-2026
  and, if so, whether it changed consolidation scope. **I found no confirmation either way**
  that Hadleigh closed; if it had closed and consolidated new vessel-owning subsidiaries,
  that would be an alternative/additional driver of the revenue jump the orchestrator asked
  me to test for — I could not rule this in or out.
- A **corporate-action / capital-raise event in H1-2026** that might explain part of the
  revenue or equity movement (e.g. a completed Sinarmas-linked placement) beyond the 2025
  Fortune Street placement already documented in Section 6.

**FACT — a live, actively-denied acquisition/investment process by Sinarmas Group is under
way, and it connects directly to two items already in this report.** [Katadata, 22 Dec
2025](https://katadata.co.id/finansial/bursa/6951e4b0e4f4f/bull-angkat-suara-terkait-kabar-masuknya-grup-sinarmas-ini-kata-manajemen):
market rumours that **Sinarmas Group is taking over a minority stake in BULL**; BULL's
Corporate Secretary (Krisnanto Tedjaprawira) would not deny it ("we don't rule out further
collaboration in coming years"); Director Wong Kevin declined comment "before there are
final specifics"; management said it is considering "various strategic steps including
corporate actions and new financing"; and — the connective finding — **management would
not disclose details about Fortune Street Limited, described in this article as a Hong
Kong investor**, which is the **same entity that took the entire 2025 private placement**
documented in Section 6 (1.40bn shares, 9.09%, IDR 253.5bn). **INFERENCE, moderate
confidence: Fortune Street Limited may be a Sinarmas-linked or Sinarmas-adjacent vehicle,**
which would mean the 2025 dilution event was **not** a clean arm's-length capital raise but
a step in an unfolding change-of-control process — I could not confirm this link directly
(the article stops short of stating it), so it remains inference, not fact. **Separately
confirmed as FACT:** PT Bank Sinarmas Tbk has been one of BULL's secured lenders since 2018
(USD 41.4m outstanding at FY2024 per Note 17) — so if a Sinarmas equity stake materialises,
**BULL's largest banking relationship and a prospective controlling/large shareholder would
be the same corporate group**, a related-party-lender configuration worth flagging for any
buyer, though as of the article's date (22 December 2025) **no transaction had closed.**

---

Target: PT Buana Lintas Lautan Tbk (IDX: BULL). Price IDR 464, mkt cap ~IDR 7,189bn (~USD 407m).
Screener fact sheet: `idx_picker/research/stocks/BULL.md` (latest filing in feed: 2026-03-31, Q1).

## 0. Scope and method
- Web research against IDX disclosure (idx.co.id), company IR, Kontan, Bisnis.com, IDNFinancials,
  Emitennews, Stockbit, and any other sources found.
- All claims labeled FACT / INFERENCE / THESIS / ASSUMPTION.
- Missing evidence stated explicitly, not filled in.

## 1. Q2-2026 / H1-2026 numbers

**FACT (Q1-2026, confirms fact sheet, USD terms):** Net income USD 14.2m (Q1-2025: USD 5.9m),
+141% YoY. Revenue USD 43.9m (Q1-2025: USD 39.3m), +11.7% YoY — matches fact sheet's
Revenue +11.8% YoY. Source: [IDX Channel](https://www.idxchannel.com/amp/market-news/laba-buana-lintas-bull-melejit-141-persen-di-kuartal-i-2026-ini-deretan-faktor-penopangnya),
[IDN Financials](https://www.idnfinancials.com/id/news/64358/konflik-as-iran-dorong-laba-bull-melonjak-141-di-kuartal-i-2026).

**FACT — driver detail not visible in the screener's fact sheet:** management attributed the
Q1-2026 jump specifically to **TCE (Time Charter Equivalent) rate increases: Aframax +40.6%
YoY, MR (Medium Range) tankers +43.7% YoY**, plus lower financing costs from debt paydown.
Framed as a genuine rate-cycle/operating-leverage story (extended voyage distances from
US-Iran conflict / Hormuz-Bab el-Mandeb disruption raising ton-mile demand), not a one-off
gain — no vessel-sale gain, insurance recovery, or FX item mentioned in this source.
[Kontan Insight](https://insight.kontan.co.id/news/blokade-hormuz-dan-bab-el-mandeb-angkat-saham-angkutan-migas-bull-jadi-pilihan-utama)
frames BULL as a direct beneficiary of the Hormuz/Bab el-Mandeb blockade trade.

**INFERENCE:** A 40-44% TCE rate rise on top of an already-charter-covered fleet is
consistent with genuine operating leverage (fixed costs, higher revenue per voyage-day)
rather than an accounting one-off. This is a real, sourced explanation the screener could
not see — it materially updates the "why did gross margin jump 14 points" question in
Section 3 below, though I have not yet independently verified TCE numbers against the
actual financial statements (no primary-source interim financials located — see below).

**Q2-2026 / H1-2026 actual results — NOT SOURCED.** Insufficient evidence — requires
further research. What I tried and could not get:
- `bull.co.id/investor-relation/annual-report` — lists annual/sustainability reports only
  through FY2025; no 2026 interim financial statements posted (fetched successfully, page
  content confirmed no Q1/Q2 2026 documents).
- Direct fetch of `idnfinancials.com/bull/...` company page — blocked (HTTP 403).
- Direct fetch of `idx.co.id` company profile / laporan-keuangan pages — not fetched (search
  snippets only; the IDX site returns a static-data PDF index, not parseable via WebSearch
  snippet alone, and WebFetch was not attempted against idx.co.id in this pass due to time
  constraints — **this is a gap, a live agent with more search budget should try
  `idx.co.id/StaticData/NewsAndAnnouncement/.../BULL...` filing indexes directly**).
- WebSearch for Q2-2026 laba/laporan keuangan returns only forward-looking analyst commentary
  (BRI Danareksa: Q1 was ~12% of FY2026 estimate; TCE revenue "expected to more than double"
  by Q2), **not actual reported Q2 results.** As of today (2026-09-04), if BULL follows the
  typical IDX interim filing deadline (H1 reports due ~end of July / late August at the
  latest with extension), a Q2/H1-2026 report should exist by now, but I could not locate its
  content, only an IDX PDF titled "PENGUMUMAN Status Penyampaian Laporan Keuangan" (filing
  status announcement, not the statements themselves) at
  `idx.co.id/StaticData/NewsAndAnnouncement/ANNOUNCEMENTSTOCK/From_EREP/202608/...pdf`
  (August 2026 timestamp in the URL, consistent with an H1-2026 filing-status notice) — I did
  not fetch this PDF's content.
- **THESIS-relevant analyst claim (unverified, treat as ASSUMPTION until confirmed):** BRI
  Danareksa Sekuritas reportedly projects BULL's FY2026 profit at roughly **3x** some prior
  base and expects Q2-2026 TCE revenue to be more than double Q1's — i.e. the sell-side is
  already underwriting the "new run-rate" bull thesis the fact sheet flags as unproven. This
  is a sell-side forecast, not a reported result, and should not be treated as confirmation.

## 2. Real depreciation charge / vessel depreciation policy — RESOLVED FROM PRIMARY SOURCE

**FACT — sourced directly from the audited FY2024 consolidated financial statements**
(`https://bull.co.id/uploads/financial/BULL%202024%20-%20LK%20Audited%2031%20December%202024.pdf`,
opinion signed 19 May 2025 by BDO Indonesia). This supersedes the ballpark estimate below
and the earlier academic-thesis source.

**Actual total depreciation expense (Note 10):**
- **FY2024: USD 15,598,365** (of which USD 15,334,919 vessel depreciation in direct costs +
  USD 263,446 in administrative expenses).
- **FY2023: USD 15,782,350** (USD 15,500,217 + USD 282,133).
- At FX ~17,684 that is **~IDR 276bn/year** — roughly **12x** the screener's implied
  IDR 23bn/yr, and it validates the fact sheet's suspicion exactly: Yahoo's `EBITDA − EBIT`
  proxy massively understates real D&A because Yahoo simply does not carry a usable D&A line
  for this name. **This is the number a rebuilt DCF should use**, not a derived EBITDA-EBIT
  gap.

**Depreciation policy (Note 2j, Note 3b):** BULL uses the **revaluation model** for vessels
under PSAK 16 — carried at fair value at the revaluation date less subsequent accumulated
depreciation/impairment, confirming the academic-thesis finding. Key terms, all sourced:
- **Useful life: 5–35 years**, straight-line, **depreciation rates 2.85%–20%** — a wide band
  that management sets per vessel/vessel-type, reviewed at least annually.
- **Residual (scrap) value: USD 470/LDT (Light Displacement Tonnage) at FY2024** (USD
  495/LDT at FY2023) — reviewed annually against scrap-market prices, so it moves with the
  scrap-steel cycle, not a fixed assumption.
- Latest formal appraisal: **31 December 2022**, by KJPP Indriani, Sauvan & Rekan (OJK-
  registered appraiser, per Indonesia Valuation Standards / Rule VIII.C.4), reviewed and
  carried forward by management since — i.e. the FY2024 revalued carrying amount is **not**
  a fresh FY2024 appraisal, it is a 2-year-old valuation rolled forward. Fair value hierarchy
  Level 2 (market-comparable + discounted-income approach).
- **If vessels were carried at historical cost instead of revaluation, net carrying amount
  would be USD 154,003,679 at FY2024 (vs USD 184,732,442 actually reported)** — i.e. the
  revaluation model currently **inflates the vessel carrying value (and thus equity/book
  value) by ~USD 30.7m, about 20% of the historical-cost base.** This directly bears on the
  fact sheet's P/B-vs-NAV question: **P/B of 1.87x is being measured against a book value
  that already includes a ~USD 31m unrealised revaluation surplus not yet validated by an
  actual arm's-length sale of the current fleet** — a real but bounded overstatement risk,
  not a fabricated one.
- **CORRECTION to an earlier draft of this section:** on closer reading of Note 2j, the
  *gain or loss on sale/retirement of a vessel* (sale proceeds vs. carrying amount) **is
  recognised in profit or loss like any normal disposal** — it is not blocked from the P&L.
  What bypasses the P&L is a **separate, secondary item**: the leftover *revaluation
  surplus* sitting in the equity reserve for that specific vessel is transferred directly to
  the deficit (retained earnings) account on disposal — an equity-to-equity reclassification
  that runs alongside, not instead of, the P&L gain/loss. **Net effect: a large vessel-sale
  gain in Q1-2026 or Q2-2026 is NOT ruled out by this accounting policy** — I was wrong to
  suggest otherwise in an earlier pass of this report. FY2024 shows the disposal side was a
  **net loss** of USD 3,074,844 (proceeds USD 38.3m vs. carrying amount USD 41.4m), i.e. in
  the one year I can see, vessel disposals were a drag on earnings, not a boost — but that is
  FY2024, not Q1/Q2-2026, and tells us nothing about whether a 2026 disposal produced a gain.
  **This remains open — see the Q2-2026 section above for the current best hypothesis
  (an LNG spot-rate spike, not a disposal gain).**

**ASSUMPTION (superseded, kept for the record):** my earlier ballpark sanity-check of
USD 15-20m/yr, made before finding the primary source, turned out to be very close to the
actual USD 15.6m — kept here only to show the estimate was directionally sound, not as a
substitute for the sourced figure above.

## 2b. [renumber note — see Section 2 above for the resolved depreciation finding]

**FACT (sourced, but from a secondary academic source citing BULL's financial statements,
not the primary statements themselves):** a STAN (Indonesian state accounting college)
thesis on BULL's fixed-asset accounting states BULL applies the **revaluation model** (per
PSAK 16) to its vessel fixed assets — carrying vessels at fair value at the revaluation date
less accumulated depreciation and impairment since that date, rather than historical cost.
Source: [perpustakaan.stan.ac.id PDF](https://perpustakaan.stan.ac.id/wp-content/uploads/ninja-forms/13/d-iii_akuntansi/d-iii_akuntansi_6-48_gandhissa-vijayanti_1302181417.pdf)
(not yet fully read — only a search-snippet summary; needs primary verification).

**INFERENCE:** A revaluation model materially changes how "depreciation" should be judged.
If vessels were revalued upward (common when scrap/second-hand values rise in a tanker
up-cycle), the depreciable base increases, which — all else equal — should show up as a
**larger**, not smaller, depreciation charge post-revaluation, plus a revaluation surplus in
OCI/equity that does not flow through the income statement or retained earnings. This cuts
against a simple "understated depreciation flatters earnings" reading and instead raises a
different risk: **equity and book value may be inflated by revaluation surpluses that have
not been market-tested by an actual asset sale**, which matters directly for the "P/B 1.87x
vs NAV" question in the fact sheet.

**NOT YET SOURCED — the actual D&A figure from the cash-flow statement (FY2023/2024/2025,
Q1-2026), and the useful-life/residual-value assumptions (years, % residual).** Insufficient
evidence — requires further research. Web search for the exact policy note (useful life in
years) did not surface a readable primary-source page; the annual report PDFs on bull.co.id
(e.g. `BULL - AR 2025.pdf`) were located but not yet fetched/parsed in this pass — **a
follow-up should fetch `https://www.bull.co.id/uploads/investor/BULL%20-%20AR%202025.pdf`
and pull the fixed-asset note (useful life, depreciation method, residual value) and the
cash-flow statement's D&A line directly.** This is the single most important unresolved item
for this report — it is what the whole DCF-defect finding in the fact sheet hinges on, and
I was not able to close it out with primary-source numbers in the time available.

**ASSUMPTION flagged in the fact sheet, still unverified by me:** Yahoo's implied D&A of
IDR ~23bn/yr is implausible against a IDR 7,211bn asset base; a fleet of oceangoing tankers
typically depreciates over 20-25 years to a residual (scrap) value of roughly 10-15% of cost,
which for BULL's ~USD 400m+ gross vessel base would imply D&A on the order of **USD 15-20m/yr
(~IDR 260-350bn/yr)** — this is a ballpark sanity-check calculation (ASSUMPTION), not a
sourced figure, and should be replaced with the real cash-flow-statement number.

## 3. Earnings quality of Q1-2026 (margin jump decomposition)

**FACT, sourced above:** management's own explanation for the Q1-2026 margin jump is TCE
rate increases (Aframax +40.6%, MR +43.7% YoY) plus lower interest expense from debt paydown
— not a disclosed one-off (no vessel-sale gain, FX gain, insurance recovery, or reversal
mentioned in the sources found). This is a genuine, sourced answer to fact-sheet open
question #3 ("why did gross margin jump 14 points"), though it comes from press coverage of
management commentary, not from reading the financial-statement notes myself line by line
(no "other income" breakdown or non-operating-line detail was available in what I could
fetch).

**Interest expense fall (61.4bn → 38.2bn per fact sheet):** consistent with the debt paydown
narrative in the same press coverage (total debt did fall in the annual/quarterly history:
2,300bn → 2,046bn IDR-equivalent FY2025 vs FY2024, and Q1-2026 debt of 2,283bn is still below
the 2025-Q1 level of 2,300bn). **INFERENCE:** the interest-expense decline is broadly
consistent with the debt trend already in the fact sheet's tables — I did not find a separate
sourced interest-rate or refinancing detail beyond "lower financing costs due to reduced debt
burden."

**Still unresolved — insufficient evidence:** I could not locate the actual income-statement
line items (gross profit USD figure, cost of revenue breakdown, "other income/expense" line)
for Q1-2026 from a primary source; the 141%/TCE explanation is corroborated by two
independent press sources but not by the raw financial statements. **A genuine one-off buried
in a small "other income" line cannot be ruled out from what I found** — this should be
flagged as a residual risk, not resolved.

## 4. Accumulated deficit — origin and dividend-blocking effect — UPDATED FROM PRIMARY SOURCE

**FACT (sourced, audited FY2024 statements, Exhibit C — Statement of Changes in Equity):**
the deficit was already **USD −309,523,121 at 1 January 2023** — i.e. **before** the FY2022
loss year the fact sheet highlights, and before the 2023-2024 recovery. FY2023 net income of
+USD 27,956,492 brought it to −274,131,330 at end-2023; FY2024 net income of +USD 13,751,711
(attributable to owners) brought it to −244,739,725 at end-2024. **This cross-checks cleanly
against the fact sheet's IDR figures at the FX rates in effect: −244.7m USD × ~17,700 ≈
−IDR 4.33tn at FY2024, and the trajectory continuing to improve to the fact sheet's quoted
−IDR 3,903bn at FY2025 and −IDR 3,637bn at Q1-2026 is exactly what continued profitability
should produce** (−244.7m + FY2025 net income of ~USD 24.7m ≈ −220m USD ≈ −IDR 3.9tn at
FX ~17,700 — matches). This is a genuine, useful cross-validation that the fact sheet's
numbers are internally consistent with the primary-source audited statements.

**INFERENCE, revised — the deficit is older and larger than a single bad year can explain.**
A deficit already exceeding USD 300m at the start of 2023 means the accumulated losses
significantly predate 2022. **NOT SOURCED — I could not pin down the exact originating
years/events (pre-2019 history) in the time available**, but the audited notes give real
supporting texture: Note 7 states that **"in connection with the impact of Covid-19, the
Group was unable to fulfill some of the provisions of the loan agreements with [5 non-bank]
creditors,"** and that in 2022-2023 the Group sold the vessels securing those loans and
applied proceeds to debt — i.e. there was a genuine **COVID-era (2020-2022) financial
distress episode involving forced/negotiated vessel sales to non-bank lenders**, on top of
which the Company separately restructured its bank facilities with Panin (April 2022) and
Sinarmas (July 2022) after being **unable to meet loan covenants**. This is a corroborated,
sourced pattern of distress-driven restructuring in 2020-2023, not merely the single 2022
loss year the fact sheet's annual table shows — the deficit is the accumulation of multiple
difficult years, of which 2022 is only the most recent large single-year loss visible in the
4-year table.

**Dividend-blocking effect — reaffirmed and now better evidenced.** No change to the
Article 71 (UU PT 40/2007) legal analysis in the original entry, but it is now on firmer
footing: an accumulated deficit that was still **−USD 244.7m at FY2024** against annual net
income in the USD 13-28m range implies BULL is **many years away** from a legally
positive-retained-earnings position even at the improved 2024-2025 profit run-rate, absent
a quasi-reorganisation (PSAK 51) — which I found **no evidence** the company has undertaken
or announced. **This alone is a sufficient, sourced explanation for the zero-dividend policy
independent of any cash-flow or covenant constraint** — even a cash-rich, covenant-compliant
version of this company would likely still be legally barred from paying a cash dividend.

## 5. Liquidity and debt ladder — RESOLVED FROM PRIMARY SOURCE, and this is a genuine red flag

**FACT — full lender roster and terms (Note 17, FY2024 audited statements):**

| Lender | FY2024 balance (USD) | Secured by |
|---|---:|---|
| PT Bank Woori Saudara Indonesia 1906 Tbk | 45,491,517 | 5 vessels, receivables, corporate guarantee |
| PT Bank Panin Tbk | 41,998,840 | 2 vessels, share pledge, corporate/personal guarantees |
| PT Bank Sinarmas Tbk | 41,444,412 | 5 vessels, controlling-shareholder-family shares/land, corp/personal guarantee |
| PT Bank Oke Indonesia Tbk | 2,997,052 | Land/building owned by entities related to majority shareholder |
| PT Bank MNC Internasional Tbk | 1,374,967 | 1 vessel |
| Short-term loan (Panin PRK) | 2,165,286 | — |

USD-denominated loans carry **7.4%–12.0%**, IDR-denominated **9.5%–11.5%** per annum. All
non-bank lender facilities (Minsheng Qiping, CIMC Aries, Fleetscape entities) were **fully
repaid during 2024**. Note the recurring pattern: **BULL's loan collateral routinely
includes shares and land owned by the Halim Jusuf family / PT Delta Royal Sejahtera group**
(not just vessels) — a related-party credit-support structure, not merely arm's-length
vessel financing (see Section 7).

**FACT — a materially more serious liquidity/covenant finding than the fact sheet's ratios
alone convey. The auditor issued a QUALIFIED opinion specifically on this point, for the
third consecutive year.** Per BDO's independent auditors' report (signed 19 May 2025):
**BULL has been unable to meet the financial-ratio covenants and collateral compliance
provisions in its bank loan agreements since 2022** (covenants include: time-interest-earned
≥2x, current ratio ≥100%, debt/equity ≤2x, debt-service coverage ≥1, loan/vessel-fair-value
and DSCR ≥1.1, collateral-market-value/loan ratio ≥125% — uniform across all facilities).
Under the applicable accounting standard, a breach of this kind should force **reclassification
of the entire non-current portion of the affected bank loans to current liabilities**. BULL's
management **elected not to make this reclassification**, arguing its own internal review of
"settlement procedures" shows no actual breach consequence — the auditor **disagreed and
qualified the audit opinion on exactly this point**, stating explicitly: **"If the
classification of loans from banks had been recognized by the Group in accordance with such
[covenant-breach] conditions, non-current liabilities would decrease by USD 70,721,758 (2023:
USD 88,118,382) and current liabilities would increase by the same amount"** at FY2024 (and
FY2023).

**This means BULL's own auditor believes the current ratio, on a covenant-compliant basis,
is materially worse than reported — by roughly USD 70.7m of understated current liabilities
at FY2024 alone.** The fact sheet's current ratio of 0.597 / quick ratio of 0.560 already look
weak; **a strict reclassification would push reported current liabilities up by roughly
70m against total current assets of only USD 77.1m at FY2024 — i.e. the "true" covenant-
adjusted current ratio would be far below 1, likely in the 0.4x area or worse, not the ~0.6x
the balance sheet shows.** **This is a genuine, sourced, and material accounting risk the
screener could not see and the fact sheet's ratio table does not capture: BULL is in
continuous, multi-year covenant breach on essentially its entire bank debt book, and its
auditor does not agree with management's balance-sheet presentation of that fact.**

**FACT — second, separate qualification, also unresolved since 2022.** Several subsidiaries
defaulted on **non-bank** financing (5 creditors: Uranus Partners, Lavies, Beta, Alpha, Eris
Partners Co. Ltd, all Marshall-Islands/offshore vehicles) during COVID; the secured vessels
were sold and proceeds applied to debt, but **the final settlement amounts were never
reconciled with the creditors.** BULL carries a net **"receivables under reconciliation" of
USD 9,929,376** based on its own unilateral calculation (using a 31 Dec 2021 loan balance
that differs from the creditors' own confirmation replies by USD 4,140,325). The auditor
**could not perform confirmation procedures** and has qualified its opinion on this point
every year since the FY2022 audit, carrying into FY2024 "because of the possible effect of
this matter on the current period." **Post-year-end (per Note 37), BULL did receive partial
payments in March 2025 from 3 of the 5 creditors (Beta, Alpha, Eris — totalling ~USD 1.96m)**
— a positive sign the reconciliation is being worked down, but not yet fully resolved as of
the audit report date.

**FACT — explicit going-concern paragraph.** The auditor's report carries a **"Material
uncertainties related to going concern"** paragraph (not itself a further opinion
modification, but a mandatory disclosure) stating: FY2024 profit of USD 13.79m notwithstanding,
the Group's **accumulated deficit was USD 244.7m and current liabilities exceeded current
assets by USD 41.46m at FY2024**; the Group could not meet the required financial ratios and
collateral provisions of its loan agreements; and the non-bank reconciliation above is
unresolved. The auditor states these conditions **"indicate that a material uncertainty
exists that may cast significant doubt on the Group's ability to continue as a going
concern."** Management's mitigants, per Note 36, are generic (monitor liquidity, seek new
financing "as they deem fit," maintain covenant compliance, "obtained financial support from
ultimate shareholder" — no further detail on what that shareholder support consists of).

**INFERENCE:** none of this necessarily means BULL is at imminent risk of default — the
company has been in this same qualified-opinion/going-concern position for at least three
years running while continuing to operate, refinance, and (per 2025-2026 news) grow its
fleet, and lenders have shown willingness to extend/restructure repeatedly rather than call
loans (e.g. the Sinarmas facility maturity was rolled month-to-month three times in early
2025 per Note 37a). **But a buyer relying on the fact sheet's 0.597 current ratio as "the"
liquidity picture is working from an incomplete number — the company's own auditor believes
the true current-liabilities figure is materially higher, and has said so in writing for
three straight annual reports.** This is one of the most important, concretely sourced
findings in this report.

## 6. Share count / dilution history

**FACT (sourced, corroborated across multiple press sources):**
- BULL held an RUPSLB (Extraordinary GMS) around **September 15, 2025** approving a private
  placement of up to **1,408,585,144 new Series B shares** (par value IDR 100), representing
  up to **10% of issued and paid-up shares**, with maximum dilution to existing shareholders
  of **~9.09%**. Source: [Kontan](https://investasi.kontan.co.id/news/buana-lintas-lautan-bull-akan-private-placement-10-saham).
- The placement was executed: BULL issued **1.40 billion Series B shares** at an execution
  price of **IDR 180/share**, raising **IDR 253.54 billion**, entirely subscribed by
  **Fortune Street Limited**. Source: [KabarBursa](https://www.kabarbursa.com/market-hari-ini/fortune-street-masuk-bull-lewat-private-placement-rp253-miliar),
  [Investor.id](https://investor.id/market-and-corporate/buana-lintas-lautan-bidik-dana-rp-425-miliar-dari-private-placement).
- Stated purpose: strengthen capital structure / balance-sheet ratios and liquidity — i.e.
  **balance-sheet repair, not disclosed as fleet-expansion capital** in the sources found.
  This is a useful, sourced counterpoint to the fact sheet's open question about whether
  dilution funds vessel growth.

**INFERENCE:** this single placement (1.408bn shares at up to 10%) is directionally
consistent with, but does not fully explain, the fact sheet's diluted-share move from
13,962m to 14,452m (a delta of ~490m shares, i.e. roughly a third of the 1.4bn-share
placement) — the placement may have been partially executed, executed in tranches, or there
may be additional dilution sources (MESOP/ESOP, warrants, or an earlier/later placement) not
captured by the one event I sourced. **NOT SOURCED — a 5-year full dilution history (rights
issues, MESOP/ESOP grants, warrant exercises) beyond this one 2025 private placement.**
Insufficient evidence — requires further research; the search surfaced this one event clearly
but no comprehensive multi-year dilution timeline.

**Governance flag (INFERENCE):** a private placement fully subscribed by a single named
entity (Fortune Street Limited) rather than pro-rata to existing shareholders is worth
flagging for the related-party/governance section below — it changes the register of who
controls BULL and was not done via rights issue (which would have preserved existing
shareholders' pro-rata rights). Whether Fortune Street Limited is affiliated with existing
controlling shareholders is **not established** from what I found.

## 7. Related parties

**FACT — historical, and directly relevant to the "who charters the vessels" question:**
PT Pertamina (Persero) issued a **blacklist sanction against BULL (then named PT Buana
Listya Tama Tbk) on 12 March 2018**, over a vessel-charter dispute involving **three Large
Range crude tankers** — two vessels were held by Indonesian customs for import-permit
violations, and all three failed to meet customs obligations at the start of the Pertamina
charter agreement. Source: [Kontan](https://industri.kontan.co.id/news/buana-lintas-lautan-masuk-daftar-hitam-pertamina),
follow-up: [Kontan — negotiation](https://investasi.kontan.co.id/news/di-blacklist-pertamina-buana-lintas-lautan-berupaya-negosiasi).

**INFERENCE / open question:** this is an 8-year-old event (2018) under the company's former
name. Given the fact sheet and general market commentary describe BULL as substantially
Pertamina-charter-exposed today (2026), **the blacklist appears to have been resolved or the
charter relationship rebuilt since 2018** — but I did NOT find a sourced confirmation of
when/how the blacklist was lifted, nor current data on what % of 2025/2026 revenue is
Pertamina vs. other counterparties vs. spot market. This is a material gap: **a buyer relying
on "stable Pertamina time-charter cover" as the reason to trust Q1-2026's margin durability
should know the counterparty relationship has a documented history of dispute**, even if
long past. Insufficient evidence on current-state contract terms and current dispute status
— requires further research (ideally the AR2025 related-party/counterparty note).

**NOT SOURCED:** controlling shareholder identity and track record, % of revenue that is
related-party, and whether vessels are bought/sold with related parties. I searched
specifically for this (Humpuss Maritim was checked as a possible affiliate given sector
adjacency — **no evidence found linking Humpuss Maritim Internasional (HUMI) to BULL; they
appear to be separate, unrelated IDX-listed shipping companies** — this is worth stating
explicitly since a superficial read of the sector could conflate them). Insufficient evidence
— requires further research, ideally IDX's company profile page
(`idx.co.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/BULL`) and the AR2025 ownership
structure page, neither of which I was able to fetch successfully in this pass.

## 8. Auditor, opinion, restatements, IDX sanctions, board listing

**NOT SOURCED — insufficient evidence, requires further research.** I did not locate the
current external auditor's name/opinion, any restatement history, late-filing history, or
current IDX sanctions/warnings against BULL in this pass (beyond the 2018 Pertamina blacklist
above, which is a counterparty sanction, not an IDX/regulatory one). I also did not confirm
or refute the task's premise that BULL is listed on the **"Papan Pengembangan" (Development
Board)** — **this should be checked against the IDX company profile page directly**, since
Development-board listing (vs. Main Board) has real implications for free-float and
governance requirements that bear on minority-shareholder protection, and I could not verify
it. Flagging as an open item rather than assuming the premise is correct.

## Verdict
*(pending — CLEAN / QUESTIONABLE / RED FLAG)*

## Accounting risks a buyer is taking
*(pending)*
