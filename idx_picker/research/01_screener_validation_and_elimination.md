# Stage 2 — Screener validation and elimination

Input: the 64 names the screener returned as **BUY (48)** or **DEEP VALUE (16)**.

The screener is candidate generation only. This stage exists to falsify its verdict.
Before spending agent research time, every candidate is tested against evidence already
in hand. That pre-screen is recorded here in full — it is part of the elimination
decision, not a shortcut around it.

## Pre-screen rules

| Rule | Threshold | Rationale |
|---|---|---|
| Margin of safety | < 20% | The entire premise is a discount to intrinsic value. Below 20% there is no cushion for the model being wrong. |
| Altman Z (non-financials) | < 1.1 | Distress zone. Cheapness in a distressed capital structure is usually a transfer to creditors. |
| Interest coverage | flagged < 1.5x | The company cannot service its debt from operating earnings. |
| Net debt / EBITDA | flagged > 4x | Leverage that removes the owner's control over outcomes. |
| Filing staleness | > 2 quarters | Ranking a company on figures nine months old is ranking history. |
| Piotroski F-Score | <= 3 | Deteriorating fundamentals across the board. |
| Daily traded value | < IDR 300mn | A position cannot be built or exited. Judged on turnover, not market cap. |

**Result: 36 survive, 28 eliminated.**

## Eliminated

| Ticker | Screener verdict | Reason |
|---|---|---|
| CASS | BUY | daily turnover IDR 36mn - too illiquid to build a position |
| JSPT | BUY | daily turnover IDR 7mn - too illiquid to build a position |
| PTSP | BUY | daily turnover IDR 5mn - too illiquid to build a position |
| DLTA | BUY | daily turnover IDR 17mn - too illiquid to build a position |
| BCIP | BUY | daily turnover IDR 261mn - too illiquid to build a position |
| MINE | BUY | daily turnover IDR 229mn - too illiquid to build a position |
| PJAA | BUY | daily turnover IDR 119mn - too illiquid to build a position |
| IGAR | DEEP VALUE | daily turnover IDR 2mn - too illiquid to build a position |
| MYOH | BUY | daily turnover IDR 10mn - too illiquid to build a position |
| MCOL | BUY | daily turnover IDR 8mn - too illiquid to build a position |
| LPLI | DEEP VALUE | daily turnover IDR 4mn - too illiquid to build a position |
| PRDA | BUY | daily turnover IDR 267mn - too illiquid to build a position |
| KBLI | DEEP VALUE | MOS -9% below the 20% floor - no valuation support; daily turnover IDR 137mn - too illiquid to build a position |
| DYAN | BUY | daily turnover IDR 127mn - too illiquid to build a position |
| BMSR | DEEP VALUE | daily turnover IDR 1mn - too illiquid to build a position |
| GPRA | DEEP VALUE | MOS 13% below the 20% floor - no valuation support |
| PANS | BUY | daily turnover IDR 57mn - too illiquid to build a position |
| MRAT | DEEP VALUE | MOS -23% below the 20% floor - no valuation support; interest coverage 1.2x; daily turnover IDR 1mn - too illiquid to build a position |
| LPCK | DEEP VALUE | MOS -100% below the 20% floor - no valuation support; daily turnover IDR 152mn - too illiquid to build a position |
| MDRN | BUY | Altman Z -31.7 - distress zone; filings 2.4 quarters stale; daily turnover IDR 85mn - too illiquid to build a position |
| LTLS | BUY | daily turnover IDR 9mn - too illiquid to build a position |
| ATIC | BUY | Altman Z 0.6 - distress zone; daily turnover IDR 15mn - too illiquid to build a position |
| RUIS | DEEP VALUE | MOS -64% below the 20% floor - no valuation support; interest coverage 1.4x; Net debt/EBITDA 5.6x; daily turnover IDR 29mn - too illiquid to build a position |
| BUKA | DEEP VALUE | interest coverage -9.8x |
| DIVA | DEEP VALUE | MOS 8% below the 20% floor - no valuation support |
| LPKR | DEEP VALUE | MOS -8% below the 20% floor - no valuation support; Net debt/EBITDA 4.6x; F-Score 3/9 |
| PPRO | DEEP VALUE | Altman Z -1.2 - distress zone; interest coverage -33.3x; daily turnover IDR 45mn - too illiquid to build a position |
| WEGE | DEEP VALUE | MOS 19% below the 20% floor - no valuation support; interest coverage -48.4x; daily turnover IDR 4mn - too illiquid to build a position |

### Note on the liquidity cut

Eleven names were eliminated **solely** on tradability, not on merit — CASS
(composite 93, the highest in the entire 956-name universe), DLTA, PTSP, JSPT,
MYOH, MCOL, IGAR, BMSR, PANS, LTLS and DYAN among them. At an IDR 300mn/day
turnover floor, a IDR 10–15mn position is a large share of daily volume, and
exiting on bad news would move the price against you.

This is a portfolio-construction constraint, not a judgement on the businesses. If
you will accumulate patiently over weeks and accept that you may not be able to
exit quickly, CASS and DLTA in particular deserve to come back into scope.

## Survivors ranked, and the research shortlist

Ranking blends composite score (50%), margin of safety (30%), balance-sheet safety
(10%) and F-Score (10%), then penalises names whose valuation leans on a cycle
recovery (normalised EBIT more than 1.8x trailing) and names with stale filings. A
**two-per-sector cap** then applies, so the research budget is not spent discovering
that eight coal miners share one macro bet.

| # | Ticker | Company | Sector | Type | MOS | Rank | Shortlist |
|---:|---|---|---|---|---:|---:|---|
| 1 | CTRA | Ciputra Development Tbk. | Properties & Real Estate | Cyclical | 58% | 77.5 | **YES** |
| 2 | LSIP | PP London Sumatra Indonesia Tbk. | Consumer Non-Cyclicals | Compounder | 49% | 76.8 | **YES** |
| 3 | MAPI | Mitra Adiperkasa Tbk. | Consumer Cyclicals | Compounder | 39% | 73.5 | **YES** |
| 4 | ACES | Aspirasi Hidup Indonesia Tbk. | Consumer Cyclicals | Compounder | 51% | 73.1 | **YES** |
| 5 | MNCN | Media Nusantara Citra Tbk. | Consumer Cyclicals | Deep Value | 71% | 72.9 | reserve |
| 6 | PWON | Pakuwon Jati Tbk. | Properties & Real Estate | Cyclical | 42% | 72.8 | **YES** |
| 7 | CNMA | Nusantara Sejahtera Raya Tbk. | Consumer Cyclicals | Compounder | 31% | 72.6 | reserve |
| 8 | AALI | Astra Agro Lestari Tbk. | Consumer Non-Cyclicals | Ordinary | 33% | 72.1 | **YES** |
| 9 | SIMP | Salim Ivomas Pratama Tbk. | Consumer Non-Cyclicals | Ordinary | 53% | 71.9 | reserve |
| 10 | LPPF | Matahari Department Store Tbk. | Consumer Cyclicals | Ordinary | 77% | 71.5 | reserve |
| 11 | DMAS | Puradelta Lestari Tbk. | Properties & Real Estate | Cyclical | 42% | 71.4 | reserve |
| 12 | KIJA | Kawasan Industri Jababeka Tbk. | Properties & Real Estate | Deep Value | 38% | 69.9 | reserve |
| 13 | MSTI | Mastersystem Infotama Tbk. | Technology | Compounder | 35% | 69.5 | **YES** |
| 14 | BSSR | Baramulti Suksessarana Tbk. | Energy | Cyclical | 47% | 69.3 | **YES** |
| 15 | PGAS | Perusahaan Gas Negara Tbk. | Infrastructures | Cyclical | 48% | 69.2 | **YES** |
| 16 | NCKL | Trimegah Bangun Persada Tbk. | Basic Materials | Cyclical | 34% | 69.1 | **YES** |
| 17 | AADI | Adaro Andalan Indonesia Tbk. | Energy | Cyclical | 58% | 68.6 | **YES** |
| 18 | SMDR | Samudera Indonesia Tbk. | Transportation & Logistic | Cyclical | 54% | 67.4 | **YES** |
| 19 | NISP | Bank OCBC NISP Tbk. | Financials | Financial | 39% | 67.3 | reserve |
| 20 | BMTR | Global Mediacom Tbk. | Consumer Cyclicals | Deep Value | 69% | 67.3 | reserve |
| 21 | INDF | Indofood Sukses Makmur Tbk. | Consumer Non-Cyclicals | Ordinary | 40% | 66.5 | reserve |
| 22 | ERAL | Sinar Eka Selaras Tbk. | Consumer Cyclicals | Ordinary | 37% | 66.3 | reserve |
| 23 | ERAA | Erajaya Swasembada Tbk. | Consumer Cyclicals | Compounder | 58% | 65.5 | reserve |
| 24 | AUTO | Astra Otoparts Tbk. | Consumer Cyclicals | Ordinary | 32% | 65.0 | reserve |
| 25 | MPMX | Mitra Pinasthika Mustika Tbk. | Consumer Cyclicals | Ordinary | 33% | 63.7 | reserve |
| 26 | PNLF | Panin Financial Tbk. | Financials | Financial | 59% | 61.9 | reserve |
| 27 | ITMG | Indo Tambangraya Megah Tbk. | Energy | Cyclical | 59% | 61.6 | reserve |
| 28 | JKON | Jaya Konstruksi Manggala Pratama Tbk. | Infrastructures | Cyclical | 31% | 60.6 | reserve |
| 29 | PNBN | Bank Pan Indonesia Tbk. | Financials | Financial | 34% | 60.2 | reserve |
| 30 | MAIN | Malindo Feedmill Tbk. | Consumer Non-Cyclicals | Ordinary | 42% | 59.2 | reserve |
| 31 | BMRI | Bank Mandiri (Persero) Tbk. | Financials | Financial | 33% | 58.9 | reserve |
| 32 | GJTL | Gajah Tunggal Tbk. | Consumer Cyclicals | Ordinary | 39% | 57.4 | reserve |
| 33 | HRUM | Harum Energy Tbk. | Energy | Cyclical | 31% | 56.8 | reserve |
| 34 | PTBA | Bukit Asam Tbk. | Energy | Cyclical | 33% | 56.5 | reserve |
| 35 | UNTR | United Tractors Tbk. | Industrials | Cyclical | 44% | 55.8 | reserve |
| 36 | ADRO | Alamtri Resources Indonesia Tbk. | Energy | Cyclical | 32% | 55.0 | reserve |

## What happens to the reserves

The 24 survivors outside the shortlist are not rejected. They are the next wave: if a
shortlist name is killed by its Thesis Killer agent, the highest-ranked reserve in an
uncovered sector takes its place.

## Status

Specialist agent research (5 agents x 12 stocks) is **pending** — the run was halted
by an account usage limit, not by anything in the analysis. Nothing below the
elimination stage has been produced yet, and no research conclusions should be
inferred from this document beyond the pre-screen itself.
