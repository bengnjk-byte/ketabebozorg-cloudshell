# Deployment gates

1. SIMULATION: `python main.py --simulate-once` and pytest must pass.
2. CONNECTED_READ_ONLY: runtime service account can read the four live control documents and empty machine registry/state log; no Drive writes.
3. OpenAI live self-test passes.
4. Grok live self-test passes with the same TASK_ID.
5. Deterministic reconciliation/cross-check/gap tests pass.
6. RESULT_BUS_TEST: append one harmless `DEPLOYMENT-SELFTEST` record and verify exact readback.
7. CONTROLLED_WRITE: enable only Result Bus and state-log writes; manuscript mutation remains unavailable.
8. Create Cloud Scheduler authenticated invocation for `/tick` only after the previous gates pass.
9. Keep production task registry empty until a live CE-C0-authorized machine task is appended. Do not convert historical/manual `NEW` text into authority automatically.
10. I9/Q10/final release remain governed by live Drive; Ben-only release cannot be automated.



V6 gate: `audit_v6_safety.py .`, `audit_residuals.py .`, and `harness_f12.py` must pass with F12 authoritative writes = 0 before any connected deployment. Do not treat a modified 520b package as frozen V5. Do not deploy until independent Work preflight on the named V6 ZIP passes.
