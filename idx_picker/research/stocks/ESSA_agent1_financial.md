# ESSA — Financial Forensics (Agent 1)

**Ticker:** ESSA (PT ESSA Industries Indonesia Tbk.) | IDX | Energy / basic chemicals — ammonia + LPG
**Price:** IDR 655 | Market cap ~IDR 11.28tn (~USD 630m @ 17,908)
**Reporting currency:** USD (functional) | Trading currency: IDR

**Primary sources read directly (not summarised second-hand):**
- 1Q26 interim consolidated financial statements, bilingual, 98pp — balance sheet, P&L, equity statement, cash flow, and Notes 5–35 including Note 24 (revenue), 25 (COGS), 29 (related parties), 30 (segments), 31 (commitments), 32 (concentration risk), 33 (FX), 34 (financing liabilities). `essa.id/wp-content/uploads/2026/04/ESSA-Industries-Indonesia-Tbk-Billingual-FS-1Q26.pdf`
- FY2025 Annual Public Expose summary + Q&A transcript, filed to IDX 8 Dec 2025 (letter No. 0406/LT/EII-EXT/2025).
- AGM/dividend announcements (RUPST 18 Jun 2026), SAF suspension disclosure (27 Jul 2026).

---

## Financial Quality Score: 62/100

The accounting is transparently presented and the accruals are honest. The score is suppressed by economics, not bookkeeping: 90% of revenue is sold to a commonly-controlled counterparty at negotiated prices, 30% of the profit belongs to minorities, ~6% of the ammonia subsidiary's EBITDA is siphoned to shareholder-affiliated "management fees," the dividend exceeds earnings, capex runs at 9% of depreciation, and every load-bearing contract in the business expires in 2027.

---

## Headline corrections to the screener

| Item | Screener | Verified from filings | Delta |
|---|---|---|---|
| **Payout ratio** | **0.2023 (20%)** | **125.59%** of FY2025 attributable NI | **6.2x wrong** |
| FY25 D&A | ~IDR 54bn implied (USD 3.0m) | **USD 46.558m** (Note 30) | **15.5x understated** |
| FY25 capex | IDR 141.7bn (USD 7.9m) | **USD 4.084m** PP&E additions (Note 30) | 1.9x overstated |
| FCF attribution | 100% to ESSA holders | **~27–30% belongs to NCI** | ~IDR 640bn/yr |
| Cash IDR 2,946.9bn | as at 31 Mar 26 | correct, but **IDR 895.8bn paid out 15 Jul 26** | 30% stale |
| Revenue concentration | not captured | **89.88% to one related party** | — |
| EV/EBITDA 6.25x | — | ~4.8x on corrected EBITDA | screener too *expensive* |
| Dividend IDR 52 | ✓ | ✓ IDR 895.8bn, paid 15 Jul 2026 | ✓ |
| Total debt ≈ nil | ✓ | ✓ USD 134,524 of lease liabilities only | ✓ |

**FACT — the lead is confirmed and quantified.** The FY2025 dividend of IDR 52/share (IDR 895.8bn total) approved at the AGM of 18 June 2026 equals **125.59% of FY2025 net profit attributable to owners of the parent of USD 40,291,033**, with approximately **IDR 182.65bn drawn from retained earnings** to cover the shortfall. The screener's 0.2023 is refutable from the screener's own table without any external data: FY2025 attributable NI of IDR 721.5bn ÷ 17,226,975,700 shares = **EPS IDR 41.9 against DPS IDR 52**.

---

## Earnings Quality

**FACT — accruals are clean; the CFO premium is depreciation, not quality.**
- 1Q26 CFO USD 45.529m vs net profit USD 26.755m (1.70x); 1Q25 CFO USD 18.347m vs NP USD 10.680m (1.72x).
- The gap reconciles precisely: FY2025 depreciation expense **USD 46.558m** (Note 30) against consolidated NP USD 55.067m → NI + D&A ≈ USD 102m, matching the ~USD 104m FY2025 CFO reported in the market.
- 1Q26 depreciation splits USD 11.365m inside manufacturing expenses (Note 25) + USD 0.290m in G&A + USD 0.444m intangible amortisation.
- No receivable or inventory build is masking earnings: trade receivables USD 31.567m vs 30.982m at Dec-25; inventories USD 40.520m vs 37.121m — a USD 3.4m build against a USD 25.6m revenue increase, i.e. genuinely modest.

**INFERENCE: the 1.7–1.9x CFO/NI ratio is not evidence of conservative accounting. It is what a plant with USD 332.7m of accumulated depreciation against USD 729.4m of gross PP&E mechanically produces. Treating it as a quality signal is the error the screener makes.**

**FACT — the cycle has turned, hard.** 1Q26 vs 1Q25: revenue USD 95.214m vs 69.622m (+36.8%); gross profit USD 43.637m vs 22.263m (+96.0%); gross margin 45.8% vs 32.0%; PBT USD 34.680m vs 13.608m (+154.9%); attributable NI USD 18.756m vs 8.128m (+130.8%). EPS (per 1,000 shares) 1.089 vs 0.472.

**Concern — a direct-method reconciliation gap.** 1Q26 "Received from customer" USD 119.312m against revenue of USD 95.214m — a USD 24.1m excess, with receivables essentially flat. **INFERENCE (moderate confidence): VAT-inclusive receipts and/or collection of a 4Q25 year-end receivable spike (Dec-25 receivables were elevated relative to 4Q revenue). Not fully resolved — requires the FY2025 audited cash flow to close.**

**Concern — cash tax is near zero and will not stay there.** 1Q26 income tax expense USD 7.925m, but the deferred tax liability rose USD 7.427m (39.420m → 46.847m), so **current tax was only ~USD 0.5m**. Cash income tax paid was USD 0.670m against a USD 1.224m refund received — **net cash tax was positive (an inflow) in 1Q26 on USD 34.7m of pre-tax profit.** *Nature and expiry of the incentive (pioneer-industry tax holiday? accelerated tax depreciation?) — insufficient evidence, requires further research (PAU commenced commercial operations 2018; a standard 10-year Indonesian tax holiday would expire 2028, which would be a material forward FCF drag, but this is an ASSUMPTION not established.)*

---

## Balance Sheet

**FACT — genuinely debt-free with a large net cash position (31 Mar 2026, USD):**

| | 31 Mar 2026 | 31 Dec 2025 |
|---|---|---|
| Cash and cash equivalents | 164,558,658 | 125,760,092 |
| Investment in bonds | 12,250,000 | 6,950,000 |
| Trade receivables (of which related party) | 31,567,147 (25,001,923) | 30,981,858 (24,701,739) |
| Inventories | 40,519,729 | 37,120,540 |
| PP&E net | 396,752,833 | 406,671,911 |
| Goodwill | 23,687,119 | 23,687,119 |
| **Total assets** | **682,797,924** | **646,558,220** |
| Total liabilities | 72,396,233 | 62,911,891 |
| — of which deferred tax liability | 46,846,629 | 39,420,001 |
| — of which employee benefits | 4,138,277 | 4,138,277 |
| — **interest-bearing (lease only)** | **134,524** | **179,264** |
| Equity attributable to owners | 465,358,288 | 446,602,727 |
| **Non-controlling interests** | **145,043,403** | **137,043,602** |
| Total equity | 610,401,691 | 583,646,329 |

- **70% of total liabilities are deferred tax and employee benefits** — non-interest-bearing, non-near-term-cash. Bank borrowings are **zero**.
- **FACT — deleveraging was recent and total.** Note 34: bank loans USD 92.233m at 1 Jan 2025 → **nil at 31 Dec 2025**, via USD 124.038m of principal repayments (partly refinanced with USD 30.0m of short-term draws) and USD 1.841m of interest. Annual total debt: IDR 4,834.5bn (2022) → 2,885.8 → 1,657.5 → 3.2bn. Interest expense IDR 445.0bn (2022) → 25.3bn (2025) → **zero in 1Q26** (Note 27: the only finance cost is USD 0.449m of "other financial charges").
- Current ratio 11.5x is real, not an artefact of misclassification.

**FACT — the screener's balance sheet is one dividend stale.** The IDR 2,946.9bn of cash was struck at 31 Mar 2026. IDR 895.8bn (30% of it) left the company on **15 July 2026**. Pro-forma cash is ~IDR 2,051bn.

**FACT — 79.2% of trade receivables are from a single related party**, Genesis Corporation (USD 25.002m of USD 31.567m). Consistent at Dec-25 (79.73%). No ageing or impairment disclosure in the interim.

**Concern — revaluation surplus is being recycled into distributable reserves.** Equity carries "Surplus revaluasi aset tetap" of USD 16.414m (Dec-25: 17.085m), released to unappropriated retained earnings at USD 0.671m/quarter (USD 2.683m in FY2025). **INFERENCE: this is a non-cash transfer that enlarges the retained-earnings pool from which the >100% payout was funded, and part of the depreciation charge in P&L relates to written-up carrying values rather than historic cash cost.**

---

## Cash Flow Quality — is the ~20% FCF yield real and repeatable?

**Verdict: real in cash terms, but the shareholder's actual claim is ~14%, and the run-rate is flattered by an under-invested asset base and a near-zero cash tax rate.**

**Deduction 1 — non-controlling interests take ~30% (largest issue).**
- **FACT:** PAU (PT Panca Amara Utama, the ammonia plant, commercial ops 2018) is **69.997% owned**, indirectly through ECI. PAU holds USD 557.98m of the group's USD 682.80m of assets — **PAU *is* the company**.
- FY2025 profit split: owners USD 40.291m / **NCI USD 14.776m (26.8%)**. 1Q26: USD 18.756m / **USD 7.999m (29.9%)**.
- **FACT — and NCI actually extracts the cash.** FY2025 dividends paid (equity statement): **USD 10.271m to owners of the parent, USD 15.001m to non-controlling interests.** The minorities took 59% of all dividends paid by the group.
- The screener divides *consolidated* FCF (IDR 2,283bn) by ESSA's *equity* market cap. **Attributable FCF yield is ~14%, not 20.2%.**

**Deduction 2 — capex is 9% of depreciation. This is a paused run-rate, not maintenance.**
- **FACT (Note 30):** FY2025 additions to PP&E **USD 4.084m** against depreciation expense of **USD 46.558m** — **8.8%**. 1Q26 additions USD 1.736m (cash capex USD 1.476m) against USD 11.655m of depreciation — **14.9%**.
- Net PP&E fell USD 406.673m → 396.753m in a single quarter. The asset base is shrinking.
- Repairs and maintenance in manufacturing expenses jumped to USD 1.788m in 1Q26 from USD 0.571m in 1Q25 (+213%) — **INFERENCE: deferred maintenance beginning to surface as expense.** (A PAU turnaround was reported in the trade press.)
- **Management guided ~USD 20m of 2026 capex for LPG and ammonia operational maintenance** (Public Expose Q&A, 3 Dec 2025) — 5x the 2025 rate, and still **43% of depreciation**. Normalising to USD 20m removes ~IDR 285bn from FCF; normalising to full D&A removes ~IDR 760bn.

**Deduction 3 — growth capex: deferred, then formally suspended, but not cancelled.**
- **FACT:** the only committed growth project is **SAF (Sustainable Aviation Fuel, HEFA route from used cooking oil)** through **PT ESSA SAF Makmur (ESM), 62% owned**, total assets USD 12.050m.
- **FACT (Note 31e):** ESM signed a **FEED agreement with PT Tripatra Engineers on 1 December 2025** for a **5,000 BPSD** SAF facility, scope including "development of an EPC capital cost estimate" — i.e. materially further along than pre-FEED.
- **FACT (Note 31d):** ESM signed an **Investment Commitment Agreement with PT Kawasan Industri Terpadu Batang (KITB) on 25 October 2024**, leasing **103,679 m² at IDR 1,000,000/m² = IDR 103,679,000,000** (~USD 5.8m) of committed land.
- Plant scale as announced: ~150,000 t/yr (260m litres), potential revenue ~USD 312m — **more than ESSA's entire FY2025 revenue of USD 295.0m.** Original COD target 4Q27–1Q28.
- **FACT: on 27 July 2026 ESSA disclosed the SAF project is postponed**, citing "strategic factors and current market conditions," with no revised timeline; management stressed it is a suspension, not a cancellation.

**THESIS: the task brief's framing is inverted. A second ammonia plant / soda ash project is not what is on the table, and near-term FCF is *not* about to be consumed by growth capex — it has been freed up precisely because the growth project was suspended. The real risk is the opposite: ESSA is distributing >100% of earnings today while carrying a suspended-but-live commitment to a plant that would likely cost several years of FCF, against a shrinking asset base and no committed feedstock beyond 2027. Suspending SAF and simultaneously stepping the dividend up 5.2x is a capital-allocation choice that spends optionality.**

---

## Capital Allocation

**FACT — the sequence is debt → dividend.**

| Year | DPS | Total | Payout on attributable NI |
|---|---|---|---|
| FY2024 | IDR 10 | ~IDR 172bn | ~23% |
| **FY2025** | **IDR 52 (5.2x)** | **IDR 895.8bn** | **125.59%** |

Bank debt was extinguished in December 2025; the payout was stepped up 5.2x six months later at the 18 June 2026 AGM, funded partly out of retained earnings (~IDR 182.65bn), and paid 15 July 2026. Indicated yield at the IDR 650 close on 18 June 2026 was ~8.0%.

**No fixed payout-ratio policy was disclosed.** At the December 2025 Public Expose, management explicitly declined to commit: *"tebaran dividen ESSA akan ditentukan oleh para pemegang saham... akan ditentukan melalui RUPS Tahunan di tahun 2026."* Management also set **no revenue or profit target for 2026**.

**FACT — the parent depends on upstreaming from a 70%-owned subsidiary to pay its dividend.** Segment Note 30 for FY2025 shows the LPG segment (the parent) booking USD 35.071m of "other gains and losses" that is eliminated on consolidation (eliminations column: −USD 35.165m of other gains, −USD 35.028m of PBT). **INFERENCE (high confidence): this is an intragroup dividend from PAU up to the parent.** The parent's own operating economics are thin — the LPG segment's standalone FY2025 result was USD 16.193m of gross profit against USD 9.879m of G&A. **The IDR 895.8bn dividend (~USD 50–55m) therefore requires PAU distributions substantially larger than FY2025's, and every dollar PAU distributes leaks 30% to the minorities.**

**FACT — a permanent related-party tax on EBITDA sits above the shareholder.** Note 29 / Note 31:
- **PT Akraya International (a shareholder): 4% of PAU's EBITDA** post-commercial-production, under an agreement running to 3 December 2027 (originally USD 2.0m/yr during construction).
- **PT Mega Consultindo Perdana: a further 2% of PAU's EBITDA**, also to 3 December 2027.
- **ESM: Akraya takes 3% of ESM's EBITDA quarterly for 20 years** from commercial operation (agreement dated 31 Jan 2025).
- **Combined, ~6% of the ammonia business's EBITDA is paid away to related/affiliated service providers before minorities and before shareholders.**
- 1Q26 management fees totalled **USD 3.354m, up 72.9% YoY** from USD 1.940m; Akraya alone took **USD 2.383m = 20.47% of all G&A**. It scales with EBITDA, so it rises with every up-cycle.

**Assessment.** ASSUMPTION: IDR 52 is a one-off catch-up enabled by the debt-free balance sheet and struck against a trough earnings year. Annualising 1Q26 attributable NI of USD 18.756m gives ~USD 75m for FY2026, which would put IDR 52 back at a ~67% payout — sustainable. **But the screener's implied combination — an 8% yield with a 20% payout — is arithmetically impossible, and a repeat of IDR 52 in another trough year would be balance-sheet liquidation.**

---

## Accounting Concerns

1. **89.88% of revenue is a single related party under common control.** Note 24/29: **Genesis Corporation (Japan)** took USD 85,581,149 of 1Q26's USD 95,213,790 (85.43% in 1Q25). Note 29 states sales prices are "determined based on agreement" and carries the standard warning that terms "may not be the same as those of the transactions between unrelated parties." **This is the single most important forensic fact about ESSA: the revenue line, the 45.8% gross margin, and therefore essentially the entire reported earnings base of the group are set by a price agreement with a commonly-controlled counterparty, and cannot be independently verified from the outside.** Mitigant: a 26 Jan 2023 amendment aligned the ammonia pricing formula to "relevant regional price index," and the gas feedstock price formula is reported to move progressively with global ammonia prices, which is consistent with observed margin behaviour. But the mitigant is disclosure, not independence.
2. **Yahoo's D&A is 15.5x understated** (implied USD 3.0m vs actual USD 46.558m). Any EV/EBITDA, EBITDA margin, or DCF depreciation assumption from the screener is void for this name. Directionally this makes ESSA look *more* expensive than it is on EV/EBITDA (~4.8x corrected vs 6.25x reported) — the one screener error that works in the investor's favour.
3. **Mixed attribution throughout the screener.** EV correctly adds NCI (11,283.7 + 2.4 − 2,946.9 + 2,597 ≈ IDR 10,939bn ✓), so EV/EBIT is internally consistent. But **FCF yield, PE, P/B and dividend yield are equity-claim metrics computed against consolidated cash flow.** Further: NCI is added to EV at **book value USD 145.0m**, whereas 30% of PAU's ~USD 49m of annual earnings at the group's ~12x multiple is worth ~USD 177m — so EV is understated by roughly USD 32m (~5% of market cap).
4. **Revaluation surplus recycling** (USD 2.683m FY2025, USD 0.671m 1Q26) — non-cash, inflates distributable reserves.
5. **Near-zero cash tax with a rapidly building deferred tax liability** (+USD 7.427m in one quarter, 94% of the tax expense). A forward FCF drag not reflected in any trailing metric.
6. **Goodwill USD 23.687m** carried flat, no interim impairment testing disclosed. Small (5.1% of parent equity).
7. **No formal FX hedging policy** (Note 33) — though see below, exposure is trivial.

---

## Priority questions — answers

**Q1 — Is the ~20% FCF yield real and repeatable?**
Cash-real, but overstated and not durable at that level. Attributable yield is **~14%** after NCI. It is further flattered by capex at 8.8% of depreciation and a ~1% cash tax rate. At guided USD 20m capex and a normalised tax rate, sustainable attributable FCF is roughly **USD 55–70m (~9–11% yield)** — still good, not 20%.

**Q2 — Dividend sustainability.**
**125.59% payout**, ~IDR 182.65bn from retained earnings, no stated policy, 5.2x step-up, and structurally dependent on upstreaming from a 70%-owned subsidiary where 30% leaks to minorities and 6% of EBITDA leaks to affiliated managers. Sustainable at 1Q26 run-rate earnings (~67% payout); not sustainable at trough earnings.

**Q3 — Why the −26% 3Y revenue CAGR? Price or volume? Trough or normal?**
**Price, not volume — INFERENCE at high confidence.** FY2022 revenue of IDR 13,099.5bn coincided with the post-Ukraine European gas crisis that drove ammonia to record levels; FY2023–25 sit in a IDR 5.3–6.2bn band. The margin signature is diagnostic: gross margin collapsed 46.6% (2022) → 29.9% (2023) and recovered to **45.8% in 1Q26 on +36.8% revenue** — a fixed-cost-base price move, not volume loss. Confirming detail: **LPG revenue was flat-to-down (USD 9.321m 1Q25 → 8.749m 1Q26) while ammonia rose 43.9% (USD 59.477m → 85.581m)**; LPG volumes are contractually fixed at 62,000 MT/yr to Pertamina Patra Niaga, so ammonia price is doing all the work. **THESIS: 2023–25 was the trough; 1Q26 is an up-leg. Do not extrapolate the −26% CAGR — but equally, do not capitalise 1Q26.** Screener's own Normalised/Trailing EBIT of 0.85 is the right instinct.

**Q4 — USD/IDR mismatch: is it naturally hedged?**
**FACT: yes, almost completely.** Functional and reporting currency is USD. Ammonia and LPG are USD-priced. Bank debt is zero, so there is no FX-denominated debt at all (the FY2025 cash-flow hedge was closed out — the hedging reserve in OCI went to nil at Dec-25, consistent with repayment). **Note 33 quantifies the entire non-USD monetary position as a net liability of USD 974,236** — 0.15% of market cap, immaterial. Residual exposures: IDR operating costs for 484 employees, and the IDR-declared dividend. **INFERENCE: the business is naturally long USD; IDR weakness is net favourable to an IDR-based holder. This is one of the few IDX names where the currency mismatch is genuinely a non-issue.** The screener's FX handling checks out exactly (USD 164.559m × 17,908 = IDR 2,946.9bn ✓).

**Q5 — Balance sheet, commitments, contingencies, related parties.**
Covered above. Commitments are modest in cash terms: **IDR 103.679bn KITB Batang land**, the Tripatra FEED contract (value undisclosed), and the EBITDA-linked management fees. **No project finance, no guarantees, and no litigation contingencies are disclosed in the 1Q26 notes.** There is no Note titled "contingent liabilities" — *the absence is itself worth confirming against the FY2025 audited annual report; insufficient evidence to conclude none exist.*

---

## The 2027 cliff — the finding that dominates everything else

**FACT.** Every load-bearing contract in the business expires within ~16 months of each other, and the company's own Note 32 (Concentration Risk) states that termination "could result in **cessation of the business** of the Company and/or subsidiary":

| Contract | Counterparty | Expiry |
|---|---|---|
| Ammonia offtake — **entire production**, FOB | Genesis Corporation (related, common control) | **3 Dec 2027** |
| PAU gas feedstock, 62 MMSCFD, **sole supplier** | JOB Pertamina Medco Tomori Sulawesi | **2027** |
| LPG plant gas feedstock, 70 MMSCF/day, 456.81 BSCF | Pertamina EP (sole supplier) | **31 Dec 2027** |
| LPG offtake, 62,000 MT/yr | Pertamina Patra Niaga | **31 Jul 2027** |
| Management services (4% of PAU EBITDA) | PT Akraya International (shareholder) | 3 Dec 2027 |
| Advisory services (2% of PAU EBITDA) | PT Mega Consultindo Perdana | 3 Dec 2027 |

Raw material concentration confirms the dependency: 1Q26 purchases were **USD 28.490m from JOBPMTS and USD 3.782m from Pertamina EP** — 62.6% of the USD 51.577m cost of revenue from two counterparties. **THESIS: ESSA is a 100%-single-supplier, ~90%-single-customer business whose entire contractual scaffolding rolls in 2027. The screener's Safety Score of 95.6 and Altman Z of 11.26 measure a pristine balance sheet and are blind to this. It is the correct place for the Thesis Killer to start.**

---

## Key Positive Findings

1. **Genuinely debt-free with a large, verified net cash position.** Interest-bearing debt USD 134,524 against cash USD 164.559m plus USD 12.250m of bonds. USD 92.2m of bank loans extinguished in FY2025. Interest expense went from IDR 445bn (2022) to zero. 70% of reported liabilities are deferred tax and employee benefits, not near-term cash claims. This one is exactly as good as the screener says.
2. **Accruals are honest and the disclosure is genuinely good.** CFO/NI of 1.70–1.72x reconciles precisely to depreciation; no receivable or inventory build masks earnings; the company discloses its related-party revenue concentration, its EBITDA-linked affiliate fees, and its single-supplier dependency explicitly and in detail. Nothing here had to be dug out — it is in the notes.
3. **The cycle has turned and the screener is looking at the trough.** 1Q26 revenue +36.8%, gross margin 45.8% vs 32.0%, attributable NI +131%, with ammonia doing all of it. The FY2025 snapshot the screener capitalises is the bottom, and the gas price formula is indexed to ammonia prices, which structurally protects the margin on the way down.
4. **The FX question is genuinely settled.** Net non-USD monetary exposure of USD 0.97m against a USD 630m market cap. Long USD, zero FX debt.

## Key Negative Findings

1. **The dividend is being paid out of the balance sheet, and the screener says the opposite.** 125.59% payout vs a reported 20.23%, IDR 182.65bn from retained earnings, a 5.2x step-up with no stated policy, structurally dependent on upstreaming from a 70%-owned subsidiary.
2. **Roughly 90% of revenue is sold to a commonly-controlled related party** whose pricing the company itself flags may not be arm's-length, under a contract that expires 3 December 2027. The entire earnings base is related-party determined and externally unverifiable.
3. **Three separate leaks sit between EBITDA and the shareholder:** ~30% to NCI at PAU (who took USD 15.0m of FY2025's USD 25.3m of dividends — more than ESSA's own shareholders), ~6% of PAU EBITDA to shareholder-affiliated management-fee counterparties, and a near-zero cash tax rate that will normalise.
4. **Capex at 8.8% of depreciation against a shrinking asset base**, with repairs and maintenance up 213% YoY and the one growth project (SAF) suspended on 27 July 2026 — cash is being distributed rather than reinvested, into a 2027 contract cliff.

## Potential Screener False Positives

1. **Payout ratio 0.2023 — wrong by 6.2x; the true figure is 125.59%.** This makes an uncovered dividend look conservatively covered and lets the model simultaneously credit an 8.19% yield *and* compounding retained earnings. It is the same cash counted twice.
2. **FCF yield 20.24% mixes consolidated cash flow with an equity-only market cap.** Attributable is ~14%, and ~9–11% once capex normalises to guided USD 20m and cash tax normalises. This same consolidated FCF (IDR 2,283bn) feeds **EPV of IDR 708/share** and the **Blended IV of IDR 732** — so the 10.5% MOS and 11.7% Upside are overstated and are plausibly **negative** on an attributable basis. **The WATCH verdict is, if anything, still too generous.**
3. **Cash of IDR 2,946.9bn is stale by one dividend.** IDR 895.8bn (30%) left on 15 July 2026, after the 31 Mar 2026 balance-sheet date. Net Debt of −IDR 2,944.5bn, Altman Z of 11.26, Current Ratio of 11.46, Working Capital of IDR 4,008bn and the EV of IDR 10,939bn all embed cash that is gone.
4. **Safety Score 95.6 and Altman Z 11.26 measure only the balance sheet** and are structurally blind to a business with one supplier per plant, one customer for 90% of revenue, and every contract expiring in 2027. Zero Red Flags is a false negative.
5. **Yahoo's D&A is 15.5x understated**, voiding EV/EBITDA 6.25x (true ~4.8x) and FY2025 EBITDA of IDR 1,343.6bn (true ~IDR 2,100bn). This one is a false *negative* — ESSA is cheaper on EV/EBITDA than shown.
6. **Beta 0.206** — below the CLAUDE.md-mandated [0.5, 2.5] trust band, so the cost-of-equity floor should be binding here. Worth confirming the DCF actually applied it.

---

## Financial Verdict: **QUESTIONABLE**

Not because the books are unreliable — the disclosure is detailed, internally consistent, and the accruals are clean — but because the reported earnings are, by the company's own Note 29, set by agreement with a commonly-controlled counterparty that buys ~90% of output under a contract expiring December 2027, and because the three headline attractions the screener surfaces (8.2% yield, 20.2% FCF yield, 10.5% MOS) are each overstated in the same direction by errors I can quantify. The balance sheet is genuinely excellent and the cycle is genuinely turning; that is what keeps this off FAIL. But a 125.6% payout funded from reserves, capex at 9% of depreciation, and a 2027 cliff on feedstock and offtake simultaneously are not the profile of a name that should reach a research shortlist on a Safety Score of 95.6 with zero red flags.

**Handoff to Agent 5 (Thesis Killer):** the kill shot is not the balance sheet, it is the December 2027 concurrent expiry of the Genesis offtake, both gas supply agreements, and the Pertamina LPG contract — against a company that has suspended its only growth project and is distributing more than it earns.
