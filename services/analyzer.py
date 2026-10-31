from models.schemas import AnalysisResult
from services.redaction import redact_sensitive_data
from services.risk_engine import analyze_transcript


def analyze(transcript: str) -> AnalysisResult:
	"""Redact sensitive data before analyzing a transcript for scam indicators."""
	redacted_transcript = redact_sensitive_data(transcript)
	return analyze_transcript(redacted_transcript)
