#!/usr/bin/env bash
# Quarterly refresh: pull the latest fundamentals, then rebuild the workbook.
#
# Run this roughly a month after each quarter end, once IDX filing season has
# passed. A full universe refresh takes 60-90 minutes; Yahoo rate-limits and the
# client backs off adaptively rather than hammering it.
#
#   ./refresh.sh                 # full universe
#   ./refresh.sh BBCA,AALI,ASII  # just these tickers (seconds)

set -euo pipefail

cd "$(dirname "$0")/.."

TICKERS="${1:-}"
STAMP="$(date +%Y%m%d-%H%M%S)"
mkdir -p idx_picker/logs

ARGS=(--workers 4)
if [[ -n "$TICKERS" ]]; then
  ARGS+=(--tickers "$TICKERS")
fi

echo "==> Refreshing fundamentals${TICKERS:+ for $TICKERS}"
python3 -m idx_picker.scraper.pipeline "${ARGS[@]}" \
  2>&1 | tee "idx_picker/logs/refresh-${STAMP}.log"

echo "==> Rebuilding workbook"
python3 -m idx_picker.workbook.build

echo "==> Running tests"
python3 -m pytest idx_picker/tests -q

echo
echo "Done. Outputs in idx_picker/output/"
ls -lh idx_picker/output/
