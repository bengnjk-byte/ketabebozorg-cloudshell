from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Worker(str, Enum):
    CHATGPT = "CHATGPT"
    GROK = "GROK"
    CE_C0 = "CE_C0"
    BEN = "BEN"

class Phase(str, Enum):
    PRIMARY = "PRIMARY"
    CROSSCHECK = "CROSSCHECK"
    GAP_SEARCH = "GAP_SEARCH"

class TaskStatus(str, Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING_FOR_PEER_RESULT = "WAITING_FOR_PEER_RESULT"
    RECONCILING = "RECONCILING"
    CROSSCHECK = "CROSSCHECK"
    GAP_SEARCH = "GAP_SEARCH"
    BLOCKED = "BLOCKED"
    HOLD = "HOLD"
    COMPLETE = "COMPLETE"
    BEN_DECISION_REQUIRED = "BEN_DECISION_REQUIRED"

class ResultState(str, Enum):
    PASS = "PASS"
    PARTIAL_PASS = "PARTIAL_PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NO_QUALIFYING_EVIDENCE = "NO_QUALIFYING_EVIDENCE"

SUCCESS_STATES = {ResultState.PASS, ResultState.PARTIAL_PASS, ResultState.NO_QUALIFYING_EVIDENCE}

class Finding(BaseModel):
    key: str
    summary: str
    block_uid: Optional[str] = None
    evidence_ids: List[str] = Field(default_factory=list)
    content_sha256: Optional[str] = None
    owner: Optional[str] = None
    provenance: Optional[str] = None
    confidence: float = 0.5
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkerResult(BaseModel):
    task_id: str
    command_id: Optional[str] = None
    worker: Worker
    phase: Phase = Phase.PRIMARY
    round: int = 0
    attempt: int = 1
    result_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    result_state: ResultState
    findings: List[Finding] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    notes: str = ""
    fence_resource: Optional[str] = None
    lease_owner: Optional[str] = None
    lease_fence: Optional[int] = None

class Task(BaseModel):
    task_id: str
    command_id: Optional[str] = None
    title: str
    scope: str
    owners: List[Worker] = Field(default_factory=lambda: [Worker.CHATGPT, Worker.GROK])
    status: TaskStatus = TaskStatus.READY
    dependencies: List[str] = Field(default_factory=list)
    do_not_redo: List[str] = Field(default_factory=list)
    ben_only: bool = False
    peer_barrier_required: bool = True
    gap_search_required: bool = True
    quality_gate: str = "publication_grade"
    max_attempts: int = 2
    max_gap_rounds: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Reconciliation(BaseModel):
    task_id: str
    common: List[Finding] = Field(default_factory=list)
    chatgpt_only: List[Finding] = Field(default_factory=list)
    grok_only: List[Finding] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    accepted: List[Finding] = Field(default_factory=list)
    rejected: List[Finding] = Field(default_factory=list)
    unresolved: List[str] = Field(default_factory=list)
