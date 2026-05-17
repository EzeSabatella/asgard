from pathlib import Path
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel
import yaml


class InstanceConfig(BaseModel):
    type: Literal["personal", "enterprise"]
    user_id: str
    language: str = "es"

class ObserversConfig(BaseModel):
    enabled: List[str]
    aggressiveness: Dict[str, float] = {}

class EmbeddingsConfig(BaseModel):
    provider: Literal["openai", "ollama"]
    model: str
    dimensions: int

class ConsolidationConfig(BaseModel):
    schedule_cron: str
    min_events_to_consolidate: int = 5

class McpConfig(BaseModel):
    enabled: bool = True
    transport: Literal["stdio", "sse"] = "stdio"
    server_name: str
    server_version: str

class ApiConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

class ChassisConfig(BaseModel):
    instance: InstanceConfig
    observers: ObserversConfig
    embeddings: EmbeddingsConfig
    consolidation: ConsolidationConfig
    mcp: McpConfig
    api: ApiConfig


def load_config(config_path: Optional[Path] = None) -> ChassisConfig:
    """
    Loads and validates chassis.config.yaml.
    Defaults to chassis/chassis.config.yaml relative to this file's package root.
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "chassis.config.yaml"
    
    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    
    return ChassisConfig(**raw)


# Singleton — cargado una vez al inicio
_config: Optional[ChassisConfig] = None

def get_config() -> ChassisConfig:
    global _config
    if _config is None:
        _config = load_config()
    return _config
