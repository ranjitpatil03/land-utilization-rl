import requests
import json

def test_ui_feedback():
    """Test submitting feedback that simulates what the UI would send"""
    
    # Feedback data that matches what the UI would send
    feedback_data = {
        "case_id": "ui-test-case",
        "input": {
            "case_id": "ui-test-case",
            "city": "Mumbai",
            "location": "urban",
            "plot_type": "residential",
            "project_type": "slum_redevelopment",
            "road_width": 15,
            "plot_size": 800
        },
        "output": {
            "selected_rules": [
                "MUM-DCPR-2034-SETBACK-FRONT",
                "MUM-DCPR-2034-COVERAGE",
                "MUM-DCPR-2034-FAR",
                "MUM-MHADA-REDEVELOPMENT"
            ],
            "calc": {
                "setback_m": 3.0,
                "max_footprint_sqm": 520,
                "total_floor_area_sqm": 2000
            },
            "rl": {
                "avg_reward": -0.2,
                "success_rate": 0.4
            }
        },
        "user_feedback": "up"
    }
    
    print("Testing UI feedback submission...")
    
    try:
        # Submit feedback to the API
        response = requests.post("http://localhost:5001/feedback", json=feedback_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("Feedback submitted successfully!")
            
            # Check the feedback file to confirm it was added
            print("\nChecking feedback file...")
            with open("feedback.json", "r") as f:
                feedback_content = json.load(f)
            
            print(f"Total feedback entries: {len(feedback_content)}")
            if len(feedback_content) > 0:
                latest_entry = feedback_content[-1]
                print(f"Latest entry case_id: {latest_entry.get('case_id')}")
                print(f"Latest entry feedback: {latest_entry.get('user_feedback')}")
                print(f"Latest entry timestamp: {latest_entry.get('timestamp')}")
        else:
            print(f"Error submitting feedback: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ui_feedback()