# V5 Repair Notes

## Trigger
Independent Work preflight on exact V4 reproduced residual probe B: an expired GLOBAL_TICK owner could persist `AUDIT -> COMPLETE` after a successor acquired the lease. V4 deployment was correctly stopped.

## Bounded repair
- Added monotonic fenced leases (`Lease.fence_token`).
- Live `/tick` uses exact owner+fence+expiry validation, not a boolean lease alone.
- Guard checks wrap Engine cache/result/state mutation boundaries and Google Drive mutation boundaries.
- Before actionable controlled work, `/tick` claims the fence on both Drive authoritative sinks.
- Result Bus and state transition records carry fence metadata.
- Drive readers preserve pre-fence history but reject lower-fence/unfenced production records appended after a newer GLOBAL_TICK fence claim.
- Idle ticks do not append fence records.
- Added direct successor-takeover and zero-second-lease regression tests.

No manuscript mutation path was added. REV7 remains READ_ONLY.
