# MOLI — Agent 2: Valuation & Model Validation

*Ticker: MOLI (Madusari Murni Indah Tbk.), IDX. Price IDR 274. Prepared 2026-08-11.*

```
Valuation Score: 48/100
Existing Screener Valuation: Blended IV 300 (DCF 61 / EPV 273 / Comps 719) — internally contradictory, not usable as reported
Current Price: 274
Conservative Value: ~209/share (EBIT reverts below mid-cycle; molasses cost pressure returns, no E5 uplift yet)
Base Value: ~273/share (EPV on 5-yr median EBIT — coincides almost exactly with the screener's own EPV figure)
Bull Value: ~448/share (E5 mandate + new capacity partly ramps; EBIT recovers toward 2023-level ~150bn)
Appropriate Valuation Method: EPV on normalised (median) EBIT, cross-checked against EV/EBITDA on mid-cycle margins and P/B vs ROE. NOT the DCF — see below.
Why Existing Valuation May Be Wrong: Blended IV of 300 averages two broken numbers in opposite directions — a DCF crushed to near-zero by one lumpy growth-capex quarter, and a comps value inflated by applying peer multiples to peak (2.2x mid-cycle) trailing earnings. Their averaging to ~300, close to price 274, is coincidence, not convergence.
Valuation Upside: Bear: -24% / Base: 0% / Bull: +64%
Margin of Safety: Bear: -31% / Base: ~0% / Bull: +39% (MOS = (IV-Price)/IV; Upside = IV/Price-1, per project convention — both shown because they diverge)
Most Important Assumption: Whether the trailing TTM EBIT run-rate (~198bn, 2.2x the 5-yr median) is a durable new earnings level or a transient input-cost (molasses price) windfall that is already reverting. This single call moves EPV per share from ~209 to ~448 — a wider range than any WACC or multiple assumption in the model.
Valuation Verdict: FAIRLY VALUED
```

---

## Priority 1 — Diagnosing the DCF-vs-blend contradiction (FACT-grounded, verified against source code)

**Method.** Read `idx_picker/scraper/metrics.py::dcf_per_share` /
`scoring.py::build_scenarios` and `scoring.py::blended_intrinsic`, then ran the
pipeline against the cached MOLI bundle (`--cache-ttl -1 --tickers MOLI`) with
temporary debug prints (reverted afterward, no permanent code change; verified
`git diff` clean and output CSVs restored via `git checkout`) to capture the
exact numbers the DCF consumes.

**FACT — the DCF is not driven by raw trailing FCF or primarily by the growth
rate, contrary to the initial hypothesis.** `build_scenarios` prefers a
normalised-EBIT-derived cash-flow base over `core.fcf_ttm` whenever normalised
EBIT is positive (MOLI's is: IDR 91.49bn). The actual construction:

```
fcf_base = normalised_ebit(91.49bn) × (1 - tax 0.22)      = 71.36bn
         + depreciation (ebitda_ttm 202.64bn - ebit_ttm 198.17bn) = +4.47bn
         + capex_ttm (-74.08bn, capex arrives negative)   = -74.08bn
         -----------------------------------------------------------
         = IDR 1.75bn   (per share: ~IDR 0.64)
```

**FACT — that IDR 1.75bn base is why the DCF collapses.** Post-tax normalised
operating earnings plus depreciation (~75.8bn) are almost exactly offset by
TTM capex (-74.08bn), leaving next to nothing to discount. The growth rate
(base -0.4%, bear -5.4%, bull +3.6%, from Revenue CAGR 3Y) is a secondary
effect — it perturbs an already-near-zero number, so in absolute IDR terms it
barely matters.

**FACT — capex_ttm is dominated by one outsized quarter, not a steady capex
run-rate.** From the quarterly history: capex was -8.1bn, -5.2bn, -12.4bn
across three quarters of 2025, then jumped to **-43.8bn in Q1 2026** (Q2 2026
-12.7bn). That single quarter is nearly double all of FY2025's capex
(-23.9bn). **FACT (news, corroborating):** MOLI announced a **Rp350 billion
2026 capex program** to raise molasses-based ethanol capacity from ~80M to
~100M litres/year via a second distillation train, new liquid-CO2 lines and a
boiler, explicitly to capture the government's E5 mandatory ethanol-blending
mandate starting July 2026 and its role supplying Pertamina in East Java
([bisnis.com](https://market.bisnis.com/read/20260609/192/1979669/molindo-moli-alokasi-capex-rp350-miliar-pacu-kapasitas-etanol),
[antaranews.com](https://www.antaranews.com/berita/5601951/moli-siapkan-capex-rp350-miliar-incar-peluang-program-bioetanol),
[investor.id](https://investor.id/market-and-corporate/300765/madusari-murni-moli-investasi-rp-240-miliar-bangun-pabrik-ke2)).
The Q1 2026 capex spike is that program landing in one quarter — **growth
capex for a step-change in capacity, not maintenance capex for the existing
business.**

**INFERENCE — this is a model-mechanics failure, not a valuation insight.** A
two-stage FCFF DCF with a 5-year explicit window nets *all* capex against
current-year earnings every year, with no distinction between maintenance and
growth spend. For a company whose capex is naturally lumpy (a single
plant-expansion quarter can dwarf a full prior year), and whose market cap
(746bn) is only ~2x the announced multi-year capex program (350bn), this
guarantees the DCF is dominated by capex-timing noise rather than earnings
power in any period where a growth-capex quarter falls inside the trailing
twelve months used as the base.

**FACT — arithmetic decomposition of the DCF "base" IV of 61/share.** Net
cash is IDR 149.13bn (`Net Debt (Quarter)` = -149,125,663,000), or
**IDR 54.75/share** on 2,724,036,608 shares. The DCF's own PV of the (nearly
zero) 5-year explicit cash flows plus terminal value contributes only
~IDR 17.4bn (~**IDR 6.4/share**) before subtracting net debt. So of the
IV-base of 61.13, **~90% is just the balance-sheet net-cash pile passing
through the model**, not any operating valuation. The DCF, as computed here,
is barely more informative than "price ≈ net cash per share plus a token
amount," which is true but adds nothing about the ethanol business.

**FACT — the comparables lens fails in the opposite direction.** `comparables_value` uses
`eps_ttm` and `ebit_ttm` (both **trailing/peak**, not normalised) against peer
medians (peer PE 10.56, peer EV/EBIT 9.13, peer PB 1.62):
- EPS_ttm(43.63) × peer PE(10.56) ≈ 461/share
- EBIT_ttm(198.17bn) × peer EV/EBIT(9.13) + net cash(149.13bn), /shares ≈ **719/share** (dominant candidate, matches reported Comparables IV of 719.27)
- BVPS(470) × peer PB(1.62) ≈ 762/share

Every comps candidate applies a peer multiple to **trailing EBIT/EPS that the
screener's own red flag says is 2.2x mid-cycle**. The comps lens therefore
compounds the peak-earnings problem instead of correcting for it — the
opposite failure mode from the DCF, which under-earns because of one lumpy
capex quarter.

**FACT — the blend arithmetic checks out exactly.** `blended_intrinsic` uses
weights {dcf 0.40, epv 0.35, comps 0.25} for an "Ordinary" business type:
`0.40×61.13 + 0.35×273.05 + 0.25×719.27 = 299.84`, matching the reported
Blended IV of 299.84 to four significant figures.

**Verdict on Priority 1: neither the DCF (59-64) nor the blended IV (300) is
usable as reported.** The DCF is crushed by a single-quarter growth-capex
spike being netted against one year of earnings inside a model with no
maintenance/growth capex split. The comps lens is inflated by applying peer
multiples to un-normalised peak earnings. Their weighted average landing near
the current price (274) is a coincidence of two offsetting errors, not
confirmation of fair value. **EPV per share (273.05)** is the one number in
the screener's own output that is built correctly for this situation — it
uses the same normalised (median) EBIT as the DCF's fcf_base, but as a
perpetuity (`normalised EBIT × (1-tax) / cost of capital − net debt`) rather
than netting one year of lumpy capex against it — and it happens to sit
almost exactly at the current price, which is itself informative (see
Priority 3).

---

## Priority 2 — Is trailing EBIT (2.2x mid-cycle) sustainable?

**FACT.** Normalised EBIT (5-yr median of annual OperatingIncome:
73.5/109.5/55.2/152.0bn for 2022-2025) = IDR 91.49bn. TTM EBIT = IDR 198.17bn.
Ratio 0.462, i.e. trailing is 2.2x the median — the screener's red flag is
arithmetically correct.

**FACT (news/press, H1 2026 results).** Gross margin expanded from **25.43%
in H1 2025 to 32.94% in H1 2026**; COGS *fell* in absolute IDR (Rp535.98bn →
Rp489.99bn, -8.6%) even as revenue rose modestly (+1.65%). Net income surged
~192% YoY in H1 2026 (Q1 2026 net income alone was reported up 240% YoY to
Rp34.43bn)
([depok24jam.com](https://www.depok24jam.com/2026/08/11/madusari-murni-indah-moli-semester-i-2026-laba-melonjak/),
corroborated in the raw quarterly table in `MOLI.md`: EBIT climbs
Q3'25 39.5bn → Q4'25 46.5bn → Q1'26 45.4bn → Q2'26 60.7bn). The margin
expansion is **cost-side**, not price-side.

**FACT — the swing input, molasses (tetes tebu), collapsed and then partially
recovered within the same window.** Molasses (a sugar-mill by-product,
MOLI's primary raw material for molasses-based ethanol) fell from roughly
**Rp1,900/litre to ~Rp1,000/litre around March 2026** (a ~47% crash), driven
by a domestic sugar-market oversupply — 2026 sugar production surplus
estimated at 207,477 tonnes against consumption, with farmer sugar stockpiling
unsold in warehouses (estimated Rp4-7 trillion in farmer losses) as refined
sugar imports flooded the consumer market. By **July 2026, molasses had
partly recovered to roughly Rp1,700-2,000/kg** (source reports mix per-litre
and per-kg units across articles — treat the recovery direction as FACT, the
exact magnitude as **INFERENCE** given the unit inconsistency).

**FACT — ethanol selling price was, if anything, a headwind, not a
tailwind.** In the same capex announcement, MOLI director Jose G. Tan cited
**"pelemahan harga etanol" (ethanol price weakness)** in 2026 as an industry
headwind, alongside domestic oversupply of non-fuel-grade ethanol and
insufficient controls on raw-material exports
([antaranews.com](https://www.antaranews.com/berita/5601951/moli-siapkan-capex-rp350-miliar-incar-peluang-program-bioetanol)).
So the H1 2026 earnings surge is attributable almost entirely to a
**temporary collapse in the molasses input cost, not to stronger ethanol
pricing or volume** — the textbook profile of an unsustainable margin spike
that the screener's peak-earnings flag exists to catch.

**INFERENCE.** Because molasses pricing was already reported recovering by
July 2026 (the most recent data point available), and because ethanol selling
prices are described as soft, the TTM EBIT run-rate (198bn) looks like it
overstates sustainable earnings power. The 5-year median (91.5bn) is the more
defensible "mid-cycle" anchor for a base case.

**THESIS — but the median may itself be a stale floor, not a fair mid-cycle.**
Two developments postdate the 2022-2025 window used to compute the median and
argue the "true" mid-cycle level could be higher going forward:
1. **E5 mandatory ethanol-gasoline blending began July 2026** nationally
   ([cnbcindonesia.com](https://www.cnbcindonesia.com/news/20260703143353-4-747871/ri-sudah-ada-bbm-campuran-tebu-segini-harga-bioetanol-di-juli-2026)),
   with the government setting a **fuel-grade bioethanol reference price of
   Rp10,933/litre effective July 2026**
   ([cnbcindonesia.com](https://www.cnbcindonesia.com/news/20260706124750-4-748363/harga-bioetanol-resmi-naik-jadi-rp10933-liter-berlaku-juli-2026)),
   and government targets fuel-grade ethanol demand reaching **1.2 million
   kilolitres by 2030** as the mandate escalates toward E10 (2028) and E20.
   MOLI has been appointed a Pertamina supplier for East Java.
2. MOLI's Rp350bn capex program (80M → 100M L/yr capacity, phased through
   September 2027) is explicitly built to capture that new demand.

Neither of these had materially hit MOLI's revenue as of the H1 2026 numbers
in hand (E5 only started July 2026, after the reporting period, and the new
plant isn't due until FY2027). **They are optionality for the bull case, not
yet evidence for the base case.**

**Verdict on Priority 2:** current TTM EBIT is very likely overstated as a
sustainable run-rate — it is substantially a molasses-cost windfall that
independent sourcing shows already mean-reverting. The 5-year median
(91.5bn) is the safer base-case anchor today, with the E5 mandate and new
capacity as a distinct, not-yet-delivered bull catalyst for FY2027+.

---

## Priority 3 — Choosing the right framework

**Agreed: DCF is the worst available tool here**, for the mechanical reasons
in Priority 1 (near-zero growth credit, small-cap with lumpy step-function
capex relative to market cap, no maintenance/growth capex split) — it should
be dropped from the blend for this name, or at minimum re-weighted to near
zero, rather than carrying a 40% weight.

**EPV on normalised EBIT (273/share) is the most defensible core lens** — it
is built on the same 5-yr median EBIT discussed above, applied as a
going-concern perpetuity rather than netted against one lumpy capex quarter.
It lands almost exactly on the current price (274), i.e. **on a strict
mid-cycle-earnings, zero-growth-credit basis, MOLI is fairly valued today, not
cheap.**

**Cross-check: EV/EBITDA on mid-cycle earnings.** The screener's reported
EV/EBIT of 4.08x uses TTM (peak) EBIT. Recomputing on normalised EBIT:
EV(807.72bn) / normalised EBIT(91.49bn) ≈ **8.83x** — essentially at the peer
EV/EBIT median of 9.13x, not a statistical outlier. This is the single most
decision-relevant recalibration in this report: **the "EV/EBIT of 4.1x, dirt
cheap" framing only holds if the TTM earnings spike is durable; on a
normalised basis MOLI trades in line with its peer group, not at a discount
to it.**

**Cross-check: P/B (0.58) vs profitability.** Book value/share ≈ 454
(equity 1,237.1bn / 2.724bn shares). PB 0.58 is well below the peer median
1.62, but ROE is modest — 9.3% TTM, and only 4.1% on the 5-year average — a
business earning near or below its cost of equity over time is not obviously
mispriced trading below book; it is a plausible equilibrium. This makes P/B a
supporting data point, not an independent buy signal, consistent with the
"cheapness alone never produces a BUY" rule.

**Replacement value of distillery capacity: Insufficient evidence — requires
further research.** One rough data point: the announced capex implies
~Rp350bn for +20M litres/year of incremental capacity (~Rp17,500 per litre of
annual capacity), but that figure bundles distillation, liquid-CO2 lines, a
boiler and supporting equipment, so it is not a clean per-litre ethanol
replacement-cost comp (ASSUMPTION-level, not independently verified against a
second capex data point or industry benchmark).

**Bear / Base / Bull (EBIT-driven, EPV method), explicit assumptions:**

| Scenario | EBIT basis & rationale | EBIT (IDR bn) | EPV/share* | Upside vs 274 |
|---|---|---|---|---|
| Bear | Molasses cost pressure returns (reversion beyond the partial July 2026 recovery), ethanol pricing stays soft per management commentary, no E5 volume yet — EBIT reverts toward the low end of the historical range (near 2024's 63.4bn actual, discounted further for a renewed cost headwind) | ~70 | ~209 | -24% |
| Base | 5-year median normalised EBIT (screener's own figure) — molasses reverts to a normal mid-cycle cost, E5 optionality not yet delivering | 91.5 | ~273 | 0% |
| Bull | E5 ramps through FY2027, new capacity partly online, molasses stays benign — EBIT recovers toward the better historical print (2023 actual EBIT 156.6bn), rounded down for execution risk on the new plant | ~150 | ~448 | +64% |

*EPV/share scaled linearly off the screener's own EPV formula
(normalised EBIT × (1−0.22) / cost of equity − net debt, /shares), holding
cost of equity and net cash constant across scenarios; only the EBIT input is
varied, per the framework requested.

**Most important assumption:** which EBIT level is the "right" mid-cycle
base — the stale 5-yr median (91.5bn, pre-E5), something between that and the
current TTM peak (198bn), or a step-up once E5 volumes and the new plant
deliver (potentially exceeding all historical prints). This one call spans
EPV/share ~209 to ~448, a wider range than the WACC, terminal-growth, or peer
multiple choices anywhere in the model. Everything else in this report is
secondary to it.

**Liquidity.** Daily traded value ~IDR 306mn (~USD 19k) is very thin. Even at
a "fairly valued, optionality-rich" conclusion, this caps any position to a
small allocation and materially raises the cost of entry/exit versus the
screener's frictionless MOS/upside numbers — a real constraint independent of
the valuation verdict.

---

## Gaps / further research

- Exact ethanol-only sales volume and average selling price (vs the blended
  Ethanol+Fertilizer+CO2 segment revenue) — **insufficient evidence**, no
  segment-level filing was pulled; would sharpen the bear/base/bull EBIT
  scenarios materially.
- Confirmed unit reconciliation for molasses pricing (per-litre vs per-kg
  figures conflict across Indonesian press) — **insufficient evidence**.
- Mechanism for the reported rupiah-depreciation benefit to ethanol producers
  (headline found, source article returned HTTP 403, mechanism unconfirmed:
  export-linked pricing vs import-competing dynamics) — **insufficient
  evidence — requires further research**.
- Historical P/B range for MOLI specifically (only current PB 0.58 vs peer
  median 1.62 was available; no MOLI-specific 5-10yr P/B band was sourced) —
  **insufficient evidence**.
- Independent replacement-cost benchmark for ethanol distillation capacity
  (Rp/litre of annual capacity) beyond the one bundled capex figure —
  **insufficient evidence**.
