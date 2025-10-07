import json
from utils.logging_utils import log

class RuleClassifierAgent:
    def __init__(self, rules_path: str):
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules = json.load(f)["rules"]

    def select_applicable_rules(self, case: dict):
        log("Classification Agent: Starting to select applicable rules.")
        selected = []
        decision_log = []

        for r in self.rules:
            rule_id = r["id"]
            cond = r.get("conditions", {})
            ok = True
            reason = []
            
            # Check conditions
            for k, v in cond.items():
                case_value = case.get(k)
                if case_value != v:
                    ok = False
                    reason.append(f"Condition mismatch: {k}={case_value}, expected {v}")
                else:
                    reason.append(f"Condition match: {k}={case_value}")
            
            if ok:
                selected.append(rule_id)
                decision_log.append(f"SELECTED rule {rule_id}: {', '.join(reason) if reason else 'No conditions'}")
                log(f"Classification Agent: SELECTED rule {rule_id}")
            else:
                decision_log.append(f"REJECTED rule {rule_id}: {', '.join(reason)}")
                log(f"Classification Agent: REJECTED rule {rule_id}")

        # Add rules with no conditions
        for r in self.rules:
            rule_id = r["id"]
            if not r.get("conditions"):
                if rule_id not in selected:
                    selected.append(rule_id)
                    decision_log.append(f"SELECTED rule {rule_id}: No conditions specified")
                    log(f"Classification Agent: SELECTED rule {rule_id} (no conditions)")

        log(f"Classification Agent: Found {len(set(selected))} applicable rules.")
        log(f"Classification Agent: Decision details - {', '.join(decision_log)}")
        return list(set(selected))