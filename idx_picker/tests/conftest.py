"""Shared fixtures and bundle builders for the idx_picker metric tests.

Everything here is offline. A "bundle" is the structure
`yahoo.YahooClient.fundamentals` returns: a mapping of
``{f"{period}{Field}": [{"asOfDate": ..., "value": ..., "currency": ...}, ...]}``
with each series sorted **oldest first**. `make_bundle` lets a test declare only
the numbers it cares about and have plausible dates filled in, so the fixtures
read as economics rather than as plumbing.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

import pytest

# The package is imported as `idx_picker.scraper.*`, so the repository root has
# to be importable regardless of where pytest is invoked from.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OUTPUT_DIR = REPO_ROOT / "idx_picker" / "output"

# Fixed anchors so no test depends on the wall clock.
QUARTER_ANCHOR = date(2025, 12, 31)
ANNUAL_ANCHOR = date(2025, 12, 31)
TODAY = date(2026, 3, 31)


def _quarter_dates(count: int) -> list[str]:
    """`count` quarter-end dates ending at QUARTER_ANCHOR, oldest first."""
    ends = [(3, 31), (6, 30), (9, 30), (12, 31)]
    out: list[str] = []
    year, index = QUARTER_ANCHOR.year, 3
    for _ in range(count):
        month, day = ends[index]
        out.append(f"{year:04d}-{month:02d}-{day:02d}")
        index -= 1
        if index < 0:
            index = 3
            year -= 1
    return list(reversed(out))


def _annual_dates(count: int) -> list[str]:
    """`count` fiscal year-ends ending at ANNUAL_ANCHOR, oldest first."""
    return [f"{ANNUAL_ANCHOR.year - offset:04d}-12-31" for offset in range(count - 1, -1, -1)]


def make_series(values: Sequence[float | None], period: str = "quarterly",
                currency: str = "IDR") -> list[dict[str, Any]]:
    """Expand bare numbers into the Yahoo series shape, oldest first.

    A ``None`` entry is dropped rather than emitted, mirroring Yahoo: it omits a
    period entirely rather than reporting a null, which is why the metric code
    can never rely on positional alignment across two different fields.
    """
    dates = _quarter_dates(len(values)) if period == "quarterly" else _annual_dates(len(values))
    return [
        {"asOfDate": as_of, "value": float(value), "currency": currency}
        for as_of, value in zip(dates, values)
        if value is not None
    ]


def make_bundle(
    quarterly: Mapping[str, Sequence[float | None]] | None = None,
    annual: Mapping[str, Sequence[float | None]] | None = None,
    currency: str = "IDR",
) -> dict[str, list[dict[str, Any]]]:
    """Build a fundamentals bundle from plain lists.

    >>> make_bundle(quarterly={"TotalRevenue": [100, 110, 120, 130]})
    {'quarterlyTotalRevenue': [{'asOfDate': '2025-03-31', 'value': 100.0, ...}, ...]}

    Values are oldest-first, matching the real feed, so ``[100, 110, 120, 130]``
    means the most recent quarter earned 130.
    """
    bundle: dict[str, list[dict[str, Any]]] = {}
    for field, values in (quarterly or {}).items():
        bundle[f"quarterly{field}"] = make_series(values, "quarterly", currency)
    for field, values in (annual or {}).items():
        bundle[f"annual{field}"] = make_series(values, "annual", currency)
    return bundle


# --------------------------------------------------------------- CSV fixtures

MIN_ROWS = 5


def load_csv(name: str) -> list[dict[str, str]]:
    """Load an output CSV, skipping the test when it is absent or too thin.

    A full universe refresh rewrites these files while the suite may be running,
    so the integration tests must degrade to a skip rather than a failure when
    they catch a partially written or missing file.
    """
    import csv

    path = OUTPUT_DIR / name
    if not path.exists():
        pytest.skip(f"{name} not present in {OUTPUT_DIR} - refresh may not have run")
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < MIN_ROWS:
        pytest.skip(f"{name} has only {len(rows)} rows (< {MIN_ROWS}) - likely mid-write")
    return rows


def as_float(value: str | None) -> float | None:
    """Parse a CSV cell to float, treating blanks and junk as absent."""
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


@pytest.fixture(scope="session")
def scores_rows() -> list[dict[str, str]]:
    return load_csv("RAW_scores.csv")


@pytest.fixture(scope="session")
def key_stats_rows() -> list[dict[str, str]]:
    return load_csv("RAW_key_statistics.csv")


@pytest.fixture(scope="session")
def idx_stock_rows() -> list[dict[str, str]]:
    return load_csv("RAW_idx_stocks.csv")
