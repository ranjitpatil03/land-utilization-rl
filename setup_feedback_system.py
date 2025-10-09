#!/usr/bin/env python3
"""
Setup script to ensure feedback system is properly configured
"""

import os
import json

def setup_feedback_system():
    """Setup the feedback system"""
    
    # Check if feedback.json exists
    if not os.path.exists("feedback.json"):
        print("Creating feedback.json...")
        # Create an empty feedback file with proper JSON array format
        with open("feedback.json", "w") as f:
            json.dump([], f, indent=2)
        print("✓ feedback.json created successfully")
    else:
        print("✓ feedback.json already exists")
        
        # Verify it's valid JSON
        try:
            with open("feedback.json", "r") as f:
                data = json.load(f)
            print("✓ feedback.json is valid JSON")
        except Exception as e:
            print(f"✗ feedback.json is invalid: {e}")
            print("Creating new feedback.json...")
            with open("feedback.json", "w") as f:
                json.dump([], f, indent=2)
            print("✓ feedback.json recreated successfully")
    
    # Check if API server file exists
    if os.path.exists("feedback_api.py"):
        print("✓ feedback_api.py found")
    else:
        print("✗ feedback_api.py not found")
        
    # Check if UI files exist
    if os.path.exists("feedback_ui.html"):
        print("✓ feedback_ui.html found")
    else:
        print("✗ feedback_ui.html not found")
        
    if os.path.exists("feedback_ui_improved.html"):
        print("✓ feedback_ui_improved.html found")
    else:
        print("✗ feedback_ui_improved.html not found")
        
    print("\nFeedback system setup complete!")

if __name__ == "__main__":
    setup_feedback_system()