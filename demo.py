#!/usr/bin/env python3
"""
Demo script to showcase all functionality of the Land Utilization Pipeline
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print its output"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("Land Utilization Pipeline - Demo Script")
    print("======================================")
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # 1. Run Mumbai redevelopment case
    print("\n1. Running Mumbai Redevelopment Case Study")
    run_command("python agents/orchestrator.py data/inputs/mumbai_redevelopment.json", 
                "Mumbai Redevelopment Analysis")
    
    # 2. Run Ahmedabad residential case
    print("\n2. Running Ahmedabad Residential Case Study")
    run_command("python agents/orchestrator.py data/inputs/ahmedabad_residential.json", 
                "Ahmedabad Residential Analysis")
    
    # 3. Show outputs
    print("\n3. Checking Generated Outputs")
    outputs_dir = project_dir / "outputs"
    if outputs_dir.exists():
        print(f"Outputs directory contents:")
        for item in outputs_dir.rglob("*"):
            if item.is_file():
                print(f"  {item.relative_to(project_dir)}")
    
    # 4. Show logs
    print("\n4. Checking Log Files")
    reports_dir = project_dir / "reports"
    if reports_dir.exists():
        for log_file in reports_dir.glob("*.txt"):
            print(f"\nContents of {log_file.name}:")
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Show last 10 lines
                    for line in lines[-10:]:
                        print(f"  {line.strip()}")
            except Exception as e:
                print(f"  Error reading {log_file.name}: {e}")
        
        for log_file in reports_dir.glob("*.jsonl"):
            print(f"\nContents of {log_file.name}:")
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Show last 5 lines
                    for line in lines[-5:]:
                        print(f"  {line.strip()}")
            except Exception as e:
                print(f"  Error reading {log_file.name}: {e}")
    
    # 5. Show feedback system
    print("\n5. Checking Feedback System")
    feedback_file = project_dir / "feedback.json"
    if feedback_file.exists():
        print("Feedback data:")
        try:
            with open(feedback_file, 'r') as f:
                feedback_data = json.load(f)
                print(json.dumps(feedback_data, indent=2))
        except Exception as e:
            print(f"Error reading feedback: {e}")
    else:
        print("No feedback data found. Creating sample feedback...")
        sample_feedback = [{
            "case_id": "mumbai-redev-001",
            "input": {"plot_size": 800},
            "output": {"total_floor_area": 2000},
            "user_feedback": "up",
            "timestamp": "2025-10-03T12:00:00"
        }]
        with open(feedback_file, 'w') as f:
            json.dump(sample_feedback, f, indent=2)
        print("Created sample feedback file")
    
    # 6. Run tests
    print("\n6. Running Test Suite")
    run_command("python -m pytest tests/ -v", "Test Suite Execution")
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60)
    print("\nTo view the feedback UI, open feedback_ui.html in a web browser")
    print("To start the feedback API server, run: python feedback_api.py")
    print("To run individual cases, use: python agents/orchestrator.py <case_file>")

if __name__ == "__main__":
    main()