from __future__ import annotations
import json
from .models import Task, Worker, Phase, Finding

OUTPUT_CONTRACT = '''Return JSON only. Final-result schema:
{
  "task_id": "exact TASK_ID",
  "result_state": "PASS|PARTIAL_PASS|FAIL|BLOCKED|NO_QUALIFYING_EVIDENCE",
  "findings": [{"key":"...","summary":"...","block_uid":null,"evidence_ids":[],"content_sha256":null,"owner":null,"provenance":null,"confidence":0.0,"metadata":{}}],
  "blockers": [], "evidence_ids": [], "notes": ""
}
Never invent Drive evidence. If evidence cannot be verified, return BLOCKED or NO_QUALIFYING_EVIDENCE.
Any PROVEN_ABSENT claim must carry metadata.absence_evidence with all six methods: parent_listing, title_variants, full_text_phrase, cross_naming, compiled_container_inspection, alternate_extension_search.
Synthetic transcripts/padding are forbidden. stable block_uid and content_sha256 are separate.
For publication_candidate=true, exact content_sha256, privacy_status=PASS, privacy_sha256 equal to content_sha256, and quality_status=PASS are required.'''

TOOL_CONTRACT = '''You may request read-only Drive evidence before finalizing. A tool request must be JSON only:
{"kind":"tool_request","tool":"drive_search|drive_list_folder|drive_read|drive_find|drive_metadata","args":{...},"reason":"..."}
The host will execute it and return TOOL_RESULT. Do not request write/delete/share/mutation tools.'''

def worker_prompt(task: Task, worker: Worker, phase: Phase, round_no: int = 0,
                  peer_findings: list[Finding] | None = None,
                  accepted: list[Finding] | None = None,
                  rejected: list[Finding] | None = None,
                  tool_history: list[dict] | None = None) -> str:
    base = f'''PROJECT: KETABEBOZORG\nTASK_ID: {task.task_id}\nCOMMAND_ID: {task.command_id or task.task_id}\nWORKER: {worker.value}\nPHASE: {phase.value}\nROUND: {round_no}\nSCOPE:\n{task.scope}\nQUALITY_GATE: {task.quality_gate}\nDO_NOT_REDO: {json.dumps(task.do_not_redo, ensure_ascii=False)}\n\n'''
    if phase == Phase.CROSSCHECK:
        base += 'MANDATORY CROSSCHECK: independently verify/challenge the peer-only or conflicting findings. For every supplied key, return a finding with metadata.crosscheck_verdict exactly CONFIRMED, REJECTED, or UNRESOLVED. Do not merely restate the peer.\nPEER_FINDINGS:\n' + json.dumps([f.model_dump() for f in (peer_findings or [])], ensure_ascii=False) + '\n'
    elif phase == Phase.GAP_SEARCH:
        base += 'ADVERSARIAL GAP SEARCH: search specifically for material evidence both prior workers may have missed. Return only materially new evidence. If none exists, use NO_QUALIFYING_EVIDENCE with findings=[].\nACCEPTED_SO_FAR:\n' + json.dumps([f.model_dump() for f in (accepted or [])], ensure_ascii=False) + '\nREJECTED_SO_FAR:\n' + json.dumps([f.model_dump() for f in (rejected or [])], ensure_ascii=False) + '\n'
    if tool_history:
        base += '\nREAD_ONLY TOOL HISTORY:\n' + json.dumps(tool_history, ensure_ascii=False) + '\n'
    return base + '\n' + TOOL_CONTRACT + '\n' + OUTPUT_CONTRACT
