KETABEBOZORG · RUNG 3 CANONICAL
DATE: 2026-09-10
2B DONE — DO NOT REOPEN
WRITE OFF. Scheduler OFF. REV7 UNCHANGED.
KEEP auth@v2 until live evidence requires otherwise.
NO JSON key. NO public Cloud Run. NO pool-wide trust. NO Owner/Editor.

CONFIRMED ONLY
1. Work Cloud Browser did not reach Google Cloud Console — CLOUD_ACCESS_BLOCKED, not WIF_FAILED.
2. WIF_PROVIDER is UNSET. Workflow fail-closes before auth even if GCP WIF already existed.

All pool/provider/SA/IAM/API/org-policy items are POSSIBLE until live GCP evidence.
Cloud Run / Cloud Build / Artifact Registry / /health / Drive are Rung 4.

GitHub OIDC capability = READY. Live token = NOT YET OBSERVED.
Expected WIF_PROVIDER (project NUMBER, not ID):
  projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
This chat may 403 on GitHub variable write. Set WIF_PROVIDER manually if needed.

TWO LAYERS, both required:
  Provider condition: assertion.repository == 'bengnjk-byte/ketabebozorg-cloudshell'
  AND roles/iam.workloadIdentityUser on repo-scoped principalSet only.

CONFIGURED = pool+provider+issuer+mapping+condition+SA enabled+binding+WIF_PROVIDER set.
PASS = live rung3-auth proves OIDC request, STS, provider admission, repo restriction, SA impersonation.
CONFIGURED != PASS.

First identity test = workflow rung3-auth (not deploy-readonly).
Only after RUNG 3 PASS: deploy-readonly for Rung 4.
Classify failures by exact step. Do not mix identity with Build/Run/Drive.

Recovery order: ACCESS → PROJECT → IAM AUTHORITY → APIs → POOL → PROVIDER → MAPPING → PROVIDER CONDITION → SERVICE ACCOUNT → REPO-SCOPED IAM → WIF_PROVIDER → AUTH TEST → RUNG 3 PASS → CLOUD RUN → HEALTH → DRIVE
Do not try to fix every possible issue at once.
First unresolved external dependency: authenticated GCP control-plane access.
