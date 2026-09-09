#!/usr/bin/env bash
set -euo pipefail
PROJECT=ketabebozorg-orchestrator
REGION=australia-southeast1
EXPECT=daede0951db98e8442bb44e43eae64c1bf1e237082dec7cd51140129b05b87f2
OUT=/tmp/kbz_stage2_result.txt
: > "$OUT"
{
  echo "START=$(date -u +%FT%TZ)"
  echo "LADDER_RUNG_TARGET=3_THEN_4_CONNECTED_READ_ONLY"
  if ! command -v gcloud >/dev/null 2>&1; then
    echo "STATUS=NEED_GCP_SESSION"
    echo "REASON=gcloud_not_present"
    echo "DO_NOT_SKIP_TO_WRITE=1"
    exit 2
  fi
  ACCOUNT=$(gcloud config get-value account 2>/dev/null || true)
  echo "ACCOUNT=${ACCOUNT}"
  if [[ -z "${ACCOUNT}" || "${ACCOUNT}" == "(unset)" ]]; then
    echo "STATUS=NEED_LOGIN"
    exit 2
  fi
  gcloud config set project "$PROJECT"
  echo "PROJECT=$(gcloud config get-value project 2>/dev/null || true)"
  echo "STATUS=GCP_SESSION_PRESENT_STOP_BEFORE_WRITE"
  echo "NEXT=CONNECTED_READ_ONLY_ONLY"
  echo "END=$(date -u +%FT%TZ)"
} 2>&1 | tee -a "$OUT"
