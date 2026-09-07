# INDY — Agent 2: Valuation & Model Validation

*First pass, 2026-08-11. Ticker: INDY (Indika Energy Tbk.), IDX Energy/Coal. Price IDR 2,680.*

## 0. Framing

CLAUDE.md's structural rule ("cheapness alone never produces BUY") plus the mission
brief both point the same way: INDY is a **holding company**, not an operating
single-asset business, so a blended DCF/EPV/comps on consolidated financials
(screener's method, Blended IV 2,072–2,140) is the wrong tool. It averages a
depleting cash cow (Kideco coal), a pre-revenue capital-intensive gold mine (Awak
Mas), several small loss-making green/EV ventures, and holdco leverage into one
number, none of which behaves like a going-concern perpetuity. **SOTP is the
correct frame.** This report builds one. Verdict below.

## 1. What INDY actually is (FACT, from search)

- **Kideco Jaya Agung**: INDY owns **91%** [FACT — multiple 2026 news sources,
  e.g. IDNFinancials "INDY addresses US$1B Kideco divestment reports"]. Kideco
  generates **72.8% of INDY's gross revenue** and materially more of consolidated
  profit — Kideco alone posted **US$42.4M net profit in Q1 2026** vs INDY's
  **consolidated** net profit of just **US$7.2M** the same quarter [FACT,
  Kompas/IDNFinancials coverage of Q1 2026 results]. The gap is the drag from
  holdco interest expense and loss-making/pre-revenue non-coal units —
  material and worth pricing explicitly, not netting to zero.
- **Kideco mine license**: IUPK renewed in Jan 2023 for **10 years, expiring
  13 March 2033** [FACT, multiple Indonesian trade press: investor.id,
  kontan.co.id, bisnis.com]. **Reserves ~531Mt proven** (dated sourcing, treat
  with caution) **at ~30–31Mt/yr production ⇒ ~17 years of reserve life**
  [INFERENCE from Petromindo production data], i.e. reserves run to roughly
  **2043** but the *license* only currently covers **2033**. This gap — 10
  years of reserve life with no current legal right to mine it — is the single
  biggest, least-priced fact in this name.
- **Kideco divestment rumor (July 2026)**: Bloomberg reported INDY exploring a
  sale of Kideco valued at **>US$1B** (≈ IDR 18 trillion) [FACT that the report
  exists; the valuation itself is **THESIS/rumor**, not confirmed — INDY's
  corporate secretary explicitly declined to confirm, calling it market
  speculation, and analysts questioned the deal given Kideco is the group's
  main cash engine]. Useful as a sanity-check anchor for Kideco's value, not
  as ground truth.
- **Awak Mas gold project** (via Nusantara Resources, ownership % **not
  confirmed** in this pass — insufficient evidence): **43% construction
  complete as of Oct 2025**, **US$234M invested** of a **~US$429M** total
  budget, targeting **trial production late 2026, commercial Q1 2027**, ramping
  to **100koz/yr → 150koz/yr by 2029**. Reserve **1.1Moz**, resource **2.0Moz**
  [FACT, SMM/IDNFinancials/Indonesia Miner coverage]. This is pre-revenue,
  fully sunk-capital-dependent, and financed partly by new debt already
  reflected in consolidated net debt.
- **Other ventures**: EMITS (solar, C&I) — **US$7.1M revenue in 2025**; ALVA
  (EV two-wheelers, via Ilectra Motor Group) — Indika + co-investors put in
  **~US$16M**; Mekko (bauxite/nickel trading). All small relative to Kideco;
  broadly cash-consuming, not cash-generative, at this stage [FACT].
- **Coal price**: 2025 was a trough year (Kideco ASP fell ~18% YoY in 2024 to
  **US$59.5/t**; INDY consolidated revenue fell 2022→2025 from IDR 77.6tn to
  36.4tn). **2026 shows a recovery**: HBA high-CV grade rose to **US$103.4/t**
  by April 2026 (+3.5% MoM), GAR 5800 index rose from 80.99 (Jan) to 107.32
  (June 2026), and Newcastle-linked futures held near **US$130/t** in July 2026
  [FACT, HBA/Discoveryalert/Coaltradeindo]. Whether this is a durable
  mid-cycle level or another spike is **not established** here.

## 2. Is P/B 0.65 real? (Priority 2)

Book value per share ≈ IDR 4,113 (parent equity IDR 21,395.7bn ÷ 5.203bn shares,
FY2025), vs price 2,680 ⇒ P/B ≈ 0.65, matching the screener. **This equity figure
is consolidated-parent, net of an implied ~IDR 2.7tn of minority interest**
(Total assets 52,529.7bn − TotalLiabilitiesNetMinorityInterest 28,442.4bn =
24,087.3bn total equity incl. minorities, vs 21,395.7bn attributable to parent)
[INFERENCE from fact-sheet arithmetic] — consistent with the ~9% Kideco minority
plus other subs' minorities. **Whether book carries goodwill or unimpaired
legacy-acquisition assets is not established in this pass** — the annual report
PDF's balance-sheet notes were not successfully extracted (fetch returned
encoded/unreadable content). Flag as **insufficient evidence — requires further
research** (specifically: goodwill line, mining-property carrying values vs
depletion schedule, any impairment history). Until that is checked, treat the
P/B 0.65 discount as **partially real** (it is arithmetically correct) but of
**unknown quality** — a discount to book on a depleting, non-replaceable reserve
with a 2033 license wall is not obviously a bargain the way a discount to
readily-marketable working capital would be.

## 3. Is mid-cycle earnings a reasonable expectation? (Priority 3)

`Normalised/Trailing EBIT` = 1.40 means the screener's mid-cycle EBIT
(IDR 3,892.5bn, ≈$217M) is 40% above FY2025 trailing EBIT (IDR 2,511.3bn,
≈$140M). EBIT history: 2022 IDR 19,662bn (supercycle) → 2023 5,674bn → 2024
2,884bn → 2025 2,511bn — a **swift, structural decline**, not noise around a
stable mean. Two things can both be true:
- **THESIS**: some reversion is legitimate — 2025 was a coal-price trough and
  2026 HBA/Newcastle data already shows a real, current recovery, so $217M
  mid-cycle EBIT is not fantasy.
- **THESIS (screener's blind spot)**: a mid-cycle assumption implicitly treats
  Kideco as a going concern indefinitely. It isn't — reserves run out around
  2043 on the *current* license only through 2033. **Normalised EBIT is a
  legitimate estimate of the annual run-rate; it is not a legitimate basis for
  a Gordon-growth terminal value**, which is what a "blended DCF/EPV" applied
  naively would do. That mismatch, not the earnings-normalisation math itself,
  is the main reason the screener's Blended IV should not be trusted at face
  value for this name.

## 4. Sum-of-the-parts (Priority 1)

All figures attributable-to-INDY-parent unless noted. FX 17,908 IDR/USD (per
fact sheet). Consolidated net debt used as the single deduction (**caveat**:
this is a group-consolidated figure; how much of the debt sits at Kideco vs.
holdco, and how much of the cash is trapped at Kideco and not freely
upstream-able to service holdco USD bonds [FACT: an 8.75% 2029 USD bond
exists], is **insufficient evidence — requires further research**. This
matters a lot if Kideco is carved out/sold and its cash leaves the group's
reach.)

| Component | Bear | Base | Bull | Key assumption |
|---|---|---|---|---|
| Kideco (91% attrib.) | ~$320–380M | ~$889M | ~$1,538M | Bear: IUPK NOT renewed past 2033 (7yr cash flow only), coal reverts to ~2025 trough, ~3x short-life multiple. Base: mid-cycle EBIT $217M (screener's own normalisation) × 4.5x — roughly half the 8.03x peer EV/EBIT median, discounted for finite reserve life vs peers presumably not depleting as fast. Bull: license renewed to full reserve life (~17yr), 2026 coal rally sustained, 6.5x. |
| Awak Mas gold (at ~100%, ownership % unconfirmed) | ~$117M | ~$245M | ~$500M | Bear: 50% haircut to $234M sunk capital (pre-production execution/gold-price risk, only 43% built). Base: carrying value = capital invested to date. Bull: broker-DCF-style NPV once ramped to 100–150koz/yr (Verdhana Research states Awak Mas = 49% of their SOTP — exact $ not retrieved this pass). |
| Other ventures (EMITS, ALVA/IMG, Mekko, etc.) | $0 | ~$75M | ~$175M | Bear: cash-burn, no realisable value. Base/Bull: rough carrying value / optionality. |
| Less: consolidated net debt | −$645M | −$645M | −$645M | FY2025 net debt, IDR 11,556.5bn ÷ 17,908. Held flat across scenarios (conservative — bull case FCF could pay some down, bear case could see it worsen; not modelled). |
| **Equity value (USD)** | **≈ −$210M → floored at $0** | **≈ $564M** | **≈ $1,568M** | |
| **Per share (IDR)** | **≈ 0** | **≈ 1,940** | **≈ 5,400** | Shares 5.203bn |

**Cross-checks that increase confidence in these ranges:**
- Base case Kideco value (~$889M for 91%) lands close to the **rumored $1B
  divestment valuation**, despite being built independently from mid-cycle
  EBIT and a depleting-asset discount multiple — two unrelated methods
  converging is a useful (not conclusive) sanity check.
- Bull-case per-share (~IDR 5,400) matches the **high end of analyst price
  targets found in search** (TradingView-aggregated average ~4,100, high
  ~5,400) — suggesting the bull case is roughly what sell-side bulls are
  already pricing, not an outlier.
- Base-case per-share (~IDR 1,940) is close to the **screener's own Blended
  IV (2,072–2,140)** — i.e., a structurally different SOTP method broadly
  agrees with the screener's rejection, even though the screener's *method*
  (single blended DCF/EPV/comps) is the wrong tool in principle. Two wrongs
  don't make a right, but this is evidence the SKIP is not simply an artifact
  of a bad methodology — the base-case number is genuinely unflattering.

## 5. Most important assumption

**The multiple/terminal-value treatment applied to Kideco — which is itself a
function of whether the IUPK is renewed past March 2033.** Moving Kideco's
valuation multiple from the bear case (~3x, license-capped) to the bull case
(~6.5x, full reserve life + sustained higher coal prices) swings attributable
Kideco value by over $1.1B — more than double the swing contributed by Awak
Mas or the other ventures combined, and by itself moves the SOTP per-share
result from roughly IDR 0 to roughly IDR 3,500+ before even adding the other
components. Coal price assumption is second-most important and is entangled
with the same variable (higher prices make renewal politically/economically
more likely for both government and operator).

## 6. Gaps — insufficient evidence, flagged rather than fabricated

- Kideco standalone (deconsolidated) balance sheet — debt/cash split between
  Kideco and holdco.
- Goodwill / impairment history on INDY's balance sheet.
- Exact INDY ownership % of Nusantara Resources / Awak Mas.
- Full-year 2025 Kideco standalone revenue, EBITDA, realised ASP (only 2024
  and partial-2025 volume data retrieved).
- Verdhana Research's actual SOTP dollar output (only the methodology and the
  "Awak Mas = 49% of SOTP" figure were retrieved, not the total).
- Whether Kideco's IUPK has a realistic path to a further extension beyond
  2033 (regulatory/ESG stance of Indonesian government on coal beyond 2030s
  not researched this pass).

## Output block

```
Valuation Score: 28/100
Existing Screener Valuation: Blended IV 2,072–2,140 (DCF/EPV/comps blend on consolidated financials), MOS -29%, SKIP
Current Price: 2,680
Conservative Value: ~0–400 (bear SOTP: IUPK not renewed past 2033, coal reverts to trough, Awak Mas haircut — equity value approaches zero)
Base Value: ~1,940 (SOTP: Kideco at mid-cycle EBIT × depleting-asset multiple, Awak Mas at carrying cost, other ventures at rough carrying value, less consolidated net debt)
Bull Value: ~5,400 (SOTP: IUPK renewed to full reserve life, sustained 2026-style coal rally, Awak Mas at broker-style ramped NPV — matches high end of analyst targets)
Appropriate Valuation Method: Sum-of-the-parts — mine-life-capped value for Kideco (not a perpetuity DCF), carrying-value/NPV range for pre-revenue Awak Mas, rough carrying value for minor ventures, less consolidated net debt. A single blended DCF/EPV/comps on consolidated financials is structurally wrong for a holdco with a depleting core asset plus unrelated pre-revenue ventures.
Why Existing Valuation May Be Wrong: Screener averages a depleting 7-to-17-year mining asset with a pre-revenue gold project and loss-making green/EV ventures into one blended perpetuity-style IV; SOTP is the correct frame for a holdco. However, an independently-built SOTP base case (~1,940) lands close to the screener's own Blended IV (2,072–2,140), so the rejection is directionally corroborated, not overturned, by the correct method — the "hidden value" hypothesis is not supported in the base case, only in the bull case (IUPK renewal + sustained coal prices + successful gold ramp).
Valuation Upside: Bear: ~-100% (equity value approaches zero) / Base: ~-28% / Bull: ~+101%
Margin of Safety: Base case MOS ≈ -38% (SOTP base 1,940 vs price 2,680) — i.e., currently priced above SOTP base case, not below it
Most Important Assumption: Kideco's valuation multiple / terminal treatment, driven by whether the IUPK mining license is renewed past its current 13 March 2033 expiry — this single lever swings attributable Kideco value by >$1.1B, more than Awak Mas and all other ventures combined
Valuation Verdict: VALUE TRAP
```

**Rationale for verdict**: P/B 0.65 is arithmetically real but reflects book
value of a depleting, license-capped reserve, not a stable earnings base —
the classic value-trap signature the mission brief flagged. Base-case SOTP
(~IDR 1,940) sits below the current price of 2,680, corroborating rather than
overturning the screener's SKIP, and the risk is asymmetric: bear case
approaches a wipeout of equity value (group leverage against a shortening
license window) while bull case requires several favourable events to align
(IUPK renewal, sustained 2026-style coal prices, on-time/on-budget gold
ramp-up) simultaneously. There is genuine, uncapped optionality in the bull
case — this is not a clean "expensive and boring" rejection — but optionality
is not the base case, and CLAUDE.md's rule holds: cheapness on P/B alone does
not clear the bar.
