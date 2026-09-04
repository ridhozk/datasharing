# BULL — Agent 3: Business & Industry Analysis (DRAFT — in progress)

*PT Buana Lintas Lautan Tbk, IDX: BULL. Price IDR 464, mkt cap ~IDR 7,189bn (~USD 407m).
Reports in USD. Draft written incrementally; will be updated as research proceeds.*

Status: IN PROGRESS — do not treat as final until this line is removed.

---

## 0. Summary verdict (fill in last)

TBD

---

## 1. The fleet

**FACT** (source: Samuel Sekuritas initiation report, 16 April 2026 — Bloomberg
BULL.IJ; and BULL's own Fleets page bull.co.id/fleets). As of 1Q26 BULL operates
**11 owned vessels**:

| Vessel | Type | Shipyard | Build | Age (yrs, at Apr-26) | Size |
|---|---|---|---:|---:|---:|
| MT Silver Tiger | MR tanker | Korea | 2002 | 24 | 37,383 DWT |
| MT Capibara | MR tanker | China | 2004 | 22 | 38,850 DWT |
| MT Silver Phoenix | MR tanker | China | 2001 | 25 | 34,826 DWT |
| MT Wildebeest | MR tanker | China | 2005 | 21 | 34,583 DWT |
| MT Mustang | MR tanker | S. Korea | 2004 | 22 | 37,330 DWT |
| MT Nusa Merdeka | Aframax | S. Korea | 2003 | 23 | 104,875 DWT |
| MT Savir Lion | Aframax | China | 2007 | 19 | 109,672 DWT |
| MT Savir Tiger | Aframax | China | 2008 | 18 | 108,942 DWT |
| MT Gas Natuna | LPG (pressurized) | Japan | 1996 | 30 | 3,213 DWT |
| MT Gas Garuda | LNG carrier | S. Korea | 2004 | 22 | 145,914 CBM |
| MT Gas Polaris | LNG carrier | S. Korea | 2002 | 24 | 140,500 CBM |

Oil tanker sub-fleet (3 Aframax + 5 MR) = **506,461 DWT combined, average age
~22 years**. **FACT — this is an old fleet.** Tanker economic/commercial life is
typically ~20-25 years before scrapping or sale to less-regulated trades
(shadow-fleet buyers); several BULL vessels (Silver Phoenix, Silver Tiger,
Gas Natuna) are already at or past that line. This contradicts any assumption
of a young, recently-renewed fleet — **INFERENCE**: high forward capex is
required just to replace age, not only to grow.

**Fleet vs BULL's own website claim of "32 vessels, 2.4m DWT, 2025":** unresolved
discrepancy — likely reflects a wider corporate group (chartered-in tonnage,
FPSO/FSO units, or historical fleet count including divested vessels) vs. the
11 vessels Samuel's analyst could identify AIS-tracked in April 2026.
**INSUFFICIENT EVIDENCE to reconcile — flagged, not resolved.** The 11-vessel,
506k DWT oil fleet is the figure corroborated by named-vessel tracking data and
should be treated as more reliable for the core tanker business.

**LNG build-out (new, TTM capex driver — answers CLAUDE.md capex question):**
- MT Gas Garuda acquired **Dec-2025** (first LNG carrier)
- MT Gas Polaris acquired **1Q-2026**
- Combined investment for these two: **~USD 60-70m**, funded **75% debt / 25%
  internal cash** (FACT, Samuel report)
- Company guidance: **3 more LNG vessels planned for 2H-2026**, targeting
  total LNG fleet capacity of ~230,000 (units unclear — report says "DWT" but
  LNG vessels are conventionally sized in CBM; likely a units error in the
  broker report — **flagged, not resolved**)
- This directly explains the TTM capex of ~USD 97m / IDR 1,724bn (2.4x TTM
  EBIT) flagged in the fact sheet: **it is predominantly LNG-carrier
  acquisition, not oil-tanker replacement.** THESIS: this is a bet on Indonesian
  domestic LNG shipping demand (see §5), not more of the existing oil-tanker
  business.
- Vessels are old (22-24 years) secondhand LNG carriers, not newbuilds — bought
  at whatever secondhand LNG carrier prices prevailed in Dec-25/1Q-26.
  **INSUFFICIENT EVIDENCE on acquisition price per vessel** — could not source
  individual purchase prices; USD 60-70m for two ~140-146k CBM secondhand LNG
  carriers (roughly two decades old) needs benchmarking against secondhand LNG
  market comps, which I could not locate. Whether this was bought cheap or at
  a cyclical top in LNG asset values is **unresolved and important** — flag for
  Financial Forensics / Valuation agents.

## 2. Revenue model — contract cover vs spot, counterparty concentration

**MAJOR FINDING — the fact sheet's central premise is very likely WRONG for
the current period.** The CLAUDE.md brief and BULL.md fact sheet hypothesize
that BULL is "closer to a contracted infrastructure/leasing business" with
heavy Pertamina time-charter cover, inferred from low 9.9% 5-year revenue
volatility. **Current primary-source data says the opposite:**

**FACT** (Samuel Sekuritas, Figure 10, citing company data, 9M25 basis):
- **BULL's oil-tanker revenue is 95% spot / 2% time charter.**
- **97.6% of operations served *international* oil markets as of 9M25** (i.e.
  not domestic Indonesian cabotage business, not Pertamina).
- Oil (crude/product tankers + FPSO/FSO) = 95% of total 9M25 revenue, gas
  (LPG) = 2%, agency fees = 3%.
- Peer comparison in the same report: **SOCI (Soechi Lines) is 13% spot / 74%
  time charter; HUMI (Humpuss Maritim) is ~20% spot / ~80% time charter.**
  BULL is the outlier — **uniquely spot-exposed** among its listed IDX tanker
  peers, not more contract-covered than them.

**This is a reversal from BULL's own historical positioning.** Earlier
reporting (Kontan, 2020-2022) shows a very different company:
- **FACT** (Kontan, ~2021): management's stated target was time charter =
  80-90% of revenue, with **Pertamina and subsidiaries targeted at a minimum
  85% of revenue composition.**
- **FACT** (Kontan, 2020): Pertamina alone generated USD 74.6m of BULL's
  USD 130.5m time-charter revenue that year — i.e. Pertamina was the dominant
  single counterparty.
- **FACT** (Kontan, 1H-2022): time-charter revenue fell 43.9% YoY to
  USD 56.3m, with Pertamina-group revenue down 58.8% to USD 14.4m — evidence
  BULL was already losing/reducing Pertamina-linked charter business by 2022.

**INFERENCE:** between roughly 2022 and 2025/26, BULL executed a strategic
pivot away from a Pertamina-dominated domestic time-charter model toward
international spot-market trading (Mediterranean, Black Sea, Asian waters —
see route map in §3). The "9.9% 5-year revenue volatility" figure in the
screener fact sheet is a trailing artefact of the *old* business model; it
describes a company that no longer exists in its current form. **Going
forward, revenue volatility should be expected to be much higher, tracking
Aframax/MR spot rates directly** — this is now much closer to a classic
cyclical shipowner than a contracted infrastructure business. **The CLAUDE.md
hypothesis in point 2 is falsified for the current period — flagged clearly
per instructions.**

Caveat: **INSUFFICIENT EVIDENCE** on exact current-year Pertamina revenue
share in dollar terms (I could not source a FY2025/1Q26 breakout by
counterparty, only the spot/TC split and domestic/international split). It
is possible a residual Pertamina relationship remains inside the "2%
domestic" tail (2 of the 11 vessels reportedly trade the Java Sea per the
route map in §3) but it is now immaterial to the group, not central.

## 3. Charter roll schedule and repricing / Q1-2026 margin jump

**Central finding: the Q1-2026 gross-margin jump (28.2% → 42.1%) is very
likely a SPOT RATE SPIKE, not charter repricing.** Given 95%+ spot exposure
(§2), "charter roll schedule" is largely the wrong frame for this company
today — there is little charter book left to roll.

**FACT** (Samuel report, dated 16 April 2026, citing MarineTraffic AIS data as
of 8 April 2026): BULL's 11 vessels were positioned as follows:
- 5 vessels (MT Capibara, Silver Tiger, Nusa Merdeka, Silver Phoenix,
  Wildebeest — note: report text says "5... Mediterranean" but the route table
  lists a mix) trading Mediterranean/Black Sea routes (~45% of routes)
- 3 vessels in Asian waters (~27%)
- 2 vessels (MT Gas Natuna, MT Gas Garuda) on domestic LPG/LNG routes (Java
  Sea) — the residual domestic book
- **None of BULL's routes transit the Strait of Hormuz** — explicitly verified
  by the broker against live AIS tracking, relevant given 2026 Iran tensions.

**FACT — the rate environment driving the margin jump:** Aframax spot
earnings hit **USD 145,343/day in March 2026 (+57% MoM)**, a new cycle high,
driven by escalating US-Iran tension. This followed Aframax rates already
having risen to ~USD 105k/day in Feb-2026 (+222% YoY), above prior
Russia-Ukraine-war peak levels of ~USD 104k/day (Samuel report, Figures 8-9).
**Given BULL's 95%+ spot exposure, a spot-rate spike of this magnitude
mechanically produces the gross-margin jump reported for Q1-2026** — this is
the most parsimonious explanation, more consistent with the evidence than a
"charter repricing" story, since there is little charter book to reprice.

**Durability — THESIS, not fact, and this is the crux of the whole
investment case:**
- **Bull case (broker's own thesis):** structural upcycle — sanctions-driven
  fleet inefficiency (~15.6% of global fleet is sanctioned/shadow, per Samuel),
  Red Sea rerouting, IMO slow-steaming, and (as of the report date) an
  escalating US-Iran confrontation threatening Hormuz closure, which would
  further tighten effective non-sanctioned tanker supply. Samuel forecasts
  FY2026 revenue of USD 434m (+193% YoY) and EBITDA of USD 181m (+269% YoY) on
  the assumption **"the market stays at this level for 2026F"** — their own
  hedge that this is a point-in-time rate capture, not a steady state.
- **Bear case (owner's framework, and my own read):** this is the textbook
  definition of peak-cycle earnings. Spot tanker rates are famously the most
  volatile input in shipping; a USD 145k/day Aframax rate driven by an acute
  geopolitical event (Iran/Hormuz brinkmanship) is not a run-rate. If the
  geopolitical premium resolves (de-escalation, or Hormuz simply doesn't
  close), Aframax spot rates could fall sharply, and BULL's revenue — 95%+
  levered to spot — falls with it almost one-for-one, with **no charter
  backlog to cushion the decline.** The stock's own price action (tripled,
  then gave back a third — see fact sheet) is consistent with the market
  first pricing this as durable and then partially repricing the geopolitical
  risk premium.
- **THESIS: the 52-week low of IDR 147 and high of IDR 685 likely bracket a
  period from "pre-rate-spike, pre-Iran-tension" to "peak rate-spike euphoria
  with BUY initiations at TP 700," and the current IDR 464 sits in between —
  consistent with a market still working out how durable Q1-2026 is,** not a
  case where the market has already concluded either way.

**No evidence located of a formal charter roll/expiry schedule** (contract
end dates, renewal terms) because the vast majority of the fleet is not on
charter — spot voyages are fixed cargo-by-cargo, not "rolled." **INSUFFICIENT
EVIDENCE** on the specific domestic LNG PLN tender status update since April
2026 (see §5) or on terms of the 2 residual domestic-route vessels' contracts.

## 4. The moat question — cabotage, competitors, Pertamina in-sourcing risk

TBD

## 5. The tanker cycle in 2026

TBD

## 6. Returns on capital across the cycle

TBD

## 7. Management, ownership, capital allocation track record

TBD

## 8. Score and classification

TBD

## Sources

TBD
