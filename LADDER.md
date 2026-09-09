KETABEBOZORG official program ladder 2026-09-10
Seal: CE-C0_RUNG3_PROCEDURE_CORRECTED_2026-09-10
Replaces prior Rung-4 role-assignment guesses.
Book lane separate. REV7 UNCHANGED.

Rung 1   Drive Lite                  DONE
Rung 2A  Frozen ZIP / Drive          DONE
Rung 2B  Exact bytes → runner        DONE — DO NOT REOPEN
Rung 3   WIF / GCP identity          OPEN
Rung 3 CONFIGURED                    NO
Rung 3 PASS                          NO
Rung 4   Cloud Run READ_ONLY         WAITING FOR RUNG 3
GitHub OIDC capability               READY
Live OIDC token                      NOT YET OBSERVED
GCP project access                   NOT VERIFIED
github-pool                          UNKNOWN
github-provider                      UNKNOWN
Provider admission condition         UNKNOWN
Repository-scoped IAM binding        UNKNOWN
Service account                      UNKNOWN
WIF_PROVIDER                         UNSET
Cloud Run URL                        NONE VERIFIED
/health                              NOT TESTED
Runtime identity                     NOT VERIFIED
Runtime Drive read                   NOT VERIFIED
WRITE                                OFF
Scheduler                            OFF
REV7                                 UNCHANGED

CONFIRMED 1: CLOUD_ACCESS_BLOCKED — not WIF_FAILED. All GCP items stay UNKNOWN until live-read.
CONFIRMED 2: WIF_PROVIDER UNSET — full name with numeric PROJECT_NUMBER required.

TWO LAYERS: provider admission on bengnjk-byte/ketabebozorg-cloudshell AND repo-scoped WorkloadIdentityUser.
CONFIGURED ≠ PASS. First identity test = rung3-auth. deploy-readonly is Rung 4 after PASS.

RUNG 4 ROLES — NOT GUESSED ONTO RUNTIME SA
Deployer = identity the workflow impersonates after WIF.
On deployer (after live doc confirmation): run.sourceDeveloper, serviceUsageConsumer.
roles/iam.serviceAccountUser: TO deployer, ON runtime Cloud Run service identity.
Build SA: live-identify first. Default in current Google source-deploy docs is Compute Engine default SA unless overridden; that identity needs run.builder. Identify → verify used → then grant/verify.

DO NOT REOPEN 2B
DO NOT DISPATCH UNTIL RUNG 3 CONFIGURATION IS COMPLETE
DO NOT CALL RUNG 3 PASS UNTIL LIVE OIDC→STS→SA IMPERSONATION PASSES
DO NOT MIX RUNG 4 BUILD/DEPLOY FAILURES WITH RUNG 3 IDENTITY
