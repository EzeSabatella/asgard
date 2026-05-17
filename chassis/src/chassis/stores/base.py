from abc import ABC, abstractmethod
from typing import List, Optional
from chassis.models.events import BaseEvent


class BaseStore(ABC):
    """Abstract interface for all event stores."""

    @abstractmethod
    async def save_event(self, event: BaseEvent) -> str:
        """
        Persists a single event. Returns the event_id assigned.
        INVARIANT: consolidated is always set to False on write.
        """
        ...

    @abstractmethod
    async def save_events(self, events: List[BaseEvent]) -> List[str]:
        """Persists multiple events atomically. Returns list of event_ids."""
        ...

    @abstractmethod
    async def get_unconsolidated(self, limit: int = 100) -> List[BaseEvent]:
        """Returns events where consolidated = False, ordered by created_at ASC."""
        ...

    @abstractmethod
    async def mark_consolidated(self, event_ids: List[str]) -> int:
        """
        Sets consolidated = True for the given event_ids.
        Returns count of rows updated.
        ONLY the consolidator may call this method.
        """
        ...

    @abstractmethod
    async def get_by_id(self, event_id: str) -> Optional[BaseEvent]:
        """Returns a single event by its ID, or None if not found."""
        ...
