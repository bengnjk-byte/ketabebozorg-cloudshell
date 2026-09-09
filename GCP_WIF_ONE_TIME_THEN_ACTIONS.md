KETABEBOZORG · WHAT TO WRITE AND WHERE
DATE: 2026-09-10
MODE AFTER BIND: CONNECTED_READ_ONLY ONLY
DO NOT: JSON key, CONTROLLED_WRITE, Scheduler, I9, Q10, REV7 mutation
DO NOT: treat helper subtree as frozen V6
DO NOT: invent SERVICE_URL

2A is DONE on Drive. Exact ZIP SHA-256:
  daede0951db98e8442bb44e43eae64c1bf1e237082dec7cd51140129b05b87f2
  Drive file 1oe7AE_PD0WvbcMh8qUjS9YbWRUj7qwlk

2B remains automation: make those exact bytes visible to the GitHub runner.
Do not convert 2B into manual Ben upload unless connector-safe transfer is exhausted.

3 is the only inherently identity-bound step: GitHub↔GCP WIF for
  repo bengnjk-byte/ketabebozorg-cloudshell
  project ketabebozorg-orchestrator
  runtime SA ketabebozorg-runner@ketabebozorg-orchestrator.iam.gserviceaccount.com
  GitHub Actions variable WIF_PROVIDER

After 2B and 3 exist, Run workflow deploy-readonly.
Do not enable WRITE.
