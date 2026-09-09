from __future__ import annotations
import tempfile
from .models import Task, Worker, WorkerResult, ResultState, Finding, Phase, TaskStatus
from .transport import LocalSimulationTransport
from .store import SQLiteStore
from .engine import Engine
from .state_machine import MasterStateMachine
from .reconcile import reconcile

class ScriptedAdapter:
    def __init__(self, worker, script): self.worker=worker; self.script=script; self.calls=[]
    def run(self, **kw):
        self.calls.append((kw['phase'],kw['round_no'],kw['attempt']))
        key=(kw['phase'].value,kw['round_no'],kw['attempt'])
        spec=self.script.get(key,self.script.get((kw['phase'].value,kw['round_no'],'*'),{}))
        findings=[Finding.model_validate(x) for x in spec.get('findings',[])]
        return WorkerResult(task_id=kw['task'].task_id,worker=self.worker,phase=kw['phase'],round=kw['round_no'],attempt=kw['attempt'],
                            result_state=ResultState(spec.get('result_state','PASS')),findings=findings,blockers=spec.get('blockers',[]))

def run_simulation_suite():
    checks={}
    sm=MasterStateMachine(); t=Task(task_id='T',title='x',scope='x',owners=[Worker.CHATGPT,Worker.GROK])
    blocked={Worker.CHATGPT:WorkerResult(task_id='T',worker=Worker.CHATGPT,result_state=ResultState.BLOCKED),Worker.GROK:WorkerResult(task_id='T',worker=Worker.GROK,result_state=ResultState.BLOCKED)}
    checks['blocked_peers_do_not_satisfy_barrier']=sm.evaluate_peer_barrier(t,blocked).next_status==TaskStatus.WAITING_FOR_PEER_RESULT
    wrong1=WorkerResult(task_id='UNRELATED',worker=Worker.CHATGPT,result_state=ResultState.PASS)
    wrong2=WorkerResult(task_id='UNRELATED',worker=Worker.GROK,result_state=ResultState.PASS)
    checks['wrong_task_rejected']=reconcile('T',wrong1,wrong2).unresolved==['TASK_ID_BINDING_MISMATCH']

    with tempfile.TemporaryDirectory() as td:
        tr=LocalSimulationTransport([t]); st=SQLiteStore(td+'/s.sqlite')
        cg=ScriptedAdapter(Worker.CHATGPT,{('PRIMARY',0,'*'):{'findings':[{'key':'A','summary':'a'}]},('CROSSCHECK',0,'*'):{'findings':[{'key':'B','summary':'b','metadata':{'crosscheck_verdict':'CONFIRMED'}}]},('GAP_SEARCH',1,'*'):{'result_state':'NO_QUALIFYING_EVIDENCE'}})
        gr=ScriptedAdapter(Worker.GROK,{('PRIMARY',0,'*'):{'findings':[{'key':'B','summary':'b'}]},('CROSSCHECK',0,'*'):{'findings':[{'key':'A','summary':'a','metadata':{'crosscheck_verdict':'CONFIRMED'}}]},('GAP_SEARCH',1,'*'):{'result_state':'NO_QUALIFYING_EVIDENCE'}})
        e=Engine(tr,st,{Worker.CHATGPT:cg,Worker.GROK:gr})
        for _ in range(4): e.tick()
        checks['crosscheck_invoked']=any(c[0]==Phase.CROSSCHECK for c in cg.calls) and any(c[0]==Phase.CROSSCHECK for c in gr.calls)
        checks['gap_search_invoked']=any(c[0]==Phase.GAP_SEARCH for c in cg.calls) and any(c[0]==Phase.GAP_SEARCH for c in gr.calls)
        checks['task_completes_after_clean_gap']=any(x['status']=='COMPLETE' for x in tr.transitions)

    with tempfile.TemporaryDirectory() as td:
        t2=Task(task_id='B',title='x',scope='x',owners=[Worker.CHATGPT,Worker.GROK],max_attempts=2)
        tr=LocalSimulationTransport([t2]); st=SQLiteStore(td+'/s.sqlite')
        bad=ScriptedAdapter(Worker.CHATGPT,{('PRIMARY',0,'*'):{'result_state':'BLOCKED','blockers':['NO_EVIDENCE']}})
        bad2=ScriptedAdapter(Worker.GROK,{('PRIMARY',0,'*'):{'result_state':'BLOCKED','blockers':['NO_EVIDENCE']}})
        e=Engine(tr,st,{Worker.CHATGPT:bad,Worker.GROK:bad2}); e.tick(); e.tick()
        checks['blocked_results_fail_closed']=any(x['status']=='BLOCKED' for x in tr.transitions) and not any(x['status']=='GAP_SEARCH' for x in tr.transitions)

    return {'passed':all(checks.values()),'checks':checks}
