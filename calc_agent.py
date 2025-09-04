import json
from utils.logging_utils import log

class CalcAgent:
    def __init__(self, rules_path: str):
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rulebook = json.load(f)["rules"]

    def _get_mapping(self, rule_id: str):
        for r in self.rulebook:
            if r["id"] == rule_id:
                return r.get("mapping", {})
        return {}

    def _get_setback(self, case: dict):
        # implement R-SETBACK-URBAN
        for r in self.rulebook:
            if r["id"] == "R-SETBACK-URBAN" and case.get("location") == "urban":
                road = case.get("road_width", 0)
                for branch in r.get("logic", []):
                    if branch.get("if") and road >= branch["if"].get("road_width_gte", 0):
                        return branch["setback"]
                return 1.5
        return 1.5

    def compute(self, case: dict, selected_rule_ids: list):
        steps = []
        plot = case["plot_size"]
        loc  = case.get("location","default")
        setback = self._get_setback(case)
        steps.append({"rule":"R-SETBACK-URBAN", "calc": f"road_width={case.get('road_width')} -> setback={setback}m"})

        cov_map = self._get_mapping("R-COVERAGE")
        coverage = cov_map.get(loc, cov_map.get("default", 0.55))
        steps.append({"rule":"R-COVERAGE", "calc": f"location={loc} -> coverage={coverage:.2f}"})

        far_map = self._get_mapping("R-FAR")
        far = far_map.get(loc, far_map.get("default", 1.5))
        steps.append({"rule":"R-FAR", "calc": f"location={loc} -> FAR={far:.2f}"})

        max_footprint = plot * coverage
        total_floor_area = plot * far

        steps.append({"rule":"RESULTS", "calc": f"max_footprint={max_footprint:.2f} sq.m, total_FAR_area={total_floor_area:.2f} sq.m"})

        result = {
            "inputs": case,
            "setback_m": setback,
            "max_footprint_sqm": max_footprint,
            "total_floor_area_sqm": total_floor_area,
            "steps": steps
        }
        return result
