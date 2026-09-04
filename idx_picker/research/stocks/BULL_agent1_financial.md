# BULL — Agent 1: Financial Forensics

*Status: IN PROGRESS — skeleton, being filled in incrementally.*

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

## 2. Real depreciation charge / vessel depreciation policy

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

## 4. Accumulated deficit — origin and dividend-blocking effect

**NOT SOURCED — insufficient evidence, requires further research.** I searched for the
origin of BULL's accumulated deficit (retained earnings −3,592bn to −3,903bn per the fact
sheet) and did not find a direct source explaining it in this pass. **INFERENCE (moderate
confidence):** BULL was formerly named **PT Buana Listya Tama Tbk** (confirmed independently
via the Pertamina blacklist search below and via Investing.com's ticker description "Buana
Listya Tama Tbk PT" for IDX:BULL) — a large legacy deficit combined with a corporate
rename is a pattern consistent with a past restructuring or financial distress episode
(BULL/Buana Listya Tama's 2022 loss year alone, per the fact sheet, was −787.5bn, which is
roughly a fifth of the total deficit and clearly does not explain all of it) — but I have
**not** confirmed a quasi-reorganisation, debt restructuring, or the pre-2019 history the
task asked for. This needs a follow-up read of the FY2019-2022 annual reports or a
restructuring-specific search ("Buana Listya Tama restrukturisasi utang" / "quasi
reorganisasi").

**On the dividend-blocking question:** under Indonesian company law (UU PT — Law 40/2007,
Art. 71), dividends may only be distributed from **positive net income after covering any
accumulated losses (laba bersih setelah dikurangi kerugian tahun-tahun sebelumnya)**. A
company with a large negative retained-earnings balance is legally required to first offset
that deficit with current profits before any dividend can be declared, unless it undergoes a
formal quasi-reorganisation (PSAK 51) to reset retained earnings to zero against
paid-in capital. **INFERENCE, not company-specific FACT:** given BULL's retained earnings
were still roughly −3,592bn to −3,903bn as of Q1-2026/FY2025 against annual net income in
the 250-580bn range, **the accumulated deficit alone is a sufficient legal explanation for
zero dividends** — BULL would need several more years of profit at even the elevated 2025/
Q1-2026 rate before retained earnings turn positive, absent a quasi-reorganisation. I did not
find a specific company disclosure invoking Art. 71 or announcing a quasi-reorganisation, so
this is my inference from general Indonesian company law applied to the numbers in the fact
sheet, not a sourced company statement.

## 5. Liquidity and debt ladder

**NOT SOURCED — insufficient evidence, requires further research.** I did not find a debt
maturity schedule, lender list, currency/fixed-floating breakdown, or covenant detail in the
web sources located in this pass (no time remained to fetch and parse the AR2025 PDF's debt
note). **INFERENCE:** for a tanker owner financing vessels with secured vessel-level loans,
negative working capital driven by the **current portion of long-term vessel debt** sitting
in current liabilities is structurally normal and not automatically a liquidity red flag —
but this is a general-industry inference, not a BULL-specific verification. The fact sheet's
own framing (current ratio 0.597, quick ratio 0.560, interest coverage 4.58x) is the
best-sourced data point available to me; I could not independently corroborate or refute it
with primary filings in this pass. **A follow-up must read the AR2025 debt note and the
Q1-2026 interim financial statements' liabilities schedule directly.**

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
