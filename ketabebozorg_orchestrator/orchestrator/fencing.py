from __future__ import annotations
import json
from .models import WorkerResult
from .commit import STAGED_PREFIX, COMMIT_PREFIX, payload_hash

STATE_PREFIX='STATE_JSON '
RESULT_PREFIX='RESULT_JSON '
FENCE_PREFIX='FENCE_JSON '
GLOBAL_FENCE_RESOURCE='GLOBAL_TICK'


def _parse_commits(text: str):
    receipts={}
    for line in text.splitlines():
        if not line.startswith(COMMIT_PREFIX): continue
        try: rec=json.loads(line[len(COMMIT_PREFIX):])
        except json.JSONDecodeError as e: raise RuntimeError(f'MALFORMED_COMMIT_JSON:{e}')
        h=rec.get('payload_hash')
        if h: receipts[h]=rec
    return receipts


def state_records_with_fencing(text: str):
    accepted=[]; active_fence=0
    receipts=_parse_commits(text)
    require_receipt=bool(receipts)
    for line in text.splitlines():
        if line.startswith(STAGED_PREFIX):
            continue
        if line.startswith(COMMIT_PREFIX):
            continue
        if line.startswith(FENCE_PREFIX):
            try: rec=json.loads(line[len(FENCE_PREFIX):])
            except json.JSONDecodeError as e: raise RuntimeError(f'MALFORMED_FENCE_JSON:{e}')
            if rec.get('resource')==GLOBAL_FENCE_RESOURCE:
                active_fence=max(active_fence,int(rec.get('fence_token') or 0))
            continue
        if not line.startswith(STATE_PREFIX): continue
        try: rec=json.loads(line[len(STATE_PREFIX):])
        except json.JSONDecodeError as e: raise RuntimeError(f'MALFORMED_STATE_JSON:{e}')
        if require_receipt:
            h=rec.get('payload_hash') or payload_hash({k:v for k,v in rec.items() if k not in {'commit_receipt_id','payload_hash'}})
            if h not in receipts: continue
        if active_fence:
            if rec.get('fence_resource') != GLOBAL_FENCE_RESOURCE: continue
            if int(rec.get('lease_fence') or 0) < active_fence: continue
        accepted.append(rec)
    return accepted


def result_records_with_fencing(text: str):
    accepted=[]; active_fence=0
    receipts=_parse_commits(text)
    require_receipt=bool(receipts)
    for line in text.splitlines():
        if line.startswith(STAGED_PREFIX):
            continue
        if line.startswith(COMMIT_PREFIX):
            continue
        if line.startswith(FENCE_PREFIX):
            try: rec=json.loads(line[len(FENCE_PREFIX):])
            except json.JSONDecodeError as e: raise RuntimeError(f'MALFORMED_FENCE_JSON:{e}')
            if rec.get('resource')==GLOBAL_FENCE_RESOURCE:
                active_fence=max(active_fence,int(rec.get('fence_token') or 0))
            continue
        if not line.startswith(RESULT_PREFIX): continue
        try: raw=json.loads(line[len(RESULT_PREFIX):])
        except json.JSONDecodeError as e: raise RuntimeError(f'MALFORMED_RESULT_JSON:{e}')
        if require_receipt:
            h=raw.get('payload_hash') or payload_hash({k:v for k,v in raw.items() if k not in {'commit_receipt_id','payload_hash'}})
            if h not in receipts and raw.get('task_id') != 'DEPLOYMENT-SELFTEST': continue
        try: result=WorkerResult.model_validate(raw)
        except Exception:
            continue
        if active_fence and result.task_id != 'DEPLOYMENT-SELFTEST':
            if result.fence_resource != GLOBAL_FENCE_RESOURCE: continue
            if int(result.lease_fence or 0) < active_fence: continue
        accepted.append(result)
    return accepted
