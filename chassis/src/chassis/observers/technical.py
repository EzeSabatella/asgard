from typing import List
from chassis.observers.base import ConversationObserver
from chassis.models.context import ConversationTurn
from chassis.models.events import TechnicalEvent, BaseEvent
import uuid

class TechnicalObserver(ConversationObserver):
    """
    Captures technical decisions, stack choices, and project context.
    """
    
    @property
    def name(self) -> str:
        return "technical"

    @property
    def description(self) -> str:
        return "Captures decisions, stack, and project context."

    @property
    def aggressiveness(self) -> float:
        return 0.3  # Conservative by default

    def is_relevant(self, turn: ConversationTurn) -> bool:
        # Basic heuristic for MVP: search for technical keywords
        keywords = ["stack", "python", "docker", "database", "api", "framework", "library", "decision"]
        content_lower = turn.content.lower()
        return any(kw in content_lower for kw in keywords)

    async def observe(self, turn: ConversationTurn) -> List[BaseEvent]:
        # In a real scenario, this would use an LLM to extract events.
        # For the MVP/Scaffold, we'll return an empty list or a mock event if a keyword is found.
        events = []
        
        # Placeholder logic: if "decision" is in text, create a mock decision event
        if "decision" in turn.content.lower():
            events.append(TechnicalEvent(
                id=f"ev_{uuid.uuid4().hex[:8]}",
                type="DECISION",
                project=turn.metadata.get("project", "unknown"),
                content=f"Possible technical decision detected: {turn.content[:100]}...",
                tags=["technical", "extracted"],
                rationale="Detected via keyword heuristic"
            ))
            
        return events
