import requests
import json

feedback_data = {
    "case_id": "test-down-manual",
    "input": {"plot_size": 600, "location": "urban"},
    "output": {"total_floor_area": 1000, "setback": 2.0},
    "user_feedback": "down"
}

try:
    response = requests.post("http://localhost:5001/feedback", json=feedback_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")