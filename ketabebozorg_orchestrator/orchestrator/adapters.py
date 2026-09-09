from __future__ import annotations
import hashlib, json, os
from abc import ABC, abstractmethod
from openai import OpenAI
from .models import WorkerResult, Worker, Phase, ResultState
from .prompts import worker_prompt

class ModelAdapter(ABC):
    @abstractmethod
    def run(self, *, task, worker: Worker, phase: Phase, round_no: int, attempt: int,
            peer_findings=None, accepted=None, rejected=None) -> WorkerResult: ...

class ResponsesAdapter(ModelAdapter):
    def __init__(self, *, api_key_env: str, model: str, worker: Worker,
                 base_url: str | None = None, evidence_provider=None,
                 max_tool_steps: int = 12, timeout_seconds: int = 180):
        self.api_key_env = api_key_env
        self.model = model
        self.worker = worker
        self.base_url = base_url
        self.evidence_provider = evidence_provider
        self.max_tool_steps = max_tool_steps
        self.timeout_seconds = timeout_seconds

    def _client(self):
        key = os.environ.get(self.api_key_env)
        if not key:
            raise RuntimeError(f"Missing {self.api_key_env}")
        kw = {'api_key': key, 'timeout': self.timeout_seconds}
        if self.base_url:
            kw['base_url'] = self.base_url
        return OpenAI(**kw)

    def run(self, *, task, worker: Worker, phase: Phase, round_no: int, attempt: int,
            peer_findings=None, accepted=None, rejected=None) -> WorkerResult:
        if worker != self.worker:
            raise RuntimeError('ADAPTER_WORKER_MISMATCH')
        client = self._client()
        history: list[dict] = []
        for step in range(self.max_tool_steps + 1):
            prompt = worker_prompt(task, worker, phase, round_no, peer_findings, accepted, rejected, history)
            response = client.responses.create(model=self.model, input=prompt)
            text = getattr(response, 'output_text', '') or ''
            try:
                data = json.loads(text)
            except Exception as e:
                raise RuntimeError(f'MODEL_NON_JSON_OUTPUT:{type(e).__name__}')
            if data.get('kind') == 'tool_request':
                if not self.evidence_provider:
                    raise RuntimeError('MODEL_REQUESTED_DRIVE_TOOL_WITHOUT_PROVIDER')
                if step >= self.max_tool_steps:
                    raise RuntimeError('MODEL_TOOL_STEP_LIMIT')
                tool = str(data.get('tool',''))
                if not tool.startswith('drive_'):
                    raise RuntimeError('MODEL_REQUESTED_NON_DRIVE_TOOL')
                out = self.evidence_provider.execute(tool, data.get('args') or {})
                history.append({'tool': tool, 'args': data.get('args') or {}, 'reason': data.get('reason',''), 'result': out})
                continue
            returned_task = data.get('task_id')
            if returned_task != task.task_id:
                return WorkerResult(
                    task_id=str(returned_task or 'MISSING_TASK_ID'), command_id=task.command_id,
                    worker=worker, phase=phase, round=round_no, attempt=attempt,
                    result_state=ResultState.FAIL, blockers=['TASK_ID_BINDING_MISMATCH'],
                    notes=f'Expected {task.task_id}; model returned {returned_task!r}'
                )
            data['worker'] = worker.value
            data['phase'] = phase.value
            data['round'] = round_no
            data['attempt'] = attempt
            data['command_id'] = task.command_id or task.task_id
            return WorkerResult.model_validate(data)
        raise RuntimeError('MODEL_TOOL_LOOP_EXHAUSTED')

class ChatGPTAdapter(ResponsesAdapter):
    def __init__(self, evidence_provider=None, model: str | None = None):
        super().__init__(api_key_env='OPENAI_API_KEY', model=model or os.getenv('OPENAI_MODEL','gpt-5.6-sol'), worker=Worker.CHATGPT, evidence_provider=evidence_provider)

class GrokAdapter(ResponsesAdapter):
    def __init__(self, evidence_provider=None, model: str | None = None):
        super().__init__(api_key_env='XAI_API_KEY', model=model or os.getenv('XAI_MODEL','grok-4.6'), worker=Worker.GROK, base_url=os.getenv('XAI_BASE_URL','https://api.x.ai/v1'), evidence_provider=evidence_provider)
