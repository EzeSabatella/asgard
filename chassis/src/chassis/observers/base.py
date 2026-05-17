from abc import ABC, abstractmethod
from typing import List
from chassis.models.context import ConversationTurn
from chassis.models.events import BaseEvent


class ConversationObserver(ABC):
    """Triggered per ConversationTurn. Extracts events from conversation."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @property
    @abstractmethod
    def aggressiveness(self) -> float: ...

    @abstractmethod
    def is_relevant(self, turn: ConversationTurn) -> bool: ...

    @abstractmethod
    async def observe(self, turn: ConversationTurn) -> List[BaseEvent]: ...


class SkillProposal(BaseEvent):
    """Output of SystemObserver — a proposal to create a new skill."""
    gap_description: str
    skill_name: str
    skill_md_content: str
    python_code: str


class SystemObserver(ABC):
    """Triggered by system state (pattern store). Detects capability gaps."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    async def analyze(self, pattern_store_snapshot: dict) -> List[SkillProposal]: ...
