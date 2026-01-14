from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Literal
from datetime import datetime
import json
import os
from pathlib import Path

app = FastAPI(title="Land Utilization Feedback API")

# Request model
class FeedbackRequest(BaseModel):
    case_id: str
    input: Dict
    output: Dict
    user_feedback: Literal["up", "down"]
    timestamp: str = None  # Make timestamp optional

# Ensure feedback directory exists
feedback_dir = Path("feedback")
feedback_dir.mkdir(exist_ok=True)
feedback_file = feedback_dir / "feedback.json"

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    """
    Accept feedback from users and store it in feedback.json
    If user_feedback is "up", add +2 reward
    If user_feedback is "down", add -2 reward
    """
    try:
        # Set timestamp if not provided
        timestamp = request.timestamp or datetime.now().isoformat()
        
        # Create feedback record
        feedback_record = {
            "case_id": request.case_id,
            "input": request.input,
            "output": request.output,
            "user_feedback": request.user_feedback,
            "timestamp": timestamp,
            "reward": 2 if request.user_feedback == "up" else -2
        }
        
        # Append feedback to file
        with open(feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_record) + "\n")
        
        return {
            "status": "success",
            "message": f"Feedback recorded with reward: {feedback_record['reward']}",
            "reward": feedback_record["reward"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)