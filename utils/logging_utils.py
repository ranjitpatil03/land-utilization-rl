import time
import json
from pathlib import Path

LOG_FILE = Path("reports/agent_log.txt")
RL_TRAINING_LOG = Path("reports/rl_training_log.jsonl")
LOG_FILE.parent.mkdir(exist_ok=True)
RL_TRAINING_LOG.parent.mkdir(exist_ok=True)

def log(msg: str):
    """Log a message to the agent log file and console"""
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_rl_training(metrics: dict, episode: int = None):
    """Log RL training metrics to a structured JSONL file"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "episode": episode,
        "metrics": metrics
    }
    
    # Log to console and agent log
    if episode is not None:
        log(f"RL Training - Episode {episode}: {metrics}")
    else:
        log(f"RL Training Summary: {metrics}")
    
    # Write to structured JSONL log
    with RL_TRAINING_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def clear_logs():
    """Clear existing log files"""
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    if RL_TRAINING_LOG.exists():
        RL_TRAINING_LOG.unlink()