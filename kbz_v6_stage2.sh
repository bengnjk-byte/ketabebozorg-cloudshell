#!/usr/bin/env bash
set -euo pipefail
PROJECT=ketabebozorg-orchestrator
REGION=australia-southeast1
EXPECT=daede0951db98e8442bb44e43eae64c1bf1e237082dec7cd51140129b05b87f2
GH_ZIP=https://raw.githubusercontent.com/bengnjk-byte/ketabebozorg-cloudshell/main/KETABEBOZORG_DUAL_ORCHESTRATOR_V6.zip
OUT=/tmp/kbz_stage2_result.txt
: > "$OUT"
{
  echo "START=$(date -u +%FT%TZ)"
  gcloud config set project "$PROJECT"
  ACCOUNT=$(gcloud config get-value account 2>/dev/null || true)
  echo "ACCOUNT=${ACCOUNT}"
  echo "PROJECT=$(gcloud config get-value project 2>/dev/null || true)"
  if [[ -z "${ACCOUNT}" || "${ACCOUNT}" == "(unset)" ]]; then
    echo "STATUS=NEED_LOGIN"
    exit 2
  fi
  gcloud secrets versions access latest --secret=OPENAI_API_KEY >/dev/null
  gcloud secrets versions access latest --secret=XAI_API_KEY >/dev/null
  echo "SECRETS=PRESENT"
  curl -fsSL "$GH_ZIP" -o /tmp/KETABEBOZORG_DUAL_ORCHESTRATOR_V6.zip
  SHA=$(sha256sum /tmp/KETABEBOZORG_DUAL_ORCHESTRATOR_V6.zip | awk '{print $1}')
  echo "SHA=${SHA}"
  if [[ "$SHA" != "$EXPECT" ]]; then
    echo "STATUS=SHA_MISMATCH_OR_ZIP_MISSING_ON_GITHUB"
    exit 3
  fi
  rm -rf /tmp/kbz-v6 && mkdir /tmp/kbz-v6
  unzip -q /tmp/KETABEBOZORG_DUAL_ORCHESTRATOR_V6.zip -d /tmp/kbz-v6
  cd /tmp/kbz-v6/ketabebozorg_orchestrator
  gcloud artifacts repositories describe ketabebozorg --location="$REGION" >/dev/null 2>&1 || \
    gcloud artifacts repositories create ketabebozorg --repository-format=docker --location="$REGION"
  IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/ketabebozorg/ketabebozorg-orchestrator:v6"
  gcloud builds submit --tag "$IMAGE" --project "$PROJECT"
  SA="${PROJECT}@appspot.gserviceaccount.com"
  gcloud run deploy ketabebozorg-orchestrator \
    --project "$PROJECT" \
    --region "$REGION" \
    --image "$IMAGE" \
    --service-account "$SA" \
    --no-allow-unauthenticated \
    --set-env-vars="ORCHESTRATOR_MODE=CONNECTED_READ_ONLY,GOOGLE_CLOUD_PROJECT=${PROJECT},MASTER_STATE_DOC_ID=1_fNS6aRK4Dsud2D5oN5c_-ljehffZjaHxoRu_8z8pvg,RESULT_BUS_DOC_ID=1mTXSNBQ2U1DXS2tAd7Hvd3M8cQ9aMYJuoM6u8eS8vuU" \
    --set-secrets="OPENAI_API_KEY=OPENAI_API_KEY:latest,XAI_API_KEY=XAI_API_KEY:latest" \
    --memory=1Gi --timeout=900
  URL=$(gcloud run services describe ketabebozorg-orchestrator --region="$REGION" --format='value(status.url)')
  REV=$(gcloud run services describe ketabebozorg-orchestrator --region="$REGION" --format='value(status.latestReadyRevisionName)')
  echo "SERVICE_URL=${URL}"
  echo "REVISION=${REV}"
  echo "MODE=CONNECTED_READ_ONLY"
  echo "SCHEDULER=OFF"
  echo "STATUS=STAGE2_DEPLOYED"
  echo "END=$(date -u +%FT%TZ)"
} 2>&1 | tee -a "$OUT"
echo
echo "==== SEND THESE LINES ==== "
grep -E '^(ACCOUNT|PROJECT|SHA|SERVICE_URL|REVISION|STATUS)=' "$OUT" || true
