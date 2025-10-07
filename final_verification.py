#!/usr/bin/env python3
"""
Final Verification Script
This script verifies that all components of the land utilization RL pipeline are working correctly.
"""

import json
import requests
import os
import sys

def check_file_exists(filepath):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {filepath}: {'Found' if exists else 'Missing'}")
    return exists

def check_directory_exists(dirpath):
    """Check if a directory exists"""
    exists = os.path.exists(dirpath) and os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {dirpath}: {'Found' if exists else 'Missing'}")
    return exists

def check_api_endpoint(url, method="GET"):
    """Check if an API endpoint is accessible"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json={}, timeout=5)
        else:
            response = None
            
        if response is not None:
            success = response.status_code in [200, 422]  # 422 is valid for validation errors
            status = "✓" if success else "✗"
            print(f"{status} API {method} {url}: {response.status_code}")
            return success
        else:
            print(f"✗ API {method} {url}: Invalid method")
            return False
    except Exception as e:
        print(f"✗ API {method} {url}: Error - {str(e)}")
        return False

def check_json_file(filepath):
    """Check if a JSON file is valid"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"✓ {filepath}: Valid JSON")
        return True
    except Exception as e:
        print(f"✗ {filepath}: Invalid JSON - {str(e)}")
        return False

def count_feedback_entries():
    """Count feedback entries"""
    try:
        with open("feedback.json", "r") as f:
            data = json.load(f)
            print(f"✓ feedback.json: {len(data)} entries")
            return len(data)
    except Exception as e:
        print(f"✗ feedback.json: Error reading - {str(e)}")
        return 0

def main():
    print("LAND UTILIZATION RL PIPELINE - FINAL VERIFICATION")
    print("=" * 50)
    
    # Check directories
    print("\nDirectories:")
    dirs_to_check = [
        "agents",
        "data",
        "rl_env",
        "rules_kb",
        "reports",
        "utils"
    ]
    
    all_dirs_exist = True
    for dir_name in dirs_to_check:
        if not check_directory_exists(dir_name):
            all_dirs_exist = False
    
    # Check key files
    print("\nKey Files:")
    files_to_check = [
        "feedback_api.py",
        "feedback_ui.html",
        "feedback_ui_improved.html",
        "feedback.json",
        "README.md",
        "handover.md"
    ]
    
    all_files_exist = True
    for file_name in files_to_check:
        if not check_file_exists(file_name):
            all_files_exist = False
    
    # Check JSON files
    print("\nJSON Validation:")
    json_files = [
        "feedback.json"
    ]
    
    all_json_valid = True
    for json_file in json_files:
        if not check_json_file(json_file):
            all_json_valid = False
    
    # Check feedback count
    print("\nFeedback Data:")
    feedback_count = count_feedback_entries()
    
    # Check API endpoints
    print("\nAPI Endpoints:")
    api_endpoints = [
        ("http://localhost:5001/feedback", "GET"),
        ("http://localhost:5001/feedback/stats", "GET"),
        ("http://localhost:5001/feedback/case/test", "GET"),
        ("http://localhost:5001/feedback", "POST")
    ]
    
    all_api_work = True
    for url, method in api_endpoints:
        if not check_api_endpoint(url, method):
            all_api_work = False
    
    # Check log files
    print("\nLog Files:")
    log_files = [
        "reports/agent_log.txt",
        "reports/rl_training_log.jsonl"
    ]
    
    all_logs_exist = True
    for log_file in log_files:
        if not check_file_exists(log_file):
            all_logs_exist = False
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    checks = [
        ("Directories", all_dirs_exist),
        ("Key Files", all_files_exist),
        ("JSON Validation", all_json_valid),
        ("Feedback Data", feedback_count > 0),
        ("API Endpoints", all_api_work),
        ("Log Files", all_logs_exist)
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"{check_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ALL CHECKS PASSED - SYSTEM IS READY FOR DEMONSTRATION")
        print(f"✅ Total feedback entries: {feedback_count}")
        print("✅ API server is running on http://localhost:5001")
    else:
        print("❌ SOME CHECKS FAILED - PLEASE REVIEW THE SYSTEM")
    
    print("=" * 50)

if __name__ == "__main__":
    main()