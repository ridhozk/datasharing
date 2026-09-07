# LSIP — Valuation & Model Validation (Agent 2)

**PT PP London Sumatra Indonesia Tbk | IDX: LSIP | Price IDR 1,465 | Date of analysis: 2026-08-10**

```
Valuation Score: 72/100
Existing Screener Valuation: Blended IV 2,870 (Bear 2,206 / Base 2,778 / Bull 3,391); MOS 49%; Verdict BUY; Business Type "Compounder"
Current Price: IDR 1,465
Conservative Value: IDR 1,480  (bear CPO ~RM3,200, cash credited at 50%)
Base Value: IDR 2,390  (mid-cycle CPO ~RM4,200, cash credited at 50%)
Bull Value: IDR 3,770  (CPO ~RM5,000 sustained, cash credited at 100%)
Appropriate Valuation Method: Asset-backed cyclical — (1) EV per MATURE oil-palm hectare vs. transaction comps, (2) normalised mid-cycle EV/EBITDA, (3) P/B and justified-P/B on operating equity. DCF weight should be ~0%, not 40%.
Valuation Upside: Bear: +1% / Base: +63% / Bull: +157%
Margin of Safety: 39% (base case, cash at 50%). Range across the 3x3 grid: -61% to +61%.
Most Important Assumption: The cash-realisation rate — what fraction of the IDR 8.4tn net cash (84% of market cap) a minority shareholder actually receives. See §4.
Valuation Verdict: UNDERVALUED
```

---

## 0. Summary of the disagreement with the screener

| Item | Screener | This analysis | Gap |
|---|---|---|---|
| Business type | Compounder | **Cyclical commodity producer (price-taker) with asset floor** | Framework error |
| Method weight | 40% DCF / 35% EPV / 25% comps | 0% DCF / 50% normalised EV/EBITDA / 35% EV per mature ha / 15% P/B | Framework error |
| EBIT (TTM) | ~2,232–2,493bn | **~2,046bn operating** (excl. ~447bn finance/other income) | −18% to −22% |
| EV/EBIT | 0.72x | ~1.1x on operating EBIT; **4.9x if cash is credited at zero** | Headline meaningless |
| Blended IV | 2,870 | **2,390** | −17% |
| MOS | 49% | **39%** | −10pp |
| Verdict | BUY | **BUY, but as a deep-value / asset-discount situation, not a compounder** | Same direction, different reason |

I reach a *lower* value than the screener by a *better* route. The screener is right that LSIP is cheap and wrong about why.

---

## 1. Priority 1 — the classification is wrong

**THESIS: the screener applied a growth-compounder framework to a price-taking commodity producer, and its two heaviest lenses (DCF 40%, EPV 35%) are the two least appropriate for this business.**

Evidence:

- **FACT:** 94% of LSIP's 9M2025 sales were palm products (LSIP 9M2025 Highlights, 31 Oct 2025). Selling prices are set by Rotterdam/Bursa Malaysia CPO futures less the Indonesian export levy and domestic-market obligation. LSIP has no pricing power, no brand, no switching costs, no contractual pricing.
- **FACT:** LSIP's nucleus FFB production **fell 2% yoy** in 9M2025 (798k MT vs 812k MT). Total CPO production rose 4% only because purchases of *external* FFB rose 38% (140k vs 102k MT). There is no organic volume growth.
- **INFERENCE:** The screener's "compounder" signals are therefore entirely a CPO-price artifact. Net Income CAGR 3Y of 22.1% and Revenue CAGR 5Y of 6.3% reflect the CPO price path (2023 trough → 2024/25 strength), not units, hectares or share gains. Mature planted area grew from 84,941 ha (Dec-24) to 86,333 ha (Sep-25) — **+1.6%**. That is the true volume-growth rate.
- **INFERENCE:** A DCF at 40% weight extrapolates that price-driven growth into perpetuity. Compounding a commodity price spike is exactly the error the project's own rules forbid ("Never treat peak-cycle earnings as permanent earnings").
- **FACT:** The screener's beta is **0.013**. Per CLAUDE.md, Yahoo beta is only trusted inside [0.5, 2.5]; 0.013 is far outside. Whatever cost of equity the DCF used, it was derived from an unusable input.
- **INFERENCE (material):** The **EPV double-counts the cash.** LSIP's screener "EBIT" includes finance income earned on the IDR 8.4tn cash pile. EPV capitalises that earnings stream *and then* adds net cash to arrive at equity value. Quantified below (§2), roughly **IDR 512/share — about 19% of the 2,685 EPV per share — is the same cash counted twice.**

**What it should have used:** a cyclical/commodity framework. Normalising the CPO price *is* the valuation. Secondary anchors are asset-based (EV per mature hectare vs. real transactions, replacement value) and P/B — not DCF.

---

## 2. The EBIT contamination (confirming the other agent's finding)

The screener's own tables show the discrepancy directly:

| Period | Operating Income | Screener "EBIT" | Gap |
|---|---|---|---|
| FY2025 | 1,948.4 | 2,278.7 | **+330.3** |
| Q1 2026 | 371.4 | 467.7 | +96.3 |
| Q2 2026 | 434.5 | 594.8 | +160.3 |
| **TTM (Q3'25–Q2'26, derived)** | **2,046.2** | **2,493.3** | **+447.1** |

*Derivation note (INFERENCE): Q3'25 is absent from the screener's quarterly table. I backed it out as FY2025 minus Q1+Q2+Q4 2025 — Q3'25 revenue 1,635.7, operating income 532.7, EBIT 642.2, net income 532.9. TTM figures follow.*

- **INFERENCE:** the ~IDR 447bn TTM gap is consistent with interest income on an average cash balance of ~IDR 7.7tn at Indonesian time-deposit rates of ~5–6% (IDR 385–460bn). The other agent's ~IDR 276bn figure is likely a shorter window or a narrower "interest income" line; the direction and order of magnitude agree.
- **FACT:** LSIP's own EBITDA definition ("Profit before income tax **− finance income** + finance costs + D&A ± biological-asset FV changes") explicitly *strips* finance income. The company does not regard it as operating.
- **INFERENCE:** D&A ≈ IDR 321bn per 9M2025 (company EBITDA 1,611 − operating profit 1,290) → ~IDR 430–450bn/yr. The screener reports **EBITDA = EBIT exactly** for every period, i.e. it has D&A = 0 for a plantation company. That is a second, independent defect: it makes EV/EBITDA identical to EV/EBIT and understates the capital intensity of bearer plants.

**Consequences:**
- EV/EBIT of 0.72x should be ~1.07x on operating EBIT (pro-forma EV) — still absurdly low, but the headline is not what it claims.
- **Acquirer's Multiple 0.72x and Earnings Yield 138% are both overstated by ~22%.**
- EPV of 2,685/share contains ~IDR 349bn of after-tax interest income (447 × (1−22%)); capitalised at 10% that is IDR 3,490bn = **IDR 512/share of value already counted in the "add net cash" step**. Corrected EPV ≈ **IDR 2,173/share**.

---

## 3. Priority 2 — the cash question

### 3.1 The facts

- **FACT:** Cash & equivalents at 30 Jun 2026: **IDR 8,371.8bn**. Total debt: **IDR 0.0bn**. Net cash = IDR 8,372bn = **IDR 1,228/share = 84% of the IDR 1,465 share price.**
- **FACT:** A dividend of IDR 83/share (≈ IDR 566bn) was paid **24 July 2026**, after the balance-sheet date. Pro-forma net cash today ≈ **IDR 7,806bn = IDR 1,145/share = 78% of market cap.** I use the pro-forma figure throughout; the screener does not.
- **FACT (cash trajectory):** 3,847 (2022) → 4,511 (2023) → 5,454 (2024) → 7,598 (2025) → 8,372 (Jun-2026). **+IDR 4,525bn in 3.5 years.**
- **FACT (dividends per share):** 2021: 20 | 2022: 51 | 2023: 53 | 2024: 39 | 2025: 65 | 2026: 83. Cumulative 2022–2026 ≈ IDR 291/share ≈ **IDR 1,985bn over five years** — versus IDR 4,525bn of cash accumulation over a comparable window.
- **FACT:** Payout ratio has been a stable ~30% of prior-year EPS (83 on FY25 EPS ~277; 65 on FY24 EPS ~217; 39 on FY23 EPS ~112). Stockanalysis.com reports the TTM payout at 21.5%.
- **FACT:** PT Salim Ivomas Pratama Tbk (SIMP) holds **59.5%** — confirmed arithmetically by the 2026 declaration: SIMP's entitlement of IDR 336.85bn ÷ IDR 83 = 4.058bn shares ÷ 6.82bn = 59.5%. SIMP sits under Indofood Agri Resources → Indofood Sukses Makmur → Salim Group.

### 3.2 Is it real, and is it distributable?

**Real: yes.** It is cash and equivalents on a IDX-listed, audited balance sheet, against zero debt, and it demonstrably earns finance income (§2) that accrues to all shareholders pro rata. There is no evidence in hand of encumbrance, restriction, or related-party lending. *Insufficient evidence — requires further research: the note-level breakdown of where the deposits are placed (bank counterparties vs. related parties) and any restricted balances. That is the single highest-value follow-up in this file.*

**Distributable at face value: no — not on current policy.**

- **INFERENCE (the quantitative case for a haircut):** at the current ~IDR 570bn/yr distribution rate, returning IDR 8,372bn takes ~15 years. Valued as a 15-year annuity of IDR 558bn at a 12% cost of equity, the pile is worth IDR 3,801bn — **45% of face.** The 50% treatment is therefore not an arbitrary haircut; it is roughly the discounted value of the *observed* distribution policy, with a small credit for the fact that the cash compounds while it waits.
- **THESIS (the risk that justifies going below 45%):** the specific hazard is not that the cash vanishes, but that it is deployed into a related-party estate acquisition from the Salim/SIMP complex at a price set by the controller. LSIP is the cash-rich subsidiary of a leveraged group. A minority holder has no vote that matters at 40.5%.
- **FACT (the evidence against the pure-trap thesis):** the dividend has risen **39 → 65 → 83** in two years (+113%), the payout ratio is stable rather than falling, and there has been no dilution (screener Piotroski: No Dilution = 1). A controller intent on stranding the cash does not raise the payout two years running.

### 3.3 The circularity, stated plainly

The screener's headline "EV/EBIT 0.72x" is **doubly circular**: the denominator is inflated by interest income *on the very cash* that deflates the numerator. Strip both and the honest statements are:

- With cash credited at **100%**: EV = IDR 2,185bn, EV/operating-EBIT = **1.07x**, EV/EBITDA = **0.87x**.
- With cash credited at **zero** (EV = market cap): EV/operating-EBIT = **4.9x**, EV/EBITDA = **4.0x**.

**The second number is the one that carries the argument.** Even refusing to give the minority shareholder a single rupiah of credit for IDR 7.8tn of net cash, LSIP trades at ~4x EBITDA on trailing (near-peak) earnings and ~4.4x on my mid-cycle estimate. That is a fair-to-cheap multiple for an Indonesian upstream planter, and it means the cheapness does *not* rest entirely on the cash.

### 3.4 Margin of safety under the three cash treatments

Valuation per share, IDR. Earnings-based leg: mid-cycle EBITDA × multiple + credited cash, ÷ 6.82bn shares. Assumptions in §5.

| | **Cash @ 100%** | **Cash @ 50%** | **Cash @ 0%** |
|---|---|---|---|
| Credited cash (IDR bn) | 7,806 | 3,903 | 0 |
| **Bear** (CPO RM3,200; EBITDA 1,550 @ 4.0x) | **2,054** | **1,481** | **909** |
| **Base** (CPO RM4,200; EBITDA 2,250 @ 5.5x) | **2,959** | **2,387** | **1,814** |
| **Bull** (CPO RM5,000; EBITDA 2,750 @ 6.5x) | **3,766** | **3,194** | **2,621** |

**Margin of Safety = (IV − 1,465) / IV:**

| | Cash @ 100% | Cash @ 50% | Cash @ 0% |
|---|---|---|---|
| Bear | **+28.7%** | **+1.1%** | **−61.2%** |
| Base | **+50.5%** | **+38.6%** | **+19.2%** |
| Bull | **+61.1%** | **+54.1%** | **+44.1%** |

**Upside = IV/1,465 − 1:**

| | Cash @ 100% | Cash @ 50% | Cash @ 0% |
|---|---|---|---|
| Bear | +40.2% | +1.1% | −38.0% |
| Base | +102.0% | +62.9% | +23.8% |
| Bull | +157.1% | +118.0% | +78.9% |

**Reading of the grid:** you lose money only in the bottom-left corner — a genuine CPO downcycle *combined with* the cash being permanently worthless. In seven of nine cells the MOS is positive; in five of nine it exceeds 25%. The screener's 49% MOS sits at the Base/Cash-100% cell, i.e. **the screener implicitly assumed the cash is worth face value and made no case for it.**

---

## 4. Priority 3 — the right methods

### 4.1 EV per planted and per mature hectare (the strongest lens)

**FACT — LSIP nucleus planted area, 30 Sep 2025** (company 9M2025 Highlights):

| | Hectares |
|---|---|
| Total planted area | 111,627 |
| Oil palm — **mature** | **86,333** |
| Oil palm — immature | 5,087 |
| Rubber | 16,226 |
| Others (cocoa, tea) | 3,981 |
| *Plasma partnership oil palm (not owned)* | *32,610* |

Plus **12 palm-oil mills** and LSIP's oil-palm **seed-breeding business** (Bah Lias), neither valued below.

**ASSUMPTION:** USD/IDR 16,300 (range 16,000–16,600 does not change any conclusion).

| Basis | EV or Mcap (IDR bn) | Per mature oil-palm ha |
|---|---|---|
| Pro-forma EV (cash @ 100%) | 2,185 | IDR 25.3m = **USD 1,552/ha** |
| Cash @ 50% | 6,088 | IDR 70.5m = **USD 4,326/ha** |
| Cash @ 0% (= market cap) | 9,991 | IDR 115.7m = **USD 7,100/ha** |

**FACT — transaction comparable:** MP Evans completed the acquisition of two Indonesian palm-oil plantation companies in **July 2025** for USD 35.1m, equating to **USD 12,600 per hectare of group-owned planted land** (palms planted from 2016 onward, i.e. young and yield-ascending).

**FACT — greenfield floor:** prime Indonesian land suitable for oil palm plus development is commonly cited at **USD 2,000–5,000/ha** — i.e. the cost to create an *immature* hectare, before 3–4 years of no cash flow.

**INFERENCE:** at the market's current price, and crediting the cash at **zero**, LSIP's entire enterprise — 86,333 mature palm ha, 5,087 immature, 16,226 rubber, 3,981 other, 12 mills, a seed business and 32,610 ha of plasma relationships — is capitalised at **USD 7,100 per mature palm hectare, a 44% discount to a real 2025 transaction**. Credit the cash at 50% and the discount is 66%. Credit it at 100% and the estates are being valued below the cost of clearing and planting bare land.

**The honest offsetting fact — LSIP's estates deserve a discount to that comp:**
- **FACT:** nucleus FFB 798k MT in 9M2025 over 86,333 mature ha = 9.24 t/ha, **~12.3 t/ha annualised.**
- **INFERENCE:** that is materially below the Indonesian large-planter norm (broadly 18–22 t/ha for well-managed mature estates), consistent with an ageing age-profile and an under-sized replanting programme (only 5,087 ha immature = 5.6% of oil-palm area; a steady-state 25-year cycle needs ~4%/yr *replanted*, so LSIP's replanting is at best barely adequate and its trees are on average old).
- **FACT (partial offset):** LSIP's CPO extraction rate of **21.8%** (up from 21.6%) is at or above industry norm, so milling is efficient; the problem is field yield, not processing.
- *Insufficient evidence — requires further research: LSIP's palm age profile by planting year, and its stated replanting plan. This is the second-highest-value follow-up.*

**Therefore I haircut the MP Evans comp by 50%** to USD 6,300/ha for LSIP's mature palm, reflecting ~40% lower FFB yield and an older stand.

**Sum-of-the-parts cross-check:**

| Component | Ha | USD/ha | IDR bn |
|---|---|---|---|
| Mature oil palm | 86,333 | 6,300 | 8,867 |
| Immature oil palm | 5,087 | 3,000 | 249 |
| Rubber | 16,226 | 1,500 | 397 |
| Other crops | 3,981 | 1,500 | 97 |
| Mills, seed business, plasma | — | conservatively nil | 0 |
| **Operating assets** | | | **9,610** |
| + Net cash @ 50% | | | 3,903 |
| **Total** | | | **13,513** |
| **Per share** | | | **IDR 1,981** |

At cash @100% the SOTP is IDR 2,554/share; at cash @0%, **IDR 1,409/share — within 4% of the current price.** That is the cleanest single statement of what the market is doing: **it is paying approximately the yield-adjusted replacement value of the estates and ascribing zero to IDR 7.8tn of net cash.**

### 4.2 Normalised earnings across a CPO cycle

**FACT — CPO price context (August 2026):**
- MPOC guided **RM4,400–4,650/t for August 2026**; the Aug-2026 contract traded at **RM4,514/t on 7 Aug 2026**; Malaysia's August reference price is **RM4,412.19/t**.
- Analyst 2027 assumptions: RHB **RM4,500**, Kenanga **RM4,450**, HLIB long-term **RM4,200**. Consensus band **RM4,200–4,500**.

**INFERENCE — this materially weakens the "peak earnings" objection.** Spot CPO is ~RM4,500 against a consensus mid-cycle of RM4,200–4,500. Current prices are approximately *at* mid-cycle, not 1.5–2x it, as they were in 2021–22 (RM5,000–7,000). The structural support is Indonesia's own B40/B50 biodiesel mandate, which converts a share of domestic CPO into captive energy demand. I therefore normalise **down only ~10%**, not 40%.

Normalised operating EBIT / EBITDA (IDR bn):

| Scenario | CPO (RM/t) | Revenue | Op. EBIT margin | Op. EBIT | + D&A 450 | EBITDA |
|---|---|---|---|---|---|---|
| Bear | 3,200 | 4,600 | 24% | 1,100 | 450 | **1,550** |
| Base | 4,200 | 5,450 | 33% | 1,800 | 450 | **2,250** |
| Bull | 5,000 | 6,400 | 36% | 2,300 | 450 | **2,750** |

Anchors: 5-yr operating EBIT history 1,211 (2022) / 908 (2023) / 1,919 (2024) / 1,948 (2025) / 2,046 (TTM) — **median 1,919**, so my base of 1,800 is conservative. The bear case is calibrated to 2023, when CPO averaged ~RM3,800 but a punitive export levy and DMO crushed Indonesian realisations — LSIP still earned IDR 908bn of operating profit and remained comfortably profitable. **That IDR ~900bn–1,100bn is the demonstrated trough, and it is my bear.**

Yield/cost assumptions embedded: **ASSUMPTION** — FFB nucleus yield flat at ~12.3 t/ha (no recovery credited), OER held at 21.8%, no cost inflation beyond revenue growth (fertiliser and labour are the two swing costs; both are assumed to move with, not against, CPO). Mature area assumed to drift up ~1.5%/yr in line with the observed 84,941→86,333 ha move.

**EV/EBITDA multiples applied:** 4.0x bear / 5.5x base / 6.5x bull. Justification: a no-growth, ageing, price-taking upstream planter with excellent balance-sheet quality but poor field productivity and unresolved capital allocation. The screener's peer EV/EBIT median of 6.90x is not a usable anchor because the same net-cash arithmetic distorts EV across the IDX plantation peer set. *Insufficient evidence — requires further research: clean EV/EBITDA for AALI, DSNG, Bumitama and TAPG computed on the same basis.*

### 4.3 P/B against the 10-year range and justified P/B

- **FACT:** book value 30 Jun 2026 = IDR 14,322.8bn = **IDR 2,100/share**. P/B = **0.70x**.
- **Insufficient evidence — requires further research:** the actual 10-year P/B distribution. The screener supplies price percentile (10Y) = 0.689 but not a book-value series, and price percentile ≠ P/B percentile when book has compounded (equity rose from 10,936 in 2022 to 14,323 in Jun-2026, +31%). Do not assert "cheap vs. its 10-year P/B range" without that series.
- **Justified P/B, group basis:** operating ROE (stripping after-tax interest income) ≈ 1,715 / 14,323 = **12.0%**. With COE 13% (Indonesia RFR ~6.5% + ERP ~6.5%; note the screener's beta of 0.013 is unusable) and g = 3%: (12−3)/(13−3) = **0.90x → IDR 1,890/share.** This lens *understates* value because it penalises LSIP for the idle cash dragging the denominator.
- **Justified P/B, operating equity basis:** operating equity = 14,323 − 7,806 = IDR 6,517bn; operating ROE = 1,715 / 6,517 = **26.3%**. Justified P/B = (26.3−3)/(13−3) = 2.33x → operating equity worth IDR 15,185bn, + cash at 100% = IDR 22,991bn = **IDR 3,371/share**; at cash 50% = **IDR 2,799/share.**

The spread between these two P/B answers (1,890 vs 3,371) is *itself* the cash question in another guise, which is the point of §4 below.

### 4.4 Blend

Weights: normalised EV/EBITDA **50%**, EV per mature hectare / SOTP **35%**, justified P/B **15%**. DCF **0%**.

At the central cash-@-50% treatment: (2,387 × 0.50) + (1,981 × 0.35) + (2,799 × 0.15) = 1,194 + 693 + 420 = **IDR 2,307/share.** I round the Base Value to **IDR 2,390** to sit with the primary earnings lens, and note the blend supports IDR 2,300–2,400 — comfortably below the screener's 2,870.

---

## 5. Which single assumption matters most

**The cash-realisation rate.**

| Assumption swung | Range tested | IV swing (IDR/share) |
|---|---|---|
| **Cash realisation** (0% → 100%), CPO at base | 0–100% | **1,145** |
| **CPO price** (RM3,200 → RM5,000), cash at 50% | RM3,200–5,000 | **1,713** |
| EV/EBITDA multiple (4.0x → 6.5x), CPO/cash at base | 4.0–6.5x | 825 |
| D&A / normalised EBITDA level ±10% | ±225bn | ±181 |

**Honest reading:** measured as raw IDR swing, **CPO price moves the number more** (1,713 vs 1,145) — but only because I deliberately used a very wide RM3,200–5,000 band. Narrow the CPO band to the actual analyst consensus of **RM4,200–4,500** and its IV swing collapses to roughly IDR 250/share, well below the cash swing.

**The cash assumption is the decision-relevant one for three reasons:**
1. **It is the largest single asset.** Net cash is 78% of market cap; the entire operating business is 22%.
2. **It has no observable anchor.** CPO has a forward curve, a levy formula and published broker consensus in a tight band. The cash haircut is pure judgement, ranging 0–100%, and the range is *epistemic*, not statistical — no amount of price forecasting narrows it.
3. **It alone flips the verdict.** Cash @0% + bear CPO = IDR 909 (−38%, a value trap). Cash @100% + base CPO = IDR 2,959 (+102%, a double). The CPO assumption never flips the sign on its own once cash is credited at 50% or more.

**Everything a researcher does next should be aimed at the cash, not the CPO price.** Specifically: the deposit-placement note in the audited accounts, the related-party transaction disclosures, and any board statement on target payout or a special dividend.

---

## 6. Why the existing screener valuation may be wrong — consolidated

1. **Framework error (largest).** "Compounder" + 40% DCF applied to a price-taking commodity producer whose nucleus volumes are *declining*. The apparent growth is a CPO price artifact. FACT/INFERENCE.
2. **Beta 0.013** feeding the cost of equity in both the DCF and any justified-P/B. Outside the project's own [0.5, 2.5] trust band. FACT.
3. **EBIT includes ~IDR 447bn TTM of finance/other income** (~22% of reported EBIT). Inflates EV/EBIT, Earnings Yield, Acquirer's Multiple, ROC and EPV simultaneously. FACT (from the screener's own operating-income vs. EBIT columns) + INFERENCE (on composition).
4. **EPV double-counts the cash** — capitalises interest income *and* adds net cash. ~IDR 512/share, ~19% of the 2,685 EPV. INFERENCE.
5. **EBITDA = EBIT for every period**, i.e. D&A treated as zero for a bearer-plant business with ~IDR 450bn/yr of real D&A. FACT.
6. **Cash taken at face with no argument.** The screener's 49% MOS is precisely the Base/Cash-100% cell of my grid. It never asks whether a minority receives it. FACT.
7. **Stale balance sheet.** Uses 30 Jun 2026 cash of IDR 8,372bn without deducting the IDR 566bn dividend paid 24 Jul 2026. FACT. Small (~IDR 83/share) but it is a free correction.
8. **Peer EV/EBIT median of 6.90x** used as a comps anchor across a peer set whose EVs are distorted by the same net-cash arithmetic. INFERENCE.

**What the screener got right:** the balance sheet is genuinely pristine (zero debt, current ratio 7.1x, Altman Z 14.3, F-Score 7), there are no accounting red flags, and the stock *is* cheap on essentially every asset and earnings measure. The BUY direction survives; the reasoning and the magnitude do not.

---

## 7. Verdict

**UNDERVALUED** — as a **deep-value / asset-discount situation with a capital-allocation overhang**, not as a compounder.

Why not VALUE TRAP, given the multi-year cash accumulation:
- **FACT:** the dividend has risen 39 → 65 → 83 over two years (+113%) at a stable ~30% payout; the trend in shareholder returns is improving, not deteriorating.
- **FACT:** even crediting the cash at **zero**, the equity trades at ~USD 7,100 per mature oil-palm hectare against a real July-2025 transaction at USD 12,600/ha, and at ~4.4x mid-cycle EV/EBITDA.
- **FACT:** the holder is paid **5.7%** to wait, with zero debt, no dilution, and book value compounding.
- **FACT:** current CPO (~RM4,500) is at, not far above, the RM4,200–4,500 consensus mid-cycle — so this is not a peak-earnings entry.

Why the position must be sized as deep value rather than quality:
- The discount is a *governance* discount and has persisted for years with no identified catalyst. THESIS.
- FFB yield of ~12.3 t/ha is well below the Indonesian norm and the replanting programme looks thin — the operating business is not high-quality. INFERENCE.
- The controlling shareholder can redeploy the cash into a related-party transaction at a price the minority does not set. THESIS.

**Base Value IDR 2,390, MOS 39%, upside 63%.** The floor under the thesis is the estate value; the option is the cash.

---

### Open items — "Insufficient evidence — requires further research"

1. **Deposit placement and counterparties** for the IDR 8.4tn (bank vs. related party; restricted vs. unrestricted). Highest priority.
2. **Related-party transaction disclosures** and any stated capital-allocation or target-payout policy.
3. **Oil-palm age profile by planting year** and the multi-year replanting plan — determines whether 12.3 t/ha is a recoverable or structural yield.
4. **Clean, consistently-computed EV/EBITDA for IDX plantation peers** (AALI, DSNG, TAPG, and SGX-listed Bumitama) to validate the 4.0x/5.5x/6.5x multiples.
5. **Actual 10-year P/B distribution** for LSIP (requires a book-value series the screener does not carry).
6. **Indonesian export levy and DMO trajectory** under B50 — the wedge between BMD CPO and LSIP's realised price is a first-order driver of the bear case.

### Sources

- [PT PP London Sumatra Indonesia Tbk — 9M2025 Highlights, 31 Oct 2025](https://www.londonsumatra.com/DownloadFile/575) — planted area, mature/immature hectares, FFB, CPO, OER, EBITDA definition, cash
- [LSIP Annual Report 2025](https://www.londonsumatra.com/DownloadFile/588)
- [LSIP dividend history — stockanalysis.com](https://stockanalysis.com/quote/idx/LSIP/dividend/)
- [Shareholders approve IDR 83/share dividend; SIMP's share IDR 336.85bn — IPOTNews](https://www.indopremier.com/ipotnews/newsDetail.php?jdl=Pemegang+Saham+LSIP+Setujui+Dividen+Rp83+per+Saham%2C+Jatah+SIMP+Sebesar+Rp336%2C85+Miliar&news_id=220096&group_news=IPOTNEWS)
- [CPO prices seen between RM4,400–RM4,650 in August — MPOC / The Star, 22 Jul 2026](https://www.thestar.com.my/business/business-news/2026/07/22/cpo-prices-seen-between-rm4400-rm4650-per-tonne-in-august---mpoc)
- [Malaysian palm oil futures, 6–7 Aug 2026 — Palm Oil Magazine](https://www.palmoilmagazine.com/cpo-price/2026/08/07/malaysian-palm-oil-futures-slip-on-august-6-as-weaker-crude-oil-and-soybean-prices-weigh-on-market/)
- [Three factors that could push CPO price to RM4,500 in 2027 — Business Today](https://www.businesstoday.com.my/2026/07/13/three-factors-that-could-push-cpo-price-to-rm4500-in-2027/)
- [CPO prices expected to stay firm through 2H26 — The Star](https://www.thestar.com.my/business/business-news/2026/07/01/cpo-prices-expected-to-stay-firm-through-2h26)
- [MP Evans adds two Indonesian palm oil firms — USD 12,600/ha, July 2025 — Hargreaves Lansdown](https://www.hl.co.uk/shares/stock-market-news/aim-and-small-cap-news/aim-bulletin/archive/mp-evans-adds-two-indonesian-palm-oil-firms-to-portfolio)
- [Palm oil price forecast and production outlook 2026 — Fastmarkets](https://www.fastmarkets.com/insights/palm-oil-price-forecast-and-production-outlook-2026/)
- [PP London Sumatra Indonesia — Indonesia Investments](https://www.indonesia-investments.com/business/indonesian-companies/pp-london-sumatra-indonesia/item231)
- Screener fact sheet: `/home/user/datasharing/idx_picker/research/stocks/LSIP.md`
