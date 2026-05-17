from datetime import datetime
from typing import List, Dict, Any, Literal
from pydantic import BaseModel

class ConversationTurn(BaseModel):
    user_id: str
    session_id: str
    turn_id: str
    timestamp: datetime
    role: Literal["user", "assistant"]
    content: str
    metadata: Dict[str, Any] = {}

class Memory(BaseModel):
    id: str
    content: str
    relevance: float
    type: str

class Pattern(BaseModel):
    id: str
    description: str
    confidence: float

class ContextResponse(BaseModel):
    user_id: str
    profile_summary: str
    relevant_memories: List[Memory] = []
    active_patterns: List[Pattern] = []
    delegation_hints: Dict[str, Any] = {}
