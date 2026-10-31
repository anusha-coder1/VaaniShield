from models.schemas import AnalysisResult, RiskLevel
from services.analyzer import analyze


def test_otp_request_is_detected_as_a_scam():
	result = analyze("Please share your OTP now.")

	assert result.scam_detected is True
	assert "credential_harvesting" in result.tactics_detected


def test_aadhaar_number_is_redacted_before_risk_analysis(monkeypatch):
	expected_result = AnalysisResult(
		scam_detected=False,
		risk_level=RiskLevel.LOW,
		stages_detected=[],
		tactics_detected=[],
		exact_phrases=[],
		confidence=0.1,
		uncertainty_note="Synthetic test result.",
	)

	def check_redacted_text(text):
		assert "[REDACTED_AADHAAR]" in text
		assert "1234 5678 9012" not in text
		return expected_result

	monkeypatch.setattr("services.analyzer.analyze_transcript", check_redacted_text)
	result = analyze("My Aadhaar number is 1234 5678 9012.")

	assert result is expected_result


def test_empty_transcript_returns_valid_result():
	result = analyze("")

	assert isinstance(result, AnalysisResult)
	assert result.scam_detected is False
	assert result.risk_level == RiskLevel.LOW
	assert result.stages_detected == []
	assert result.tactics_detected == []
	assert result.exact_phrases == []


def test_harmless_conversation_is_not_classified_as_a_scam():
	result = analyze(
		"I visited the police station beside my bank to ask about opening an account."
	)

	assert result.scam_detected is False
	assert result.stages_detected == []
	assert result.tactics_detected == []


def test_result_follows_analysis_result_schema():
	result = analyze("Please share your OTP now.")

	assert isinstance(result, AnalysisResult)
	assert isinstance(result.scam_detected, bool)
	assert isinstance(result.risk_level, RiskLevel)
	assert isinstance(result.stages_detected, list)
	assert isinstance(result.tactics_detected, list)
	assert isinstance(result.exact_phrases, list)
	assert isinstance(result.confidence, float)
	assert 0.0 <= result.confidence <= 1.0
	assert isinstance(result.uncertainty_note, str)
