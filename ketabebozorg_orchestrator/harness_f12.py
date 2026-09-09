"""Exact F12 regression harness. No network. Exit 0 only if invariant holds.

A owns fence N.
A passes its last ordinary validation.
Lease expires before authoritative commit.
A attempts commit.
Commit MUST be rejected atomically.
authoritative writes = 0.
Staged data may exist and must not be authoritative.
"""
from __future__ import annotations
import json, sys, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))

from orchestrator.commit import payload_hash
from orchestrator.engine import Engine
from orchestrator.models import Task, Worker
from orchestrator.simulation import ScriptedAdapter
from orchestrator.store import SQLiteStore, LeaseLostError
from orchestrator.transport import LocalSimulationTransport


def expire(st, resource='GLOBAL_TICK'):
    with st._conn() as c:
        c.execute('UPDATE locks SET expires_at=? WHERE resource=?',
                  ((datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat(), resource))


def run():
    with tempfile.TemporaryDirectory() as td:
        st=SQLiteStore(Path(td)/'s.sqlite')
        task=Task(task_id='AUDIT',command_id='AUDIT-CMD',title='x',scope='x',gap_search_required=False)
        tr=LocalSimulationTransport([task])
        eng=Engine(tr,st,{w:ScriptedAdapter(w,{}) for w in (Worker.CHATGPT,Worker.GROK)})
        lease_a=st.acquire_lease('GLOBAL_TICK','A',60)
        assert lease_a is not None
        fence_n=lease_a.fence_token
        guard=lambda: st.require_lease(lease_a)
        tr.set_write_guard(guard); eng.set_lease_guard(guard,lease_a)

        st.require_lease(lease_a)  # last ordinary validation PASSES
        real=st.commit_authoritative
        def raced(lease, kind, h, payload=None):
            expire(st)
            return real(lease, kind, h, payload)
        st.commit_authoritative=raced
        lost=False
        try:
            eng.tick()
        except LeaseLostError:
            lost=True
        rec={'task_id':'AUDIT','status':'COMPLETE','reason':'F12'}
        direct_lost=False
        try:
            st.commit_authoritative(lease_a,'STATE',payload_hash(rec),rec)
        except LeaseLostError:
            direct_lost=True
        out={
            'probe':'F12',
            'fence_n':fence_n,
            'ordinary_validation':'PASS',
            'lease_expired_before_commit':True,
            'commit_rejected_atomically':lost and direct_lost,
            'authoritative_writes':len(tr.transitions)+st.receipt_count(),
            'staged_count':len(tr.staged),
            'receipt_count':st.receipt_count(),
            'transitions':tr.transitions,
        }
        out['safety_pass']=(lost and direct_lost and out['authoritative_writes']==0
                            and not tr.transitions and st.receipt_count()==0)
        print(json.dumps(out, indent=2, default=str))
        return out['safety_pass']


if __name__=='__main__':
    raise SystemExit(0 if run() else 1)
