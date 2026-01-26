from pydantic import BaseModel
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    query: str
    session_id: str
