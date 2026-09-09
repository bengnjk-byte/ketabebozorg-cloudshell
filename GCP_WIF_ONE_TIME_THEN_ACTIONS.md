KETABEBOZORG · RUNG 3 PROCEDURE CORRECTED
DATE: 2026-09-10
SEAL: CE-C0_RUNG3_PROCEDURE_CORRECTED_2026-09-10
REPLACES prior role-assignment text. Do not bind Rung-4 roles by guess.

2B DONE — DO NOT REOPEN
WRITE OFF. Scheduler OFF. REV7 UNCHANGED.
KEEP auth@v2 until live evidence requires otherwise.
NO JSON key. NO public Cloud Run. NO pool-wide trust. NO Owner/Editor.

CONFIRMED ONLY
1. CLOUD_ACCESS_BLOCKED — Console never reached. Not WIF_FAILED.
2. WIF_PROVIDER UNSET — fail-closes before auth.
   projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
All other GCP items remain UNKNOWN until live-read.

TWO-LAYER REPO RESTRICTION
Layer 1 provider admission:
  google.subject=assertion.sub
  attribute.repository=assertion.repository
  assertion.repository == 'bengnjk-byte/ketabebozorg-cloudshell'
Layer 2 SA impersonation only for repo-scoped principalSet:
  principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/bengnjk-byte/ketabebozorg-cloudshell
  roles/iam.workloadIdentityUser
Never whole pool. Never all GitHub repositories.

SA target (must be live EXISTS+ENABLED, not YAML-proven):
  ketabebozorg-runner@ketabebozorg-orchestrator.iam.gserviceaccount.com

Rung 3 identity APIs (blockers if unusable): iam, sts, iamcredentials, serviceusage.

CONFIGURED = live-verified project, identity APIs, pool ACTIVE, provider ACTIVE,
issuer, mapping, admission condition, SA exists/enabled, principalSet, WorkloadIdentityUser, WIF_PROVIDER set.
PASS = live rung3-auth: OIDC request, STS, provider admission, repo restriction, SA impersonation.
CONFIGURED ≠ PASS.

First identity test = workflow rung3-auth. deploy-readonly is Rung 4 only after PASS.

RUNG 4 IDENTITY MODEL — DO NOT GUESS-BIND ONTO RUNTIME SA
After WIF, the impersonated identity is the deployer.
Deployer roles (on the deployer, after live confirmation of current Google source-deploy docs):
  roles/run.sourceDeveloper
  roles/serviceusage.serviceUsageConsumer
Service Account User is granted TO the deployer ON the runtime service identity:
  WHO = deployer
  WHICH SA = runtime Cloud Run service identity
  WHERE = that SA resource (or documented project binding)
  ROLE = roles/iam.serviceAccountUser
Do not self-bind this by guess onto ketabebozorg-runner.

Build identity must be live-identified. Do not bind from a historical name.
Google current source-deploy default is the Compute Engine default SA unless overridden,
and that identity needs roles/run.builder. Method: identify actual build SA → verify it is used → then verify/grant run.builder.

Rung 4 APIs: run, cloudbuild, artifactregistry.
Private 401/403 is not service-down. /health must be authenticated.
URL is not PASS. /health is not Drive. Drive must read an authoritative KETABEBOZORG artifact.

Recovery: ACCESS → PROJECT → ACCOUNT → IAM AUTHORITY → PROJECT_NUMBER → IDENTITY APIs → POOL → PROVIDER → ISSUER → MAPPING → PROVIDER CONDITION → SA → PRINCIPALSET → WorkloadIdentityUser → WIF_PROVIDER → REREAD → CONFIGURED → AUTH-ONLY TEST → PASS → identify deployer → identify runtime SA → SA User → identify build SA → run.builder → Rung-4 APIs → deploy READ_ONLY → ZIP → build → revision READY → traffic → URL → runtime identity → authenticated /health → Drive → WRITE OFF → Scheduler OFF → RUNG 4 PASS

DO NOT DISPATCH UNTIL RUNG 3 CONFIGURATION IS COMPLETE.
DO NOT CALL RUNG 3 PASS UNTIL LIVE OIDC→STS→SA IMPERSONATION PASSES.
DO NOT MIX RUNG 4 BUILD/DEPLOY FAILURES WITH RUNG 3 IDENTITY.
