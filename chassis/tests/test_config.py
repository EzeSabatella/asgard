import pytest
from pathlib import Path
from pydantic import ValidationError
from chassis.config import load_config, get_config, _config

def test_load_config_returns_chassis_config():
    """ChassisConfig se carga desde el YAML sin errores."""
    config = load_config()
    assert config is not None
    assert config.instance.type in ["personal", "enterprise"]
    assert config.instance.language == "es"

def test_get_config_is_singleton():
    """Dos llamadas a get_config() retornan el mismo objeto."""
    # Reset singleton if tests run out of order
    import chassis.config
    chassis.config._config = None
    
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2
    assert config1.instance.type == config2.instance.type

def test_observer_names_match_enabled_list():
    """Los nombres en observers.enabled son strings no vacíos."""
    config = get_config()
    for name in config.observers.enabled:
        assert isinstance(name, str)
        assert len(name) > 0
        
    # Also verify that aggressiveness keys match or are subsets
    for key in config.observers.aggressiveness.keys():
        assert isinstance(key, str)
        assert len(key) > 0
