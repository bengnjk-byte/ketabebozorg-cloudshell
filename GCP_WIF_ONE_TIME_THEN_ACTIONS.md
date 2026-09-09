KETABEBOZORG · WHAT TO WRITE AND WHERE
ONE HUMAN COPY-PASTE. AFTER THIS, GITHUB ACTIONS DEPLOYS.
DATE: 2026-09-10
MODE AFTER BIND: CONNECTED_READ_ONLY ONLY
DO NOT: JSON key, CONTROLLED_WRITE, Scheduler, I9, Q10, REV7

WHERE YOU TYPE
Google Cloud Shell of project ketabebozorg-orchestrator
or a terminal already logged in as Owner / IAM Admin of that project.
Not ChatGPT. Not this Grok chat. Not Drive.

Paste BLOCK A from this file, then set GitHub Actions variable:
  WIF_PROVIDER = projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
Put KETABEBOZORG_DUAL_ORCHESTRATOR_V6.zip in the repo root or a Release.
SHA-256 daede0951db98e8442bb44e43eae64c1bf1e237082dec7cd51140129b05b87f2
Run workflow deploy-readonly. Do not enable WRITE.
