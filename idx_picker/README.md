# IDX Personal Stock Picker

A value-investing screener for the Indonesian Stock Exchange (and US equities),
built around four quantitative lenses — Magic Formula, Piotroski F-Score,
Acquirer's Multiple and Graham Net-Nets — plus scenario valuation and an
explicit BUY / WATCH / SKIP / DEEP VALUE verdict.

It replaces a Google-Sheets workbook fed by a 2020-era scraper that no longer
runs.

---

## Quick start

```bash
pip install requests openpyxl pandas

# Refresh the whole IDX universe (~956 tickers, roughly 60-90 minutes)
python3 -m idx_picker.scraper.pipeline --workers 4

# Refresh a handful of names (seconds)
python3 -m idx_picker.scraper.pipeline --tickers BBCA,AALI,ASII

# US equities
python3 -m idx_picker.scraper.pipeline --tickers AAPL,MSFT --market US

# Rebuild the workbook from the refreshed CSVs
python3 -m idx_picker.workbook.build
```

Outputs land in `idx_picker/output/`.

---

## Why the old scraper was replaced

`basnugroho/indonesia-stocks-scraper` cannot run today, for four independent
reasons:

| Problem | Detail |
|---|---|
| Dead Selenium API | Uses `driver.find_element_by_xpath(...)`, removed in Selenium 4 |
| Interactive logins | RTI and Stockbit both require a human to log in mid-run |
| Hardcoded paths | Download directories point at the original author's Google Drive |
| Pinned binaries | Ships `chromedriver` 85, incompatible with any current Chrome |

Its last substantive commit was 2020. The RTI and Stockbit endpoints it targets
are also now auth-walled, and `idx.co.id` sits behind Cloudflare and returns 403
to non-browser clients.

**The replacement uses Yahoo Finance**, which carries every IDX ticker under the
`.JK` suffix and needs no account.

---

## Architecture

```
idx_picker/
├── scraper/
│   ├── yahoo.py      HTTP client: crumb auth, adaptive rate limiting, disk cache
│   ├── metrics.py    Pure functions: TTM roll-ups, ratios, Piotroski, Altman, DCF, EPV
│   ├── scoring.py    Business classification, scenarios, red flags, the verdict
│   └── pipeline.py   Orchestration, cross-sectional ranks, peer groups, CSV output
├── workbook/
│   └── build.py      Generates the Excel/Sheets workbook from the CSVs
├── data/             Ticker seed lists and the HTTP cache
├── output/           Generated CSVs and the workbook
└── tests/            pytest suite
```

`metrics.py` and `scoring.py` are pure and network-free, which is what makes the
test suite meaningful — every number the screener produces can be reproduced from
a hand-built fixture.

---

## Output files

| File | Contents |
|---|---|
| `RAW_idx_stocks.csv` | Listing and market data, original column order preserved |
| `RAW_key_statistics.csv` | 131 per-ticker statistics; the original 70 columns kept in place, 61 appended |
| `RAW_analyses.csv` | Derived composite-rank table |
| `RAW_scores.csv` | Classification, scenario valuations, verdict, red flags |
| `RAW_history_quarterly.csv` | Long-format quarterly statements |
| `RAW_history_annual.csv` | Long-format annual statements |
| `run_summary.json` | Coverage, failures, timing, cache statistics |

The first three keep their original column order deliberately, so existing
formulas that reference those tabs keep resolving.

---

## Known data limitations

These are properties of the free Yahoo Finance feed, not bugs. They are stated
here because a screener that hides its data limits is worse than one that has
them.

**History depth is shorter than you might want.** Yahoo returns roughly 4 annual
periods and 5-6 quarters per ticker. That is enough for a year-over-year
Piotroski, a 3-year CAGR and a 4-year earnings normalisation, but not for the
10-year history a full cycle analysis wants. Two things mitigate it:

- **Ten years of monthly price history** *is* available and is used — price
  CAGR, position within the decade-long range, and maximum drawdown all come
  from it.
- **The cache is append-only across runs.** Run the refresh each quarter and the
  fundamental history deepens permanently from this point forward.

**IDX auto-rejection data is unavailable.** ARA/ARB limits and buy/sell order
frequency are RTI-specific. Those columns are retained in `RAW_idx_stocks.csv`
for layout compatibility but are blank.

**Piotroski is computed on an annual basis for most tickers.** The TTM basis
needs eight consecutive quarters and Yahoo supplies five or six. The
`F-Score Basis` column records which basis each row used.

**Some IDX issuers report in USD.** ITMG, ADRO and several other coal, energy and
shipping names file in USD while their shares trade in IDR. The pipeline detects
the statement currency and converts at spot; `Statement Currency` and
`FX Rate Applied` record what happened. Left unconverted, these names' per-share
figures are wrong by roughly 16,000x.

---

## The four lenses, as implemented

**Magic Formula (Greenblatt).** Earnings Yield is `EBIT / Enterprise Value` —
not the net-income-based E/P that some data providers label "earnings yield",
which double-counts capital structure. ROC is
`EBIT / (net working capital + net fixed assets)`, Greenblatt's definition, which
deliberately excludes goodwill and excess cash. ROIC is computed separately and
reported alongside; the two are not interchangeable.

**Piotroski F-Score.** All nine signals, each exposed as its own column so a
score can be interrogated rather than trusted. More than three unevaluable
signals returns blank rather than a misleadingly low total.

**Acquirer's Multiple (Carlisle).** `EV / EBIT`, with negative-EBIT names
excluded from peer medians rather than silently contributing zeros.

**Graham Net-Net.** `NCAV = Current Assets − Total Liabilities` (total, not
current — using current liabilities alone overstates NCAV for anything carrying
long-term debt). The classic test `Price < 2/3 × NCAV per share` is applied and
reported as a boolean.

---

## Valuation

Each name is routed to the framework that fits it:

| Business type | Anchored on |
|---|---|
| Compounder | DCF 40%, EPV 35%, comparables 25% |
| Cyclical | EPV 50%, comparables 30%, DCF 20% — mid-cycle earnings dominate |
| Financial | Justified P/B and comparables; no EV/EBIT, no FCF |
| Deep Value | The minimum of NCAV, EPV and comparables — the asset floor |

EPV normalises EBIT using the **median** of available annual figures, not the
mean. One commodity supercycle year in a four-year window dominates a mean:
ITMG's 2022 EBIT was five times its 2025 figure. Where mid-cycle EBIT still sits
more than 2x above trailing EBIT, a red flag says so explicitly — the valuation
is then a bet on the cycle turning, and that should be a visible assumption.

Margin of safety is `(IV − Price) / IV`. Upside is `IV / Price − 1`. They are
different numbers and both are reported.

---

## The verdict is layered, not a weighted average

Cheapness alone never produces a BUY. A name that clears the margin-of-safety
threshold must additionally pass:

1. Balance-sheet safety above 40/100
2. Piotroski F-Score above 3
3. Quality score above 35/100
4. No unresolved red flag

Failing any one drops it to WATCH. This is the value-trap filter, and it is
structural — it lives in `scoring.classify`, where it cannot be diluted by
reweighting.

Filings more than three quarters stale return SKIP regardless of valuation. A
screen that ranks on figures nine months old is ranking history.

---

## Refresh cadence

Quarterly, after IDX filing season (roughly one month after each quarter end).
The cache TTL defaults to 20 hours, so a same-day re-run costs no network.

```bash
python3 -m idx_picker.scraper.pipeline --workers 4
python3 -m idx_picker.workbook.build
```

Use `--cache-ttl -1` to force everything from cache, or delete `data/cache/` to
force a full re-fetch.

---

## Tests

```bash
python3 -m pytest idx_picker/tests -q
```

`metrics.py` and `scoring.py` are covered by unit tests built on hand-computed
fixtures. `tests/test_pipeline_integration.py` validates the generated CSVs for
internal consistency — that reported margins of safety reconcile to their
intrinsic values, that net-net flags actually satisfy the Graham test, and that
the Piotroski components sum to the reported total.
