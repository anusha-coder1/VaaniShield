from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
	LOW = "LOW"
	MEDIUM = "MEDIUM"
	HIGH = "HIGH"
	CRITICAL = "CRITICAL"


Stage = Literal[
	"authority_claim",
	"accusation",
	"isolation",
	"payment_demand",
]

Tactic = Literal[
	"urgency",
	"authority_impersonation",
	"credential_harvesting",
	"payment_pressure",
	"secrecy",
]


class AnalysisResult(BaseModel):
	scam_detected: bool
	risk_level: RiskLevel
	stages_detected: list[Stage]
	tactics_detected: list[Tactic]
	exact_phrases: list[str]
	indicator_evidence: list[IndicatorEvidence] = Field(default_factory=list)
	confidence: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)
	uncertainty_note: str

class IndicatorEvidence(BaseModel):
	indicator: str
	exact_phrases: list[str]
	explanation: str
	potential_risk: str
