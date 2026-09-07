# AMMN — Financial Forensics

*Financial Forensics Agent output. All figures cross-checked between the screener sheet (IDR bn, FX 17908) and USD-denominated third-party sources (stockanalysis.com, AMMAN press releases). USD and IDR figures reconcile closely (e.g. FY2025 revenue: IDR 33,067.5bn / 17,908 = US$1,846.5M vs. US$1,847M reported — confirms the screener's FX conversion is not materially distorting this name, unlike the ITMG-type cases flagged in project memory).*

```
Financial Quality Score: 34/100
```

## Earnings Quality

**FACT.** FY2025 net income attributable to parent owners was US$248.97M (IDR 4,458.7bn), down from US$636.9M (IDR 11,405.5bn) in FY2024 — a 61% YoY decline, consistent with screener's Net Income CAGR 3Y of −38.9%. [amman.co.id FY2025 Earnings Release; search corroboration]

**FACT.** Operating cash flow (which the screener records as missing/blank) was **negative** in 3 of the last 5 fiscal years per third-party data: FY2021 +$293.6M, FY2022 +$990.5M, FY2023 **−$121.2M**, FY2024 +$151.7M, FY2025 **−$475.0M**. [stockanalysis.com/quote/idx/AMMN/financials]

**INFERENCE.** FY2025 net income (+$249M) was positive while operating cash flow was negative (−$475M) — a ~$724M gap between reported profit and cash generated. This is a classic accrual/earnings-quality red flag: profit is being recognized (likely via unbilled receivables, inventory build from concentrate-export restrictions, or capitalized costs) faster than cash is collected. This single fact is sufficient to explain much of the F-Score weakness.

**FACT.** Gross margin compressed from 57.9% (2022) → 44.4% (2023) → 50.5% (2024) → 45.3% (2025), computed from the screener's annual GrossProfit/TotalRevenue. Asset turnover (Revenue/TotalAssets) fell from 0.44x (2022) to 0.13x (2025) as the balance sheet nearly tripled (TotalAssets IDR 116.4tn → 248.4tn) while revenue fell — assets are being added far faster than they are producing revenue, consistent with a large under-construction, non-revenue-generating smelter sitting on the balance sheet.

**INFERENCE — reconstructed Piotroski components.** Using the screener's disclosed annual line items, the 9 Piotroski tests resolve approximately as follows:
| Test | Result | Basis |
|---|---|---|
| ROA > 0 | **PASS** | TTM ROA 3.1%, FY2025 NI positive |
| CFO > 0 | **FAIL** | FY2025 OCF ≈ −$475M |
| ΔROA > 0 | **FAIL** | NI −61% YoY on a growing asset base |
| CFO > NI (accrual quality) | **FAIL** | OCF (−$475M) << NI (+$249M) |
| Δ Leverage (down) | **FAIL** | Total debt +50% YoY (IDR 76.7tn→115.2tn 2024→2025); D/E rose |
| Δ Current ratio (up) | **FAIL/mixed** | 3.45x (2022) → 2.02x (2024), partial recovery to 2.24x (2025) |
| Δ Shares outstanding (flat/down) | **PASS (roughly)** | Diluted shares 71.9→68.8→72.5→72.5 (2022–2025), no material recent dilution |
| Δ Gross margin (up) | **FAIL** | 50.5% (2024) → 45.3% (2025) |
| Δ Asset turnover (up) | **FAIL** | 0.24x (2024) → 0.13x (2025) |

This reconstruction yields ~2 of 9 passes, closely matching GuruFocus's independently reported Piotroski F-Score of **2** for AMMN [gurufocus.com/term/fscore/ISX:AMMN] and corroborating the screener's F-Score of 3. **Conclusion: the F-Score of 3 is real, not a data artifact** — it is driven by genuinely negative operating cash flow, an accrual gap between NI and CFO, rising leverage, margin compression, and collapsing asset turnover, all simultaneously.

## Balance Sheet

**FACT.** Net debt at FY2025 year-end: US$5,756M (per AMMAN's own FY2025 earnings release) to US$5,785M (stockanalysis.com) — both sources agree closely. Total debt US$6,432–6,462M against consolidated cash of ~US$677M. This converts to the screener's Net Debt (Quarter) of IDR 101.4tn and Total Debt of IDR 116.0tn at Q1 2026 (which is in USD terms roughly flat-to-slightly-down from FY2025, consistent with early smelter capex tapering).

**FACT.** Total debt has grown from US$1,842M (2022) → US$3,251M (2023) → US$4,318M (2024) → US$6,462M (2025) — a **3.5x increase in three years**, funding the smelter/refinery build. Debt/Equity (Quarter) is 1.18x per screener.

**FACT.** AMMAN describes its debt maturity profile as "back-ended," structured to align with the ramp-up of the smelter/mine expansion [FY2025 Earnings Release, per search summary]. **INSUFFICIENT EVIDENCE** — the specific year-by-year maturity schedule, coupon rates, covenant package (leverage covenants, DSRA requirements), and lender identities (export prepayment facility vs. syndicated term loan vs. bonds) could not be extracted from the PDF earnings releases via automated fetch (binary/encoded PDF content defeated the fetch tool) or from search snippets. This is a material gap given BI's 5.75% policy rate and the scale of near-term refinancing risk implied by a back-ended structure — **requires further research** (direct read of the FY2025 audited financial statement notes on borrowings, or the AMMN bond/loan prospectus, via IDX filing portal).

**FACT.** Interest expense has risen from IDR 2,550.1bn (2022) to IDR 6,913.3bn (2025), a 2.7x increase, consistent with the debt build-up. Screener's Interest Coverage (TTM) of 2.35x is thin for a company this leveraged and mid-capex-cycle — a moderate commodity price or production shortfall could pressure coverage below 1x.

**FACT — minority interest.** AMMN's operating subsidiary, PT Amman Mineral Nusa Tenggara (AMNT, which holds the Batu Hijau/Elang assets), was 82.2%-owned by AMMN after the 2016 acquisition from Newmont-related sellers, with PT Pukuafu Indah holding 17.8%; AMMN subsequently **acquired the remaining stake from Pukuafu Indah in December 2020, bringing its ownership of AMNT to 99.99%** [amman.co.id / historical M&A reporting]. **INFERENCE:** consolidated-level non-controlling interest is therefore likely immaterial post-2020 — consistent with the screener's FY2025 net income (IDR 4,458.7bn / $249M) matching almost exactly the externally reported "net profit attributable to parent owners" of $248.97M. This is a reassuring finding against the project memory's standing concern that "net income is Yahoo's consolidated figure and may include minority interest" — for AMMN specifically, the attributable and consolidated figures appear to converge, so EPS/PE/ROE are **not** materially overstated by a minority-interest omission. Note: PT Medco Energi Internasional's ~20.9% stake is at the **AMMN parent/listco level** (a shareholder of the company being valued, i.e., already reflected in the share count), not a subsidiary-level minority interest — it does not affect EV or attributable earnings.

## Cash Flow Quality

**FACT.** FCF was negative in FY2023, FY2024, and FY2025 (−$1,641M, −$1,640M, −$1,847M respectively per stockanalysis.com), matching the screener's IDR figures closely (FreeCashFlow: −29,383.8bn, −29,371.0bn, −33,083.0bn). The screener's TTM FCF yield of −6.6% on a US$20bn+ market cap represents cash burn in the billions of dollars, funded almost entirely by debt issuance (total debt +$2.1bn in FY2025 alone).

**FACT — capex breakdown.** Total FY2025 capex was ~US$1,372M (IDR 24,577.4bn per screener). Quarterly capex is now declining sharply: IDR 7,156.6bn (Q4-2024) → 6,439.0 → 6,437.9 → 5,630.7 → **2,042.0bn (Q1-2026)**, and quarterly FCF turned **positive** in the two most recent quarters (Q4-2025: +1,769.1bn; Q1-2026: +1,423.3bn) as smelter spending tapers and cathode/refined-metal sales ramp. **INSUFFICIENT EVIDENCE** on the precise split between smelter/refinery construction capex vs. sustaining/stripping capex within these totals — the PDF earnings releases (FY2025 and Q1-2026) could not be parsed by the automated fetch tool (returned as opaque binary/font streams); this breakdown is typically disclosed in the MD&A capex table and should be pulled by direct PDF read or from the audited financial statement notes.

**FACT — smelter capital cost.** Public reporting cites the copper smelter and precious-metal refinery (PMR) project cost at **IDR 21 trillion (~US$1.4 billion)** at commissioning [Jakarta Globe: "Jokowi Launches Amman Mineral's $1.4 Billion Copper Smelter"; AsiaToday: "Investing IDR 21 Trillion"], though a separate analyst estimate references a much larger **US$5.5 billion "end-to-end" investment** figure covering the integrated mine-smelter-port-refinery value chain (broader scope, not smelter-only). **FACT — completion status:** the Completion and Project Acceptance Certificate (PAC) for the smelter was signed with EPC contractor NFC (China Nonferrous) in Beijing on **18 July 2026**, confirming construction, commissioning, and performance-guarantee tests are complete; the smelter can now process all mine output as of June 2026, targeting 162,662 dmt copper cathode in 2026 (vs. 79,848 dmt in 2025 — roughly double). **INSUFFICIENT EVIDENCE** on total spend-to-date vs. remaining committed capex as a discrete number — inferred from the capex trend (declining quarterly capex, now at the lowest level in 6 quarters) that the bulk of committed smelter spend is now behind the company, but this should be confirmed against the FY2025 financial statement capital-commitments note.

**FACT — funding source.** The near-tripling of total debt (2022→2025) alongside consistently negative FCF makes clear the smelter/refinery build has been funded overwhelmingly by **debt**, not operating cash flow or equity issuance (diluted shares outstanding have been roughly flat at ~72.5bn since the 2023 IPO/placement). No dividend was paid for FY2025 (screener Payout Ratio 0.0; AGM on 19 May 2026 confirmed no FY2025 dividend) — cash conservation is being prioritized over shareholder returns during the capex cycle, which is prudent given the leverage level but confirms equity holders bear the funding risk that debt cannot cover.

## Capital Allocation

**INFERENCE.** Capital allocation over FY2023–2025 was single-mindedly directed at the smelter/PMR build and mine-development capex (Phase 8 stripping, Elang project preparation), funded by debt, with zero dividends. This is a defensible strategy for a mine operator securing downstream value capture and regulatory compliance (Indonesia's concentrate-export ban made a domestic smelter close to mandatory for continued export flexibility — see "Amman secures export recommendation for copper concentrate until April 2026"), **but** it has produced three consecutive years of FCF-negative operation on top of a revenue base that itself fell 13% CAGR (3Y) — a "double negative" that is now easing as the smelter completes and Phase 8 grades recover (Q1-2026 concentrate production +110% YoY, net income of $163M vs. a $138M loss in Q1-2025).

## Accounting Concerns

**INFERENCE.** The FY2025 gap between net income (+$249M) and operating cash flow (−$475M) is the single largest red flag and warrants direct scrutiny of receivables, inventory, and any capitalized interest/cost policies in the FY2025 audited notes — **not established here as fraud or misstatement, simply flagged as unreconciled** given tool limitations on parsing the primary PDF filings.

**ASSUMPTION.** No explicit going-concern, restatement, auditor-change, or related-party-transaction irregularity was found in available search results, but this reflects the depth of search conducted, not a clean bill of health — **insufficient evidence to rule out related-party transaction concerns** given PT Medco Energi's board-level relationship as a major shareholder; a proper pass would require reading the FY2025 related-party-transactions note directly.

## Key Positive Findings
1. Net income figure used by the screener already approximates net income *attributable to parent* (minority interest at the AMNT subsidiary level is immaterial post-2020, when AMMN raised its stake to 99.99%) — so EPS/PE/ROE are **not** meaningfully distorted by the consolidated-vs-attributable issue the project memory flags generically.
2. Quarterly capex has fallen sharply (IDR 7.2tn → 2.0tn over 6 quarters) and quarterly FCF turned positive in Q4-2025 and Q1-2026, consistent with the smelter capex cycle peaking and the PAC (completion certificate) being signed July 2026 — the cash-burn phase appears to be ending, not open-ended.
3. Q1-2026 operating results show a sharp inflection: concentrate production +110% YoY, net income of +$163M vs. a −$138M loss in Q1-2025, EBITDA of $508M (63% margin) vs. −$42M a year earlier — directionally validating that the FY2025 numbers reflect a trough (Phase 8 low-grade transition + smelter ramp disruption), not a structural decline.

## Key Negative Findings
1. Operating cash flow was negative in FY2023 and FY2025 while net income was positive in both years — a persistent, large (>$700M in FY2025) accrual gap that independently explains most of the F-Score weakness and is a genuine earnings-quality concern, not a data artifact.
2. Total debt has grown 3.5x in three years (US$1.8bn → US$6.5bn) funding a capex programme that has produced three straight years of negative FCF; interest coverage (TTM 2.35x) is thin for this leverage level, and the debt maturity schedule, covenant package, and lender concentration could not be verified from available sources — a real refinancing-risk gap in this analysis.
3. Revenue fell at a −13% CAGR (3Y) despite strong copper/gold prices, driven by the Batu Hijau Phase 7→Phase 8 transition: mining moved into the low-grade outer/upper pit sections requiring large-scale waste stripping before higher-grade ore could be reached, pulling milled copper grade to a trough of 0.31% Cu in Q1-2025 — this is grade phasing, not a demand or pricing problem, but it confirms the project memory's warning that grade phasing can halve revenue with no change in prices, and the *next* down-cycle in the grade schedule is a known, recurring risk for this asset, not a one-off.

## Potential Screener False Positives
1. **FCF yield of −7% may overstate the ongoing (steady-state) cash burn rate.** The trailing twelve months captured in the screener span the tail of peak smelter capex; the two most recent quarters (Q4-2025, Q1-2026) show *positive* FCF as capex has roughly halved and the smelter reached commercial operation. A TTM figure computed today is a backward-looking number for a business whose capex profile has structurally shifted in the last two quarters — the screener's mechanical TTM window cannot see this inflection.
2. **F-Score of 3 (or reconstructed ~2) is real and not a data-quality artifact**, but it is heavily driven by a temporary confluence (smelter ramp disruption + Phase 8 low-grade transition + heavy capex) rather than by chronic operating deterioration — the underlying asset (Batu Hijau/Elang, one of the world's larger copper-gold deposits) is not impaired; the F-Score captures a cyclical/project trough, and investors should distinguish "temporarily terrible fundamentals during a capex/ramp trough" from "structurally deteriorating business," even though the low F-Score is the correct mechanical read of FY2025 alone.
3. **Revenue CAGR 3Y of −13% is not a demand-destruction or competitive-loss story** — it is fully explained by disclosed grade phasing at a single, well-understood mine plan (Phase 7→8 transition), which is now reversing (Q1-2026 concentrate production +110% YoY). A screener that only sees trailing revenue trend cannot distinguish this from genuine business decay.

## Financial Verdict: **QUESTIONABLE**

*(Leaning toward FAIL on capital structure/cash-flow-quality grounds alone, but not a clean FAIL because the negative FCF and weak F-Score are substantially explained by an identifiable, largely-complete capex programme and a disclosed, mechanical grade-phasing cycle rather than open-ended value destruction. The unresolved debt-maturity/covenant gap and the unreconciled NI-vs-CFO accrual gap are the reasons this cannot be called ACCEPTABLE without further primary-document research.)*

---

**FACT — Elang / next-phase capex.** AMMN has guided to a broader expansion capex budget of **~US$2.0 billion (IDR 31.2tn)**, separate from and larger than the US$1.4bn (IDR 21tn) smelter+PMR figure — the US$1.4bn was specifically flagged as covering "smelter, power plants, and processing plant expansion" from Q4-2024 through 2025, while the US$2.0bn appears to be the larger multi-year expansion envelope. **Batu Hijau Phase 8 mining continues to ~2030; the Elang deposit (definitive feasibility study targeted for completion 1H2025) is planned to begin development around 2027 and replace Batu Hijau production from 2031–2046** (reserves of ~1,436Mt ore). **INFERENCE:** this means AMMN's capex cycle is not a one-off "finish the smelter and de-lever" story — a second major capex wave (Elang development) is scheduled to begin within the next 1-2 years, before the smelter-funded debt has had much time to amortize. This materially raises the leverage/refinancing stakes versus a simpler "smelter completes, capex falls, FCF turns positive and stays positive" narrative. **Insufficient evidence** on Elang's specific capital cost estimate or funding plan (debt vs. cash flow vs. equity) — requires further research.

### Gaps requiring further research (flagged per protocol, not fabricated)
- Exact debt maturity schedule by year, coupon/interest rate, covenant terms (leverage ratio caps, DSRA), and lender/bondholder identity — needed to assess refinancing risk against BI 5.75%. Search for AMMN bond/note ISINs and syndicated loan tranches was inconclusive; direct read of the FY2025 audited statement's borrowings note is required.
- Precise capex split (smelter/PMR construction vs. sustaining/stripping capex) for FY2024–2026.
- Total smelter+PMR capital cost reconciliation (the $1.4bn "smelter" figure vs. the $2.0bn broader "expansion" figure vs. the $5.5bn "end-to-end" figure are three different scopes, not one number) and remaining committed capex, if any, post-PAC signing (July 2026).
- Elang project's specific capital cost estimate and funding plan — a second capex wave is scheduled to begin ~2027, well before FY2025-vintage smelter debt would be substantially amortized under a "back-ended" repayment structure.
- FY2025 related-party-transaction note (Medco Energi board relationship) and any capitalized-interest policy that could explain the NI-vs-CFO gap.
