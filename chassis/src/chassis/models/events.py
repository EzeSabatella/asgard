from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    id: str
    ts: datetime = Field(default_factory=datetime.now)
    source: str = "conversation"
    consolidated: bool = False
    metadata: Dict[str, Any] = {}

class TechnicalEvent(BaseEvent):
    type: Literal["DECISION", "PREFERENCE", "INSIGHT", "PROJECT_UPDATE", "BLOCKER", "MILESTONE"]
    project: str
    tags: List[str] = []
    content: str
    rationale: Optional[str] = None

class EmotionalEvent(BaseEvent):
    type: Literal["EMOTIONAL_SIGNAL", "RELATIONAL_PATTERN", "SUPPORT_OUTCOME", "HUMOR_SIGNAL", "BOND_REINFORCEMENT"]
    signal: str
    trigger: Optional[str] = None
    intensity: float = Field(ge=0.0, le=1.0)
    context: str
