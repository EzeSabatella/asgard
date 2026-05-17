from typing import List
from chassis.models.context import ConversationTurn
from chassis.observers.base import ConversationObserver
from chassis.observers.registry import ObserverRegistry
from chassis.config import get_config


class Classifier:
    """
    Determines which ConversationObservers should process a given turn.
    Uses each observer's is_relevant() + aggressiveness threshold from config.
    """

    def __init__(self, registry: ObserverRegistry):
        self._registry = registry

    def classify(self, turn: ConversationTurn) -> List[ConversationObserver]:
        """
        Returns the list of observers that should process this turn.

        Selection criteria:
        1. Observer is in config.observers.enabled
        2. observer.is_relevant(turn) returns True
        3. observer.aggressiveness >= threshold defined in config (default 0.0)
        """
        config = get_config()
        enabled_names = set(config.observers.enabled)
        aggressiveness_map = config.observers.aggressiveness

        selected = []
        for observer in self._registry.get_all():
            if observer.name not in enabled_names:
                continue
            threshold = aggressiveness_map.get(observer.name, 0.0)
            if observer.aggressiveness < threshold:
                continue
            if observer.is_relevant(turn):
                selected.append(observer)

        return selected
