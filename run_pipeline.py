from agents.orchestrator import Orchestrator
from utils.logging_utils import log
from pathlib import Path
import time

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent

    cases = [
        BASE_DIR / "io" / "cases" / "mumbai_case.json",
        BASE_DIR / "io" / "cases" / "pune_case.json",
    ]

    orch = Orchestrator()
    for case in cases:
        log("=" * 60)
        orch.run_case(str(case))

    print("Pipeline done. Keeping service alive for Render free tier.")
    while True:
        time.sleep(3600)
