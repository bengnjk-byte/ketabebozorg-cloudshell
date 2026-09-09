"""V6 atomic commit-time fencing.

Authority is a receipt created in the same transaction that re-validates
owner + fence_token + unreleased + expires_at > commit-time.

Staged Drive/transport lines without a matching receipt are not authoritative.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import hashlib, json


STAGED_PREFIX = 'STAGED_JSON '
COMMIT_PREFIX = 'COMMIT_JSON '


def payload_hash(payload) -> str:
    if isinstance(payload, str):
        raw = payload.encode()
    else:
        raw = json.dumps(payload, sort_keys=True, default=str, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def receipt_id_for(*, kind: str, payload_hash: str, owner: str, fence_token: int, committed_at: datetime) -> str:
    raw = f'{kind}|{payload_hash}|{owner}|{fence_token}|{committed_at.isoformat()}'
    return hashlib.sha256(raw.encode()).hexdigest()


@dataclass(frozen=True)
class CommitReceipt:
    receipt_id: str
    kind: str
    payload_hash: str
    resource: str
    owner: str
    fence_token: int
    committed_at: datetime

    def as_dict(self) -> dict:
        return {
            'receipt_id': self.receipt_id,
            'kind': self.kind,
            'payload_hash': self.payload_hash,
            'resource': self.resource,
            'owner': self.owner,
            'fence_token': self.fence_token,
            'committed_at': self.committed_at.isoformat(),
        }
