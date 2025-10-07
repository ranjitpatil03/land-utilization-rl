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

    def _get_setback(self, case: dict, selected_rule_ids: list):
        # Find applicable setback rules from selected rules
        for rule_id in selected_rule_ids:
            for r in self.rulebook:
                if r["id"] == rule_id and "SETBACK" in rule_id:
                    road = case.get("road_width", 0)
                    log(f"Calculation Agent: Evaluating setback for rule {rule_id} with road width {road}")
                    
                    # Handle logic-based rules
                    if "logic" in r:
                        for branch in r.get("logic", []):
                            if branch.get("if") and road >= branch["if"].get("road_width_gte", 0):
                                setback = branch["setback"]
                                log(f"Calculation Agent: Applied setback rule: road_width >= {branch['if'].get('road_width_gte', 0)} -> setback = {setback}")
                                return setback
                            elif branch.get("elif") and road >= branch["elif"].get("road_width_gte", 0):
                                setback = branch["setback"]
                                log(f"Calculation Agent: Applied setback rule: road_width >= {branch['elif'].get('road_width_gte', 0)} -> setback = {setback}")
                                return setback
                        # Handle else case
                        for branch in r.get("logic", []):
                            if branch.get("else"):
                                setback = branch["setback"]
                                log(f"Calculation Agent: Using default setback value: {setback}")
                                return setback
                    
                    # Handle mapping-based rules
                    mapping = r.get("mapping", {})
                    if mapping:
                        setback = mapping.get("default", 1.5)
                        log(f"Calculation Agent: Using mapped setback value: {setback}")
                        return setback
        
        default_setback = 1.5
        log(f"Calculation Agent: No specific setback rule found, using default: {default_setback}")
        return default_setback

    def _get_coverage(self, case: dict, selected_rule_ids: list):
        loc = case.get("location", "default")
        
        # Find applicable coverage rules from selected rules
        for rule_id in selected_rule_ids:
            for r in self.rulebook:
                if r["id"] == rule_id and "COVERAGE" in rule_id:
                    mapping = r.get("mapping", {})
                    if mapping:
                        coverage = mapping.get(loc, mapping.get("default", 0.55))
                        log(f"Calculation Agent: Coverage for {loc} is {coverage} (from rule {rule_id})")
                        return coverage
        
        default_coverage = 0.55
        log(f"Calculation Agent: No specific coverage rule found, using default: {default_coverage}")
        return default_coverage

    def _get_far(self, case: dict, selected_rule_ids: list):
        loc = case.get("location", "default")
        
        # Find applicable FAR rules from selected rules
        for rule_id in selected_rule_ids:
            for r in self.rulebook:
                if r["id"] == rule_id and "FAR" in rule_id and "REDEVELOPMENT" not in rule_id:
                    mapping = r.get("mapping", {})
                    if mapping:
                        far = mapping.get(loc, mapping.get("default", 1.5))
                        log(f"Calculation Agent: FAR for {loc} is {far} (from rule {rule_id})")
                        return far
        
        default_far = 1.5
        log(f"Calculation Agent: No specific FAR rule found, using default: {default_far}")
        return default_far

    def _get_additional_far(self, case: dict, selected_rule_ids: list):
        # Find applicable additional FAR rules (like for redevelopment)
        for rule_id in selected_rule_ids:
            for r in self.rulebook:
                if r["id"] == rule_id and "REDEVELOPMENT" in rule_id:
                    mapping = r.get("mapping", {})
                    if mapping:
                        additional_far = mapping.get("default", 0.0)
                        log(f"Calculation Agent: Additional FAR from {rule_id} is {additional_far}")
                        return additional_far
        
        log(f"Calculation Agent: No additional FAR rule found")
        return 0.0

    def compute(self, case: dict, selected_rule_ids: list):
        log("Calculation Agent: Starting computations.")
        steps = []
        plot = case.get("plot_size")
        if plot is None:
            raise ValueError("ERROR: 'plot_size' missing in the input JSON!")

        log(f"Calculation Agent: Processing case with plot size: {plot} sqm")
        
        loc = case.get("location", "default")
        log(f"Calculation Agent: Location is {loc}")
        
        setback = self._get_setback(case, selected_rule_ids)
        steps.append({"rule": "SETBACK", "calc": f"road_width={case.get('road_width')} -> setback={setback}"})

        coverage = self._get_coverage(case, selected_rule_ids)
        steps.append({"rule": "COVERAGE", "calc": f"location={loc} -> coverage={coverage}"})

        base_far = self._get_far(case, selected_rule_ids)
        additional_far = self._get_additional_far(case, selected_rule_ids)
        far = base_far + additional_far
        steps.append({"rule": "FAR", "calc": f"base_FAR={base_far} + additional_FAR={additional_far} -> total_FAR={far}"})

        max_footprint = plot * coverage
        total_floor_area = plot * far
        log(f"Calculation Agent: Max footprint: {max_footprint} sqm, Total floor area: {total_floor_area} sqm")
        steps.append({"rule": "RESULTS", "calc": f"max_footprint={max_footprint}, total_floor_area={total_floor_area}"})

        result = {
            "inputs": case,
            "setback_m": setback,
            "max_footprint_sqm": max_footprint,
            "total_floor_area_sqm": total_floor_area,
            "steps": steps
        }

        log(f"Calculation Agent: Finished. Total floor area: {total_floor_area} sqm.")
        return result