import os, json
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

    def run_case(self, case_path: str):
        case = self.input_agent.load_case(case_path)
        self.fetch_agent.fetch_docs(["https://example.com/regulations.pdf"])
        self.parse_agent.parse_pdfs(["rules_kb/sample_rules.json"])

        selected_rules = self.classify_agent.select_applicable_rules(case)
        calc = self.calc_agent.compute(case, selected_rules)
        rl = self.rl_agent.run(case, selected_rules)

        report = {
            "case": case,
            "selected_rules": selected_rules,
            "calc": calc,
            "rl": rl
        }
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        city = case.get("city","case")
        out_json = os.path.join(OUTPUT_DIR, f"{city}_report.json")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        geom_path = export_from_results(GEOM_EXPORT_DIR, city, calc)
        log(f"Wrote report: {out_json}")
        log(f"Wrote geometry: {geom_path}")
        return out_json, geom_path
