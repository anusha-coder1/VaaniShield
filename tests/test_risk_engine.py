import pytest

from models.schemas import RiskLevel
from services.risk_engine import analyze_transcript


def test_authority_impersonation_with_accusation_is_detected():
	result = analyze_transcript(
		"This is the police. You are under investigation for fraud."
	)

	assert result.scam_detected is True
	assert "authority_claim" in result.stages_detected
	assert "accusation" in result.stages_detected
	assert "authority_impersonation" in result.tactics_detected


def test_isolation_language_is_detected_as_a_stage():
	result = analyze_transcript("Do not tell anyone. Stay on the line.")

	assert "isolation" in result.stages_detected
	assert result.scam_detected is False


def test_otp_request_is_credential_harvesting_and_scam_alert():
	result = analyze_transcript("Share your OTP with me.")

	assert "credential_harvesting" in result.tactics_detected
	assert result.scam_detected is True
	assert result.risk_level == RiskLevel.HIGH


@pytest.mark.parametrize(
	"transcript",
	[
		"Never share your OTP with anyone.",
		"Do not share your PIN.",
		"Please never reveal your password.",
		"The bank will never ask for your OTP.",
	],
)
def test_protective_credential_warnings_are_not_scam_indicators(transcript):
	result = analyze_transcript(transcript)

	assert "credential_harvesting" not in result.tactics_detected
	assert result.scam_detected is False


def test_negated_warning_does_not_suppress_a_later_credential_request():
	result = analyze_transcript(
		"Never share your OTP with anyone. Share your OTP with me."
	)

	assert "credential_harvesting" in result.tactics_detected
	assert result.scam_detected is True
	assert "Share your OTP" in result.exact_phrases


def test_payment_demand_with_authority_claim_is_detected():
	result = analyze_transcript("This is the police. Transfer the money.")

	assert "authority_claim" in result.stages_detected
	assert "payment_demand" in result.stages_detected
	assert result.scam_detected is True
	assert result.risk_level == RiskLevel.HIGH


def test_urgency_phrase_is_detected():
	result = analyze_transcript("Please respond immediately.")

	assert "urgency" in result.tactics_detected
	assert result.scam_detected is False


def test_serious_criminal_investigation_is_detected_as_accusation():
	result = analyze_transcript("You are under a serious criminal investigation.")

	assert "accusation" in result.stages_detected
	assert "serious criminal investigation" in result.exact_phrases[0]


def test_standalone_immediately_is_detected_as_urgency():
	result = analyze_transcript("You must respond immediately.")

	assert "urgency" in result.tactics_detected
	assert result.scam_detected is False


def test_confidential_investigation_is_detected_as_secrecy():
	result = analyze_transcript("Keep the investigation confidential.")

	assert "secrecy" in result.tactics_detected
	assert result.scam_detected is False


def test_payment_demand_with_consequence_is_payment_pressure():
	result = analyze_transcript(
		"Pay the fine immediately or you will be arrested."
	)

	assert "payment_demand" in result.stages_detected
	assert "urgency" in result.tactics_detected
	assert "payment_pressure" in result.tactics_detected
	assert result.scam_detected is True


def test_combined_scam_indicators_reach_critical_risk():
	result = analyze_transcript(
		"This is the police. You are under a serious criminal investigation. "
		"Pay the fine immediately or you will be arrested. Keep this confidential."
	)

	assert result.scam_detected is True
	assert result.risk_level == RiskLevel.CRITICAL
	assert "accusation" in result.stages_detected
	assert {"urgency", "payment_pressure", "secrecy"}.issubset(
		set(result.tactics_detected)
	)


def test_aadhaar_linked_to_criminal_investigation_is_accusation():
	result = analyze_transcript(
		"Your Aadhaar number has been linked to a serious criminal investigation."
	)

	assert "accusation" in result.stages_detected
	assert result.scam_detected is False


def test_rupee_transfer_with_arrest_consequence_is_payment_pressure():
	result = analyze_transcript(
		"You must transfer ₹50,000 immediately to the verification account to avoid arrest."
	)

	assert "payment_demand" in result.stages_detected
	assert "urgency" in result.tactics_detected
	assert "payment_pressure" in result.tactics_detected
	assert result.scam_detected is True


def test_legitimate_security_warning_is_not_classified_as_a_scam():
	result = analyze_transcript(
		"The bank said never share your OTP or PIN. "
		"I immediately called them about a confidential investigation."
	)

	assert "credential_harvesting" not in result.tactics_detected
	assert result.scam_detected is False


@pytest.mark.parametrize(
	"transcript",
	[
		"Our bank is investigating a delayed transfer from yesterday.",
		"I transferred ₹50,000 to the clinic for a scheduled procedure.",
	],
)
def test_investigations_and_ordinary_payments_are_not_automatically_scams(transcript):
	result = analyze_transcript(transcript)

	assert result.scam_detected is False
	assert "payment_pressure" not in result.tactics_detected


def test_harmless_police_station_and_bank_mentions_are_not_a_scam():
	result = analyze_transcript(
		"I visited the police station near my bank to ask about opening an account."
	)

	assert result.scam_detected is False
	assert result.stages_detected == []
	assert result.tactics_detected == []
	assert result.exact_phrases == []


def test_empty_transcript_returns_a_safe_result():
	result = analyze_transcript("")

	assert result.scam_detected is False
	assert result.risk_level == RiskLevel.LOW
	assert result.stages_detected == []
	assert result.tactics_detected == []
	assert result.exact_phrases == []


@pytest.mark.parametrize(
	"transcript",
	[
		"",
		"The station is beside my bank.",
		"Please respond immediately.",
		"Share your OTP now.",
		"This is the police. Transfer the money.",
	],
)
def test_confidence_stays_between_zero_and_one(transcript):
	result = analyze_transcript(transcript)

	assert 0.0 <= result.confidence <= 1.0


def test_exact_matched_phrases_are_included():
	result = analyze_transcript(
		"This is the police. You are under investigation for fraud."
	)

	assert "This is the police" in result.exact_phrases
	assert "You are under investigation for fraud" in result.exact_phrases
