import requests
import json

def test_api():
    try:
        # Test getting all feedback
        print("Testing GET /feedback...")
        response = requests.get("http://localhost:5001/feedback")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test getting statistics
        print("\nTesting GET /feedback/stats...")
        response = requests.get("http://localhost:5001/feedback/stats")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Statistics: {response.json()}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_api()