from typing import Dict, List, Optional
from chassis.observers.base import ConversationObserver

class ObserverRegistry:
    """
    Registry to manage and retrieve active observers.
    """
    def __init__(self):
        self._observers: Dict[str, ConversationObserver] = {}

    def register(self, observer: ConversationObserver):
        self._observers[observer.name] = observer

    def get_observer(self, name: str) -> Optional[ConversationObserver]:
        return self._observers.get(name)

    def list_observers(self) -> List[ConversationObserver]:
        return list(self._observers.values())

    def get_all(self) -> List[ConversationObserver]:
        return self.list_observers()

# Global registry instance
registry = ObserverRegistry()
