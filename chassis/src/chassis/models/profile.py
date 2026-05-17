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
