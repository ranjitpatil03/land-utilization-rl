import random
from utils.logging_utils import log

class RulePathEnv:
    """
    Minimal toy environment:
    - State: index in a list of candidate rule IDs
    - Actions: choose one of candidate paths (index)
    - Reward: +1 if chosen path matches expected, else -1
    """
    def __init__(self, candidate_paths, expected_path):
        self.candidate_paths = candidate_paths
        self.expected_path = expected_path
        self.state = 0

    def reset(self):
        self.state = 0
        return self.state

    def step(self, action):
        chosen = self.candidate_paths[action]
        reward = 1 if chosen == self.expected_path else -1
        done = True
        info = {"chosen": chosen, "expected": self.expected_path}
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
            log(f"EP {ep+1}: action={action}, reward={r}, chosen={info['chosen']} expected={info['expected']}")
        avg = total / episodes
        log(f"Avg reward: {avg:.2f}")
        return {"avg_reward": avg}
