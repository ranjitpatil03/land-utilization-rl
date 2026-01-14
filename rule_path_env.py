import random
from utils.logging_utils import log
import json
from pathlib import Path

class RulePathEnv:
    """
    Minimal toy environment:
    - State: index in a list of candidate rule IDs
    - Actions: choose one of candidate paths (index)
    - Reward: +1 if chosen path matches expected, else -1
    - Incorporates user feedback rewards from feedback file
    """
    def __init__(self, candidate_paths, expected_path):
        self.candidate_paths = candidate_paths
        self.expected_path = expected_path
        self.state = 0
        self.feedback_file = Path("feedback/feedback.json")

    def _get_feedback_reward(self, chosen_path):
        """Read feedback file and calculate cumulative reward for this path"""
        try:
            if not self.feedback_file.exists():
                return 0
            
            total_feedback_reward = 0
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            feedback_entry = json.loads(line)
                            # Check if this feedback is for our chosen path
                            if feedback_entry.get("output", {}).get("chosen_rule_path") == chosen_path:
                                total_feedback_reward += feedback_entry.get("reward", 0)
                        except json.JSONDecodeError:
                            continue  # Skip malformed lines
            return total_feedback_reward
        except Exception:
            return 0  # If there's any error reading feedback, return 0

    def reset(self):
        self.state = 0
        return self.state

    def step(self, action):
        chosen = self.candidate_paths[action]
        
        # Base reward: +1 if matches expected, -1 otherwise
        base_reward = 1 if chosen == self.expected_path else -1
        
        # Add feedback reward from user feedback
        feedback_reward = self._get_feedback_reward(chosen)
        
        # Combined reward
        reward = base_reward + feedback_reward
        
        done = True
        info = {"chosen": chosen, "expected": self.expected_path, "feedback_reward": feedback_reward}
        return self.state, reward, done, info

class RLTrainer:
    def train(self, env, episodes=10):
        # random policy as placeholder
        log(f"Training RL (random policy) for {episodes} episodes...")
        total = 0
        for ep in range(episodes):
            env.reset()
            action = random.randrange(len(env.candidate_paths))
            _, r, done, info = env.step(action)
            total += r
            log(f"EP {ep+1}: action={action}, reward={r}, chosen={info['chosen']} expected={info['expected']}, feedback_reward={info['feedback_reward']}")
        avg = total / episodes
        log(f"Avg reward: {avg:.2f}")
        return {"avg_reward": avg}