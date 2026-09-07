# Logic Audit — PERSONAL_STOCKS_PICKER_Quarterly_UPDATE.xlsx

**File audited:** `/root/.claude/uploads/553b4cb5-c74f-5362-839f-32c117ee1e0c/408baa4d-PERSONAL_STOCKS_PICKER_Quarterly_UPDATE.xlsx`
**Sheet under audit:** `Universe`, headers row 3, data rows **4–959 = 956 tickers**, columns A–CS (97 cols).
**Method:** two openpyxl passes (formulas + cached values), plus the raw feed in `RAW_key_statistics` (956 rows × 94 cols). Every claim below is backed by cached numbers pulled from the file. Nothing was modified.

**Headline:** the model is not primarily broken by its formulas — it is broken by the data feed underneath it. `RAW_key_statistics` delivers **every money column as an unsigned absolute value**. 289 of 956 companies have a positive Net Income recorded for a company the same feed says has a negative P/E; 299 have net *cash* recorded as net *debt*. On top of that, the two headline Magic Formula inputs are not Greenblatt's, the Setup sheet is 100 % dead, and 16 of 97 columns are frozen cached text in Excel.

---

## 1. Summary table

| ID | Column(s) | Severity | One-line | Rows affected |
|---|---|---|---|---|
| **B-01** | O,R,S,T,U,V,W,X,Y,Z,AE,AF (via `RAW_key_statistics`) | **Critical** | Source feed strips the sign off every money column; losses are recorded as profits | 289 of 956 (NI sign wrong); 192 (WC); 51 (equity) |
| **B-02** | BU, BK → BV, BW, BX, BY, CA, CB, CC, BL | **Critical** | Net debt is unsigned, so net-cash companies get their cash **subtracted** from intrinsic value | 299 of 956 net-cash rows; 180 with an EPV price, 264 with a comparables price |
| **B-03** | AX, AZ, BB | **Critical** | "Magic Formula Earnings Yield" is net income / market cap (1÷PE), not EBIT/EV | 853 of 897 rows verified identical to 1/PE |
| **B-04** | AY, BA, BB | **Critical** | "ROC" is TradingView's after-tax ROIC, not Greenblatt EBIT/(NWC+net fixed assets) | 956 of 956 |
| **B-05** | BZ, CA, CB, CC | **Critical** | EPV capitalises an *unlevered after-tax EBIT* at the *cost of equity*, uses TTM (not cycle-average) earnings, and hardcodes tax 0.22 | 499 rows with an EPV price |
| **B-06** | Setup!C4:C9 | **Critical** | All six Setup parameters (and their 6 named ranges) are referenced by **zero** formulas | whole model |
| **B-07** | BE, BF, BG, BN, BY, CC | **Critical** | `""` silently coerces to 0 in Google Sheets, producing fake values: NCAV = −Total Liabilities, MOS = −100 % | BE 103; BN 587; BY 290; CC 457 |
| **B-08** | CS, CR (and absent DCF) | **Critical** | No BUY/WATCH/SKIP formula exists; no DEEP VALUE bucket; no DCF at all. Classification is hand-typed | 48 of 956 rows classified; 908 blank |
| **B-09** | whole model | **Critical** | No sector gate: banks/insurers run through EV/EBIT, EPV, NCAV, FCF | 122 Financials rows (48 Banks, 16 Insurance) |
| **B-10** | BN, BY, CC | **High** | All three "MOS" columns compute *upside* (IV−P)/P, not MOS (IV−P)/IV; only one number is shown, not both | 956 |
| **B-11** | BF | **High** | Graham's 2/3 test is absent — flag fires at Price < 1.0 × NCAV | 47 flagged, only 27 pass 2/3 → 20 false positives |
| **B-12** | P, Q → BT, BZ | **High** | Two EBIT estimates that contradict each other are arithmetically averaged | 117 rows opposite signs; 245 rows >50 % apart; median disagreement 34.9 % |
| **B-13** | BO, CQ, BP, BQ | **High** | Peer groups are keyed on the *resolved* label string, so a company that falls to a coarser level is compared only to other fall-throughs — often to itself | 92 rows at CQ=2/3, 43 of them in a group of <4; 3 groups of exactly 1 |
| **B-14** | CE vs CF → CG:CL, CN:CP | **High** | CG:CL read the volatile `CF`, not the hardcoded `CE`; CF has 78 refusals, 417 blanks, two different prompt versions, and at least one row holding another ticker's review | AI scores on 442 of 956; CE's 315 hardcoded reviews referenced 0 times |
| **B-15** | BD | **High** | Piotroski is imported whole from the scraper; it cannot be recomputed or verified from anything in the workbook | 956 |
| **B-16** | AA, AB, AC, AD | **Medium** | The `<1` sign hack forces `AA = −|WC|`, so the "Match?" check is guaranteed FALSE for every current-ratio-below-1 company | 297 FALSE of 956; 290 of them are CR<1 by construction |
| **B-17** | BJ, BL, BM | **Medium** | DDM parameters hardcoded in BJ1/BL1 not Setup; Gordon uses D₀ not D₁; the k−g floor is currently safe **only because of B-02** and will break when B-02 is fixed | 954 rows with a DDM value |
| **B-18** | BX | **Medium** | "min of both" mixes an equity-multiple price with an EV-multiple price and silently degrades to a single leg without flagging | 65 rows run on one leg only; 290 rows blank → B-07 |
| **B-19** | V | **Medium** | Header says "Free Cashflows **per Share**"; formula pulls total FCF/1e6 | 956 |
| **B-20** | BG | **Medium** | Labelled "Discount Percentage" but computes upside vs price, not discount to NCAV | 956 |
| **B-21** | all money cols | **Medium** | Feed is quantised to 1 billion IDR; genuine zeros are converted to `""` by the `IF(x/1e6=0,"")` idiom | 70 tickers with NI = 0; 63 with \|NI\| ≤ 3 rounding units |
| **B-22** | AZ, BA | **Medium** | Negative-EY and negative-ROC names still occupy rank slots (Greenblatt excludes them) | 292 negative-EY, 228 negative-ROC ranked |
| **B-23** | A–CP | **Medium** | 16 columns are `__xludf.DUMMYFUNCTION` stubs — dead in Excel, frozen cached values only | 14,754 cells |
| **B-24** | AW / AX | **Low** | Duplicate columns pulling the identical source field | 956 |
| **B-25** | CM | **Low** | `Active?` is hardcoded TRUE on all 956 rows, so every exclusion filter built on it is inert | 956 |
| **B-26** | CR, TradingView_Scrap, Peers!A:B | **Low** | Dead/stale artefacts: CR populated on 44 rows and static; TradingView_Scrap referenced 0 times | — |

---

## 2. Bug detail

### B-01 — Critical — The source feed strips the sign off every money column

**What it does.** `RAW_key_statistics` is the sole numeric source (columns O–AF, BU all `XLOOKUP` into it). Across all 18 money columns the minimum value is **0.00 and there are zero negatives**:

```
Revenue (TTM)                 min=0   negatives=0
Gross Profit (TTM)            min=0   negatives=0
Net Income (TTM)              min=0   negatives=0
Cash From Operations (TTM)    min=0   negatives=0
Cash From Financing (TTM)     min=0   negatives=0
Free cash flow (TTM)          min=0   negatives=0
Working Capital (Quarter)     min=0   negatives=0
Total Equity                  min=0   negatives=0
Net Debt (Quarter)            min=0   negatives=0
...
```

The *ratio* columns from the same feed keep their signs (293 negative ROAs, 293 negative P/Es, 243 negative EV/EBITs). So the feed knows the sign; the money columns have had it removed.

**Worked example — ABBA (Mahaka Media, row 5).** From the raw sheet:

| field | value |
|---|---|
| Net Income (TTM) | **+6,000 mio IDR** |
| Current PE Ratio (TTM) | −37.99 |
| Return on Assets (TTM) | −2.12 % |
| Return on Equity (TTM) | −12.38 % |
| Net Profit Margin (Q) | −8.31 % |
| Market Cap | 216,000 mio |

Market Cap ÷ PE = 216,000 ÷ (−37.99) = **−5,686 mio**. That is the true net income; the feed reports +6,000. Repeating this across the universe: **289 of 956 rows** have NI > 0 while PE or ROA is < 0, and the median of |MarketCap/PE| ÷ reported NI over those rows is **0.9994** — i.e. the reported figure is exactly the absolute value.

The balance sheet confirms it independently. ABBA: Total Assets 269,000, Total Liabilities 354,000, Total Equity **+46,000**. Liabilities exceed assets, so equity must be −85,000. **51 rows** report positive equity while L > A.

Working capital shows the same: **192 rows** report a positive Working Capital while the same feed reports Current Ratio < 1 — arithmetically impossible.

**What it should do.** Column S must be the signed net income. **Concrete fix:** rebuild the sign in the Universe layer rather than trusting the feed —
`S = IF(AR<0, -ABS(rawNI), ABS(rawNI))/1e6` (use the PE sign), `Y_equity = IF(X>W, -ABS(rawEquity), ABS(rawEquity))/1e6`, `Z_WC = IF(CurrentRatio<1, -ABS(rawWC), ABS(rawWC))/1e6`. Longer term: fix the scraper.

**Downstream damage:** AM (NPM TTM) reads +2.9 % for ABBA against a true −8.3 %; BE, BZ, CA, BT all consume the unsigned figures; any future computed Piotroski "positive net income" test would pass for 289 loss-makers.

---

### B-02 — Critical — Net debt is unsigned, so net-cash companies get their cash subtracted

**What it does.** BU = `XLOOKUP(..., keyStats[Net Debt (Quarter)])/1e6`. The feed reports net debt as a magnitude. BV = BT − BU (implied equity), CA = BZ − BU (EPV equity), BK = NetDebt/Equity (feeds cost of equity BL).

**Worked example — AALI (Astra Agro Lestari, row 4).**

```
Cash (Quarter)          4,929,000 mio
Total Debt (Quarter)       90,000 mio
→ true net debt        = 90,000 − 4,929,000 = −4,839,000 (net CASH)
Feed "Net Debt"         = +4,839,000        ← exact absolute value
Independent check: EV − MktCap = 10,558,000 − 14,820,000 = −4,262,000 (also net cash)
```

EPV chain as the sheet computes it:

```
P = 1,888,290.1 ; Q = 2,270,537.6 ; avg = 2,079,413.9
BZ = 2,079,413.9 × (1−0.22) / 0.1262787 = 12,844,151   (matches cached BZ4)
CA = 12,844,151 − 4,839,000 = 8,005,151                (matches cached CA4)
CB = 8,005,151 / 1,920 sh    = 4,169.35 IDR            (matches cached CB4)
CC = (4,169.35 − 7,700)/7,700 = −45.85 %               (matches cached CC4)
```

With the sign corrected (net cash **added**):

```
CA' = 12,844,151 + 4,839,000 = 17,683,151
CB' = 9,209.97 IDR/share
Upside = 9,210/7,700 − 1 = +19.6 %   (or +15.7 % using the EV-derived −4,262,000)
```

AALI flips from "45.9 % overvalued" to "≈16–20 % undervalued" on the sign of one cell. The same cell also inflates the cost of equity: BK should be −0.2093, giving BL = 0.12 + 0.03×(−0.2093) = **0.1137** rather than the 0.1263 used.

**Rows affected:** 299 net-cash companies carry a positive "net debt". Of those, **180 have an EPV price (CB)** and **264 have an implied equity value (BV)** — every one understated by roughly twice the net cash.

**Concrete fix:** stop using the feed's Net Debt. Compute it in-sheet: `BU = AF − AE` (Total Debt − Cash), or `BU = M − L` (EV − Market Cap), both of which are already correctly signed in this workbook. Then `CA = BZ − BU` works for both net-debt and net-cash names.

---

### B-03 — Critical — Magic Formula "Earnings Yield" is E/P, not EBIT/EV

**What it does.** `AX = XLOOKUP($A4:$A960, keyStats[Ticker], keyStats[Earnings Yield (TTM)], "")` — a straight pull of the vendor's earnings yield.

**Verification.** Comparing AX against 1/AR (1 ÷ trailing P/E) over the 897 rows where both are numeric: **853 rows agree to within 0.0005**. Comparing AX against 1/AU (1 ÷ EV/EBIT) gives a mean absolute error of 0.19 and a max of 33.5.

**Worked example — AALI.** AX = 0.0956. 1 ÷ PE(TTM) = 1 ÷ 10.46 = **0.09560**. Greenblatt's EBIT/EV = 1 ÷ (EV/EBIT) = 1 ÷ 4.65 = **0.2151**. The sheet is using the wrong one by a factor of 2.25×.

**Why it matters.** Greenblatt uses EBIT/EV precisely to neutralise capital structure and tax. Using E/P re-introduces both, systematically favouring low-tax, high-leverage names and penalising cash-rich ones. Every AZ rank and every BB score in the workbook is therefore not a Magic Formula rank.

**Concrete fix:** `AX = IFERROR(1/AU, "")` — column AU already holds EV/EBIT (TTM) — or better, once B-12 is resolved, `AX = chosenEBIT / M`.

---

### B-04 — Critical — "ROC" is ROIC, not Greenblatt's Return on Capital

**What it does.** `AY = IF(AJ<>"", AJ, AI)` — take ROIC, else ROCE. Both are vendor-computed.

**Verification.** AY equals AJ (ROIC) on **956 of 956 rows**; AJ is never blank, so the ROCE fallback in the formula is unreachable dead code.

**Worked example — AALI.** AY = 0.0622 (vendor ROIC). Greenblatt's ROC = EBIT / (net working capital + net fixed assets). Using the sheet's own numbers: EBIT ≈ 2,079,414 (avg of P and Q); NWC = AC − AD = 9,111,572 − 3,337,572 = 5,774,000; net fixed assets ≈ W − AC = 27,963,000 − 9,111,572 = 18,851,428. ROC ≈ 2,079,414 / 24,625,428 = **8.4 %**, versus the 6.2 % used. Direction and magnitude both differ, and ROIC is after-tax while Greenblatt's is pre-tax.

**Concrete fix:** `AY = IFERROR(EBIT / (MAX(0, AC-AD) + (W - AC)), "")`, excluding excess cash from current assets per Greenblatt.

---

### B-05 — Critical — EPV: wrong discount rate, wrong earnings base, hardcoded tax

`BZ = IFERROR(IF(((P+Q)/2)*(1-0.22)/BL < 0, "", ((P+Q)/2)*(1-0.22)/BL), "")`

Three separate defects in one formula:

1. **Discount rate.** `(EBIT × (1−t))` is NOPAT — an *unlevered, enterprise-level* cash flow. It is being capitalised at **BL, the levered cost of equity**, then net debt is subtracted afterwards. That double-counts leverage. For AALI, BL = 0.1263 vs the Setup WACC of 0.12: BZ = 12,844,151 instead of 2,079,414×0.78/0.12 = **13,516,190** (and, with B-02 fixed, 9,560 IDR/share instead of 9,210).
2. **Not normalised.** Greenwald's EPV requires cycle-average earnings adjusted for one-offs. Both P and Q are TTM. AALI is a CPO producer whose Revenue YoY (AN) is +28.4 % and Gross Profit YoY (AO) is +40.6 % — this is a cyclical peak being capitalised into perpetuity, exactly what the stated intent said to avoid.
3. **Hardcoded tax.** `0.22` is a literal. `Setup!C4` also holds 0.22, and the named range `Tax_Rate` points at it — but the formula does not reference either (see B-06). The numbers agree today by coincidence only.

**Concrete fix:** `BZ = normEBIT * (1 - Tax_Rate) / WACC_ID`, where `normEBIT` is a 3–5 year average EBIT (this data is not currently in the workbook and would need to be scraped), and WACC_ID/Tax_Rate are the named ranges.

---

### B-06 — Critical — The entire Setup sheet is dead

`Setup!B4:C9` holds Tax Rate 0.22, WACC 0.12, Terminal Growth 0.03, Risk Free 0.065, MOS Buy 0.30, MOS Watch 0.10. Six workbook-level named ranges point at them: `Tax_Rate`→`Setup!$C$4`, `WACC_ID`→`$C$5`, `Terminal_Growth_ID`→`$C$6`, `Risk_Free_ID`→`$C$7`, `MOS_Buy`→`$C$8`, `MOS_Watch`→`$C$9`.

**A regex scan of every formula in all 11 sheets returns 0 hits for the string `Setup` and 0 hits for each of the six named ranges.** Full detail in §3.

The consequence is that editing the Setup sheet changes nothing. The parameters actually driving the model are literals scattered across the Universe sheet: `0.22` inside BZ4, `0.12` in cell **BL1**, `0.03` and `0.18` inside BL4, `0.07` in cell **BJ1**. MOS Buy 0.30, MOS Watch 0.10, Terminal Growth 0.03 and Risk Free 0.065 have no counterpart anywhere.

**Concrete fix:** replace the literals with the named ranges (`WACC_ID`, `Tax_Rate`, …), move BJ1/BL1 onto the Setup sheet, and delete the shadow parameter cells.

---

### B-07 — Critical — `""` coerces to 0, manufacturing fake NCAVs and fake −100 % margins of safety

Google Sheets (unlike Excel) coerces an empty string to 0 inside arithmetic. Almost every formula in this workbook returns `""` on failure, and those `""`s then flow into subtraction and division.

**Case 1 — NCAV becomes minus total liabilities.** `BE = IF(AC-X = 0, "", AC-X)`. When AC (Current Assets) is `""`, the expression evaluates as `0 − X`.

Worked example — **BBCA (Bank Central Asia)**: AC = `""`, X (Total Liabilities) = 1,261,870,000 mio. Cached **BE = −1,261,870,000**, exactly −X. This holds on **103 of 956 rows** — BE = −X to within 1e-6 on every one of them. BG for BBCA then reads **−2.2755**, presented as a "Discount Percentage (%)".

**Case 2 — blank valuations report as −100 % margin of safety.** `BY = IFERROR((BX−K)/K, "")`. When BX is `""`, this is `(0 − K)/K = −1`.

| column | numeric | blank | cells reading exactly −1 |
|---|---|---|---|
| BX → BY | 666 | 290 | **290** |
| CB → CC | 499 | 457 | **457** |
| BM → BN | 954 | 585 are BM = 0 | **587** |

The match is exact: every blank produces a −1. So 457 companies display "Core MOS = −100 %" when the truth is "no EPV could be computed", and 587 display "DDM MOS = −100 %" when the truth is "pays no dividend". Any sort, filter or median over these columns is being fed 457–587 fabricated −1s.

**Concrete fix:** guard every consumer explicitly — `BY = IF(OR(BX="", K=""), "", (BX-K)/K)` — and for BE, `BE = IF(OR(AC="", X=""), "", AC-X)`.

---

### B-08 — Critical — There is no classification engine

Intent items 5 and 7 require a 5-year Bear/Base/Bull DCF and a BUY/WATCH/SKIP output with a separate DEEP VALUE / SPECIAL SITUATION bucket, with the explicit rule that cheapness alone must never produce a BUY.

**What exists.** Column CS (`Shortlist?`) contains **hand-typed text on 48 of 956 rows** (BUY 11, WATCH 28, SKIP 9); 908 rows are blank. There is no formula in the column. CR (`Last Review Date`) is a static timestamp on 44 rows (the header comment `=NOW()` is text in CR1, not a formula). No DCF columns exist anywhere in A–CS — no growth ramp, no terminal value, no scenario columns.

So `MOS_Buy` = 0.30 and `MOS_Watch` = 0.10 are not merely unwired (B-06); there is nothing for them to drive.

**Concrete fix:** add a computed classification that requires *both* a quality gate and a value gate, e.g.
`= IF(OR(BD<5, CG+CH+CI<3, K="") , "SKIP", IF(AND(MOS>=MOS_Buy, BD>=6, CK>=1), "BUY", IF(MOS>=MOS_Watch,"WATCH","SKIP")))`
with the DEEP VALUE bucket as a separate boolean column driven by BF (post-B-11 fix) rather than folded into the same ladder.

---

### B-09 — Critical — No sector gate: banks are valued on EV/EBIT, EPV and NCAV

**What it does.** Nothing in columns A–CS branches on column D (Sector) or E (Subsector). The only sector awareness anywhere in the workbook is *inside the Gemini prompt text* (column CF), which is a dead `DUMMYFUNCTION` in Excel and covers only 442 of 956 rows anyway.

**Rows affected:** 122 Financials (48 Banks, 16 Insurance, 14 Financing Service, 32 Holding & Investment, 12 Investment Service). Of these, 88 carry an EPV intrinsic price, 102 a comparables price, 120 an NCAV.

**Worked examples from the cached values.**

*BBCA (Bank Central Asia):*
- `AC`/`AD` = `""` (banks have no classified current assets) → **BE (NCAV) = −1,261,870,000 mio**, i.e. minus the entire deposit base, presented as a Graham net-net figure, with `BG = −227.6 %` presented as a discount.
- `AU` EV/EBIT = 13.65 for an entity whose "EV" (971,205,000 mio) is market cap minus cash while deposits — its actual funding — are ignored.
- `BU` net debt = **0** because the feed records Total Debt = 0 for banks. So `CA = BZ` and the whole net-debt bridge silently no-ops.
- `CB` EPV price = 3,688 vs a market price of 8,025 → `CC` = −54 %.

*BBNI (Bank Negara Indonesia):* `CB` = 4,367 vs price 4,220 → **`CC` = +3.5 %**, and `BY` (comparables MOS) = **+137.8 %**. A bank surfaces as one of the cheapest names in the sheet purely from a peer-PE median applied to an EPS figure.

*Magic Formula contamination:* **13 of the top 100** by BB score are Financials, including BFIN (BFI Finance) at rank #8 overall (BB = 116).

**Concrete fix:** add a `IsFinancial = OR(D="Financials", …)` helper column; blank BE, BF, BG, BZ, CA, CB, CC, BC and the Magic Formula ranks for those rows, and route them to a parallel ROE / P-B / NPL block.

---

### B-10 — High — All three "MOS" columns compute upside, not margin of safety

`BN = (BM−K)/K`, `BY = (BX−K)/K`, `CC = (CB−K)/K`. All three divide by **Price**. The stated intent is explicit: MOS = (IV − P) / **IV**, Upside = IV/P − 1, and "these are different numbers and must be shown separately". Only the upside number exists.

**Worked example — AALI with B-02 corrected** (CB' = 9,209.97, K = 7,700):
- Upside = 9,209.97/7,700 − 1 = **+19.6 %**
- MOS = (9,209.97 − 7,700)/9,209.97 = **+16.4 %**

The gap widens fast: at an IV of 15,400 the upside is +100 % but the MOS is only 50 %. Screening on the upside number against a 30 % threshold admits everything with a true MOS of 23 % or better — a materially looser gate than the one the owner believes he set.

**Concrete fix:** keep the existing columns but rename them `… Upside`, and add three MOS columns `= IF(OR(IV="",IV<=0),"",(IV-K)/IV)`. Compare `MOS_Buy` / `MOS_Watch` only against the MOS columns.

---

### B-11 — High — The Graham 2/3 test is not applied

`BF = IF(BE="", "", L < BE)` — market cap below 1.0 × NCAV. Graham's classic net-net test is Price < **2/3** × NCAV per share.

**Counts.** 47 rows currently flag TRUE. Applying `L < (2/3)*BE` to the same cached values leaves **27**. So **20 of the 47 "net-nets" (43 %) fail the actual Graham test.**

**Worked example — EKAD (Ekadharma International, row 159):** L = 657,000 mio, BE = 659,449 mio. The sheet flags it TRUE at a 0.4 % discount (BG = +0.37 %). Graham's threshold would be 2/3 × 659,449 = 439,633 — EKAD trades at 1.49× that. Same story for CLPI (L 464,000 vs BE 476,315, a 2.7 % discount) and SCCO (9.8 %).

Note also that BE itself is built on the back-solved AC (B-16) and on unsigned liabilities (B-01), so even the 27 survivors need re-checking.

**Concrete fix:** `BF = IF(OR(BE="", BE<=0, L=""), "", L < (2/3)*BE)` and add a companion column showing NCAV per share = `BE/N` for a like-for-like comparison against price K.

---

### B-12 — High — Two contradictory EBIT estimates are averaged

`P = Revenue(TTM) × Operating Margin (Quarter)` — a TTM revenue scaled by a *single quarter's* margin.
`Q = EV ÷ EV/EBIT (TTM)` — implied by the vendor's own multiple.
`BT` and `BZ` both then use `(P+Q)/2`.

**Disagreement statistics over the 893 rows where both are numeric:**

| measure | value |
|---|---|
| median relative disagreement | **34.9 %** |
| rows more than 25 % apart (same sign) | 409 |
| rows more than 50 % apart (same sign) | 245 |
| rows with **opposite signs** | **117** |
| rows where the average has the opposite sign to P | 45 |

**Worked example — BAYU (Bayu Buana, row 55):** P = +110,806.5, Q = −102,380.95. The average is **+4,212.77** — a number 26× smaller than either input and of arbitrary sign. That average is then divided into `BZ`, so a rounding-scale artefact becomes the denominator of an intrinsic value. ASGR (Astra Graphia): P = +321,724.2, Q = −238,297.9, average +41,713.2. AALI itself disagrees by 20 % (1,888,290 vs 2,270,538).

Averaging is not defensible when the two estimates disagree on whether the company makes money at all. The Q derivation is also circular for valuation purposes: it is EV ÷ (EV/EBIT), so any EPV built on it is partly just re-deriving the market's own price.

**Concrete fix:** pick one primary (Q, since it comes from the vendor's own EBIT) with P as a sanity check, and add a `EBIT_Disagreement = ABS(P-Q)/ABS((P+Q)/2)` gate that blanks the valuation when it exceeds ~25 %, and blanks unconditionally when `SIGN(P)<>SIGN(Q)`. Never build a valuation on a negative or near-zero EBIT.

---

### B-13 — High — Peer groups are partitioned by label string, producing self-referential medians

`CQ` picks a granularity level: 1 if the 4-token group (H) has ≥4 members per `Peers data comparison!D`, else 2 if the 3-token group (I) has ≥4 per `!J`, else **3 — with no size check at all**. `BO = SWITCH(CQ, 1,H, 2,I, 3,J)`. `BP`/`BQ` then take `MEDIAN(FILTER(AR, BO = pg, AR>0, CM=TRUE))`.

The filter matches on `BO = pg`. So a company that fell through to level 3 is only compared to *other companies that also fell through to level 3* — not to its sector.

**Worked example — SAMF (Saraswanti Anugerah Makmur, row 654).** SAMF's subindustry is "Agricultural Chemicals" and it is the only one, so it falls to CQ = 3 and BO = `"Basic Materials | Chemicals"`. **There are 34 Basic Materials | Chemicals companies in the universe** — but 33 of them resolved at level 1, so their BO strings are the 4-token variants and the FILTER does not see them. SAMF's peer group therefore has exactly one member: itself.

```
BP (peer PE median)      = 11.87  = SAMF's own AR
BQ (peer EV/EBIT median) =  8.94  = SAMF's own AU
BS (PE implied price)    = 308.03   vs market price K = 308
BY (comparables MOS)     = +0.0086 %
```

A pure tautology dressed up as a relative valuation. The same holds for CMRY (BY = +0.017 %) and APEX. **3 groups have exactly 1 member; 21 groups have fewer than 4; 43 of the 92 rows at CQ=2/3 sit in a sub-4 group.**

**Worked example of the opposite failure — ASII (Astra International, row 41).** Peer group `"Industrials | Multi-sector Holdings | Multi-sector Holdings | Multi-sector Holdings"` has 2 members: ASII (EV/EBIT 10.23) and BNBR (EV/EBIT **522.32**). Median of two = **266.275**. ASII's implied EV price BW = **249,684.68 IDR/share** against a market price of 7,000. It is only masked because BX takes the min and falls back to BS — and BS is itself self-referential (BNBR's PE is negative and gets filtered out, leaving BP = ASII's own 8.67, giving BS = 6,996.60 ≈ the market price, BY = −0.05 %).

**Concrete fix:** (a) add a size check at level 3 and a level-2 (sector-only) fallback with its own count table; (b) exclude the subject company from its own median — `FILTER(AR, sectorKey=mySectorKey, ticker<>myTicker, AR>0)`; (c) match on a stable sector key (e.g. column D&E) rather than the resolved BO label, so all members of a sector see each other; (d) blank BP/BQ when the surviving peer count is < 4 and surface that count in a visible column.

*Checked and correct within this bug:* the `AR>0` / `AU>0` filters **do** keep negative-multiple peers out of the medians. Negative-EBIT peers do not pollute them.

---

### B-14 — High — The AI layer reads the wrong column, is only 46 % populated, and is internally inconsistent

**Which column is read.** CE holds hardcoded JSON on 315 rows. CF holds the live `GEMINI()` formula. CG:CL and CN:CP all regex against **`$CF`**. A scan of every formula in the workbook finds **0 references to column CE**. The 315 hand-pasted reviews are entirely inert.

That is probably not the intent: CF is the volatile column (a live model call that re-runs and returns different text each recalculation), CE is the frozen snapshot. Scoring off CF means the scores are non-reproducible; scoring off CE means they are stale. Neither is currently a deliberate choice — the sheet just reads whichever one the formula happened to name.

**Coverage.**

| column | non-empty of 956 |
|---|---|
| CE (hardcode, unused) | 315 |
| CF (live, read) | 539 — of which **414 valid JSON, 78 outright refusals ("I'm still learning and can't help with that"), 417 blank** |
| CG:CL (scores) | 442 |
| CN (Core Business Driver) | **129** |

**Worked example — AALI (row 4).** CF4's cached value is the literal string `"I'm still learning and can't help with that. Do you need help with anything else?"`. Every one of CG4:CL4 and CO4:CP4 is therefore blank, while CE4 contains a complete, usable review that the sheet ignores.

**Row contamination.** CF5 sits on ABBA's row and its formula argument is `CD5` (ABBA's data pack). Its cached value reads: *"**AALI** shows strong operational quality with a Piotroski F Score of 9 and an extremely low EV/EBITDA of 3.0…"* — with scores governance 2, earnings quality 2, confidence 5. Those are AALI's numbers (ABBA's own F-Score is 6 and its EV/EBITDA is 10.1). CO5 and CG5:CL5 propagate them. Meanwhile CE5 — the ignored hardcode — correctly describes ABBA as distressed with 0s across the board. So ABBA is currently scored with another company's review.

**Two prompt versions in one column.** 129 CF cells carry a prompt that requests `core_business_summary` and `upside_or_downside`; **399 carry an older prompt that does not**. That is exactly why CN is populated on 129 rows and empty on the rest. The prompts also differ in scoring guidance (the newer one drops the explicit 0/1/2 rubric definitions), so the CG:CL scores are not on a common scale across rows.

**Stale hardcodes.** CE4 asserts *"negative Core MOS (-0.287) and low returns (ROIC 0.0411)"*. The sheet's live values are CC = −0.4585 and AJ = 0.0622. The hardcode was pasted from an earlier data vintage.

**Also.** The CF prompt instructs the model to check "Altman Z … if provided". `RAW_key_statistics` column 31 holds `Altman Z-Score (Modified)` — but it is never pulled into Universe, so it is never in the CD data pack. The prompt asks about a field that is structurally absent.

**Concrete fix:** decide explicitly — for a reproducible screener, run CF once, paste-special the JSON into CE, and point CG:CL at `$CE`. Regenerate all 956 rows with a single prompt version. Add `IF(NOT(ISNUMBER(SEARCH("moat_score",CF4))), "REVIEW_FAILED", …)` so refusals are visible rather than silently blank. Pull Altman Z into the Universe columns if the prompt is going to ask about it.

---

### B-15 — High — Piotroski is imported, not computed, and cannot be checked

`BD = XLOOKUP($A4:$A960, keyStats[Ticker], keyStats[Piotroski F-Score], "")`. Distribution across 956 rows: 0→1, 1→3, 2→61, 3→96, 4→159, 5→187, 6→204, 7→144, 8→69, 9→32.

**Why it can't be verified.** The full 9-point F-Score needs **prior-year** ROA, leverage, current ratio, share count, gross margin and asset turnover. The workbook holds only current-period values plus three YoY *growth* rates (AN, AO, AP). Six of the nine signals are unreconstructable from anything in this file. There is no way to know whether the vendor uses Piotroski's original definitions, a modified variant, or which fiscal periods it compares.

**Observable inconsistencies.** 23 rows carry F ≥ 7 while ROA, Net Income or CFO is negative in the same row. Example — **HERO (DFI Retail Nusantara, row 197):** F = 7, Net Income (S) = +119,000 mio, ROA (AG) = **−2.65 %**. Net income and ROA cannot have opposite signs; per B-01, HERO's true net income is negative, which means the "positive net income" and "positive ROA" points must both fail and F ≤ 7 is only barely reachable. Whatever the vendor computed, it was not computed from the numbers this sheet displays.

**Risk.** The value of the F-Score in this framework is as the *quality* gate that stops cheapness alone from producing a BUY (intent item 7). Outsourcing it to an unauditable third-party integer, sourced from the same feed that has sign errors on 30 % of rows, is the single weakest link in that gate.

**Concrete fix:** scrape prior-year balance sheet and income statement, compute all 9 signals in-sheet as visible sub-columns, and keep the vendor figure alongside as a cross-check with a variance flag.

---

### B-16 — Medium — The `<1` sign hack makes the "Match?" check structurally unpassable

The algebra is right: CA = CL × CR and WC = CA − CL, so CL = WC/(CR−1) and CA = CL × CR. AD and AC implement exactly that.

The problem is the hack that compensates for B-01:

```
AD = IF(CR < 1, -ABS(WC), WC) / (CR - 1) / 1e6
AA = AC - AD
AB = (Z = AA)
```

When CR < 1 the numerator is forced to −|WC| and the denominator (CR−1) is negative, so AD is positive (correct) — but then `AA = AC − AD = AD×CR − AD = AD×(CR−1) = −|WC|`, i.e. **AA is always the negative of Z**. Since Z is unsigned (B-01) and positive, `Z = AA` is **guaranteed FALSE** for every CR < 1 company.

**Worked examples.**

*AIMS (row 959):* CR = 0.24, Z = 2,000. AD = −2,000/(0.24−1) = **2,631.58**; AC = 2,631.58 × 0.24 = **631.58**; AA = 631.58 − 2,631.58 = **−2,000**. AB = FALSE.
*ABBA (row 5):* CR = 0.53, Z = 100,000. AD = 212,765.96, AC = 112,765.96, AA = **−100,000**. AB = FALSE.

**Counts:** AB is FALSE on **297 of 956 rows**. All **290 CR<1 rows** are FALSE by construction (192 of them exact sign flips; the other 98 have a blank Z from the `=0→""` idiom). Only 7 FALSEs are genuine anomalies. There are **zero** floating-point near-misses — `=` exact comparison is not the problem here, the sign hack is.

Note the reconstruction itself is sound and should be kept: AC and AD are the *more* trustworthy figures. It is AA and AB that are broken.

**Concrete fix:** `AA = AC - AD` is fine; the comparator should be `AB = IF(OR(Z="",AA=""),"", ABS(ABS(Z)-ABS(AA)) <= 0.005*ABS(AA))` — compare magnitudes with a tolerance, and add a separate `WC Sign Conflict?` column = `AND(Z>0, CR<1)` so the 192 genuine feed errors are surfaced instead of drowned in 290 false alarms.

---

### B-17 — Medium — DDM: shadow parameters, D₀ instead of D₁, and a k−g floor that is only safe by accident

```
BJ (growth)  = clamp( IF(AO<>"",AO,AN), 0, $BJ$1 )      BJ1 = 0.07  (literal)
BL (CoE)     = MIN( BL1 + 0.03*MIN(BK,1), 0.18 )        BL1 = 0.12  (literal)
BM (value)   = IF(BL-BJ = 0, "", BH/(BL-BJ))
```

1. **Shadow parameters.** BJ1 = 0.07 and BL1 = 0.12 are literals typed into row 1 of the Universe sheet. `Setup!C5` (WACC 0.12) and `Setup!C7` (Risk Free 0.065) are not consulted. A user editing Setup will change nothing (B-06). The `0.03` leverage slope and the `0.18` cap are hardcoded inside the formula body.
2. **D₀ not D₁.** Gordon is V = D₁/(k−g) = D₀(1+g)/(k−g). The sheet uses D₀. AALI: BH = 307, BL = 0.12628, BJ = 0.07 → 307/0.05628 = **5,454.99** (matches cached BM4). Correct would be 307 × 1.07 / 0.05628 = **5,836.84**, a 7 % understatement. Systematic across all 369 dividend payers.
3. **The k−g floor is safe today only because of B-02.** The clamp guarantees g ≤ 0.07, and BL ≥ 0.12 — but *only because BK ≥ 0 on every row*, which is true only because net debt is unsigned. Verified: BK minimum = **0.0**, BL minimum = **0.12**, minimum spread = **0.05**, zero rows with a negative or near-zero denominator. **The moment B-02 is fixed, 299 net-cash companies get a negative BK.** With BK = −2, BL = 0.12 − 0.06 = 0.06 < g = 0.07 → negative denominator → negative "intrinsic value". The guard `IF(BL-BJ = 0, "", …)` tests for *exactly* zero, which floating point will essentially never hit; it does not catch negative or near-zero.
4. Also: `IF(BK>1,1,BK)` caps the leverage adjustment upward but has no floor.

**Concrete fix (apply together with B-02):**
`BL = MEDIAN(Risk_Free_ID + 0.05, MIN(BL_base + 0.03*MEDIAN(-0.5, BK, 1), 0.18), 0.18)` — i.e. floor the leverage input at −0.5 and floor the whole cost of equity above the risk-free rate — and `BM = IF(OR(BH="", BH<=0, BL-BJ < 0.02), "", BH*(1+BJ)/(BL-BJ))`.

---

### B-18 — Medium — BX mixes two incompatible price estimates and silently degrades

```
BX = IF((BS<0)*(BW<0), "", IF(BS<0, BW, IF(BW<0, BS, MIN(BS,BW))))
```

`BS` is an equity-multiple price (peer PE × own EPS). `BW` is an EV-multiple price (peer EV/EBIT × avg EBIT, less net debt, ÷ shares). Taking the minimum of the two treats them as interchangeable draws from one distribution. Where both are positive (547 rows) they disagree by more than 2× in **164 rows**.

**Silent single-leg fallback.** BS is blank on 352 rows (BR filters out non-positive EPS). Because `"" < 0` is FALSE in Sheets (text sorts above numbers), the formula skips the `BS<0` branch and lands on `MIN(BS,BW)` → returns BW. That is the right answer, but nothing records that only one leg was used. **62 rows are priced on the EV/EBIT leg alone and 3 on the PE leg alone**, indistinguishable in the output from the 601 rows where both agreed.

**Worked example — UCID (Uni-Charm, row 641):** BS = 281.65 (PE leg), BW = **−619.31** (EV leg, negative). BX returns 281.65 with no indication that half the evidence pointed to a negative enterprise value. Compare BIPI (row 78): BS blank, BW = 120.24 → BX = 120.24, again unflagged.

And on the 290 rows where both legs fail, BX = `""` → BY = **−1** (B-07).

**Concrete fix:** add a `Legs Used` column (`=IF(ISNUMBER(BS),1,0)+IF(ISNUMBER(BW),1,0)`), require ≥1 explicitly, and prefer a *weighted* or explicitly-chosen estimate over MIN — MIN is only "conservative" if both estimates are equally credible, which B-12 shows they are not.

---

### B-19 — Medium — Column V header is wrong

Header: `Free Cashflows per Share (TTM)`. Formula: `XLOOKUP(..., keyStats[Free cash flow (TTM)])/1e6` — total free cash flow in mio IDR.

**Worked example — AALI:** V4 = **4,362,000** (mio IDR = 4.36 trillion). AALI's actual FCF per share is 4,362,000/1,920 ≈ 2,272 IDR. The value shown is 1,920× too large to be a per-share figure.

The correctly-named source field exists and is unused: `RAW_key_statistics` column 21, `Free Cashflow Per Share (TTM)`. Nothing downstream consumes V today, so the impact is confined to human misreading — but V *is* included in the CD data pack sent to the AI reviewer, labelled "Free Cashflows per Share (TTM); 4362000".

**Concrete fix:** rename the header to `Free Cash Flow (TTM) — mio IDR`, and add a separate per-share column from the field that already exists.

---

### B-20 — Medium — BG is labelled a discount but computes an upside

`BG = (BE − L)/L`. **Worked example — AALI:** (4,846,572 − 14,820,000)/14,820,000 = **−0.67297** (matches cached BG4). That is "market cap is 67 % above NCAV", expressed against price. A discount *to* NCAV is `(BE − L)/BE`, which for AALI is −2.058. Same conflation as B-10. Combined with B-07 it produces values like BBCA's −227.6 % "discount".

**Concrete fix:** rename to `Premium/(Discount) to NCAV vs Price`, or switch to `(BE-L)/BE` and keep the name. Either way, guard the blank case.

---

### B-21 — Medium — The feed is quantised to 1 billion IDR, and genuine zeros are converted to blanks

Every money field in `RAW_key_statistics` is an exact multiple of 1e9 (verified: 100 % of non-null values, minimum non-zero magnitude exactly 1,000,000,000). In the Universe's mio-IDR units, the smallest representable non-zero figure is **1,000**.

**Consequences.** **70 companies have Net Income recorded as exactly 0**; 63 more have |NI| ≤ 3 rounding units, meaning up to ±50 % quantisation error on the earnings that drive their PE, earnings yield and EPV. Example — **APLI (Asiaplast Industries, row 30):** S = 1,000 mio, and the derived P (EBIT) = 24,101 against Q = −2,930. Micro-caps are effectively unvaluable at this resolution.

**Compounding idiom.** Every scraped column uses `IF(x/1e6 = 0, "", x/1e6)`. A genuine zero — 64 companies with zero revenue, 70 with zero net income, 236 with zero total debt, 98 with zero working capital — becomes `""`, which then coerces back to 0 in arithmetic (B-07) but breaks `ISNUMBER`, `MEDIAN` and `RANK` in ways that differ per consumer. Zero and "no data" are not the same fact and this idiom merges them.

**Concrete fix:** replace `IF(x/1e6=0,"",x/1e6)` with `IF(NOT(ISNUMBER(x)), "", x/1e6)`, and add a `Data Resolution Warning` column = `ABS(S) <= 3000` to exclude sub-3-billion-earnings names from the ranking population.

---

### B-22 — Medium — Loss-makers occupy rank slots in the Magic Formula

`AZ`/`BA` use `RANK(value, FILTER(range, CM=TRUE), 0)` over all active rows. **292 rows have a negative earnings yield and still receive an EY rank; 228 have a negative ROC and still receive a ROC rank.** Greenblatt excludes negative-EBIT companies from the universe entirely before ranking.

Because RANK with order 0 is descending, the negatives land at the bottom and do not directly displace the top of the list — the practical harm is that BB scores are drawn from a 956-name population instead of the ~664 that should qualify, so the score scale is inflated and not comparable to a canonical Magic Formula run. It also means a name can rank respectably on one leg while being unrankable on the other (e.g. ABBA: EY rank 766, ROC rank 878, BB = 1,644 — a meaningless composite for a company with negative EBIT on both derivations).

**Concrete fix:** rank over `FILTER(AX, CM=TRUE, AX>0, AY>0, NOT(IsFinancial))` and blank BB for any row failing the eligibility test.

*Checked and correct:* the RANK **direction** is right. Order 0 = descending, so the highest earnings yield gets rank 1 and the header comment "Lower is better" (meaning a lower rank *number*) is accurate. I replicated all 956 AZ values with a descending min-rank in pandas: **0 mismatches**. Same for BA. There are no blank/`""` values leaking into either rank column (AX and AY are numeric on all 956 rows).

---

### B-23 — Medium — 16 columns are dead in Excel

See §4.

---

### B-24 — Low — AW and AX are duplicates

Both are `XLOOKUP($A4:$A960, keyStats[Ticker], keyStats[Earnings Yield (TTM)], "")`. AW is headed "Earnings Yield % (TTM)" under *Valuation Multiples*; AX is headed "Earnings Yield (TTM)" under *Magic Formula*. Identical on all 956 rows (AALI 0.0956 in both). Harmless duplication today; becomes a real hazard once B-03 is fixed, because whoever fixes AX will leave AW showing the old number under a near-identical label.

---

### B-25 — Low — `Active?` is inert

`CM` is the literal `TRUE` on all 956 rows (1 blank at row 960). Every filter built on it — the RANK populations in AZ/BA, the peer medians in BP/BQ — currently excludes nothing. The machinery is correct; it has simply never been exercised, so it is untested. Any bug in the exclusion path would be invisible today.

---

### B-26 — Low — Dead and stale artefacts

- **`TradingView_Scrap`** (857 × 18): referenced by **0** formulas in the workbook.
- **`Peers data comparison`** columns A and B ("Peers PE Median", "Peers EV/EBIT") are headers with no data; only D/E (lvl4 counts) and I/J (lvl3 counts) are used. There is no lvl2 count table, which is what B-13 needs.
- **`CR` (Last Review Date)**: populated on 44 of 956 rows with static timestamps. `CR1` contains the *text* `=NOW()` (a note, not a formula).
- **`Dashboard`** and **`PROCESSOR>>>`** are empty; `INPUT>>>` is 1×2.
- Array-formula spill ranges run to **row 960** while data ends at **959**; `BB` alone runs to 959. Cosmetic today (row 960 is blank) but will misalign if the universe grows.

---

## 3. Setup sheet — every parameter, wired or dead

`Setup!B2` = "IDX Market". Parameters in `B4:C9`, each with a workbook-level named range.

| Setup cell | Parameter | Value | Named range | Referenced by | Status |
|---|---|---|---|---|---|
| C4 | Tax Rate | 0.22 | `Tax_Rate` | **nothing** | **DEAD.** BZ4 hardcodes the literal `0.22`. Values match today by coincidence. |
| C5 | WACC | 0.12 | `WACC_ID` | **nothing** | **DEAD.** No column discounts at WACC. `BL1` holds a separate literal `0.12` used as the *cost of equity* base — a different concept that happens to share the number. |
| C6 | Terminal Growth | 0.03 | `Terminal_Growth_ID` | **nothing** | **DEAD.** No terminal value exists anywhere (no DCF — see B-08). The literal `0.03` appears in BL4 as a leverage-premium slope, unrelated to growth. |
| C7 | Risk Free Rate | 0.065 | `Risk_Free_ID` | **nothing** | **DEAD.** The value 0.065 appears in no formula in the workbook. The cost of equity starts from BL1 = 0.12 with no risk-free build-up. |
| C8 | MOS Buy | 0.30 | `MOS_Buy` | **nothing** | **DEAD.** No formula compares any MOS against a threshold. CS is hand-typed. |
| C9 | MOS Watch | 0.10 | `MOS_Watch` | **nothing** | **DEAD.** As above. |

**Verification method:** regex scan of every cell in all 11 worksheets (formula strings, ArrayFormula `.text`, and the inner argument of every `__xludf.DUMMYFUNCTION`) for the literal `Setup` → **0 hits**; and for each of the six named-range identifiers → **0 hits each**.

**Every parameter the user believes is driving the model is actually a decoration.** The real parameters are:

| Real driver | Location | Value | Used by |
|---|---|---|---|
| DDM growth cap | `Universe!BJ1` (literal) | 0.07 | BJ4 |
| Cost of equity base | `Universe!BL1` (literal) | 0.12 | BL4 |
| Leverage premium slope | inside BL4 (literal) | 0.03 | BL4 |
| Cost of equity cap | inside BL4 (literal) | 0.18 | BL4 |
| Tax rate | inside BZ4 (literal) | 0.22 | BZ4 |
| Peer group min size | `Peers data comparison`, via CQ4 | 4 | CQ4 |
| 2/3 Graham factor | — | **absent** | — |

---

## 4. Excel portability

### Dead in Excel: 16 of 97 columns

These columns were exported as `=IFERROR(__xludf.DUMMYFUNCTION("<real formula>"), <cached value>)`. In Excel the `__xludf.DUMMYFUNCTION` name does not resolve, `IFERROR` swallows the `#NAME?`, and the cell returns a **frozen literal**. The formula is gone — it will never recalculate, and refreshing the raw data will silently leave these columns showing last quarter's answers.

| Column | Header | Google-only construct |
|---|---|---|
| **A** | Ticker | `UNIQUE(FILTER(...))` |
| **AZ** | Rank EY | `ARRAYFORMULA` + `FILTER` inside `RANK` |
| **BA** | Rank ROC | `ARRAYFORMULA` + `FILTER` inside `RANK` |
| **BP** | Peer PE Median | `ARRAYFORMULA` + `MAP`/`LAMBDA` + `FILTER` |
| **BQ** | Peer EV/EBIT Median | `ARRAYFORMULA` + `MAP`/`LAMBDA` + `FILTER` |
| **CD** | AI Pack Per Range Row | `LET` + `BYCOL` + `LAMBDA` + `TEXTJOIN` + `TO_TEXT` + `XMATCH` |
| **CF** | Gemini Review — JSON FORMULA | `GEMINI()` |
| **CG** | MOAT Score | `REGEXEXTRACT` |
| **CH** | Governance Score | `REGEXEXTRACT` |
| **CI** | Earnings Quality Score | `REGEXEXTRACT` |
| **CJ** | Cyclicality Score | `REGEXEXTRACT` |
| **CK** | Redflag Score | `REGEXEXTRACT` |
| **CL** | Confidence Score | `REGEXEXTRACT` |
| **CN** | Core Business Driver | `REGEXEXTRACT` |
| **CO** | Summary Thesis | `REGEXEXTRACT` |
| **CP** | Key Risk | `REGEXEXTRACT` + `REGEXREPLACE` + `TEXTJOIN` |

**16 dead columns × ~956 rows = 14,754 dead cells** (counted directly).

The damage is concentrated: **the entire Magic Formula ranking (AZ, BA — and therefore BB, which depends on them), the entire comparables peer-median layer (BP, BQ — and therefore BS, BT, BW, BX, BY), and the entire AI scoring layer (CD–CP)** are frozen. Only the raw pulls and the arithmetic derivations survive an Excel round-trip.

### Construct inventory (by number of columns using it)

| Construct | Columns | Excel status |
|---|---|---|
| `XLOOKUP` with table-name syntax `keyStats[...]` | 50 | **Fine** — Excel 365 supports both. The `idx_stocks` table is a real xlsx table (`A1:T957`); `keyStats`, `Ticker` etc. resolve via structured references. |
| `GEMINI()` | 1 (CF) | **Impossible** — no Excel equivalent. Needs Copilot, a UDF, or an out-of-band pipeline. |
| `REGEXEXTRACT` / `REGEXREPLACE` | 9 / 1 | **Rewrite required** — Excel 365 has `TEXTAFTER`/`TEXTBEFORE`, or the new `REGEXEXTRACT` in current Insider builds only. |
| `FILTER` | 5 | Fine in Excel 365, but the dead stubs must be retyped by hand. |
| `MAP` / `LAMBDA` / `BYCOL` / `LET` | 2 / 3 / 1 / 1 | Fine in Excel 365; dead stubs must be retyped. |
| `TEXTJOIN` | 2 | Fine. |
| `UNIQUE` | 1 | Fine in Excel 365; dead stub. |
| `ARRAYFORMULA` | 4 | **No Excel equivalent** — must be dropped; Excel 365 spills natively. |
| `SWITCH`, `XMATCH`, `TO_TEXT` | 1 each | `SWITCH`/`XMATCH` fine; `TO_TEXT` → `TEXT(x,"@")`. |
| Single-cell array formulas spilling `X4:X960` | 73 | Fine in Excel 365 (dynamic arrays); **broken in Excel 2019 and earlier**. |

**Bottom line on portability:** this workbook is a Google Sheets application. In Excel 365 roughly 76 columns keep working, 16 become frozen constants that must be retyped from the `DUMMYFUNCTION` argument strings, and one (CF) cannot be reproduced at all. In Excel 2019 or earlier, essentially nothing works.

---

## 5. Checked and correct

Things that look suspicious but verify clean. Worth recording so they are not "fixed" into breakage:

1. **RANK direction (AZ, BA).** `RANK(x, range, 0)` is descending, so the highest earnings yield and highest ROC each get rank 1, and "lower is better" refers to the rank *number*. Correct. I replicated all 956 AZ and BA values with a descending min-rank — **0 mismatches**.
2. **No `""` leaks into the rank columns.** AX and AY are numeric on all 956 rows; `IFERROR` around RANK never fires; BB has no blanks and no spurious zeros. The `""`-to-0 hazard (B-07) is real elsewhere but does **not** affect the Magic Formula ranks.
3. **BE uses TOTAL liabilities, not current liabilities.** `BE = AC − X`, and X is `keyStats[Total Liabilities (Quarter)]`. This matches Graham's definition exactly. (Its inputs are corrupted by B-01/B-07, but the formula's intent is right.)
4. **NCAV unit consistency.** L (Market Cap) and BE (NCAV) are both in mio IDR. AALI: L = 14,820,000 mio vs BE = 4,846,572 mio — same scale. `BF = L < BE` is a valid comparison. No mio/raw-IDR mismatch here. Confirmed against the raw feed (Market Cap 14.82e12 IDR ÷ 1e6 = 14,820,000).
5. **The AC/AD back-solve algebra is correct.** CL = WC/(CR−1), CA = CL × CR. Verified on AALI: CR = 2.73, WC = 5,774,000 → AD = 3,337,572.25, AC = 9,111,572.25, AC − AD = 5,774,000 = Z exactly. AD is never negative (0 rows) and AC is never negative (0 rows). AC and AD are the *more* reliable pair; AA and AB are the broken outputs (B-16).
6. **Peer medians already exclude negative multiples.** `FILTER($AR, ..., $AR>0, ...)` and `FILTER($AU, ..., $AU>0, ...)`. Negative-PE and negative-EV/EBIT peers do **not** pollute BP or BQ. (BNBR's −219.8 PE is correctly excluded from ASII's median; its +522.32 EV/EBIT is not excluded because it is positive — but that is an outlier problem, not a sign problem.)
7. **The EPV net-debt bridge has the right sign convention.** `CA = BZ − BU` is correct *given a correctly signed BU*. The bug is in BU's contents (B-02), not in this formula.
8. **The DDM growth clamp works as designed.** BJ correctly floors at 0 and caps at BJ1 = 0.07 — verified, BJ ∈ [0, 0.07] on all rows, prefers Gross Profit growth (AO) with Revenue growth (AN) as fallback.
9. **The cost-of-equity cap works.** BL is capped at 0.18 and never exceeds it; the `IF(BK>1,1,BK)` upper clamp fires correctly.
10. **`BR` correctly screens out negative EPS** before computing the PE-implied price, so BS never reflects a negative-earnings PE multiple. 604 rows priced, 352 correctly blank.
11. **`BX`'s handling of the blank-BS case happens to be right.** Because `"" < 0` is FALSE in Sheets, the formula falls through to `MIN(BS,BW)` and — again because text sorts above numbers — returns BW. The right answer, reached by accident; it should be made explicit (B-18).
12. **No mio/raw-IDR unit mixing found anywhere.** I checked every arithmetic combination in A–CC. All money columns are consistently `/1e6`; K (price), N (shares, mio) and the per-share divisions (`BV/N`, `CA/N`) are dimensionally correct: mio-IDR ÷ mio-shares = IDR/share. AALI: 8,005,151 mio ÷ 1,920 mio sh = 4,169 IDR/share. The only labelling failure is column V (B-19), which is a header error, not a unit error in a calculation.

---

## 6. Suggested fix order

1. **B-01 / B-02** — restore signs in the Universe layer. Nothing downstream can be trusted until this is done, and several other bugs (B-11, B-16, B-22) partly evaporate once it is.
2. **B-17 item 3** — add the k−g floor *in the same change*, because fixing B-02 is what will expose it.
3. **B-06** — wire the Setup named ranges into BJ1, BL1, BZ4. Cheap, and makes every later parameter change safe.
4. **B-03 / B-04** — make the Magic Formula actually Greenblatt's, then B-22.
5. **B-07** — replace the `""` guards, which also fixes the fake −100 % MOS readings across BN/BY/CC.
6. **B-09** — add the financial-sector gate before anyone acts on a bank's NCAV.
7. **B-05 / B-12** — EPV discount rate and the EBIT reconciliation gate.
8. **B-10 / B-11** — the definitional fixes (MOS vs upside, the 2/3 factor).
9. **B-13 / B-14 / B-15** — peers, AI layer, Piotroski.
10. **B-08** — build the classification engine last, once its inputs are trustworthy.
