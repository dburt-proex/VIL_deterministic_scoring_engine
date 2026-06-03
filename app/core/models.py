from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


SignalType = Literal[
    "lead",
    "rfi",
    "content",
    "support",
    "research",
    "workflow_request",
    "other",
]


class Route(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    CLARIFY = "CLARIFY"
    ARCHIVE = "ARCHIVE"
    HALT = "HALT"


class SourcePointer(BaseModel):
    type: str = Field(default="unknown", description="url, file, email, form, note, or other source pointer")
    value: str = Field(..., min_length=1)


class SignalInput(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{uuid4().hex[:12]}")
    source: str = Field(..., min_length=1)
    signal_type: SignalType = "other"
    content: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    source_pointers: List[SourcePointer] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)


class BatchSignalInput(BaseModel):
    signals: List[SignalInput] = Field(..., min_length=1)


class CriteriaScores(BaseModel):
    strategic_alignment: float = 0
    revenue_potential: float = 0
    compounding_leverage: float = 0
    automation_potential: float = 0
    cognitive_load_reduction: float = 0
    urgency: float = 0
    source_quality: float = 0
    completeness: float = 0

    @field_validator("*", mode="before")
    @classmethod
    def clamp_score(cls, value: Any) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return 0.0
        return max(0.0, min(10.0, numeric))

    def as_dict(self) -> Dict[str, float]:
        return self.model_dump()


class AuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"audit_{uuid4().hex[:12]}")
    signal_id: str
    input_hash: str
    criteria_scores: Dict[str, float]
    weights_used: Dict[str, float]
    thresholds_used: Dict[str, float]
    weighted_signal_score: float
    verifiability_score: float
    vil_score: float
    route: Route
    reason: str
    risk_flags: List[str] = Field(default_factory=list)
    decision_rule: str = "vil_score = min(weighted_signal_score, verifiability_score)"


class VILScoreObject(BaseModel):
    signal_id: str
    weighted_signal_score: float
    verifiability_score: float
    vil_score: float
    route: Route
    reason: str
    criteria_scores: Dict[str, float]
    risk_flags: List[str] = Field(default_factory=list)
    audit: AuditRecord


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "Verified Intelligence Layer"
    version: str = "1.0.0"
