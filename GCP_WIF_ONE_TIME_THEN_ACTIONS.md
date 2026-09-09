KETABEBOZORG · RUNG 3 PROCEDURE (CORRECTED)
DATE: 2026-09-10
MODE AFTER BIND: CONNECTED_READ_ONLY ONLY
DO NOT: JSON key, WRITE, Scheduler, I9, Q10, REV7 mutation
DO NOT: treat helper subtree as frozen V6
DO NOT: invent SERVICE_URL
DO NOT: call configuration-complete RUNG 3 PASS
DO NOT: mix Cloud Build / Artifact Registry failures with WIF failures
KEEP: google-github-actions/auth@v2 until live evidence requires otherwise

TWO-LAYER REPOSITORY RESTRICTION (required)
  1) Provider admission condition
     assertion.repository == 'bengnjk-byte/ketabebozorg-cloudshell'
  2) Service-account IAM
     roles/iam.workloadIdentityUser
     only for that repository principalSet
Do not rely on IAM alone. Google WIF guidance requires the provider condition.

SAFER SEQUENCE
1  Open project ketabebozorg-orchestrator
2  Verify the signed-in account can manage Workload Identity Pools and SA IAM
   (opening the project is not enough)
3  Verify/enable APIs: iam, iamcredentials, sts, plus cloudresourcemanager
4  Verify/create github-pool
5  Verify/create github-provider
6  Map:
     google.subject=assertion.sub
     attribute.repository=assertion.repository
7  Add provider condition restricting admission to:
     bengnjk-byte/ketabebozorg-cloudshell
8  Verify ketabebozorg-runner@ketabebozorg-orchestrator.iam.gserviceaccount.com
   exists and is enabled BEFORE binding
9  Bind roles/iam.workloadIdentityUser only to the repo-scoped principalSet
10 Obtain full provider resource name using PROJECT_NUMBER, not project ID:
     projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
11 Set GitHub Actions repository variable WIF_PROVIDER to that name
   This chat may not be able to write GitHub variables; set manually if needed
12 Re-read all configuration
13 Controlled deploy-readonly run ONCE with allow_rung4=false
14 Prove OIDC request → Google STS → provider condition → SA impersonation
15 RUNG 3 = PASS only after step 14
   After 10–11 only: RUNG 3 CONFIGURED
16 Only then allow Rung 4 CONNECTED_READ_ONLY (allow_rung4=true)

RUNG 4 (not Rung 3)
Cloud Run deploy --source needs Cloud Build, Artifact Registry, and extra IAM.
Those failures are not WIF failures.
Private /health needs authenticated invocation.
Cloud Run success is not Drive-read proof.

OIDC JWT is short-lived (~5 min). Do not pause between issuance and Google auth.

2B DONE. Do not reopen.
WRITE OFF. Scheduler OFF.
