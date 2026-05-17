# Brief 01 — Correcciones base del chassis

**Tipo:** BRIEF  
**Fecha:** 2026-05-03 18:10  
**Autor:** Claude  
**Relacionado con:** DEC-006, DEC-007 (docs/20260503-1800_DECISION_decisions-log-sesion-01.md)  
**Estado:** Vigente

---

## Objetivo

Corregir los gaps estructurales del código existente: `__init__.py` faltantes, renombrar `Observer` → `ConversationObserver`, agregar `SystemObserver`, y actualizar `profile.py` con la jerarquía `BaseProfile` + extensiones tipadas.

## Skills a activar

- [ ] `python-backend-dev` — Pydantic models, imports, ABC
- [ ] `ai-ml-engineer` — Contratos de Observer, lógica de aggressiveness

## Contexto — documentos a leer primero

- `CLAUDE.md` — roles y principios del proyecto
- `SUPERAGENT.md` — sección "Capa de Observadores" y "Profile Schema"
- `docs/20260503-1800_DECISION_decisions-log-sesion-01.md` — DEC-006 y DEC-007
- `chassis/src/chassis/observers/base.py` — clase actual (a modificar)
- `chassis/src/chassis/models/profile.py` — modelo actual (a reemplazar)

---

## Tareas

### Tarea 1: Agregar `__init__.py` faltantes

**Archivos a crear:**
- `chassis/src/chassis/models/__init__.py` — vacío (solo hace el directorio un paquete Python)
- `chassis/src/chassis/observers/__init__.py` — vacío

**Constraints:**
- No importar nada en estos `__init__.py` — solo existir
- No modificar ningún otro archivo en esta tarea

**Comportamiento esperado:**
```python
from chassis.models.profile import BaseProfile  # debe funcionar sin ImportError
from chassis.observers.base import ConversationObserver  # idem
```

---

### Tarea 2: Renombrar `Observer` → `ConversationObserver` y agregar `SystemObserver`

**Archivos a modificar:**
- `chassis/src/chassis/observers/base.py` — renombrar clase + agregar SystemObserver
- `chassis/src/chassis/observers/technical.py` — actualizar herencia e imports
- `chassis/src/chassis/observers/registry.py` — actualizar imports y type hints

**Contrato — `chassis/src/chassis/observers/base.py` debe quedar:**

```python
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
```

**Contrato — `chassis/src/chassis/observers/technical.py`:**
- La clase `TechnicalObserver` debe heredar de `ConversationObserver` (no de `Observer`)
- Actualizar el import: `from chassis.observers.base import ConversationObserver`
- No cambiar ninguna lógica interna del observer

**Contrato — `chassis/src/chassis/observers/registry.py`:**
- Actualizar todos los type hints que usen `Observer` → `ConversationObserver`
- Actualizar el import en la primera línea

**Constraints:**
- `SkillProposal` hereda de `BaseEvent` — importar desde `chassis.models.events`
- No crear implementaciones concretas de `SystemObserver` en este brief (eso es Fase 2)
- Conservar la lógica existente en `technical.py` y `registry.py` — solo renombrar

---

### Tarea 3: Actualizar `profile.py` con jerarquía BaseProfile

**Archivo a reemplazar:**
- `chassis/src/chassis/models/profile.py`

**Contrato — schema completo:**

```python
from datetime import datetime
from typing import Dict, List, Literal, Any
from pydantic import BaseModel, Field


# --- Sub-modelos compartidos ---

class CommunicationProfile(BaseModel):
    tone_preferred: str
    humor_style: List[str] = []
    responds_well_to: str
    language: str = "es"

class ProjectStatus(BaseModel):
    status: str
    priority: int

class DelegationMap(BaseModel):
    auto_execute: List[str] = []
    execute_with_log: List[str] = []
    recommend_only: List[str] = []
    always_escalate: List[str] = []


# --- Sub-modelos personales ---

class CognitiveProfile(BaseModel):
    learning_style: str
    decision_making: str
    prefers_analogies: bool = True
    domain_expertise: Dict[str, float] = {}

class EmotionalPatterns(BaseModel):
    humor_as_defense: Dict[str, Any] = {}
    energy_peak: str = ""
    support_style_effective: str = ""


# --- Sub-modelos enterprise ---

class OrganizationalProfile(BaseModel):
    industry: str
    size: str
    decision_structure: str

class OperationalPatterns(BaseModel):
    peak_hours: List[str] = []
    escalation_paths: Dict[str, str] = {}
    recurring_workflows: List[str] = []


# --- Jerarquía de perfiles ---

class BaseProfile(BaseModel):
    user_id: str
    version: int = 1
    last_updated: datetime = Field(default_factory=datetime.now)
    instance_type: Literal["personal", "enterprise"]
    communication: CommunicationProfile
    active_projects: Dict[str, ProjectStatus] = {}
    delegation_map: DelegationMap
    decisions_log_refs: List[str] = []
    episodic_refs: List[str] = []

class PersonalProfile(BaseProfile):
    instance_type: Literal["personal"] = "personal"
    cognitive_profile: CognitiveProfile
    emotional_patterns: EmotionalPatterns

class EnterpriseProfile(BaseProfile):
    instance_type: Literal["enterprise"] = "enterprise"
    organizational_profile: OrganizationalProfile
    operational_patterns: OperationalPatterns
```

**Constraints:**
- El modelo `UserProfile` existente debe eliminarse — queda reemplazado por esta jerarquía
- No usar `Union` explícito para el discriminador — Pydantic lo resuelve via `instance_type: Literal[...]`
- `DelegationMap` debe conservar las 4 listas de la versión anterior

---

## Lo que NO entra en este brief

- Implementar lógica de negocio en los observers (solo contratos)
- Crear stores, API, ni endpoints
- Implementar `SystemObserver` concreto (Völundr es Fase 2)
- Modificar `docker-compose.yml` ni configuración de infra

## Definición de Done

- [ ] `from chassis.models.profile import BaseProfile, PersonalProfile, EnterpriseProfile` funciona sin error
- [ ] `from chassis.observers.base import ConversationObserver, SystemObserver` funciona sin error
- [ ] `TechnicalObserver` hereda de `ConversationObserver`
- [ ] `registry.py` no tiene ninguna referencia a la clase `Observer` (solo `ConversationObserver`)
- [ ] El modelo `UserProfile` no existe más en el codebase
- [ ] Tests existentes de `TechnicalObserver` siguen pasando (si alguno falla por el renombrado, corregirlo)
- [ ] Sin credenciales hardcodeadas