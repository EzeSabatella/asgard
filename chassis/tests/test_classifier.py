from datetime import datetime
from unittest.mock import MagicMock, patch
from chassis.classifier import Classifier
from chassis.models.context import ConversationTurn


def _make_turn() -> ConversationTurn:
    return ConversationTurn(
        user_id="u1",
        session_id="s1",
        turn_id="t1",
        timestamp=datetime.now(),
        role="user",
        content="hello",
    )

def _setup_mock_config(patcher, enabled, aggressiveness):
    mock_config = MagicMock()
    mock_config.observers.enabled = enabled
    mock_config.observers.aggressiveness = aggressiveness
    patcher.return_value = mock_config

def test_disabled_observer_not_selected():
    """Observer fuera de config.observers.enabled no se selecciona."""
    observer = MagicMock()
    observer.name = "test_obs"
    observer.aggressiveness = 0.5
    observer.is_relevant.return_value = True
    
    registry = MagicMock()
    registry.get_all.return_value = [observer]
    
    classifier = Classifier(registry)
    turn = _make_turn()
    
    with patch("chassis.classifier.get_config") as mock_get_config:
        _setup_mock_config(mock_get_config, enabled=[], aggressiveness={})
        result = classifier.classify(turn)
        
    assert len(result) == 0

def test_irrelevant_observer_not_selected():
    """Observer cuyo is_relevant() retorna False no se selecciona."""
    observer = MagicMock()
    observer.name = "test_obs"
    observer.aggressiveness = 0.5
    observer.is_relevant.return_value = False
    
    registry = MagicMock()
    registry.get_all.return_value = [observer]
    
    classifier = Classifier(registry)
    turn = _make_turn()
    
    with patch("chassis.classifier.get_config") as mock_get_config:
        _setup_mock_config(mock_get_config, enabled=["test_obs"], aggressiveness={})
        result = classifier.classify(turn)
        
    assert len(result) == 0

def test_relevant_enabled_observer_selected():
    """Observer habilitado y relevante aparece en el resultado."""
    observer = MagicMock()
    observer.name = "test_obs"
    observer.aggressiveness = 0.5
    observer.is_relevant.return_value = True
    
    registry = MagicMock()
    registry.get_all.return_value = [observer]
    
    classifier = Classifier(registry)
    turn = _make_turn()
    
    with patch("chassis.classifier.get_config") as mock_get_config:
        _setup_mock_config(mock_get_config, enabled=["test_obs"], aggressiveness={"test_obs": 0.1})
        result = classifier.classify(turn)
        
    assert len(result) == 1
    assert result[0] == observer

def test_aggressiveness_below_threshold_excluded():
    """Observer con aggressiveness menor al threshold del config no se selecciona."""
    observer = MagicMock()
    observer.name = "test_obs"
    observer.aggressiveness = 0.2  # Below threshold
    observer.is_relevant.return_value = True
    
    registry = MagicMock()
    registry.get_all.return_value = [observer]
    
    classifier = Classifier(registry)
    turn = _make_turn()
    
    with patch("chassis.classifier.get_config") as mock_get_config:
        # Threshold is 0.5
        _setup_mock_config(mock_get_config, enabled=["test_obs"], aggressiveness={"test_obs": 0.5})
        result = classifier.classify(turn)
        
    assert len(result) == 0
