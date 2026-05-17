# Brief 02 — Sistema de configuración

**Tipo:** BRIEF  
**Fecha:** 2026-05-03 18:20  
**Autor:** Claude  
**Relacionado con:** DEC-010 (docs/20260503-1800_DECISION_decisions-log-sesion-01.md)  
**Estado:** Vigente

---

## Objetivo

Implementar el sistema de configuración del chassis: `chassis.config.yaml` como fuente de configuración de comportamiento, módulo `config.py` que lo carga y valida con Pydantic, e integración en el startup de la aplicación.

## Skills a activar

- [ ] `python-backend-dev` — Pydantic, carga de YAML, variables de entorno
- [ ] `devops-engineer` — separación secretos (.env) vs configuración (YAML)

## Contexto — documentos a leer primero

- `CLAUDE.md` — sección "Sistema de configuración"
- `SUPERAGENT.md` — sección "Configuración"
- `docs/20260503-1800_DECISION_decisions-log-sesion-01.md` — DEC-010
- `chassis/src/chassis/observers/registry.py` — ver cómo se registran los observers (el config debe referenciarlos por nombre)

---

## Tareas

### Tarea 1: Crear `chassis.config.yaml`

**Archivo a crear:**
- `chassis/chassis.config.yaml` (en la raíz del subproyecto chassis, no en la raíz del monorepo)

**Contrato — estructura completa del YAML:**

```yaml
# chassis.config.yaml
# Configuración de comportamiento del chassis.
# NO contiene secretos — para secretos, usar .env

instance:
  type: personal           # personal | enterprise
  user_id: "default-user"
  language: "es"

observers:
  enabled:
    - technical
    - empathic
    - humor
    - social
  aggressiveness:
    technical: 0.7
    empathic: 0.5
    humor: 0.3
    social: 0.4

embeddings:
  provider: openai           # openai | ollama
  model: text-embedding-3-small
  dimensions: 1536

consolidation:
  schedule_cron: "0 3 * * *"  # 3am diario
  min_events_to_consolidate: 5

mcp:
  enabled: true
  transport: stdio           # stdio | sse
  server_name: "superagent-chassis"
  server_version: "0.1.0"

api:
  host: "0.0.0.0"
  port: 8000
  debug: false
```

**Constraints:**
- Este archivo va al repositorio (no contiene secretos)
- Los valores del YAML son defaults razonables — el usuario los sobreescribe para su instancia

---

### Tarea 2: Crear módulo `config.py`

**Archivo a crear:**
- `chassis/src/chassis/config.py`

**Contrato — modelos Pydantic y función de carga:**

```python
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
```

**Constraints:**
- `get_config()` es el punto de acceso único a la configuración en toda la aplicación
- No leer variables de entorno en este módulo — ese trabajo es de `python-dotenv` en el entrypoint
- Si el YAML no existe o es inválido, lanzar excepción descriptiva (no silenciar el error)
- La dependencia `pyyaml` debe agregarse a `chassis/requirements.txt`

---

### Tarea 3: Agregar `pyyaml` a dependencias

**Archivo a modificar:**
- `chassis/requirements.txt` — agregar `pyyaml>=6.0`

**Constraints:**
- No pinear a una versión exacta — usar `>=`
- No agregar otras dependencias no requeridas por este brief

---

### Tarea 4: Test de carga de configuración

**Archivo a crear:**
- `chassis/tests/test_config.py`

**Contrato:**

```python
def test_load_config_returns_chassis_config():
    """ChassisConfig se carga desde el YAML sin errores."""

def test_get_config_is_singleton():
    """Dos llamadas a get_config() retornan el mismo objeto."""

def test_observer_names_match_enabled_list():
    """Los nombres en observers.enabled son strings no vacíos."""
```

**Constraints:**
- El test usa el `chassis.config.yaml` real del proyecto (no mock)
- Si hay algún campo requerido faltante en el YAML, el test debe fallar con mensaje claro

---

## Lo que NO entra en este brief

- Implementar observers reales a partir del config (eso es responsabilidad del registry)
- Conectar el config con la API de FastAPI
- Leer credenciales o secretos (eso es `.env` + `python-dotenv`, no este módulo)
- Crear el entrypoint de la aplicación

## Definición de Done

- [ ] `chassis/chassis.config.yaml` existe y tiene todos los campos del contrato
- [ ] `from chassis.config import get_config` funciona sin error
- [ ] `get_config()` retorna un `ChassisConfig` válido
- [ ] `test_config.py` pasa los 3 tests
- [ ] `pyyaml` agregado a `requirements.txt`
- [ ] Sin credenciales hardcodeadas
