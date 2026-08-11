# MOLI — Stock Synthesis

**PT Madusari Murni Indah Tbk** (Molindo Group) · IDX: MOLI · Price IDR 274
Market cap ~IDR 746bn · Screener: **SKIP → WATCH** after a model fix · Synthesis 2026-08-11
All five agents on Sonnet.

| Agent | Score | Verdict |
|---|---:|---|
| 1 Financial Forensics | 55/100 | QUESTIONABLE |
| 2 Valuation | — | **FAIRLY VALUED** (bear 209 / base 273 / bull 448) |
| 3 Business / Industry | — | CYCLICAL |
| 4 Macro / Catalyst | — | **WEAK** |
| 5 Thesis Killer | — | **REJECT** |

---

## Why this row was worth the research

MOLI was the most statistically attractive rejection the screener produced: **F-Score 9/9,
zero debt, Altman Z 11.2, FCF yield 48%, PE 6.3, PB 0.58, EV/EBIT 4.1** — thrown out by
**one percentage point** (MOS 9% against a 10% floor). Either the screener was being
absurdly precious, or its peak-earnings flag was carrying the whole verdict.

**It was the flag.** And the research both vindicated it and found a real bug alongside it.

---

## The one number that settles it

Two agents, working independently, computed the same thing:

> **EV against normalised (5-year median) EBIT = 8.8x, against a peer median of 9.13x.**

The celebrated **4.1x EV/EBIT exists only on peak trailing earnings**. On mid-cycle
earnings MOLI trades *at* its peer multiple, not below it. There is no bargain — there is
one very good year.

## What produced the good year

**A molasses input-cost collapse, with named regulations on both sides.** MOLI converts
molasses (a sugar by-product) into ethanol; the spread is the entire business.

| | |
|---|---|
| Molasses 2024 | ~IDR 2,400–3,000/kg |
| Molasses mid-2025 | **~IDR 700–1,000/kg** — after **Permendag 16/2025** liberalised imports |
| Molasses July 2026 | **recovered to IDR 1,700–2,000/kg** |
| Reversal driver | **Permendag 18/2026** — government protecting sugarcane farmers |

H1 2026, released the day of this review: **revenue +1.65%, net profit +192%**, COGS −8.58%,
gross margin 25.4% → 32.9%. Essentially all profit growth came from the input, not from
ethanol pricing or volume.

*(The three agents cite slightly different price vintages and units — 2,500→700/kg,
2,400–3,000→700–1,000/kg, 1,900→1,000/litre. Direction, magnitude and mechanism agree, and
all three independently confirm the recovery is under way.)*

**It is already unwinding in the reported numbers:** quarterly FCF has fallen from
**IDR 157.5bn (Q3 2025) to IDR 41.5bn (Q2 2026)** — down 74%.

## What is genuinely true

- **The 48% FCF yield is real, not a data artifact.** Forensics pulled the audited FY2025
  consolidated cash flow from the IDX filing: **audited OCF IDR 446.87bn against the
  screener's implied 446.9bn.** Net income also correctly excludes minority interest.
- **But ~IDR 381bn of it is not repeatable** — inventory drawdown plus a full debt paydown,
  with a further ~IDR 45bn tax refund on top.
- **Through the cycle the business is mediocre:** 5-year average **ROE 4.1%**, gross margin
  **24.4%**. A perfect F-Score measures *improvement*, not *level* — and improvement off a
  low base during an input windfall is exactly what it caught.

## The structural weakness

**MOLI buys molasses on the open market with no captive supply.** Its principal competitor
is the state-owned **PTPN I / Enero / SGN group, vertically integrated across 42 sugar
mills**, which has already pledged 30,000 KL to Pertamina. In a pure spread business,
owning neither end is decisive — and management's own commentary concedes minimal pricing
power.

## The catalyst is real law and a weak catalyst

The **E5 bioethanol mandate genuinely exists** — Permen ESDM No. 4/2025 with implementing
Kepmen ESDM No. 113.K/EK.05/MEM.E/2026, in force **1 July 2026**, non-subsidised gasoline,
Java-only, requiring domestically-sourced ethanol, with a government-set monthly price
index (IDR 10,933/L reference).

Why it does not carry the thesis:
- **No levy-funded subsidy pool.** Biodiesel has BPDPKS; ethanol has no equivalent. The
  B50 analogy is tempting and wrong.
- **Capacity is an order of magnitude short** — ~60,000 kl national fuel-grade against the
  ~1–1.2m kl/yr a full E5 rollout needs.
- **Rollout is narrow** — ~170 Pertamina stations, East Java and Jakarta.
- **It already fired**, over a month before this review. Priced-in public information.
- **E10 is a 2027–28 event**, outside the window, and MOLI's own 80m→100m litre expansion
  phases through September 2027.

---

## The screener bug this exposed (fixed)

The DCF returned **59 / 61 / 64** against a 274 price while the blend said 300 — a
five-fold internal contradiction I wrongly assumed meant the *blend* was right.

**The valuation agent diagnosed it correctly and I was wrong.** The scenario builder
deducted reinvestment on a *different time basis* from the earnings it deducted from: a
five-year median EBIT netted against **trailing-twelve-month** capex. MOLI's Q1 2026
carried a IDR 43.8bn expansion outlay that pushed TTM capex to IDR 74.1bn — about **2x its
IDR 36.7bn annual median** — collapsing the cash-flow base from a NOPAT of IDR 71.4bn to
**IDR 1.7bn**. Roughly 90% of the resulting IV was just the per-share cash pile passing
through.

Fixed universe-wide: `normalised_capex` now supplies a median annual figure so earnings and
reinvestment share a basis. MOLI's DCF moves to **145 / 197 / 254**, and its screener
verdict from SKIP to WATCH (MOS 23%).

**But the blended IV of 354 is still too generous**, because the comparables lens applies
peer multiples to peak trailing EBIT. The agents' EPV on normalised earnings — **273 against
a 274 price** — is the number to trust.

---

## Valuation

| Lens | Value | vs price 274 |
|---|---:|---:|
| Screener blended IV (still peak-contaminated) | 354 | +29% |
| Screener DCF base (post-fix) | 197 | −28% |
| **EPV on normalised EBIT (adopted)** | **273** | **−0.4%** |
| Agent bear / bull | 209 / 448 | −24% / +64% |

**Adopted: bear 209 / base 273 / bull 448. MOS ≈ 0%.**

## Final stock score

| Factor | Score | Note |
|---|---:|---|
| Valuation | 8 / 25 | Fairly valued on mid-cycle; the cheapness is entirely peak-earnings |
| Business Quality | 8 / 20 | 5-yr ROE 4.1%; no captive input; no pricing power |
| Balance Sheet / Downside | 14 / 15 | Genuinely zero debt, Altman 11.2, audited cash flow — the real strength |
| Catalyst | 4 / 15 | E5 is law but unfunded, narrow, and already fired |
| Fundamental Momentum | 3 / 10 | Windfall already reversing; FCF −74% since Q3 2025 |
| Macro / Industry | 5 / 10 | E5 direction positive; molasses reversal negative |
| Mispricing / Information Edge | 2 / 5 | The market has this roughly right |
| **Total** | **44 / 100** | Screener composite was 80 |

---

## Verdict

**NO POSITION. Watchlist for re-underwriting in 2–3 years.**

The screener's original SKIP was **right, and arguably too generous** — a properly
normalised margin of safety is ~0%, not +9%. The 1-percentage-point rejection that looked
like excessive precision was in fact the peak-earnings flag doing its job.

The irony is worth recording: **fixing a genuine bug in my DCF moved MOLI from SKIP to
WATCH — in the wrong direction.** The bug and the correct answer happened to point the same
way. Two wrongs made a right, and the fix is still worth having because it was corrupting
every capital-intensive name in the universe.

**What would make this interesting:** E5 scaling with a funding mechanism, MOLI securing
captive or contracted molasses supply, or a price near **IDR 200** — where the bear case
provides a genuine floor and you would be buying a debt-free licensed producer rather than
a molasses price forecast.

**Liquidity caveat regardless:** ~IDR 306mn daily traded value against a **9.27% free
float** (controlling family ~90.7%). Even a small position takes weeks to build and would
be very hard to exit on bad news.
