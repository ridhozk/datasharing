# INDY — Financial Forensics Agent Report

*Ticker: INDY (Indika Energy Tbk.), IDX Energy/Coal. Price IDR 2,680, mkt cap ~IDR 13.9tn (~US$778.6M at FX 17,908). Reports in USD.*

```
Financial Quality Score: 33/100
Earnings Quality: Weak/volatile — see below
Balance Sheet: Adequate near-term liquidity, rapidly rising leverage
Cash Flow Quality: Negative FCF driven almost entirely by growth capex
Capital Allocation: Aggressive redeployment of coal cash into unproven ventures mid-downcycle
Accounting Concerns: Minority-interest treatment and goodwill/impairment unverified from primary filings
Financial Verdict: QUESTIONABLE
```

## 1. Why PE 51.6 vs PB 0.65 — is the E real?

**FACT** (screener, `INDY.md`): Consolidated/attributable NetIncome collapsed from IDR 8,106.5bn (2022) → 2,143.3bn (2023) → 180.6bn (2024) → 107.9bn (2025), a ~99% decline from the 2022 peak, while EBIT fell far less steeply (19,662.4bn → 5,674.4bn → 2,883.5bn → 2,511.3bn, a ~87% decline). Revenue also nearly halved (77,629.6bn → 36,369.4bn).

**FACT** (Indika AGM disclosure, 20 May 2026 news release, via search): the FY2025 final dividend of US$3,013,598 was declared as "50% of the Company's Net Profit attributable to owners of the Company for the year 2025" — implying FY2025 attributable net profit of **≈US$6.03M**. This matches the screener's IDR 107.9bn (÷ FX 17,908 = US$6.03M) almost exactly.

**INFERENCE**: this reconciliation suggests the screener's NetIncome line for INDY is *already* the parent-attributable figure, not the pure consolidated (pre-minority) number — a more favorable read than CLAUDE.md's general caution that Yahoo's net income "may include minority interest." This should still be verified against the primary audited FS (I could not get readable text from the FY25 PDF release), so treat as INFERENCE, not FACT.

**FACT** (search, 9M25/1H25 press coverage): 9M25 net profit attributable to owners was **US$0.48M**, down from US$34.4M in 9M24 — and 1H25 attributable profit was US$2.2M (1H26: US$10.2M). Back-solving, **Q3 2025 alone was a net loss (~ -US$1.8M attributable)**, followed by a recovery in Q4 2025 (~US$5.5M) and Q1 2026 (~US$7.0M). The trailing-twelve-month E that produces the screener's PE of 51.6 is therefore not a stable number — it is the sum of a loss quarter and several thin, uneven profit quarters, sitting right at the margin of profit/loss.

**Conclusion on Q1**: the E is a real, audited (or at least AGM-disclosed) number, not overstated — but it is **not repeatable or normalized**. It reflects (a) a genuine collapse in coal profitability from 2022 supercycle levels, (b) margin compression (gross margin 33.5%→13.3% 2022→2025 per screener), and (c) a business sitting near operating breakeven at the net-income line even though EBIT is still solidly positive (EBIT margin still ~7% in 2025). PE 51.6x is a multiple on a trough/noise-level E, not a normalized earnings power multiple — it is close to meaningless as a valuation signal in either direction.

## 2. Is book value credible?

**FACT**: Screener's Price-to-Book (0.65) is computed against parent StockholdersEquity of IDR 21,395.7bn (2025) ≈ US$1,195M — market cap (US$778.6M) / that equity ≈ 0.65, consistent.

**FACT** (Yahoo balance-sheet query, via search — flag data-quality caveat per CLAUDE.md's documented Yahoo/IDX unreliability): Gross Minority Interest ≈ US$1,345M, Net Minority Interest ≈ **US$1,588M** as of Dec 2025 — larger than INDY's own attributable equity (US$1,195M) and larger than its entire market cap (US$778.6M).

**FACT**: Kideco Jaya Agung (the core coal-producing subsidiary and primary profit engine) is **91%-owned** by INDY; South Korea's Samtan holds the remaining **9%** (Indika completed the acquisition raising its stake to 91% in Dec 2017 for ~US$517–678M across tranches).

**INFERENCE**: a US$1.6bn minority-interest balance from a 9% stake in Kideco is plausible only if Kideco's own multi-decade accumulated equity/retained earnings (built through the 2018 and 2021-22 coal supercycles) is very large — i.e., a large legacy asset base, not necessarily an accounting red flag by itself. But it means a substantial share of INDY's consolidated book value does **not** belong to INDY shareholders, and it also means EV/EBIT and EV/EBITDA multiples computed as (market cap + net debt) — as the screener does — **exclude minority interest from EV while EBIT/EBITDA are 100% consolidated (including Kideco's minority-owned 9%)**. A look-through EV that added the ~US$1.6bn (~IDR 28.4tn) minority claim would roughly double reported EV, pushing EV/EBIT from the screener's 9.1x toward the high teens/low 20s — a materially less cheap picture than the headline multiple implies.

**Gap**: I could not obtain goodwill/intangible-asset balances or confirm whether any impairment has been taken on Kideco reserves or the non-coal ventures (Alva/EV, gold, EPC). **Insufficient evidence — requires further research** (primary FS notes needed).

**Conclusion on Q2**: PB 0.65 is calculated on the correct (parent-only) denominator, but the size of the minority claim means look-through economics for INDY shareholders are meaningfully worse than the headline PB/EV multiples suggest. Goodwill/impairment risk is unverified.

## 3. Negative FCF (−6% yield) — capex mix

**FACT** (screener): FCF (TTM) = -IDR 831.0bn; Capex (TTM) = -IDR 2,743.5bn; FreeCashFlow swung 2022→2025: +15,265.4bn → -5,696.1bn → -2,862.5bn → +167.3bn (IDR bn), i.e. the coal-price collapse plus stepped-up capex drove three straight years of cash burn before a marginal FY2025 positive.

**FACT** (Indika 1H26 results release, 31 Jul 2026, via search): 1H2026 capex was **US$83.1M, with 99.1% allocated to non-coal businesses**. Combined with Moody's commentary (below) that the FY2026 capex/debt increase is driven "mainly by rising capital spending at the Awak Mas gold project," this establishes that **growth capex into the gold (and other non-coal) ventures — not coal maintenance capex — is now the dominant driver of negative free cash flow.**

**FACT** (search, Awak Mas project coverage): Awak Mas gold project total capex ≈ **US$429M**; as of Oct 2025, construction was 43% complete with ~US$234M invested; trial production targeted Q4 2026, commercial production Q4 2026/early 2027; annual production target 100,000 oz; an associated gold refining smelter investment of ~US$426M was also cited.

**Conclusion on Q3**: this is exactly the pattern CLAUDE.md flags as the central question for this name — cash generated (or previously generated) by the maturing, declining coal business (Kideco) is being redeployed into a large, not-yet-cash-generative gold project plus other non-coal ventures (EV/Alva, EPC, shipping). The bet is that Awak Mas converts this into a second profit engine from 2027; until then, FCF should be expected to stay negative or marginal, funded by debt.

## 4. Debt — maturity, currency, covenants, refinancing risk

**FACT** (screener): Net Debt/Equity ≈1.04x, Total Debt IDR 22,446.1bn (~US$1.25bn) vs Cash IDR 10,889.6bn (~US$0.61bn), Net Debt IDR 11,556.5bn (~US$0.65bn); Interest Coverage (TTM) only 2.55x; Current Ratio 2.07x (adequate short-term liquidity); Altman Z 3.27 (safe zone under the standard model, though the model is less reliable for a cyclical resource company mid-transition).

**FACT** (search, Moody's rating action, Feb 2026): Moody's downgraded Indika Energy and its 8.75% notes due 2029 to **B1 from Ba3**, citing weakening credit metrics "driven mainly by rising capital spending at the Awak Mas gold project amid weakened thermal coal prices." Moody's projects **adjusted debt rising to ~US$1.4bn in 2026 from ~US$1.1bn in 2025**, pushing leverage to **~7.0x in 2026**, improving only after Awak Mas commercial production begins in 2027.

**FACT** (search, Fitch rating action, ~April 2025): Fitch downgraded INDY to **B+ from BB-**, citing declining coal prices and rising costs, projecting **EBITDA net leverage above 3.0x in 2025-2026** (vs 2.9x in 2024).

**FACT** (screener/company filings, most recent granular maturity data found is from a 2024 investor presentation, may be stale): post-2024 refinancing, maturity ladder cited as ~US$129.3M (2026), ~US$187.6M (2027), ~US$150.9M (2028), and US$455M of 8.75% senior notes due May 2029 (the notes now rated B1/downgraded).

**Conclusion on Q4**: this is the single strongest negative finding. Two independent rating agencies downgraded INDY within the last ~16 months, both citing the same mechanism CLAUDE.md warns about generically for the sector — a coal borrower increasing debt-funded capex into an unproven venture while its core commodity cash flow weakens, against a backdrop (BI-Rate 5.75%, +100bp since May 2026) of tightening domestic rates and likely reduced lender appetite for coal-linked credit. Leverage is forecast to peak near 7.0x in 2026 before an expected recovery in 2027 **conditional on Awak Mas ramping successfully** — an unproven, execution-dependent bet, not a certainty. Near-term (2026-2027) maturities (~US$317M combined per the stale 2024 ladder) will need refinancing or repayment against this weaker credit profile; **current, precise maturity figures require verification against the FY2025/1H2026 filings — insufficient evidence for the up-to-date ladder.**

## 5. Minority interests

**FACT**: Kideco is 91%-owned by INDY (Samtan holds 9%) — Kideco is the primary earnings/cash engine of the group.

**FACT/INFERENCE** (reconciliation above): the FY2025 attributable net profit (US$6.03M, per AGM dividend disclosure) matches the screener's reported NetIncome almost exactly, suggesting the screener figure is *already net of minority interest* for INDY, unlike CLAUDE.md's generic caution. This is an INFERENCE from external reconciliation, not a direct read of the audited income statement's "profit attributable to non-controlling interests" line — **primary-source confirmation still needed.**

**FACT**: the balance-sheet-level minority interest claim is large (~US$1.6bn per Yahoo, flagged for IDX data-quality caution) relative to INDY's own equity and market cap, meaning a substantial share of consolidated book value and (in strong coal years) consolidated EBITDA accrues to non-INDY shareholders. This matters most for EV-based multiples (EV/EBIT, EV/EBITDA), which likely understate the true look-through multiple by excluding the minority claim from EV while including 100% of Kideco's EBIT/EBITDA in the numerator.

## 6. Related-party transactions and governance

**FACT** (search): Indika Energy states its transactions do not contain conflicts of interest under OJK Regulation 42/2020 and publishes shareholder disclosures under OJK Regulation 17/2020; the company reports a whistleblowing system as part of its governance framework.

**Insufficient evidence — requires further research**: I was not able to retrieve specific related-party transaction schedules, intercompany pricing with affiliated entities (e.g., EPC/logistics contracts awarded to group companies such as Tripatra, Petrosea, Interport, MBSS), or any OJK enforcement history. This is a meaningful gap given the complexity of the group structure and the priority the mandate places on this question.

---

## Key Positive Findings
1. The core coal business (Kideco, 91%-owned) remains solidly EBIT-positive (2025 EBIT margin ~7%, EV/EBIT 9.1x on headline basis) and is still paying a dividend, with FY2025 attributable profit and the declared dividend cross-verifying against the screener's numbers.
2. Coal-segment fundamentals were improving into 1H2026 — Kideco revenue +10.2% YoY, gross margin improving 14.2%→19%, average selling price +6.8% — suggesting the coal business itself is not currently in crisis, unlike the group's consolidated bottom line.
3. Short-term liquidity is adequate (Current Ratio 2.07x) and Altman Z (3.27) sits in the "safe" zone, arguing against near-term insolvency risk despite rising leverage.

## Key Negative Findings
1. Two independent credit-rating downgrades within ~16 months (Fitch to B+, Moody's to B1) explicitly tied to rising debt-funded capex on the unproven Awak Mas gold project amid weak coal prices — leverage forecast to peak ~7.0x in 2026, recovering only if Awak Mas execution succeeds in 2027.
2. Consolidated/attributable net income is thin and volatile — swinging to a loss in Q3 2025 — making the screener's PE (51.6x) effectively a multiple on noise rather than a normalized earnings number; the 99% decline in net income since the 2022 coal supercycle peak is real, not an accounting artifact, but is not a stable base for valuation.
3. Nearly all growth capex (99.1% in 1H2026) is being funneled into non-coal, pre-commercial ventures (chiefly the US$429M Awak Mas project) funded increasingly by debt while the legacy coal cash-cow's own profitability has compressed — the central "cash from a declining business chasing ventures that don't yet earn" pattern the mandate specifically asked to test for, and it is present.

## Potential Screener False Positives
1. **PB 0.65 looks cheap but understates minority claims on look-through EV.** A ~US$1.6bn minority-interest balance (mostly the 9% Kideco stake held by Samtan) is excluded from the screener's EV calculation (market cap + net debt only), while consolidated EBIT/EBITDA include 100% of Kideco. Adding the minority claim to EV would push EV/EBIT well above the reported 9.1x, closer to or above the peer median (8.0x) rather than below it.
2. **PE 51.6 is not "expensive earnings," it is a near-zero/volatile denominator.** The headline PE overstates how meaningful the multiple is in either direction; a screener designed to penalize "expensive" PE is scoring noise here, not a genuine valuation signal.
3. **F-Score 4 / Value Score 38 likely already partially capture the deterioration** (revenue CAGR 3Y -22%, FCF yield -6%), but the screener's "Normalised/Trailing EBIT" of 1.40 (suggesting current EBIT is *below* its 5-year normalized level, i.e. depressed, not elevated) could tempt a mean-reversion bull case — that reversion is conditional on both coal price recovery *and* Awak Mas execution risk, which the multiple-based screener cannot see.

---

**Financial Verdict: QUESTIONABLE**

The core coal asset (Kideco) appears real and still cash-generative, and short-term liquidity is not in immediate danger. But group-level earnings quality is poor and unrepeatable (thin/volatile attributable profit, one loss quarter in the trailing period), leverage is rising into a two-agency-downgraded credit profile explicitly driven by debt-funded speculative growth capex (Awak Mas) at the same time the legacy coal business is past peak profitability, and a large, only partially verified minority-interest claim complicates both the PB and EV-multiple reads. Key gaps (goodwill/impairment detail, current debt maturity ladder, granular related-party transactions, and primary-source confirmation of the minority-interest income-statement split) remain **insufficient evidence — requires further research** before any BUY/DEEP VALUE case could be underwritten; on what is verified, this does not look like a name where cheapness reflects overlooked quality — it looks like cheapness with real reasons behind it.

---

*Sources consulted (WebSearch/WebFetch, Aug 2026): Indika Energy FY2025 and 1H2026 news releases (indikaenergy.co.id); Indika Energy AGM 2026 dividend disclosure; Moody's Ratings action (Feb 2026); Fitch Ratings action (~Apr 2025); Indonesia Business Post (Kideco divestment commentary); IDNFinancials; Indopremier/IPOTNews (1H2026 results, Awak Mas coverage); Wood Mackenzie / Jakarta Post / Insider Stories (Kideco ownership history); general search aggregation for Awak Mas project capex and timeline. The FY2025 PDF news release itself could not be parsed as text by the fetch tool — figures were cross-verified via multiple secondary citations of the same release instead of a single primary read.*
