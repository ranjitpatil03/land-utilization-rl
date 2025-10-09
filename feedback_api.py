from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
from utils.logging_utils import log

app = FastAPI(title="Land Utilization Feedback API", version="1.0.0")

# Add CORS middleware to allow requests from file:// and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (UI HTML files)
app.mount("/ui", StaticFiles(directory=".", html=True), name="ui")

# Ensure feedback directory exists
FEEDBACK_FILE = "feedback.json"
os.makedirs(os.path.dirname(FEEDBACK_FILE) if os.path.dirname(FEEDBACK_FILE) else ".", exist_ok=True)

class Feedback(BaseModel):
    case_id: str
    input: dict
    output: dict
    user_feedback: str  # "up" or "down"
    timestamp: Optional[str] = None

class FeedbackResponse(BaseModel):
    message: str
    id: int

class FeedbackStats(BaseModel):
    total_feedback: int
    positive_feedback: int
    negative_feedback: int
    positive_ratio: float

def load_feedback():
    """Load existing feedback from file"""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedback(feedback_data):
    """Save feedback to file"""
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: Feedback):
    """Submit feedback for a case"""
    try:
        # Validate feedback value
        if feedback.user_feedback not in ['up', 'down']:
            raise HTTPException(status_code=400, detail='user_feedback must be "up" or "down"')
        
        # Add timestamp if not provided
        if not feedback.timestamp:
            feedback.timestamp = datetime.now().isoformat()
        
        # Convert to dictionary
        feedback_entry = feedback.dict()
        
        # Load existing feedback
        feedback_data = load_feedback()
        
        # Add new feedback
        feedback_data.append(feedback_entry)
        
        # Save feedback
        save_feedback(feedback_data)
        
        # Log the feedback
        log(f"Feedback received for case {feedback.case_id}: {feedback.user_feedback}")
        
        return FeedbackResponse(message="Feedback submitted successfully", id=len(feedback_data))
    
    except Exception as e:
        log(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/feedback", response_model=List[Feedback])
async def get_feedback():
    """Get all feedback"""
    try:
        feedback_data = load_feedback()
        return feedback_data
    except Exception as e:
        log(f"Error retrieving feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/feedback/case/{case_id}", response_model=List[Feedback])
async def get_feedback_by_case(case_id: str):
    """Get feedback for a specific case"""
    try:
        feedback_data = load_feedback()
        case_feedback = [f for f in feedback_data if f['case_id'] == case_id]
        return case_feedback
    except Exception as e:
        log(f"Error retrieving feedback for case {case_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/feedback/stats", response_model=FeedbackStats)
async def get_feedback_stats():
    """Get feedback statistics"""
    try:
        feedback_data = load_feedback()
        total = len(feedback_data)
        up_votes = len([f for f in feedback_data if f['user_feedback'] == 'up'])
        down_votes = len([f for f in feedback_data if f['user_feedback'] == 'down'])
        
        stats = FeedbackStats(
            total_feedback=total,
            positive_feedback=up_votes,
            negative_feedback=down_votes,
            positive_ratio=up_votes / total if total > 0 else 0
        )
        
        return stats
    except Exception as e:
        log(f"Error calculating feedback stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")