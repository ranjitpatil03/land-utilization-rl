from rl_env.rule_path_env import RulePathEnv, RLTrainer
from utils.logging_utils import log

class RLAgent:
    def run(self, case, selected_rules):
        # candidate paths: true path vs some permutations (toy)
        expected = case.get("expected_rule_path", selected_rules)
        candidates = [expected, list(reversed(expected))]
        if len(expected) >= 2:
            alt = expected[1:] + expected[:1]
            candidates.append(alt)
        env = RulePathEnv(candidates, expected)
        trainer = RLTrainer()
        metrics = trainer.train(env, episodes=10)
        log(f"RL metrics: {metrics}")
        # choose the best (here we pretend to pick expected for demo)
        return {"chosen_rule_path": expected, "rl_metrics": metrics}
