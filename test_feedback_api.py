import requests
import json

def test_feedback_api():
    """Test the feedback API endpoints"""
    
    # Base URL for the API
    base_url = "http://localhost:5001"
    
    # Test data
    feedback_data = {
        "case_id": "test-case-001",
        "input": {"plot_size": 500, "location": "urban"},
        "output": {"total_floor_area": 900, "setback": 1.5},
        "user_feedback": "up"
    }
    
    print("Testing Feedback API...")
    
    # Test 1: Submit feedback
    print("\n1. Submitting feedback...")
    try:
        response = requests.post(f"{base_url}/feedback", json=feedback_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error submitting feedback: {e}")
        return
    
    # Test 2: Get all feedback
    print("\n2. Retrieving all feedback...")
    try:
        response = requests.get(f"{base_url}/feedback")
        print(f"Status Code: {response.status_code}")
        feedback_list = response.json()
        print(f"Total feedback entries: {len(feedback_list)}")
        if feedback_list:
            print("Sample feedback entry:")
            print(json.dumps(feedback_list[0], indent=2))
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
    
    # Test 3: Get feedback stats
    print("\n3. Retrieving feedback statistics...")
    try:
        response = requests.get(f"{base_url}/feedback/stats")
        print(f"Status Code: {response.status_code}")
        stats = response.json()
        print("Feedback Statistics:")
        print(json.dumps(stats, indent=2))
    except Exception as e:
        print(f"Error retrieving feedback stats: {e}")
    
    # Test 4: Get feedback for specific case
    print("\n4. Retrieving feedback for specific case...")
    try:
        response = requests.get(f"{base_url}/feedback/case/test-case-001")
        print(f"Status Code: {response.status_code}")
        case_feedback = response.json()
        print(f"Feedback for case 'test-case-001': {len(case_feedback)} entries")
        if case_feedback:
            print(json.dumps(case_feedback[0], indent=2))
    except Exception as e:
        print(f"Error retrieving case feedback: {e}")
    
    print("\nAPI testing completed!")

if __name__ == "__main__":
    test_feedback_api()