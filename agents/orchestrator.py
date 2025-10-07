import sys
import os
import json
from pathlib import Path

# Ensure project root is in Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import agents (all in same folder)
from agents.input_agent import InputAgent
from agents.fetch_agent import FetchAgent
from agents.parse_agent import ParseAgent
from agents.classify_agent import RuleClassifierAgent
from agents.calc_agent import CalcAgent
from agents.rl_agent import RLAgent

from geometry.export_geometry import export_from_results
from utils.logging_utils import log
from config import RULES_PATH, OUTPUT_DIR, GEOM_EXPORT_DIR

class Orchestrator:
    def __init__(self):
        self.input_agent = InputAgent()
        self.fetch_agent = FetchAgent()
        self.parse_agent = ParseAgent()
        self.classify_agent = RuleClassifierAgent(RULES_PATH)
        self.calc_agent = CalcAgent(RULES_PATH)
        self.rl_agent = RLAgent()

        # Ensure output directories exist
        Path(OUTPUT_DIR, "json").mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_DIR, "geometry").mkdir(parents=True, exist_ok=True)

    def run_case(self, case_path: str):
        try:
            log(f"Orchestrator: Starting run for case: {case_path}")

            # Load input case
            case = self.input_agent.load_case(case_path)

            # Fetch and parse rules/docs
            self.fetch_agent.fetch_docs(["https://example.com/regulations.pdf"])
            self.parse_agent.parse_pdfs(["rules_kb/sample_rules.json"])

            # Apply rules and compute
            selected_rules = self.classify_agent.select_applicable_rules(case)
            calc = self.calc_agent.compute(case, selected_rules)
            rl = self.rl_agent.run(case, selected_rules)

            # Prepare report
            report = {
                "case": case,
                "selected_rules": selected_rules,
                "calc": calc,
                "rl": rl
            }

            # Save JSON report
            base_filename = os.path.basename(case_path).replace("_case.json", "_output.json")
            output_json_path = os.path.join(OUTPUT_DIR, "json", base_filename)
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            log(f"Orchestrator: Saved JSON report to {output_json_path}")

            # Extract city name for geometry file
            city_name = case.get("city") or os.path.basename(case_path).replace("_case.json", "")
            
            # Save geometry
            output_geom_path = os.path.join(OUTPUT_DIR, "geometry", base_filename.replace("_output.json", "_model.stl"))
            export_from_results(output_geom_path, city_name, calc)
            log(f"Orchestrator: Saved geometry to {output_geom_path}")

            log("Orchestrator: Run complete.")
            return output_json_path, output_geom_path

        except Exception as e:
            log(f"Orchestrator: ERROR while running case {case_path}: {e}")
            raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log("Please provide the input JSON file path as an argument.")
        sys.exit(1)

    case_file_path = sys.argv[1]
    orchestrator = Orchestrator()
    orchestrator.run_case(case_file_path)