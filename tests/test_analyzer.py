from pathlib import Path

from streamlit.testing.v1 import AppTest

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
	assert isinstance(result.indicator_evidence, list)


def test_redacted_sensitive_value_is_not_exposed_in_evidence():
	result = analyze(
		"Your Aadhaar number 1234 5678 9012 has been linked to a criminal investigation."
	)

	assert "accusation" in result.stages_detected
	all_evidence = " ".join(
		phrase
		for evidence in result.indicator_evidence
		for phrase in evidence.exact_phrases
	)
	assert "[REDACTED_AADHAAR]" in all_evidence
	assert "1234 5678 9012" not in all_evidence


def _submit_text_analysis(transcript):
	app_path = Path(__file__).resolve().parents[1] / "app.py"
	app = AppTest.from_file(app_path, default_timeout=15).run()
	next(button for button in app.button if button.label == "Analyze").click().run()
	text_area = next(
		widget for widget in app.text_area if widget.label == "Suspicious call transcript"
	)
	text_area.set_value(transcript)
	next(button for button in app.button if button.label == "Analyze Conversation").click().run()
	return app


def test_ui_labels_undetected_indicators_narrowly():
	app = _submit_text_analysis("I use UPI for ordinary bank transactions.")

	assert not app.exception
	assert sum(
		"Not detected in the supplied conversation." in caption.value
		for caption in app.caption
	) == 9


def test_ui_shows_high_risk_safety_recommendations_without_submitting_reports():
	app = _submit_text_analysis(
		"This is the police. You are under investigation for fraud. "
		"Pay the fine immediately or you will be arrested."
	)

	assert not app.exception
	warnings = " ".join(item.value for item in app.warning)
	assert "end the suspicious call" in warnings
	assert "Do not transfer money" in warnings
	assert "independently sourced official contact details" in warnings
	assert "inform someone you trust" in warnings
	assert "1930" in warnings
	assert "cybercrime.gov.in" in warnings
	assert "will not contact anyone or submit a report" in warnings
