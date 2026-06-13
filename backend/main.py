"""
SOCweave Backend — FastAPI entry point.
Exposes:
  POST /alert       -> run the full multi-agent pipeline on an alert
  GET  /health      -> health check
  GET  /scenario/{name} -> load mock scenario (a or b) and run pipeline
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="SOCweave API", version="1.0")

# Allow frontend (React dev server) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_DIR = os.path.join(os.path.dirname(__file__), "..", "mock_data")


class AlertPayload(BaseModel):
    alert_id: str
    severity: str
    title: str
    timestamp: str
    asset: str
    details: str
    foundry_iq: dict | None = None
    fabric_iq: dict | None = None
    work_iq: dict | None = None


class QuestionPayload(BaseModel):
    question: str
    context: dict


@app.post("/ask")
def ask_copilot(payload: QuestionPayload):
    from agent.copilot import answer_question
    return {"answer": answer_question(payload.question, payload.context)}


@app.get("/health")
def health():
    return {"status": "ok", "service": "SOCweave"}


@app.get("/scenario/{name}")
def run_scenario(name: str):
    """Load a mock scenario file and run it through the agent pipeline."""
    filepath = os.path.join(MOCK_DIR, f"scenario_{name}.json")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Scenario '{name}' not found")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Import here to avoid circular import issues at module load
    from agent.orchestrator import run_pipeline
    result = run_pipeline(data)
    return result


@app.post("/alert")
def submit_alert(alert: AlertPayload):
    """Accept a custom alert JSON and run the pipeline on it."""
    from agent.orchestrator import run_pipeline
    result = run_pipeline(alert.dict())
    return result