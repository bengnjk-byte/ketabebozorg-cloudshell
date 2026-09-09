# V4 bounded repair notes

Source archive: `KETABEBOZORG_DUAL_ORCHESTRATOR_V3.zip`
Verified source SHA-256: `6be18fa40b1f59a957df2740b6a0fb6f71e0d34b18fa5a9a585eeecec12bdaef`

V3 was not deployed. Three additional offline safety defects were independently reproduced before repair:

1. Firestore `results_for(..., command_id=...)` returned results from other COMMAND_ID values.
2. When a completed gap round discovered new material, the next tick compared that round against an effective evidence set that already included it, misclassified it as clean, and could emit COMPLETE without a subsequent final gap search.
3. Firestore lock release used non-transactional owner-read then delete; a successor lease acquired in the race window could be deleted by the stale owner.

V4 repairs only these bounded defects and preserves V3's seven prior fixes. No deployment, Drive production mutation, manuscript mutation, REV7 mutation, Scheduler change, or secret access is part of this repair.

Regression evidence is stored under `evidence/` and `audit_v4_safety.py` exercises all ten known safety regressions offline.
