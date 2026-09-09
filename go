#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$ROOT/kbz_v6_stage2.sh" ]]; then
  exec bash "$ROOT/kbz_v6_stage2.sh" "$@"
fi
exec bash <(curl -fsSL https://raw.githubusercontent.com/bengnjk-byte/ketabebozorg-cloudshell/main/kbz_v6_stage2.sh) "$@"
