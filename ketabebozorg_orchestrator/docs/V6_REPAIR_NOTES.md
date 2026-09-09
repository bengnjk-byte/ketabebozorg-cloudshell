# V6 Repair Notes

Frozen source: `KETABEBOZORG_DUAL_ORCHESTRATOR_V5.zip`
Frozen V5 SHA-256: `e1637a18ad583a3a9c6341b1f2306cab8267583245ec9fe3d4cd72300462bc1c`

The `520b…` package is an intermediate V6 candidate only. This tree is the named V6 repair.

## Trigger
Work FAIL_CLOSED was correct. F11 (stale owner after successor acquire) is closed on V5. The remaining defect is F12: check → expiry → commit. Owner A can pass `require_lease()`, the lease can expire before the Drive/Firestore write, and V5 still persists the write because the guard and the write are not one atomic operation.

Adding another `check_lease()` before or after the write does not close this window.

## Bounded repair
- `store.commit_authoritative(lease, kind, payload_hash, payload)` re-validates owner + fence_token + unreleased + `expires_at > commit-time` and inserts the receipt in the **same transaction**.
- Transport/Drive write path stages first (`STAGED_JSON`). Staging is never authority.
- Authoritative lists (`transitions`, Result Bus production records, `STATE_JSON`/`RESULT_JSON`) grow only after a successful receipt.
- Readers ignore staged lines. Once any `COMMIT_JSON` exists, unmatched state/result lines are ignored.
- Firestore uses a single transaction on the lock document + receipt document.
- SQLite uses one connection-level transaction around the lock SELECT and receipt INSERT.
- No manuscript mutation path. REV7 remains READ_ONLY. CE-I9 / CE-Q10 are not started.

## F12 invariant
A owns fence N → last ordinary validation passes → lease expires → A attempts commit → commit rejected atomically → authoritative writes = 0.

## Residuals A–E
A stale release cannot clobber successor; B F11 transition; C F11 result append; D zero-second lease; E F12 check-then-commit.
