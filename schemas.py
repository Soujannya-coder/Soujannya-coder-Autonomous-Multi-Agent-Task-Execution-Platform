from pydantic import BaseModel
from typing import List, Dict, Optional

class RunRequest(BaseModel):
    session_id: str
    task: str

class RunResponse(BaseModel):
    status: str
    result: Optional[str] = None

class HistoryResponse(BaseModel):
    data: List[Dict]