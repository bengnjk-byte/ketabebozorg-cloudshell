from __future__ import annotations
import json
from orchestrator.simulation import run_simulation_suite
if __name__ == '__main__':
    out=run_simulation_suite()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out['passed'] else 1)
