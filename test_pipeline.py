import json, os
from agents.orchestrator import Orchestrator

def test_run():
    orch = Orchestrator()
    out_json, obj = orch.run_case("io/cases/mumbai_case.json")
    assert os.path.exists(out_json)
    data = json.load(open(out_json, "r", encoding="utf-8"))
    assert "calc" in data and "selected_rules" in data
