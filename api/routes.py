from fastapi import APIRouter
from schemas import RunRequest, RunResponse
from services.orchestrator import Orchestrator

router = APIRouter()

orchestrator = None  # injected later

def set_orchestrator(o):
    global orchestrator
    orchestrator = o


@router.post("/run", response_model=RunResponse)
def run(req: RunRequest):
    return orchestrator.run(req.session_id, req.task)


@router.get("/history/{session_id}")
def history(session_id: str):
    return orchestrator.memory.fetch(session_id)


@router.get("/health")
def health():
    return {"status": "ok"}