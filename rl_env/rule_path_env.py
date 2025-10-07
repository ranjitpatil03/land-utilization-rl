import random
import json
import os
from utils.logging_utils import log, log_rl_training

class RulePathEnv:
    """
    Minimal toy environment:
    - State: index in a list of candidate rule IDs
    - Actions: choose one of candidate paths (index)
    - Reward: +1 if chosen path matches expected, else -1
    """
    def __init__(self, candidate_paths, expected_path, case_id=None):
        self.candidate_paths = candidate_paths
        self.expected_path = expected_path
        self.case_id = case_id
        self.state = 0
        log(f"RL Environment: Initialized with {len(candidate_paths)} candidate paths")
        for i, path in enumerate(candidate_paths):
            log(f"RL Environment: Candidate {i}: {path}")

    def reset(self):
        self.state = 0
        log("RL Environment: Reset")
        return self.state

    def _get_feedback_reward(self):
        """Get additional reward from user feedback"""
        feedback_reward = 0
        if self.case_id and os.path.exists("feedback.json"):
            try:
                with open("feedback.json", "r") as f:
                    feedback_data = json.load(f)
                
                # Find feedback for this case
                case_feedback = [f for f in feedback_data if f.get('case_id') == self.case_id]
                
                # Calculate feedback reward
                for feedback in case_feedback:
                    if feedback.get('user_feedback') == 'up':
                        feedback_reward += 2  # Positive feedback
                    elif feedback.get('user_feedback') == 'down':
                        feedback_reward -= 2  # Negative feedback
                        
                log(f"RL Environment: Feedback reward for case {self.case_id}: {feedback_reward}")
            except Exception as e:
                log(f"RL Environment: Error reading feedback: {e}")
        
        return feedback_reward

    def step(self, action):
        chosen = self.candidate_paths[action]
        base_reward = 1 if chosen == self.expected_path else -1
        
        # Add feedback reward
        feedback_reward = self._get_feedback_reward()
        total_reward = base_reward + feedback_reward
        
        done = True
        info = {"chosen": chosen, "expected": self.expected_path, "base_reward": base_reward, "feedback_reward": feedback_reward, "total_reward": total_reward}
        log(f"RL Environment: Action {action} -> Chosen: {chosen}, Expected: {self.expected_path}, Base Reward: {base_reward}, Feedback Reward: {feedback_reward}, Total Reward: {total_reward}")
        return self.state, total_reward, done, info

class RLTrainer:
    def train(self, env, episodes=10):
        # random policy as placeholder
        log(f"Training RL (random policy) for {episodes} episodes...")
        total = 0
        success_count = 0
        
        # Log training start
        log_rl_training({"status": "training_started", "episodes": episodes})
        
        for ep in range(episodes):
            env.reset()
            action = random.randrange(len(env.candidate_paths))
            _, r, done, info = env.step(action)
            total += r
            if info["base_reward"] > 0:  # Success based on base reward only
                success_count += 1
            
            # Log each episode
            episode_metrics = {
                "episode": ep + 1,
                "action": action,
                "base_reward": info["base_reward"],
                "feedback_reward": info["feedback_reward"],
                "total_reward": info["total_reward"],
                "chosen_path": info['chosen'],
                "expected_path": info['expected'],
                "running_avg_reward": total / (ep + 1),
                "success_rate": success_count / (ep + 1)
            }
            log_rl_training(episode_metrics, ep + 1)
            
            log(f"EP {ep+1}: action={action}, base_reward={info['base_reward']}, feedback_reward={info['feedback_reward']}, total_reward={info['total_reward']}, chosen={info['chosen']} expected={info['expected']}")
        
        avg = total / episodes
        success_rate = success_count / episodes
        log(f"Avg reward: {avg:.2f}, Success rate: {success_rate:.2%}")
        
        # Log training summary
        summary_metrics = {
            "status": "training_completed",
            "avg_reward": avg,
            "success_rate": success_rate,
            "episodes": episodes,
            "total_reward": total
        }
        log_rl_training(summary_metrics)
        
        return {"avg_reward": avg, "success_rate": success_rate, "episodes": episodes}