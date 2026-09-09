KETABEBOZORG official program ladder 2026-09-10
Authority: CE-C0 canonical reassessment.
Book lane separate. REV7 UNCHANGED. I9/Q10 HOLD.

CURRENT VERIFIED STATE
Rung 1   Drive Lite                  DONE
Rung 2A  Frozen ZIP / Drive          DONE
Rung 2B  Exact bytes → runner        DONE — DO NOT REOPEN
Rung 3   WIF / GCP identity          OPEN
Rung 3 CONFIGURED                    NO
Rung 3 PASS                          NO
Rung 4   Cloud Run READ_ONLY         WAITING FOR RUNG 3 / NOT STARTED
GitHub OIDC capability               READY
Live OIDC token                      NOT YET OBSERVED
WIF_PROVIDER                         UNSET
GCP WIF pool                         UNKNOWN
GCP WIF provider                     UNKNOWN
Repository restriction               UNKNOWN
Service account                      UNKNOWN
WorkloadIdentityUser binding         UNKNOWN
Cloud Run URL                        NONE VERIFIED
/health                              NOT TESTED
Runtime identity                     NOT VERIFIED
Runtime Drive read                   NOT VERIFIED
WRITE                                OFF
Scheduler                            OFF
REV7                                 UNCHANGED

CONFIRMED ERRORS ONLY
1. CLOUD_ACCESS_BLOCKED — Cloud Browser never reached Console or login.
   No GCP inspection or mutation. Not WIF_FAILED. WIF was never reached.
2. WIF_PROVIDER UNSET — fail-closes before authentication.
   Expected: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider

POSSIBLE Rung 3 until live GCP evidence: wrong account, project state, IAM authority,
identity APIs, missing/wrong pool or provider, issuer, mapping, admission condition,
principalSet, disabled SA, org policy, Actions policy, variable location/value,
IAM delay, token exchange mismatch.
POSSIBLE Rung 4 only after PASS: Run/Build/AR APIs and roles, region, billing,
source build, startup, private 401/403, revision/traffic, runtime SA, Drive share,
accidental WRITE, stale Scheduler/services.

2B remains CLOSED. Do not change 2B because Rung 3 is unresolved.
First identity test: workflow rung3-auth. deploy-readonly is Rung 4.
Keep auth@v2. No JSON key. No public service. No pool-wide trust.

Recovery: ACCESS → PROJECT → IAM AUTHORITY → APIs → POOL → PROVIDER → MAPPING → PROVIDER CONDITION → SERVICE ACCOUNT → REPO-SCOPED IAM → WIF_PROVIDER → AUTH TEST → RUNG 3 PASS → CLOUD RUN → HEALTH → DRIVE
First unresolved external dependency: authenticated GCP control-plane access.
Do not dispatch while WIF_PROVIDER is UNSET.
Do not invent SERVICE_URL. Do not open WRITE, Scheduler, I9, Q10. Do not reopen 2B.
