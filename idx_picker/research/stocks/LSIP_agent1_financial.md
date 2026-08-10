# LSIP — Financial Forensics (Agent 1)

**PT PP London Sumatra Indonesia Tbk | IDX:LSIP | Price IDR 1,465 | Date of work: 2026-08-10**

Primary sources read directly:
- **LSIP Annual Report 2025** (233pp), containing the **full audited FY2025 consolidated financial statements with comparatives for FY2024** — income statement, cash flow statement, and Notes 5, 8, 13, 18, 20, 23, 24, 25, 27, 30, 32. This is the controlling evidence for everything below.
- LSIP interim consolidated financial statements, 30 September 2025 (unaudited).
- LSIP press release, 31 July 2026 (1H2026 results).
- stockanalysis.com dividend history (ex-dates and DPS 2021–2026).
- NEXT Indonesia Center, 14 June 2026 (sector-wide affiliate-transaction / under-invoicing commentary).

All IDR figures in **millions** unless stated (as the statements present them). "bn" = billion.

---

## Financial Quality Score: 68/100

| Component | Score | Rationale |
|---|---|---|
| Accounting integrity / conservatism | 17/20 | Conservative. One-offs hit the downside, not the upside. No bearer-plant revaluation. |
| Cash conversion | 16/20 | CFO 1.60× NI in FY2025, 1.06× in FY2024. Real, but FY2025 flattered by a related-party receivable unwind. |
| Balance sheet strength | 19/20 | Zero funded debt five years running; net cash = 84% of market cap. Docked for related-party bank concentration. |
| Capital allocation | 8/20 | Payout ratio **cut** from 35% to 30% while the cash pile doubled. This is the crux and it is trending the wrong way. |
| Related-party / governance | 8/20 | 64.5% of revenue sold to the 59.5% parent, at prices with no disclosed independent verification. |

---

## Earnings Quality

### The screener's "EBIT" is pre-tax profit including interest income — CONFIRMED

**FACT.** The FY2025 audited consolidated statement of profit or loss reads (IDR million):

| Line | FY2025 | FY2024 |
|---|---:|---:|
| Revenue from contracts with customers | 5,511,706 | 4,562,503 |
| Cost of goods sold | (3,250,368) | (2,570,542) |
| **Gross profit** | **2,261,338** | **1,991,961** |
| (Losses)/gains — changes in fair value of biological assets | (59,571) | 142,439 |
| Selling and distribution expenses | (73,099) | (48,267) |
| General and administrative expenses | (247,878) | (239,897) |
| Other operating income | 136,905 | 142,225 |
| **Other operating expenses** | **(9,307)** | **(437,610)** |
| **Operating profit (laba usaha)** | **2,008,388** | **1,550,851** |
| **Finance income** | **276,021** | **216,888** |
| Finance costs | (1,176) | (653) |
| Share in (losses)/profits of associates | (5,691) | 5,967 |
| **Profit before income tax** | **2,277,542** | **1,773,053** |
| Income tax expense | (391,187) | (297,399) |
| **Profit for the year** | **1,886,355** | **1,475,654** |
| Attributable to owners of the parent | 1,887,756 | 1,476,909 |

**FACT.** Reconciliation to the screener, exactly:
- Screener EBIT FY2025 = **2,278.7bn** = PBT 2,277,542 + finance costs 1,176 = **2,278,718**. Identical.
- Screener EBIT FY2024 = **1,773.7bn** = PBT 1,773,053 + 653 = **1,773,706**. Identical.

So the screener's EBIT is **profit before tax grossed up for interest expense**, not operating profit. For FY2025 it embeds **Rp276,021m of finance income** and **−Rp5,691m of associate losses**; the gap to true `laba usaha` is **Rp270,330m (13.5% of true operating profit)**. For FY2024 the gap is Rp222,855m (14.4%).

**FACT.** Note 24 confirms finance income is *"interest income from placements of current accounts and time deposits and interest income from short-term loans to related parties"*. It is pure return on the cash pile. It is not operating profit under any definition.

**FACT.** Yahoo's separate `OperatingIncome` field is also wrong and should not be substituted: FY2025 1,948.4bn vs reported 2,008.4bn; FY2024 **1,918.7bn vs reported 1,550.9bn — a Rp368bn overstatement**. *INFERENCE:* the FY2025 gap equals the biological fair-value loss (59,571), and the FY2024 figure appears to strip the Rp437.6bn one-off, but neither reconciles cleanly. Neither Yahoo operating-profit field is usable.

**FACT.** Screener `EBITDA` = screener `EBIT` for FY2023, FY2024 and FY2025 (identical values), and `EV/EBITDA` = `EV/EBIT` = 0.7235 on the fact sheet. **D&A is not being added back at all.** Note 25 gives FY2025 D&A of 383,284 (fixed assets) + 5,129 (right-of-use) + 1,040 (deferred charges) = **389,453m**. True operating EBITDA = 2,008,388 + 389,453 = **2,397,841m**; company-reported EBITDA = 2,451,720m. For a plantation, where D&A is 19% of operating profit, a null EBITDA is a real defect.

### Quantifying the distortion

**FACT.** True operating profit (`laba usaha`), 5-year series from the AR2025 financial highlights (IDR million):

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|
| Operating profit (reported) | 1,192,706 | 1,205,856 | 759,425 | 1,550,851 | 2,008,388 |
| Screener "EBIT" | n/a | 1,284,200 | 912,000 | 1,773,700 | 2,278,700 |

**FACT.** Screener `Normalised EBIT (5Y)` = **1,528,953m**, which is exactly the median of the four contaminated years (1,284.2 / 912.0 / 1,773.7 / 2,278.7) — i.e. it is a **4-year** median, not 5-year (Yahoo carries only ~4 annual periods, as CLAUDE.md notes).

**INFERENCE.** Corrected normalisation:
- Median of true operating profit 2022–2025 = **1,378,354m** → screener overstates by **10.9%**.
- Median of true operating profit **2021–2025** (the real 5-year median) = **1,205,856m** → screener overstates by **26.8%**.

**INFERENCE — effect on each valuation lens.** Back-solving the screener's EPV: EPV/share 2,684.76 × 6,819.96m shares = 18,309.7bn; less net cash 8,371.8bn = 9,937.9bn operating value; ÷ (1,528.95 × 0.78) = 8.33× → implied WACC ≈ 12.0%. Re-running that machinery:

| Normalised EBIT used | EPV/share | vs screener |
|---|---:|---:|
| Screener 1,528.95bn (contaminated, 4y) | **2,684.8** | — |
| True 4y median 1,378.35bn | **2,541.3** | −5.3% |
| True 5y median 1,205.86bn | **2,377.2** | −11.5% |

Comparables IV (3,275.4/share) applies the peer median 6.90× EV/EBIT to the same contaminated EBIT; a 10.9% EBIT haircut takes it to roughly **3,050/share (−6.8%)**. Blended IV of 2,869.8 falls to roughly **2,650–2,730**, so **MOS ≈ 45–47% rather than 49%, upside ≈ 84–86% rather than 96%.**

**Material, but it does not on its own flip the verdict for LSIP** — the median normalisation absorbs much of the contamination, and EV is so small (Rp1,615bn) that EV/EBIT moves only from 0.72 to ~0.80. I state this plainly rather than overclaiming.

### The structural defect (matters beyond LSIP)

**FACT.** Average cash FY2025 = (5,453,691 + 7,597,470)/2 = 6,525,581m; finance income 276,021m → a **4.23% pre-tax yield on cash**.

**INFERENCE — this is a double count.** EPV and comparables both compute *operating value + net cash at face*. If the EBIT fed into "operating value" includes interest earned *on that same cash*, the cash is counted twice. Quantified: after-tax interest income ≈ 276,021 × 0.80 (20% final tax on Indonesian interest) = 220,817m; capitalised at the implied 12.0% WACC = **1,840bn of phantom value**, against year-end cash of 7,597bn. **The cash is effectively being valued at ~124% of face.** Any screener name with (a) large net cash and (b) EBIT taken as PBT + interest expense inherits this. LSIP is a mild case because it is highly profitable operationally; a low-margin cash-box would be severely mispriced. **This should be fixed in `metrics.py` — EBIT must be built up from operating profit, not down from pre-tax profit.**

### The FY2024 Rp437.6bn one-off — CONFIRMED, and it is non-recurring

**FACT.** Note 23, "Other operating expenses" (IDR million):

| | 2025 | 2024 |
|---|---:|---:|
| Losses on disposals and write-off of fixed assets (Note 13) | 4,370 | **138,110** |
| Loss on impairment of fixed assets (Notes 3 and 13) | — | **296,164** |
| Allowance for impairment / EIR amortization of plasma receivables (Note 9) | — | 1,286 |
| Others, net | 4,937 | 2,050 |
| **Total** | **9,307** | **437,610** |

**FACT.** Note 3 identifies the impairment precisely: *"impairment losses of CGU of **rubber plantations** was amounting to Rp296,164 ... recoverable amount based on FVLCD using income approach (Level 3) ... discounted at a rate of 11.13%."* The segment note allocates the entire Rp296,164 to the **"Others"** segment (i.e. rubber/cocoa/tea, not oil palm).

**FACT.** It did not recur in FY2025 (Rp9,307m total, of which Rp4,370m disposals).

**INFERENCE.** Direction matters: this one-off **depressed** FY2024, it did not flatter it. Cleaning both years — adding back FY2024's Rp434.3bn of impairment/write-offs and stripping the FY2024 biological gain of +142.4bn and the FY2025 biological loss of −59.6bn:

| | FY2024 clean | FY2025 clean | Growth |
|---|---:|---:|---:|
| Operating profit as reported | 1,550.9 | 2,008.4 | +29.5% |
| **Adjusted (ex one-off, ex biological FV)** | **1,842.8** | **2,068.0** | **+12.2%** |

So the apparent +29.5% operating and +27.9% net-income surge in FY2025 is **mostly a one-off reversal**, not underlying momentum. The screener's `Net Income CAGR 3Y` of 22.1% is measured off a cyclically depressed 2022–2023 base and is not a growth rate.

**THESIS.** The rubber CGU impairment is not just an accounting event — it is management writing off a business line. Rubber production fell from 6.2kt (2021) to 4.5kt (2025), −27%. Rubber is 16,203 ha, 14.6% of planted area, and appears to be earning below its cost of capital.

### Biological assets — clean

**FACT.** Note 8: biological assets are **only "growing agricultural produce on the bearer plants"** (unharvested FFB and rubber latex), carried in *current* assets, at **Level 2** fair value = applicable market price × estimated volume. Balance Rp245,735m (2024: 305,306m). Bearer plants themselves sit in fixed assets **at cost less depreciation and impairment**.

**FACT.** Fair-value changes **do route through P&L**, above the operating-profit line: −59,571 (2025), +142,439 (2024).

**INFERENCE.** This is the conservative end of IAS 41/PSAK 69 practice and materially better than peers who revalue bearer plants. Magnitude is small (≤7% of operating profit) and mean-reverting with CPO price. **Low manipulation risk. This is a genuine positive.**

### Revenue quality — price, not volume

**FACT.** FY2025 revenue +20.8%. Volumes: CPO sales 290kt vs 280kt (+3.6%), PK and derivatives 87kt vs 77kt (+13.0%). **FFB nucleus production 1,139kt vs 1,204kt in 2021 (−5.4% over four years).** CPO production 292kt vs 306kt in 2021.

**INFERENCE.** Essentially all revenue growth is CPO price. Screener `Revenue CAGR 5Y` of 6.33% (identical to the 3Y figure, because only four annual periods exist) is a commodity price series, not a growth rate. **CLAUDE.md's "never treat peak-cycle earnings as permanent earnings" applies squarely.** The screener's `Normalised/Trailing EBIT` of 0.685 does flag this correctly.

**FACT.** Gross margin fell 43.7% → 41.0% in a year of rising CPO prices (COGS +26.4% vs revenue +20.8%). *INFERENCE:* higher purchases of external FFB (the 1H2026 release attributes higher CPO output partly to external FFB) plus wage inflation (salaries 1,602,038 vs 1,524,225, +5.1%). Not alarming, but margin is not expanding with price.

---

## Balance Sheet

**FACT (audited, 31-Dec-2025; IDR million).**

| | 2025 | 2024 |
|---|---:|---:|
| Cash and cash equivalents | 7,597,470 | 5,453,691 |
| Total current assets | 8,699,271 | 7,117,283 |
| Total assets | 15,540,077 | 13,841,956 |
| Total current liabilities | 920,410 | 677,973 |
| Total liabilities | 1,543,964 | 1,285,202 |
| Total equity (incl. NCI) | 13,996,113 | 12,556,754 |
| **Non-controlling interests** | **(3,833)** | **(2,432)** |
| **Funded (interest-bearing) debt** | **NIL** | **NIL** |

**FACT.** The AR2025 five-year table shows **"Funded Debt: — " for every year 2021 through 2025.** The only interest-bearing obligations are lease liabilities (finance costs Rp1,176m in 2025, being *"bank administration fees and interest on lease liabilities"*). Net gearing −0.54×. Screener `Total Debt 0.0`, `Net Debt −8,371,777m` (June-2026) is correct.

**FACT.** Net cash at 30-Jun-2026 of Rp8,371,777m ÷ 6,819.96m shares = **Rp1,227.5 per share = 83.8% of the Rp1,465 price.**

**INFERENCE — the single most important number in this file.** Ex-cash, the market pays **Rp237.5/share** for the operating business. FY2025 EPS was Rp277, of which after-tax interest income was ~Rp32.4 (220,817m ÷ 6,820m), leaving **operating EPS of ~Rp244.6**. That is an **ex-cash P/E of roughly 1.0×.** Either the market is grossly wrong, or the market has decided the cash is not worth face value to a minority shareholder. **The entire investment reduces to which of those is true.** (See Capital Allocation.)

### Related-party bank concentration — a real, quantified concern

**FACT.** Note 5 and Note 27, cash at **PT Bank Ina Perdana Tbk (a related party)**, IDR million:

| | 2025 | 2024 |
|---|---:|---:|
| Current account — Rupiah | 915,788 | 121,293 |
| Current account — USD | 23,768 | 15,379 |
| Time deposits — Rupiah | 700,000 | 770,000 |
| **Total at Bank Ina Perdana** | **1,639,556** | **906,672** |
| **% of total assets (per Note 27)** | **10.55%** | **6.55%** |

**FACT.** That is **21.6% of the Dec-2025 cash pile at a single small related-party bank**, and the balance rose 81% year-on-year while total cash rose 39%. Third-party deposits are diversified (OCBC NISP 2,000,000; Danamon 2,000,000; Mega USD 822,318; Mandiri USD 479,525; SMBC 186,280; BRI 60,000 etc.).

**FACT.** Rp44,005m — **15.94% of all finance income** — was earned from Bank Ina Perdana.

**THESIS.** Indonesia's LPS deposit guarantee caps at Rp2bn per depositor per bank. Rp1.64tn at an affiliated bank is unsecured credit exposure to a Salim-linked institution. It is not evidence of wrongdoing, but it is exactly the kind of arrangement that makes a minority shareholder's claim on "net cash" softer than face value.

### Restricted cash / contingencies

**INFERENCE.** No restricted-cash line appears in Note 5; the note comprises cash on hand, cash in banks, and time deposits only. **FACT (Note 32d):** *"As of December 31, 2025, there is no litigation against the Group that may cause material future losses."* **FACT (Note 32b/c):** capex commitments Rp71,766 + US$216,681; supporting-materials commitments Rp200,253 + US$5,348. Immaterial against Rp8.4tn of cash.

**FACT.** Tax: subsidiary SAS received SKPKB (underpayment assessments) from the DGT; cash "payments of tax assessment of income taxes" were Rp200m (2025) and Rp98m (2024). Immaterial.

**FACT.** Effective tax rate 391,187/2,277,542 = **17.2%** (FY2024: 16.8%), below the 22% statutory rate. *INFERENCE:* explained by the 3ppt public-company rate reduction (LSIP free float ~40%) giving 19%, plus interest income taxed at 20% final and excluded from the corporate base. Sustainable, not a red flag — but note that a **higher effective tax rate would apply to any future profit mix with less interest income**.

**FACT.** NCI is **negative Rp3,833m** and loss-making (−1,401 in 2025). Immaterial; no minority leakage. Screener `StockholdersEquity 13,999.9` is parent-only equity, consistent.

---

## Cash Flow Quality

**FACT.** FY2025 audited consolidated statement of cash flows (IDR million):

| | 2025 | 2024 |
|---|---:|---:|
| Cash received from customers | 6,154,917 | 4,079,221 |
| Payments to employees | (1,652,263) | (1,550,478) |
| Cash paid to suppliers and other operating expenses | (1,327,458) | (958,401) |
| **Cash generated from operations** | **3,175,196** | **1,570,342** |
| Receipts of interest income | 259,853 | 209,741 |
| Tax refund / assessment payments | 599 / (200) | 490 / (98) |
| Corporate income tax paid | (419,715) | (215,142) |
| **Net cash from operating activities** | **3,015,733** | **1,565,333** |
| Additions to fixed assets (capex) | (433,312) | (376,249) |
| Additions to plasma receivables | (1,933) | (18,359) |
| Net payments for other non-current assets | (40,199) | (27,250) |
| **Net cash used in investing** | **(478,989)** | **(419,795)** |
| **Payments of cash dividends** | **(443,234)** | **(265,944)** |
| Payments of lease liabilities | (6,284) | (4,859) |
| **Net increase in cash** | **2,087,226** | **875,435** |

**FACT.** The screener's derived CFO check works here: `FreeCashFlow 2,582,421 + capex 433,312 = 3,015,733` — **exactly** the audited CFO. The CLAUDE.md workaround for Yahoo's missing IDX operating cash flow is validated for this name.

**FACT.** CFO/NI = 3,015,733/1,886,355 = **1.60×** (FY2024: 1.06×). Piotroski `Accruals = 1` is correctly earned.

### But FY2025 CFO is flattered by a related-party receivable unwind

**FACT.** Cash received from customers (6,154,917) **exceeded** revenue (5,511,706) by Rp643,211m in FY2025; in FY2024 receipts (4,079,221) **fell short** of revenue (4,562,503) by Rp483,282m.

**FACT (Note 27).** Trade receivable from parent **SIMP: Rp466,684m at 31-Dec-2024 (3.37% of total assets) → NIL at 31-Dec-2025.**

**INFERENCE.** ~Rp467bn of the FY2025 CFO is the collection of a receivable that the parent was allowed to carry into 2024 year-end. Normalising for it, **FY2025 CFO ≈ Rp2,549bn and CFO/NI ≈ 1.35×** — still good, but the headline 1.60× and the headline FCF of Rp2,582bn (FCF yield 15.7%) are **not a run rate**. Consistent with this, 1H2026 FCF (Rp217.8 + 468.7 = Rp686.5bn) is running at roughly half the FY2025 pace.

**FACT.** LSIP's stated credit terms (Note 30) are *"1 to 35 days from issuance of invoice"* for domestic sales, with bank guarantees required from sub-distributors. Rp466.7bn owed by SIMP at end-2024 is well outside that against Q4 sales run-rate. **THESIS:** the parent used LSIP's balance sheet as a short-term lender. It was repaid, and Note 24 confirms LSIP also earns interest on *"short-term loans to related parties"* — but the mechanism is available and unpoliced by any independent party.

### Replanting capex — the deferral question

**FACT.** Planted area (hectares), from the AR2025 operational highlights:

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|
| Total nucleus planted | 114,111 | 111,240 | 111,940 | 111,367 | **110,982** |
| Oil palm — mature | 85,630 | 83,742 | 85,198 | 84,941 | 84,744 |
| **Oil palm — immature** | **8,223** | **7,409** | **6,561** | **6,211** | **6,054** |
| Immature as % of oil palm | 8.8% | 8.1% | 7.2% | 6.8% | **6.7%** |
| Rubber — immature | 1,958 | 2,041 | 2,043 | 1,687 | **1,325** |
| FFB nucleus production ('000t) | 1,204 | 1,174 | 1,177 | 1,173 | **1,139** |
| CPO production ('000t) | 306 | 306 | 294 | 287 | 292 |
| Capex (Rp bn) | 308 | 321 | 369 | 376 | **433** |

**INFERENCE — replanting is running well below replacement.** Oil palm immature area has fallen for **five consecutive years** and total planted area has shrunk 3,129 ha since 2021. With a ~3-year immature period, 6,054 ha immature implies roughly **2,000 ha/year of new + replanting**. Against 90,798 ha of oil palm on a ~25-year economic cycle, steady-state replanting requires roughly **3,600 ha/year**. **Replanting is running at ~55% of the replacement rate.**

**INFERENCE — corroborated by output, not just area.** FFB nucleus production is down 5.4% since 2021 on a mature area that is essentially flat (85,630 → 84,744 ha), i.e. **yield per mature hectare is falling** — the signature of an ageing stand.

**FACT.** FY2025 capex Rp433,312m vs D&A Rp389,453m — capex is only **1.11× depreciation** for a business whose principal asset is a depreciating biological stand. Capex per planted hectare is Rp3.9m.

**FACT.** The 1H2026 press release quotes the President Director committing to *"cost control, operational efficiency and **prioritization of capital expenditure**"* — language consistent with capex restraint, not acceleration.

**THESIS.** **Reported free cash flow is flattered by under-replanting.** True maintenance capex — the spend needed to hold FFB output flat — is materially above the reported Rp433bn. If the deficit is ~1,600 ha/year at a normal Indonesian replanting cost of roughly Rp60–70m/ha spread over the immature period, the understatement is on the order of **Rp100bn/year**, i.e. ~4% of reported FCF, with the compounding effect showing up as a continuing decline in FFB yield rather than as a cash charge. *(ASSUMPTION: the Rp60–70m/ha replanting cost is a sector norm, not an LSIP disclosure. LSIP does not disclose replanting hectares or cost per hectare separately — **insufficient evidence for a precise maintenance-capex figure; requires further research**, ideally from the SIMP/IndoAgri disclosures or a direct IR question.)*

---

## Capital Allocation

**This is the crux of the investment, and the evidence is negative.**

**FACT.** Dividend history (DPS from ex-date records; totals and payout ratios confirmed against the AR2025 narrative and cash flow statement):

| FY | NI attributable (Rp m) | DPS (Rp) | Paid | Total (Rp m) | **Payout** |
|---|---:|---:|---|---:|---:|
| 2020 | *insufficient evidence* | 20 | Sep 2021 | 136,399 | n/a |
| 2021 | 992,423 | 51 | Aug 2022 | 347,818 | **35.0%** |
| 2022 | 1,036,448 | 53 | Jul 2023 | 361,458 | **34.9%** |
| 2023 | 761,995 | 39 | Jul 2024 | 265,978 | **34.9%** |
| 2024 | 1,476,909 | 65 | Jul 2025 | 443,298 | **30.0%** |
| 2025 | 1,887,756 | 83 | Jul 2026 | 566,057 | **29.99%** |

**FACT.** The AR2025 confirms both recent resolutions verbatim: the AGM of 19 June 2025 approved *"a total dividend of Rp443.3 billion or Rp65 per share, represent around 30% dividend payout"*; the AGM of 27 June 2024 approved *"Rp266.0 [billion] ... 35% dividend payout"*. The cash flow statement records dividends paid of 443,234 (2025) and 265,944 (2024). The FY2025 dividend of Rp83 was approved at a **29.99% payout** (ex-date 6 July 2026).

**FACT.** **The payout ratio was cut from ~35% to ~30% precisely as earnings and the cash pile rose.** Over FY2021–FY2025, cumulative earnings were Rp6,155.5bn and cumulative dividends Rp1,984.7bn — an average payout of **32.2%**, with Rp4,170.8bn retained. Over the same window cash went from Rp3,847bn (Dec-2022) to Rp8,372bn (Jun-2026), **+Rp4,524bn**. Essentially every rupiah retained went into a bank deposit.

**FACT.** FY2025 dividends of Rp443.2bn were **17.2% of FY2025 free cash flow of Rp2,582bn**. Even the raised FY2025 dividend (Rp566bn) is 21.9% of that FCF.

**FACT.** No share buyback appears in the FY2025 or FY2024 financing cash flows. `DilutedAverageShares` is unchanged at 6,819,964k for five years — no dilution either (Piotroski `No Dilution = 1` correctly earned).

**FACT.** No acquisition, no expansion into new planted area (area is shrinking), no announced capital project of scale in Note 32.

**THESIS — the value trap mechanism, stated explicitly.** LSIP earns a 4.23% pre-tax return on Rp8.4tn of deposits, i.e. **well below its cost of equity and below its own ~13% ROE on operating assets**. Every year the cash pile grows, group ROE is diluted (ROE 14.2% in 2025 despite an operating business earning far more on its Rp5.1tn of net fixed assets). Management has responded to a doubling of the cash pile by **reducing** the fraction of earnings distributed. The parent SIMP owns 59.51% and receives 59.51% of every rupiah paid out — but SIMP's own leverage and cash needs, not LSIP minorities', determine whether that rupiah is paid. **Nothing in five years of behaviour suggests a special dividend or a step-change in payout.** A 30% payout on Rp1,888bn of earnings is a 5.67% yield at Rp1,465 — respectable, but it is a *yield stock's* return, not the ~96% upside the screener's MOS implies, unless the cash is released.

**INFERENCE.** The screener's `Payout Ratio 0.2739` (Yahoo) is close enough to the true 30%, and `Dividend Yield 5.67%` is exact. Those are the honest numbers. The Rp1,227/share of net cash is real but has, on the evidence, an indefinite holding period.

---

## Accounting Concerns

### 1. Related-party sales — 64.5% of revenue to the controlling parent (the central governance question)

**FACT (Note 27).** Revenue from contracts with customers, related parties (IDR million):

| Counterparty | Relationship | 2025 | % of total sales | 2024 | % of total sales |
|---|---|---:|---:|---:|---:|
| **PT Salim Ivomas Pratama Tbk (SIMP)** | **Parent (direct)** | **3,486,712** | **63.26%** | **3,640,887** | **79.80%** |
| PT Kebun Mandiri Sejahtera | Common control | 59,328 | 1.08% | 13 | * |
| PT Mentari Subur Abadi | Common control | 5,594 | 0.10% | 22 | * |
| PT Indomarco Adi Prima | Other related | 2,945 | 0.05% | 2,675 | 0.06% |
| Others | | 58 | * | 165 | * |
| **Total related-party revenue** | | **3,554,637** | **64.49%** | **3,643,762** | **79.86%** |

**FACT.** SIMP owns **4,058,425,010 shares = 59.51%** of LSIP. SIMP is itself controlled by Indofood Agri Resources Ltd (IndoAgri) / the Salim group. The buyer of two-thirds of LSIP's output is its own controlling shareholder.

**FACT.** The entirety of LSIP's disclosed pricing assurance is one sentence: *"Sales and purchases from related parties are made at agreed prices depending on the type of product involved **with reference to market prices**."* The segment note adds: *"Transfer prices between legal entities and segments are set on a manner similar to transactions with third parties."* **No independent appraisal, no benchmarking to a published CPO index (KPB/Rotterdam/Malaysia), no independent-commissioner pricing opinion, and no arm's-length certification is disclosed anywhere in the FY2025 financial statements.**

**FACT.** LSIP's affiliate-sales share is the **highest among listed Indonesian palm producers**: LSIP 64.49% vs SMART 49.79%, SIMP 39.45%, TBLA 33.57%, SSMS 27.11% (NEXT Indonesia Center, 14 June 2026). The same commentary notes the practice is legal and subject to POJK 42/2020 and PMK 172/2023, and that an under-invoicing / transfer-pricing question has been raised at sector level, with reporting (June 2026) that the Attorney General's Office is examining CPO export under-invoicing involving Salim-group CPO companies. **I could not confirm from any primary source that LSIP itself is a named subject; Note 32d states there was no material litigation at 31-Dec-2025. Insufficient evidence — requires further research (this belongs to the Macro/Catalyst and Thesis Killer agents).**

**INFERENCE — a partial counter-argument, in fairness.** If LSIP were being systematically under-priced by its parent, its margins should be depressed relative to independent planters. They are not: gross margin 41.0% and operating margin 36.4% in FY2025, ROE 14.2%, and operating margin averaged 33.4% over five years. That is *inconsistent* with severe value transfer on price. **But it does not rule out smaller, cycle-timed transfers**, and it is an indirect inference, not evidence of arm's-length pricing.

**THESIS.** The correct way to hold this: **LSIP's reported earnings are not independently verifiable.** They are set, in substantial part, by the counterparty that controls the board. This is not a reason to assume fraud; it is a reason to refuse to pay a full multiple, and it is a large part of why the market values the operating business at ~1× ex-cash earnings.

### 2. Other related-party items

**FACT (Note 27).** Finance income from related parties Rp48,665m = **17.63%** of all finance income (Bank Ina Perdana 44,005 = 15.94%; associate PT Sumalindo Alam Lestari 4,660 = 1.69%). Freight and insurance expense to related parties Rp17,211m = **23.54%** of that expense line (SIMP 3,846 = 5.26%; PT Samudera Sejahtera Pratama 13,365 = **18.28%**, newly appearing in 2025). Rental to associate PT Aston Inti Makmur Rp7,625m. Finished-goods purchases from SIMP and Kebun Mandiri Sejahtera Rp26,519m (new in 2025). Fixed-asset/spares purchases from PT Indo Traktor Utama and PT Indomobil Prima Niaga Rp10,097m.

**FACT (Note 27).** LSIP also transacts *"advances for the sale of palm products (Note 17)"* with related parties. *INFERENCE:* this explains the half-year spikes in current liabilities (Rp1,184.6bn at Jun-25, Rp1,341.3bn at Jun-26 vs Rp920.4bn at Dec-25) — customer prepayments, which are cash-positive for LSIP but make interim working capital and the interim current ratio non-comparable to year-end.

**INFERENCE.** Individually small, but the picture is a company whose sales, a fifth of its interest income, a quarter of its freight cost, its rented head office, its insurance and its vehicle fleet all run through the controlling group. Cost lines are the mirror image of the revenue risk: overcharging on costs transfers value out just as effectively as under-pricing revenue.

### 3. Screener-specific accounting distortions

**FACT.** Beta of 0.013 on the fact sheet is nonsense (CLAUDE.md already flags Yahoo betas for illiquid IDX names). `Justified PB IV` is blank so no bank-style lens is polluted, but any COE derived from this beta would be floored, not computed.

**FACT.** `Business Type: Compounder`. **INFERENCE:** wrong. Production volume is declining, planted area is shrinking, revenue growth is 100% commodity price, and the five-year operating-profit series (1,193 / 1,206 / 759 / 1,551 / 2,008) is a cycle, not a compounding curve. LSIP is a **commodity price-taker with a large idle cash balance** — analytically closer to "average business, very cheap on assets" than to "good business at a fair price."

---

## Key Positive Findings

1. **The balance sheet is exactly as advertised and then some.** Zero funded debt for five consecutive years (AR five-year table: "Funded Debt —" every year), only immaterial lease liabilities, negative and immaterial NCI (−Rp3,833m), no restricted cash, no material litigation (Note 32d), immaterial tax assessments. Net cash Rp8,372bn = **Rp1,227.5/share = 83.8% of the share price**. The Altman Z of 14.3 and Interest Coverage of 1,980× are meaningless artefacts, but the underlying safety is real.

2. **Accounting is conservative, and the one-offs cut the right way.** Biological assets are *only* unharvested produce at Level 2 market prices (Rp245.7bn); **bearer plants are held at cost**, not revalued — the conservative end of PSAK 69 and materially better than peers. The FY2024 Rp437.6bn charge was a genuine impairment (Rp296.2bn rubber-plantation CGU, discounted at 11.13%) plus Rp138.1bn of fixed-asset write-offs, both of which **depressed** FY2024. There is no evidence of earnings inflation anywhere in the statements.

3. **Cash generation is genuine and independently verified.** Audited FY2025 CFO of Rp3,015,733m ties **exactly** to the screener's derived figure (FCF 2,582,421 + capex 433,312), validating the CLAUDE.md workaround for Yahoo's missing IDX operating cash flow. Cash generated from operations of Rp3,175bn against Rp2,008bn of operating profit is real conversion, and net cash rose Rp2,087bn in the year after paying Rp443bn of dividends.

## Key Negative Findings

1. **Capital allocation is deteriorating, and it is the whole thesis.** The payout ratio was **cut from ~35% (FY2021–FY2023) to 30.0% (FY2024) to 29.99% (FY2025)** precisely as earnings doubled and cash doubled. Cumulative FY2021–25: Rp6,155bn earned, Rp1,985bn distributed (32.2%), Rp4,171bn retained — and cash rose Rp4,524bn. FY2025 dividends were **17.2% of free cash flow**. There is no buyback, no acquisition, no expansion. The company earns **4.23% on Rp8.4tn** of deposits, far below its cost of equity, and shows no intention of stopping.

2. **64.49% of revenue is sold to the 59.51% parent with no disclosed independent pricing verification** (Rp3,554,637m in 2025; 79.86% in 2024). The highest affiliate-sales ratio among listed Indonesian palm producers. Add Rp1,639,556m of cash (10.55% of total assets, 21.6% of the cash pile) at related-party PT Bank Ina Perdana, a Rp466,684m trade receivable extended to SIMP at end-2024 against stated 1–35 day terms, and 17.6% of finance income / 23.5% of freight cost running through affiliates. **Reported earnings are structurally unverifiable by an outside investor.**

3. **Replanting appears deferred and production is already declining.** Oil palm immature area has fallen five years running (8,223 → 6,054 ha; 8.8% → 6.7% of oil palm), total planted area is down 3,129 ha since 2021, capex is only 1.11× depreciation, and **FFB nucleus production is down 5.4% since 2021 on flat mature hectarage** — falling yield per mature hectare. Implied replanting of ~2,000 ha/yr is roughly **55% of the ~3,600 ha/yr steady-state requirement**. Reported FCF is therefore flattered; the deficit will surface as continued volume decline rather than as a cash charge.

## Potential Screener False Positives

1. **`EBIT` is pre-tax profit including interest income — CONFIRMED, and it is a systemic pipeline defect.** Screener EBIT FY2025 (2,278.7bn) = PBT (2,277,542) + finance costs (1,176), exactly; true `laba usaha` is **2,008,388**, so **Rp276,021m of interest income and Rp5,691m of associate losses are being capitalised as operating profit (a 13.5% overstatement)**. The `Normalised EBIT (5Y)` of Rp1,528,953m is the median of only four contaminated years; the true 4-year median is **Rp1,378,354m (−10.9%)** and the true 5-year median is **Rp1,205,856m (−26.8%)**. Effect: **EPV/share falls from 2,684.8 to 2,541 (−5.3%) or 2,377 (−11.5%)**; comparables IV falls ~6.8%; **blended IV ≈ 2,650–2,730, MOS ≈ 45–47% not 49%, upside ≈ 84–86% not 96%.** The principle is worse than the LSIP magnitude: EPV adds net cash at face **and** capitalises the interest that same cash earns, valuing the cash at ~124% of face. **Fix `metrics.py` to build EBIT up from operating profit, and note that Yahoo's `OperatingIncome` field is also unusable here (FY2024: 1,918.7 reported vs 1,550.9 actual, a Rp368bn overstatement).** Related bug: **`EBITDA` is set equal to `EBIT` — D&A of Rp389,453m is never added back**, so `EV/EBITDA` is not a real metric for this name.

2. **"BUY, MOS 49%" is really "the market values the operating business at ~1× ex-cash earnings, and the cash is not being distributed."** 83.8% of the price is net cash; the MOS is almost entirely a claim on a cash balance that management has, over five years, chosen to retain at an *increasing* rate. The screener has no gate for "cash exists but is not accessible to minorities." At a 30% payout the realistic shareholder return is a **5.67% dividend yield plus CPO-cycle earnings**, not a 96% re-rating. **This is the classic value-trap shape and the Thesis Killer should be pointed straight at it.**

3. **`Business Type: Compounder` and the growth rates are cycle artefacts.** FY2025 revenue +20.8% came from CPO price, not volume (CPO sales +3.6%, FFB nucleus production −5.4% since 2021). The `Net Income CAGR 3Y` of 22.1% is measured off a 2023 trough (operating profit Rp759bn); cleaning the FY2024 one-off and biological fair-value swings, adjusted operating profit grew **+12.2%, not +29.5%**. `Revenue CAGR 5Y` equals `Revenue CAGR 3Y` because only four annual periods exist. **Trailing earnings are near peak-cycle** — the screener's own `Normalised/Trailing EBIT` of 0.685 is the honest signal, and it should be weighted more heavily than the trailing-based lenses. Secondary: `Beta 0.013` is not a beta; `Quality Score 73.3` rests partly on the contaminated EBIT and on ROE flattered by a nil-debt, cash-heavy balance sheet.

---

## Financial Verdict: **ACCEPTABLE**

**Not STRONG:** two-thirds of revenue is priced by the controlling shareholder with no disclosed independent verification, and capital allocation is moving away from shareholders (payout cut 35% → 30% as cash doubled). Neither of those can be resolved from the outside.

**Not QUESTIONABLE or FAIL:** the accounting itself is clean and, if anything, conservative — bearer plants at cost, biological fair value confined to unharvested produce, one-off charges taken not avoided, cash flow that ties exactly to the audited statements, and Rp8.4tn of cash sitting in named banks with zero funded debt.

**The financial statements do not kill this thesis. The capital-allocation record and the related-party structure are what will decide it**, and both point toward "average business, very cheap, with a controlling shareholder who has no observable intention of releasing the cash" rather than "good business at a fair price." Adjusted for the EBIT defect, MOS is ~45–47%, not 49%.

### Open items — insufficient evidence, requires further research
- The precise maintenance-capex requirement. LSIP does not disclose replanting hectares or cost per hectare; my ~3,600 ha/yr steady-state figure is a derived estimate, not a company disclosure.
- Whether LSIP is specifically a subject of the June 2026 CPO export under-invoicing examination reported against Salim-group companies (Note 32d says no material litigation at 31-Dec-2025; nothing later confirmed from a primary source).
- Independent benchmarking of the SIMP transfer price against published CPO indices — the single highest-value follow-up. SIMP's and IndoAgri's own segment disclosures may permit a cross-check.
- FY2020 net income (for the FY2020 payout ratio) and the identity of the external auditor were not verified.
