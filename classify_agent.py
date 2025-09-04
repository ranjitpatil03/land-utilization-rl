import json
from utils.logging_utils import log

class RuleClassifierAgent:
    def __init__(self, rules_path: str):
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules = json.load(f)["rules"]

    def select_applicable_rules(self, case: dict):
        selected = []
        for r in self.rules:
            cond = r.get("conditions", {})
            ok = True
            for k,v in cond.items():
                if case.get(k) != v:
                    ok = False
                    break
            if ok:
                selected.append(r["id"])
        # also include rules with empty conditions
        for r in self.rules:
            if not r.get("conditions"):
                selected.append(r["id"])
        # ensure unique order by original appearance
        seen = set()
        ordered = []
        for rid in selected:
            if rid not in seen:
                ordered.append(rid); seen.add(rid)
        log(f"Applicable rules: {ordered}")
        return ordered
