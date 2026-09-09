#!/usr/bin/env bash
set -euo pipefail
BASE=https://raw.githubusercontent.com/bengnjk-byte/ketabebozorg-cloudshell/main
mkdir -p "$HOME/kbz"
curl -fsSL "$BASE/kbz_v6_stage2.sh" -o "$HOME/kbz/kbz_v6_stage2.sh"
curl -fsSL "$BASE/go" -o "$HOME/kbz/go"
chmod +x "$HOME/kbz/go" "$HOME/kbz/kbz_v6_stage2.sh"
ln -sfn "$HOME/kbz/go" "$HOME/go"
touch "$HOME/.bashrc"
grep -q 'alias go=' "$HOME/.bashrc" || echo 'alias go="$HOME/kbz/go"' >> "$HOME/.bashrc"
grep -q 'alias گو=' "$HOME/.bashrc" || echo 'alias گو="$HOME/kbz/go"' >> "$HOME/.bashrc"
echo "INSTALLED. Starting stage 2."
exec bash "$HOME/kbz/go"
