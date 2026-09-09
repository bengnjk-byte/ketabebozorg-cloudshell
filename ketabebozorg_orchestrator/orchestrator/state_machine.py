from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from .models import Task, TaskStatus, Worker, WorkerResult, Reconciliation, SUCCESS_STATES

@dataclass
class TransitionDecision:
    next_status: TaskStatus
    reason: str
    next_owner: Worker | None = None

class MasterStateMachine:
    """Deterministic controller. It never treats blocked/failed peers as a satisfied barrier."""

    def evaluate_peer_barrier(self, task: Task, results: Dict[Worker, WorkerResult]) -> TransitionDecision:
        if task.ben_only:
            return TransitionDecision(TaskStatus.BEN_DECISION_REQUIRED, "Ben-only gate", Worker.BEN)
        if not task.peer_barrier_required:
            return TransitionDecision(TaskStatus.RECONCILING, "Peer barrier disabled", Worker.CE_C0)
        expected = set(task.owners)
        present = {w for w, r in results.items() if r.task_id == task.task_id and r.result_state in SUCCESS_STATES}
        missing = expected - present
        if missing:
            return TransitionDecision(TaskStatus.WAITING_FOR_PEER_RESULT, f"Waiting for successful peer results: {sorted(x.value for x in missing)}")
        return TransitionDecision(TaskStatus.RECONCILING, "All required successful peer results present", Worker.CE_C0)

    def after_reconciliation(self, task: Task, rec: Reconciliation) -> TransitionDecision:
        if rec.unresolved or rec.conflicts or rec.chatgpt_only or rec.grok_only:
            return TransitionDecision(TaskStatus.CROSSCHECK, "Differences/conflicts require mandatory cross-check")
        if task.gap_search_required:
            return TransitionDecision(TaskStatus.GAP_SEARCH, "Run bounded adversarial gap search")
        return TransitionDecision(TaskStatus.COMPLETE, "Reconciliation complete")

    def after_crosscheck(self, task: Task, unresolved_count: int) -> TransitionDecision:
        if unresolved_count:
            return TransitionDecision(TaskStatus.HOLD, "Unresolved conflict remains after cross-check", Worker.CE_C0)
        if task.gap_search_required:
            return TransitionDecision(TaskStatus.GAP_SEARCH, "Cross-check clear; perform bounded gap search")
        return TransitionDecision(TaskStatus.COMPLETE, "Cross-check clear")

    def after_gap_search(self, new_findings: int, unresolved: int, round_no: int, max_rounds: int) -> TransitionDecision:
        if unresolved:
            return TransitionDecision(TaskStatus.CROSSCHECK, "Gap search created unresolved findings")
        if new_findings:
            if round_no >= max_rounds:
                return TransitionDecision(TaskStatus.HOLD, "Gap-search round limit reached with new material evidence", Worker.CE_C0)
            return TransitionDecision(TaskStatus.RECONCILING, "Gap search found new evidence; reconcile again", Worker.CE_C0)
        return TransitionDecision(TaskStatus.COMPLETE, "No material gaps found")
