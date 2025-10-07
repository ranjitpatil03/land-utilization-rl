#!/usr/bin/env python3
"""
Complete System Workflow Demonstration
This script demonstrates the entire workflow of the land utilization RL pipeline.
"""

import json
import requests
import time
from datetime import datetime
import os

def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)

def check_api_status():
    """Check if the API server is running"""
    try:
        response = requests.get("http://localhost:5001/feedback", timeout=5)
        return response.status_code == 200
    except:
        return False

def count_feedback_entries():
    """Count the number of feedback entries"""
    try:
        with open("feedback.json", "r") as f:
            data = json.load(f)
            return len(data)
    except:
        return 0

def show_feedback_sample(count=3):
    """Show a sample of feedback entries"""
    try:
        with open("feedback.json", "r") as f:
            data = json.load(f)
            print(f"Total feedback entries: {len(data)}")
            if data:
                print(f"\nLatest {min(count, len(data))} entries:")
                for i, entry in enumerate(data[-count:]):
                    print(f"  {i+1}. Case: {entry.get('case_id', 'N/A')}")
                    print(f"     Feedback: {entry.get('user_feedback', 'N/A')}")
                    print(f"     Timestamp: {entry.get('timestamp', 'N/A')}")
            else:
                print("No feedback entries found")
    except Exception as e:
        print(f"Error reading feedback: {e}")

def submit_feedback(case_id, feedback_type):
    """Submit a feedback entry"""
    feedback_data = {
        "case_id": case_id,
        "input": {
            "plot_size": 1000,
            "location": "urban",
            "city": "Mumbai"
        },
        "output": {
            "total_floor_area": 1500,
            "setback": 2.0,
            "applicable_rules": ["MUM-DCPR-2034-FAR", "MUM-MHADA-REDEVELOPMENT"]
        },
        "user_feedback": feedback_type  # "up" or "down"
    }
    
    try:
        response = requests.post("http://localhost:5001/feedback", json=feedback_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Feedback submitted successfully! ID: {result['id']}")
            return True
        else:
            print(f"✗ Error submitting feedback: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error submitting feedback: {e}")
        return False

def show_feedback_stats():
    """Show feedback statistics"""
    try:
        response = requests.get("http://localhost:5001/feedback/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("\nFeedback Statistics:")
            print(f"  Total Feedback: {stats['total_feedback']}")
            print(f"  Positive: {stats['positive_feedback']}")
            print(f"  Negative: {stats['negative_feedback']}")
            print(f"  Positive Ratio: {stats['positive_ratio']:.2%}")
            return stats
        else:
            print(f"✗ Error getting stats: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error getting stats: {e}")
        return None

def show_log_sample():
    """Show a sample of log entries"""
    try:
        # Show agent logs
        if os.path.exists("reports/agent_log.txt"):
            with open("reports/agent_log.txt", "r") as f:
                lines = f.readlines()
                print(f"\nAgent Log Entries (total: {len(lines)}):")
                if lines:
                    # Show last 3 entries
                    for line in lines[-3:]:
                        print(f"  {line.strip()}")
        
        # Show RL training logs
        if os.path.exists("reports/rl_training_log.jsonl"):
            with open("reports/rl_training_log.jsonl", "r") as f:
                lines = f.readlines()
                print(f"\nRL Training Log Entries (total: {len(lines)}):")
                if lines:
                    # Show last 2 entries
                    for line in lines[-2:]:
                        try:
                            entry = json.loads(line)
                            print(f"  {entry.get('timestamp', 'N/A')}: {entry.get('metrics', {})}")
                        except:
                            print(f"  {line.strip()}")
    except Exception as e:
        print(f"Error reading logs: {e}")

def demonstrate_rl_feedback_integration():
    """Demonstrate how RL integrates feedback"""
    print("\nRL Feedback Integration:")
    print("The RL system now considers user feedback when calculating rewards:")
    print("  - Base Reward: +1 for correct path, -1 for incorrect path")
    print("  - Feedback Reward: +2 for positive feedback, -2 for negative feedback")
    print("  - Total Reward = Base Reward + Feedback Reward")
    print("\nThis allows the RL agent to learn from both its decisions and user preferences.")

def main():
    print("LAND UTILIZATION RL PIPELINE - COMPLETE WORKFLOW DEMONSTRATION")
    print("=============================================================")
    
    # Section 1: System Overview
    print_section("1. SYSTEM OVERVIEW")
    print("This demonstration shows the complete workflow of the land utilization RL pipeline:")
    print("  1. Multi-agent system processes land utilization cases")
    print("  2. RL agent optimizes rule path selection")
    print("  3. User feedback is collected through web interface")
    print("  4. Feedback influences RL training through reward adjustment")
    print("  5. All actions are logged for analysis and debugging")
    
    # Section 2: API Status Check
    print_section("2. FEEDBACK API STATUS")
    if check_api_status():
        print("✓ Feedback API Server is running on http://localhost:5001")
    else:
        print("✗ Feedback API Server is not running")
        print("  To start the server, run: python feedback_api.py")
        return
    
    # Section 3: Current Feedback Data
    print_section("3. CURRENT FEEDBACK DATA")
    initial_count = count_feedback_entries()
    show_feedback_sample()
    
    # Section 4: Submit New Feedback
    print_section("4. SUBMITTING NEW FEEDBACK")
    print("Simulating user feedback submission...")
    
    # Submit positive feedback
    print("\nSubmitting positive feedback...")
    case_id_up = f"demo-up-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    if submit_feedback(case_id_up, "up"):
        time.sleep(1)  # Wait for processing
    
    # Submit negative feedback
    print("\nSubmitting negative feedback...")
    case_id_down = f"demo-down-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    if submit_feedback(case_id_down, "down"):
        time.sleep(1)  # Wait for processing
    
    # Section 5: Verify Feedback Storage
    print_section("5. VERIFYING FEEDBACK STORAGE")
    new_count = count_feedback_entries()
    print(f"Feedback entries before: {initial_count}")
    print(f"Feedback entries after: {new_count}")
    if new_count > initial_count:
        print("✓ New feedback successfully stored")
        show_feedback_sample(5)  # Show more entries now
    else:
        print("✗ Feedback was not stored correctly")
    
    # Section 6: Feedback Statistics
    print_section("6. FEEDBACK STATISTICS")
    stats = show_feedback_stats()
    
    # Section 7: Log Files
    print_section("7. SYSTEM LOGS")
    show_log_sample()
    
    # Section 8: RL Feedback Integration
    print_section("8. RL FEEDBACK INTEGRATION")
    demonstrate_rl_feedback_integration()
    
    # Section 9: System Architecture
    print_section("9. SYSTEM ARCHITECTURE")
    print("Multi-Agent System:")
    print("  ├── Input Agent: Processes user inputs")
    print("  ├── Fetch Agent: Retrieves regulatory rules")
    print("  ├── Classify Agent: Categorizes applicable rules")
    print("  ├── Calc Agent: Performs calculations")
    print("  ├── RL Agent: Optimizes rule paths")
    print("  └── Feedback System: Collects user preferences")
    print("\nData Flow:")
    print("  1. User input → Agents process → RL optimization")
    print("  2. Results presented to user via UI")
    print("  3. User provides feedback via UI")
    print("  4. Feedback stored in feedback.json")
    print("  5. RL agent reads feedback to adjust rewards")
    print("  6. Adjusted rewards improve future recommendations")
    
    # Section 10: Key Features
    print_section("10. KEY FEATURES")
    print("✓ Production-Ready Logging: Structured JSONL format")
    print("✓ Real Regulatory Data: Mumbai and Ahmedabad building regulations")
    print("✓ Interactive Feedback System: Web UI with RESTful API")
    print("✓ RL Reward Integration: User feedback influences training")
    print("✓ Comprehensive Testing: API and component tests")
    print("✓ Detailed Documentation: Complete handover materials")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nThis system is now production-ready with all components properly integrated.")

if __name__ == "__main__":
    main()