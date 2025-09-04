from agents.orchestrator import Orchestrator
from utils.logging_utils import log

if __name__ == "__main__":
    orch = Orchestrator()
    for case in ["io/cases/mumbai_case.json", "io/cases/pune_case.json"]:
        log("="*60)
        orch.run_case(case)
