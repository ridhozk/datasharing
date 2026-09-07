# ERAA — Valuation & Model Validation

*Agent 2 of Stage-2 research pipeline. FACT / INFERENCE / THESIS / ASSUMPTION labelled throughout.*

## PRIORITY 1 — Testing the working-capital hypothesis

**Verdict: hypothesis CONFIRMED at the code level, and PARTIALLY CONFIRMED at the
valuation-impact level.** The DCF is structurally missing a working-capital term —
but adding one back does not, by itself, get the DCF anywhere near a defensible
number. A second, larger flaw (the terminal-value spread) is doing more damage.

### Code confirmation (FACT)

Read `idx_picker/scraper/scoring.py:266-303` and `idx_picker/scraper/metrics.py:704-739`.
`build_scenarios()` constructs `fcf_base` as:

```
fcf_base = normalised_EBIT × (1 − tax_rate) + depreciation + normalised_capex
```

(`depreciation = core.ebitda_ttm − core.ebit_ttm`, `normalised_capex` is negative).
This `fcf_base` is then grown at `growth_stage1` (clamped historical revenue CAGR)
for 5 years and terminalised in `dcf_per_share()`. **There is no working-capital
line anywhere in this path** — no `ΔNWC`, no inventory/receivables/payables term,
nothing. Growth is treated as costing only capex. Confirmed by grep across
`metrics.py` and `scoring.py`: `working_capital` appears only in `CoreFinancials`,
Altman Z, and Greenblatt ROC — never in the DCF.

### ERAA's actual working-capital behaviour (FACT, from ERAA.md annual history)

Net working capital (Inventory + AR − AP), IDR bn:
| Year | Revenue | Inventory | AR | AP | NWC | NWC/Revenue |
|---|---|---|---|---|---|---|
| 2022 | 49,471.5 | 6,064.7 | 1,054.8 | 2,400.8 | 4,718.7 | 9.54% |
| 2023 | 60,139.4 | 8,046.6 | 1,364.8 | 3,671.4 | 5,740.0 | 9.54% |
| 2024 | 65,279.7 | 7,130.9 | 1,156.5 | 3,869.9 | 4,417.5 | 6.77% |
| 2025 | 76,606.9 | 11,644.7 | 1,512.2 | 5,964.9 | 7,192.0 | 9.39% |

Cash conversion cycle (FACT, computed from the same table): DIO ≈50–62 days,
DSO ≈6–8 days, DPO ≈20–32 days → **CCC ≈27–38 days**, consistent with the
screener's own quarterly CCC of 38.3 days. NWC/Revenue sits at **~9.5% in three
of the four years**; 2024 is the outlier (a destocking year — inventory fell
IDR 916bn even as revenue rose 8.6%, which is why 2024 is the only year with
positive FCF, +1,316.9bn). 2025 reversed that hard: inventory jumped +63.3%
(7,130.9 → 11,644.7bn) against only +17.4% revenue growth, consuming
+2,774.5bn of cash in NWC alone and producing FCF of −679.5bn. TTM FCF yield is
−32.4% and TTM FCF is −2,380.9bn against a market cap of only 7,352bn — a
company financing roughly a third of its market cap's worth of cash burn per
year, currently funded by debt (total debt rose 8,638.5→7,980.8bn choppy but
net debt is 6,668.4bn, D/E 0.84, and external sourcing (INFERENCE, weak
evidence) shows total D/E climbing from ~29% to ~80-99% over five years —
i.e. **growth has been financed by rising leverage, not free cash flow**, exactly
what a DCF with no WC drag would fail to price.

**INFERENCE (moderate confidence):** the 2025 inventory spike coincides with
public statements from Erajaya about deliberately holding more smartphone stock
to protect supply and pricing against Rupiah weakness/import-cost risk
("Erajaya jaga stok smartphone di tengah pelemahan Rupiah" — Bisnis.com, May
2026). That is a plausible, non-value-destroying reason for elevated inventory,
but it does not change the cash-flow fact: the stock sat on the balance sheet as
cash-consuming inventory in 2025, and any DCF that grows the P&L at 15%/year
without charging for that buildup is fabricating free cash flow.

### Quantified impact — reconstructing the DCF with an explicit WC term

I rebuilt the base-case DCF by hand using the model's own inputs (verified my
reconstruction reproduces the reported IV Base of 2,736.8 to within rounding —
`fcf_base` ≈ IDR 2,678bn, wacc 12%, terminal growth 3%, growth 15% clamped,
net debt 6,668.4bn, shares 15.642bn — confirms I have the mechanism right).
I then added `ΔNWC = ΔRevenue × 9.5%` (the historical steady-state ratio,
excluding the 2024 destocking outlier) as an explicit outflow each forecast year:

| | Original DCF (no WC term) | WC-corrected DCF |
|---|---|---|
| IV Base | **2,736.8** | **≈1,617** |
| Change | — | **−41%** |

**So: yes, the missing WC term is real and material — it overstates the base-case
DCF by roughly 40%.** But even corrected, ≈1,617/share is still **3.4× the
current price (470)** and far above the sell-side consensus target of ~566
(range 450–680, see Priority 3). **The WC omission alone does not explain why
the DCF is wrong by 3–8×** — a second flaw does most of the remaining damage:
the terminal value (wacc 12% − terminal g 3% = a 9-point spread, i.e. an implied
terminal multiple of ~11× FCF) accounts for **~70% of total PV in both the
original and the WC-corrected DCF**. For a distribution business with ROIC
~10% (barely above its own cost of capital) and a business model that consumes
cash to grow, capitalising 15%-then-3% growth forever at an 11× terminal
multiple is the dominant source of overvaluation, not just the missing WC line.

**Conclusion for the wider screener:** this is a real, generalisable bug. Any
working-capital-intensive distributor/retailer in the universe with growing
inventory will have its DCF overstated by the missing WC term — this
project should add `ΔNWC = ΔRevenue × NWC/Revenue(normalised)` to
`build_scenarios()`. But the WC fix alone is not sufficient; the terminal
wacc−g spread also needs tightening (or a fade-to-ROIC-at-cost-of-capital
terminal assumption) for capital-intensive growth names generally.

## PRIORITY 2 — Proper valuation

### Multiples cross-check (the more defensible lens for this business type)

- **ERAA's own TTM EV/EBIT (7.33x) is already close to the peer median
  (7.65x, 12 Consumer Cyclicals/Specialty Retail peers)** — i.e., on a
  trailing basis the market is *not* mispricing ERAA relative to peers. The
  cheap P/E (4.7x) coexists with a roughly fair EV/EBIT because **leverage**
  is doing the work: net debt of 6,668bn is 91% of market cap, so the same
  enterprise value splits into a small, levered equity slice. This is a
  leverage/risk story, not a "hidden bargain vs peers" story.
- Applying the peer-median EV/EBIT (7.65x) to **TTM EBIT** (≈2,114bn, derived
  from OperatingIncome, consistent with the "EBIT from OperatingIncome"
  convention noted in ERAA.md) less net debt (6,668.4bn), divided by shares
  (15.642bn): **≈ IDR 607/share.**
- Applying the same multiple to **normalised (5-yr median) EBIT** (1,590.6bn,
  the more conservative, cycle-smoothed base) gives: **≈ IDR 352/share.**
- These two bracket the current price (470) and closely bracket the sell-side
  12-month consensus target (**average IDR 566, range 450–680, 7 analysts,
  "Strong Buy" per aggregator data** — WebSearch, unverified primary source,
  moderate confidence) — a much better external sanity check than the
  screener's own 2,737–3,979 DCF range.
- **Sum-of-the-parts (INSUFFICIENT EVIDENCE — requires further research):** I
  could not obtain segment-level EBIT/margin splits for iBox/Apple premium
  retail vs. Android/commodity distribution vs. F&B/beauty from the sources
  available in this pass. Given iBox commands >180 stores and is described as
  Indonesia's largest Apple reseller with premium-format expansion
  (stand-alone APP stores, Plaza Indonesia flagship), it plausibly deserves a
  higher multiple than commodity distribution, which would modestly lift a
  proper SOTP value above the blended EV/EBIT figure above — but this is
  THESIS, not quantified.

### Bear / Base / Bull (explicit assumptions)

| Case | EBIT basis | Multiple | Rationale |
|---|---|---|---|
| **Bear** | Normalised EBIT 1,590.6bn | 6.0x (below peer median — leverage/FX/margin stress) | Rupiah weakness raises import costs, margin compresses, multiple de-rates | 
| **Base** | Blend of TTM (2,114bn) and normalised (1,591bn) EBIT | 7.5x (≈ peer median) | Current trading multiple persists, growth continues but working-capital-funded |
| **Bull** | TTM EBIT 2,114bn (iPhone-cycle strength sustained) | 9.0x (re-rating) | Leverage stabilises, iBox premium mix re-rates the whole entity |

Bear: 6.0×1,590.6 − 6,668.4 net debt = 2,875.4bn equity ÷ 15.642bn shares ≈ **IDR 184/share**
Base: 7.5×((2,114+1,591)/2) − 6,668.4 ≈ 6,879 - wait, recompute: 7.5×1,852.3=13,892bn EV −6,668.4=7,224bn ÷15.642 ≈ **IDR 462/share** (essentially at price)
Bull: 9.0×2,113.6 − 6,668.4 = 12,354bn ÷ 15.642 ≈ **IDR 790/share**

(These are hand-built cross-checks against the screener's own peer-comp
engine, not a re-run of the pipeline; screener's own `Comparables IV` output
was 894.5, in the same order of magnitude as this bull case, for reference.)

## PRIORITY 3 — Is PE 4.7x / PB 0.78x real cheapness?

- ROE 16.45% (TTM) vs **ROIC only 9.9%** — the gap is leverage. DuPont: net
  margin 1.6% × asset turnover 2.94x × equity multiplier 3.16x ≈ 14.9%,
  consistent with the reported ROE. **A meaningful share of the "attractive"
  ROE is financial leverage, not operating economics** (ROIC ~10% is only
  modestly above WACC, i.e. barely economic-profit-positive).
- Interest coverage is thin (3.43x) and net debt/TTM EBITDA ≈1.5x — not
  distressed, but rising fast: external sources put total D/E climbing from
  ~29% to ~80-99% over five years (WebSearch, moderate confidence, not
  independently re-derived from the balance sheet history above but directionally
  consistent with TotalDebt rising from 4,833bn(2022)→9,400bn(2025) against
  equity growing much more slowly, 6,742bn→9,142bn).
- Justified P/B via Gordon (ROE 16.45%, g 3%, COE floored at rf+300bp=9.5%
  since beta 0.338 is far below the [0.5, 2.5] trust band per project
  convention): (0.1645−0.03)/(0.095−0.03) ≈ **2.07x** — well above the actual
  0.78x. On this lens alone ERAA looks cheap, but this uses the leverage-
  inflated ROE as an input; it should not be read at face value.
- **What the market is plausibly pricing in (THESIS):** (1) leverage risk
  from debt-funded, working-capital-hungry growth in a thin-margin (≈11%
  gross, ≈2.6% operating) distribution business; (2) Rupiah/import-cost
  exposure (most product is imported); (3) growth that consumes cash rather
  than generating it, meaning continued expansion likely requires continued
  debt issuance, a real risk given already-thin interest coverage; (4)
  ordinary retail/distribution multiples generally (peer EV/EBIT median 7.65x,
  peer PE median 10.6x — ERAA's own 4.7x PE is *below* peer PE median, which
  is the leverage effect showing up again).
- **Not obviously a classic value trap** — earnings are real, growing (net
  income +63% YoY quarterly, Piotroski F-Score only 4/9 though, flagging
  quality concerns: ROA not improving, accruals negative, current ratio not
  improving, gross margin not improving, asset turnover not improving).
  F-Score of 4 is mediocre, consistent with "growing but not yet
  compounding cleanly."

## Most important assumption

**The terminal-value spread (WACC 12% − terminal growth 3% = 9 points, implying
an ~11x terminal FCF multiple) drives ~70% of the DCF's present value, in both
the original and the WC-corrected version.** This single assumption matters
more than the WC fix itself: even after adding a realistic working-capital
drag, the DCF still overshoots the peer-multiple-based and analyst-consensus
values by ~3x, because it still capitalises perpetual double-digit growth for
a 10%-ROIC distributor at a multiple far above what any comparable actually
trades at (peer EV/EBIT median 7.65x ≈ an 8-9% "terminal cap rate", not 9%
wacc-minus-3%-growth-forever). For the EV/EBIT lens, the second most important
assumption is which EBIT base is used (TTM 2,114bn vs 5-yr normalised
1,591bn) — a 33% swing that alone moves fair value between ~352 and ~607.

---

```
Valuation Score: 30/100
Existing Screener Valuation:
Current Price: 470
Conservative Value: 1,560.7 (screener IV Bear)
Base Value: 2,736.8 (screener IV Base)
Bull Value: 3,978.98 (screener IV Bull)
Appropriate Valuation Method: EV/EBIT vs. distribution/specialty-retail peers (primary), cross-checked with P/E on normalised margins; DCF only usable once an explicit ΔNWC = ΔRevenue × NWC-intensity term is added AND the terminal WACC−g spread is tightened toward the peer-implied terminal multiple (~7.6x EBIT, not ~11x FCF).
Why Existing Valuation May Be Wrong: DCF has no working-capital reinvestment term (confirmed in code, scoring.py:266-303 / metrics.py:704-739) — for a distributor funding growth almost entirely via inventory/receivables (NWC ≈9.5% of revenue, CCC ≈27-38 days), this overstates free cash flow. Quantified: adding the WC term cuts IV Base from 2,736.8 to ≈1,617 (-41%), but a second, larger flaw — an overly generous terminal WACC-minus-growth spread implying an ~11x terminal multiple vs. the sector's observed ~7.6x EV/EBIT — accounts for most of the remaining overstatement.
Valuation Upside: Bear: -61% (≈184) / Base: -2% to 0% (≈352-607, midpoint ≈462-480, roughly at price) / Bull: +68% (≈790)
Margin of Safety: Base case ≈0-15% (essentially none to modest) using peer-multiple valuation; the screener's reported 66% MOS is an artifact of the broken DCF feeding the blended IV and should not be trusted.
Most Important Assumption: The DCF's terminal WACC−terminal-growth spread (9 points → ~11x terminal FCF multiple), which drives ~70% of DCF present value even after correcting for working capital; for the multiples approach, whether TTM (2,114bn) or 5-yr normalised (1,591bn) EBIT is used swings fair value by ~70%.
Valuation Verdict: FAIRLY VALUED
```
