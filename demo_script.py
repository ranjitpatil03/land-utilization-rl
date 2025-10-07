#!/usr/bin/env python3
"""
Demo Script for Land Utilization RL Pipeline
This script demonstrates the complete workflow of the system.
"""

import json
import requests
import time
from datetime import datetime

def demo_step(title):
    """Print a demo step with clear separation"""
    print("\n" + "="*60)
    print(f"DEMO: {title}")
    print("="*60)

def check_api_status():
    """Check if the API server is running"""
    try:
        response = requests.get("http://localhost:5001/feedback")
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

def show_feedback_sample():
    """Show a sample of feedback entries"""
    try:
        with open("feedback.json", "r") as f:
            data = json.load(f)
            if data:
                print(f"Sample feedback entry:")
                print(json.dumps(data[-1], indent=2))
            else:
                print("No feedback entries found")
    except Exception as e:
        print(f"Error reading feedback: {e}")

def submit_sample_feedback():
    """Submit a sample feedback entry"""
    feedback_data = {
        "case_id": f"demo-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
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
        "user_feedback": "up"
    }
    
    try:
        response = requests.post("http://localhost:5001/feedback", json=feedback_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Feedback submitted successfully! ID: {result['id']}")
            return True
        else:
            print(f"Error submitting feedback: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error submitting feedback: {e}")
        return False

def show_feedback_stats():
    """Show feedback statistics"""
    try:
        response = requests.get("http://localhost:5001/feedback/stats")
        if response.status_code == 200:
            stats = response.json()
            print("Feedback Statistics:")
            print(f"  Total Feedback: {stats['total_feedback']}")
            print(f"  Positive: {stats['positive_feedback']}")
            print(f"  Negative: {stats['negative_feedback']}")
            print(f"  Positive Ratio: {stats['positive_ratio']:.2%}")
        else:
            print(f"Error getting stats: {response.status_code}")
    except Exception as e:
        print(f"Error getting stats: {e}")

def main():
    print("LAND UTILIZATION RL PIPELINE - DEMONSTRATION")
    print("=============================================")
    
    # Step 1: Check API Status
    demo_step("1. Checking API Server Status")
    if check_api_status():
        print("✓ API Server is running")
    else:
        print("✗ API Server is not running")
        print("  Please start the server with: python feedback_api.py")
        return
    
    # Step 2: Show Current Feedback Data
    demo_step("2. Current Feedback Data")
    initial_count = count_feedback_entries()
    print(f"Current feedback entries: {initial_count}")
    if initial_count > 0:
        show_feedback_sample()
    
    # Step 3: Submit New Feedback
    demo_step("3. Submitting New Feedback")
    print("Submitting sample feedback...")
    if submit_sample_feedback():
        print("Waiting for system to process...")
        time.sleep(2)
        
        # Step 4: Verify Feedback Storage
        demo_step("4. Verifying Feedback Storage")
        new_count = count_feedback_entries()
        print(f"Feedback entries after submission: {new_count}")
        if new_count > initial_count:
            print("✓ New feedback successfully stored")
            show_feedback_sample()
        else:
            print("✗ Feedback was not stored correctly")
    
    # Step 5: Show Statistics
    demo_step("5. Feedback Statistics")
    show_feedback_stats()
    
    # Step 6: Show Log File
    demo_step("6. System Logs")
    try:
        with open("reports/agent_log.txt", "r") as f:
            lines = f.readlines()
            print(f"Total log entries: {len(lines)}")
            if lines:
                print("Latest log entries:")
                # Show last 3 entries
                for line in lines[-3:]:
                    print(f"  {line.strip()}")
    except Exception as e:
        print(f"Error reading logs: {e}")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nKey Points:")
    print("1. API Server handles feedback submission and retrieval")
    print("2. Feedback is stored persistently in feedback.json")
    print("3. Statistics are calculated in real-time")
    print("4. All actions are logged in structured format")
    print("5. RL system uses feedback to improve recommendations")

if __name__ == "__main__":
    main()