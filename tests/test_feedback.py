import pytest
import json
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feedback_api import load_feedback, save_feedback

def test_feedback_storage():
    """Test that feedback can be saved and loaded correctly"""
    # Clear any existing feedback
    if os.path.exists("feedback.json"):
        os.remove("feedback.json")
    
    # Test data
    test_feedback = [
        {
            "case_id": "test-001",
            "input": {"plot_size": 500},
            "output": {"total_floor_area": 900},
            "user_feedback": "up",
            "timestamp": datetime.now().isoformat()
        },
        {
            "case_id": "test-002",
            "input": {"plot_size": 600},
            "output": {"total_floor_area": 1200},
            "user_feedback": "down",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    # Save feedback
    save_feedback(test_feedback)
    
    # Load feedback
    loaded_feedback = load_feedback()
    
    # Verify
    assert len(loaded_feedback) == 2
    assert loaded_feedback[0]["case_id"] == "test-001"
    assert loaded_feedback[1]["user_feedback"] == "down"
    
    # Clean up
    if os.path.exists("feedback.json"):
        os.remove("feedback.json")

def test_empty_feedback():
    """Test loading feedback when no file exists"""
    # Ensure no feedback file exists
    if os.path.exists("feedback.json"):
        os.remove("feedback.json")
    
    # Load feedback
    feedback = load_feedback()
    
    # Verify it's empty
    assert isinstance(feedback, list)
    assert len(feedback) == 0

def test_feedback_validation():
    """Test that feedback validation works correctly"""
    from feedback_api import app
    import json
    
    with app.test_client() as client:
        # Test missing required fields
        response = client.post('/feedback', 
                             data=json.dumps({"case_id": "test"}),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Test invalid feedback value
        response = client.post('/feedback',
                             data=json.dumps({
                                 "case_id": "test",
                                 "input": {},
                                 "output": {},
                                 "user_feedback": "invalid"
                             }),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Test valid feedback
        response = client.post('/feedback',
                             data=json.dumps({
                                 "case_id": "test",
                                 "input": {"plot": 500},
                                 "output": {"area": 900},
                                 "user_feedback": "up"
                             }),
                             content_type='application/json')
        assert response.status_code == 201

if __name__ == "__main__":
    pytest.main([__file__, "-v"])