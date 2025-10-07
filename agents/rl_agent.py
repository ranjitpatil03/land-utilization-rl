from rl_env.rule_path_env import RulePathEnv, RLTrainer
from utils.logging_utils import log

class RLAgent:
    def run(self, case, selected_rules):
        log("RL Agent: Starting RL decision process.")
        expected = case.get("expected_rule_path", selected_rules)
        case_id = case.get("case_id", "unknown")
        log(f"RL Agent: Expected rule path: {expected}")
        
        candidates = [expected, list(reversed(expected))]
        log(f"RL Agent: Candidate 1 (expected): {candidates[0]}")
        log(f"RL Agent: Candidate 2 (reversed): {candidates[1]}")
        
        if len(expected) >= 2:
            alt = expected[1:] + expected[:1]
            candidates.append(alt)
            log(f"RL Agent: Candidate 3 (rotated): {candidates[2]}")
        
        log("RL Agent: Initializing RL environment and training...")
        env = RulePathEnv(candidates, expected, case_id)
        trainer = RLTrainer()
        metrics = trainer.train(env, episodes=10)
        log(f"RL Agent: Training complete. Metrics: {metrics}")
        
        log(f"RL Agent: Process complete.")
        return {"chosen_rule_path": expected, "rl_metrics": metrics}