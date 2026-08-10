"""Yahoo Finance client for IDX (Jakarta) listed equities.

Replaces the original Selenium/RTI/Stockbit scrapers, which are unusable today:
they target 2020-era DOM structures, require interactive logins, ship pinned
chromedriver binaries, and call Selenium 3 APIs (`find_element_by_xpath`) that
were removed in Selenium 4.

Yahoo Finance carries every IDX ticker under the `.JK` suffix and exposes
quarterly and annual fundamentals going back ~5 years without authentication
beyond a session cookie plus crumb.

Two endpoints are used:

* ``/ws/fundamentals-timeseries`` - historical statement lines. No crumb needed.
* ``/v10/finance/quoteSummary``   - point-in-time market data. Crumb required.

Yahoo throttles aggressively (HTTP 429 with an HTML body, not JSON), so every
request runs through a shared token-bucket limiter with exponential backoff, and
every successful payload is cached to disk. A re-run within the cache TTL costs
no network at all, which makes iterating on the derived metrics cheap.
"""

from __future__ import annotations

import json
import logging
import random
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import requests

log = logging.getLogger(__name__)

BASE_TS = "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries"
BASE_QS = "https://query2.finance.yahoo.com/v10/finance/quoteSummary"
BASE_CHART = "https://query2.finance.yahoo.com/v8/finance/chart"
CRUMB_URL = "https://query2.finance.yahoo.com/v1/test/getcrumb"
COOKIE_URL = "https://fc.yahoo.com"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Statement lines pulled for both `quarterly` and `annual` periods. Yahoo returns
# nothing (rather than an error) for a line a given filer does not report, so
# over-requesting is safe -- financials, for instance, report no Inventory.
STATEMENT_FIELDS: tuple[str, ...] = (
    # Income statement
    "TotalRevenue",
    "CostOfRevenue",
    "GrossProfit",
    "OperatingIncome",
    "EBIT",
    "EBITDA",
    "NetIncome",
    "PretaxIncome",
    "TaxProvision",
    "InterestExpense",
    "SellingGeneralAndAdministration",
    "ResearchAndDevelopment",
    "BasicAverageShares",
    "DilutedAverageShares",
    # Balance sheet
    "TotalAssets",
    "TotalLiabilitiesNetMinorityInterest",
    "StockholdersEquity",
    "CashAndCashEquivalents",
    "CashCashEquivalentsAndShortTermInvestments",
    "TotalDebt",
    "LongTermDebt",
    "CurrentAssets",
    "CurrentLiabilities",
    "WorkingCapital",
    "Inventory",
    "AccountsReceivable",
    "AccountsPayable",
    "RetainedEarnings",
    "InvestedCapital",
    "NetPPE",
    # Cash flow
    "OperatingCashFlow",
    "CapitalExpenditure",
    "FreeCashFlow",
    "CommonStockDividendPaid",
)

QUOTE_MODULES = (
    "price",
    "summaryDetail",
    "defaultKeyStatistics",
    "financialData",
    "summaryProfile",
)


class RateLimitError(RuntimeError):
    """Raised when Yahoo returns 429 and retries are exhausted."""


@dataclass
class RateLimiter:
    """Token bucket shared across threads.

    `min_interval` is adaptive: a 429 widens it, a run of clean responses slowly
    narrows it back toward the floor. Yahoo's limit is not documented and drifts
    with load, so probing beats guessing a fixed constant.
    """

    min_interval: float = 1.1
    floor: float = 0.6
    ceiling: float = 12.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _next_at: float = 0.0
    _clean_streak: int = 0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            sleep_for = max(0.0, self._next_at - now)
            self._next_at = max(now, self._next_at) + self.min_interval
        if sleep_for:
            time.sleep(sleep_for)

    def penalise(self) -> None:
        with self._lock:
            self.min_interval = min(self.ceiling, self.min_interval * 2.0)
            self._clean_streak = 0
            # Push the whole bucket out so concurrent workers also back off.
            self._next_at = time.monotonic() + self.min_interval
        log.warning("rate limited; interval widened to %.2fs", self.min_interval)

    def reward(self) -> None:
        with self._lock:
            self._clean_streak += 1
            if self._clean_streak >= 25 and self.min_interval > self.floor:
                self.min_interval = max(self.floor, self.min_interval * 0.85)
                self._clean_streak = 0


class YahooClient:
    """Thread-safe Yahoo Finance client with disk cache and adaptive throttling."""

    def __init__(
        self,
        cache_dir: Path | str,
        cache_ttl_hours: float = 20.0,
        max_retries: int = 6,
        rate_limiter: RateLimiter | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = cache_ttl_hours * 3600
        self.max_retries = max_retries
        self.timeout = timeout
        self.limiter = rate_limiter or RateLimiter()
        self._session = requests.Session()
        # No global `Accept: application/json`: the crumb endpoint returns
        # text/plain and answers "Not Acceptable" when JSON is demanded.
        self._session.headers.update({"User-Agent": USER_AGENT})
        self._crumb: str | None = None
        self._crumb_lock = threading.Lock()
        self.stats = {"cache_hits": 0, "network": 0, "retries": 0, "failures": 0}

    # ------------------------------------------------------------------ cache

    def _cache_path(self, key: str) -> Path:
        safe = key.replace("/", "_").replace(":", "_")
        return self.cache_dir / f"{safe}.json"

    def _read_cache(self, key: str) -> Any | None:
        path = self._cache_path(key)
        if not path.exists():
            return None
        if self.cache_ttl >= 0 and (time.time() - path.stat().st_mtime) > self.cache_ttl:
            return None
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return None

    def _write_cache(self, key: str, payload: Any) -> None:
        try:
            self._cache_path(key).write_text(json.dumps(payload))
        except OSError as exc:  # a full disk must not abort a 950-ticker run
            log.warning("cache write failed for %s: %s", key, exc)

    # ------------------------------------------------------------------ crumb

    def _get_crumb(self) -> str:
        with self._crumb_lock:
            if self._crumb:
                return self._crumb
            self._session.get(COOKIE_URL, timeout=self.timeout)
            resp = self._session.get(CRUMB_URL, timeout=self.timeout)
            crumb = resp.text.strip()
            # A valid crumb is a short opaque token; an HTML error page is not.
            if not crumb or len(crumb) > 32 or "<" in crumb:
                raise RuntimeError(f"could not obtain Yahoo crumb (got {crumb[:60]!r})")
            self._crumb = crumb
            log.info("obtained Yahoo crumb")
            return crumb

    def _invalidate_crumb(self) -> None:
        with self._crumb_lock:
            self._crumb = None

    # ---------------------------------------------------------------- request

    def _request(self, url: str, params: dict[str, Any], cache_key: str | None) -> Any:
        if cache_key:
            cached = self._read_cache(cache_key)
            if cached is not None:
                self.stats["cache_hits"] += 1
                return cached

        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            self.limiter.wait()
            try:
                self.stats["network"] += 1
                resp = self._session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = exc
                self.stats["retries"] += 1
                time.sleep(min(30.0, 2**attempt) + random.random())
                continue

            if resp.status_code == 429:
                self.limiter.penalise()
                self.stats["retries"] += 1
                time.sleep(min(60.0, 3 * 2**attempt) + random.random() * 2)
                continue

            if resp.status_code == 401:
                # Crumb rotated mid-run; drop it and let the next attempt refetch.
                self._invalidate_crumb()
                self.stats["retries"] += 1
                if "crumb" in params:
                    params = {**params, "crumb": self._get_crumb()}
                continue

            if resp.status_code == 404:
                # Delisted or unknown on Yahoo. Cache the miss so the next run
                # does not pay for it again.
                if cache_key:
                    self._write_cache(cache_key, {"__not_found__": True})
                return {"__not_found__": True}

            if resp.status_code >= 500:
                last_error = RuntimeError(f"HTTP {resp.status_code}")
                self.stats["retries"] += 1
                time.sleep(min(30.0, 2**attempt) + random.random())
                continue

            try:
                payload = resp.json()
            except ValueError as exc:
                last_error = exc
                self.stats["retries"] += 1
                time.sleep(min(30.0, 2**attempt))
                continue

            self.limiter.reward()
            if cache_key:
                self._write_cache(cache_key, payload)
            return payload

        self.stats["failures"] += 1
        raise RateLimitError(f"exhausted retries for {url} ({last_error})")

    # ------------------------------------------------------------- public API

    def fundamentals(
        self,
        ticker: str,
        fields: Sequence[str] = STATEMENT_FIELDS,
        periods: Iterable[str] = ("quarterly", "annual"),
        start: int = 1_262_304_000,  # 2010-01-01; Yahoo clamps to what it holds
        end: int | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        """Return ``{type_name: [{asOfDate, value}, ...]}`` sorted oldest first.

        Requests are chunked at 15 types to keep the query string well inside
        the length Yahoo accepts, and each chunk is cached independently so a
        partial failure only re-fetches the missing slice.
        """
        symbol = yahoo_symbol(ticker)
        end = end or int(time.time())
        types = [f"{period}{field_}" for period in periods for field_ in fields]

        out: dict[str, list[dict[str, Any]]] = {}
        for index in range(0, len(types), 15):
            chunk = types[index : index + 15]
            payload = self._request(
                f"{BASE_TS}/{symbol}",
                {
                    "symbol": symbol,
                    "type": ",".join(chunk),
                    "period1": start,
                    "period2": end,
                    "merge": "false",
                },
                cache_key=f"ts_{ticker}_{index // 15}",
            )
            if payload.get("__not_found__"):
                continue
            for result in (payload.get("timeseries") or {}).get("result") or []:
                type_name = result.get("meta", {}).get("type", [None])[0]
                if not type_name:
                    continue
                series = []
                for entry in result.get(type_name) or []:
                    if not entry:
                        continue
                    raw = (entry.get("reportedValue") or {}).get("raw")
                    if raw is None:
                        continue
                    # `currencyCode` is retained because several IDX issuers --
                    # the coal and energy names especially (ITMG, ADRO, INDY) --
                    # report their financials in USD while their shares trade in
                    # IDR. Without it, every per-share figure is wrong by the
                    # exchange rate.
                    series.append({
                        "asOfDate": entry.get("asOfDate"),
                        "value": float(raw),
                        "currency": entry.get("currencyCode"),
                    })
                series.sort(key=lambda item: item["asOfDate"] or "")
                if series:
                    out[type_name] = series
        return out

    def quote_summary(self, ticker: str, modules: Sequence[str] = QUOTE_MODULES) -> dict[str, Any]:
        """Return the merged quoteSummary modules for one ticker."""
        symbol = yahoo_symbol(ticker)
        payload = self._request(
            f"{BASE_QS}/{symbol}",
            {"modules": ",".join(modules), "crumb": self._get_crumb()},
            cache_key=f"qs_{ticker}",
        )
        if payload.get("__not_found__"):
            return {}
        results = (payload.get("quoteSummary") or {}).get("result") or []
        return results[0] if results else {}

    def fx_rate(self, base: str, quote: str) -> float | None:
        """Spot rate to convert `base` into `quote` (e.g. USD -> IDR).

        Cached like everything else, and shared across the run, so a 950-ticker
        refresh costs one request per currency pair rather than one per ticker.
        """
        base, quote = base.upper(), quote.upper()
        if base == quote:
            return 1.0
        payload = self._request(
            f"{BASE_CHART}/{base}{quote}=X",
            {"range": "5d", "interval": "1d"},
            cache_key=f"fx_{base}{quote}",
        )
        if payload.get("__not_found__"):
            return None
        results = (payload.get("chart") or {}).get("result") or []
        if not results:
            return None
        rate = (results[0].get("meta") or {}).get("regularMarketPrice")
        return float(rate) if rate else None

    def price_history(self, ticker: str, range_: str = "1y", interval: str = "1d") -> dict[str, Any]:
        """Daily OHLCV, used for the 52-week band and trailing price change."""
        symbol = yahoo_symbol(ticker)
        payload = self._request(
            f"{BASE_CHART}/{symbol}",
            {"range": range_, "interval": interval, "includeAdjustedClose": "true"},
            cache_key=f"chart_{ticker}_{range_}",
        )
        if payload.get("__not_found__"):
            return {}
        results = (payload.get("chart") or {}).get("result") or []
        return results[0] if results else {}


def yahoo_symbol(ticker: str) -> str:
    """`AALI` -> `AALI.JK`. Passes through anything already suffixed."""
    ticker = ticker.strip().upper()
    return ticker if "." in ticker else f"{ticker}.JK"
