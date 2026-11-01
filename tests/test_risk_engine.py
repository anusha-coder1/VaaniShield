import pytest

from models.schemas import RiskLevel
from services.risk_engine import analyze_transcript


def test_authority_claim_with_accusation_alone_does_not_prove_coercion():
	result = analyze_transcript(
		"This is the police. You are under investigation for fraud."
	)

	assert result.scam_detected is True
	assert "authority_claim" in result.stages_detected
	assert "accusation" in result.stages_detected
	assert "authority_based_coercion" not in result.tactics_detected


def test_authority_claim_alone_does_not_prove_impersonation():
	result = analyze_transcript("This is the police investigation unit.")

	assert "authority_claim" in result.stages_detected
	assert "authority_impersonation" not in result.tactics_detected


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


@pytest.mark.parametrize(
	"transcript",
	[
		"I am calling from the cybercrime department.",
		"This is the police investigation unit.",
		"We are calling from the CBI office.",
		"Your case has been transferred to our department.",
	],
)
def test_authority_claim_language_variations(transcript):
	result = analyze_transcript(transcript)

	assert "authority_claim" in result.stages_detected
	assert "authority_impersonation" not in result.tactics_detected
	assert result.exact_phrases


def test_telugu_digital_arrest_patterns_have_separate_evidence():
	result = analyze_transcript(
		"సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం. "
		"మీ ఆధార్ నంబర్ క్రిమినల్ దర్యాప్తుతో సంబంధం ఉంది. "
		"కాల్ కట్ చేయకండి, కుటుంబానికి చెప్పకండి. "
		"అరెస్టు తప్పించుకోవడానికి వెంటనే డబ్బు బదిలీ చేయండి."
	)

	assert result.scam_detected is True
	assert {"authority_claim", "accusation", "isolation", "payment_demand"}.issubset(
		set(result.stages_detected)
	)
	assert {"urgency", "authority_based_coercion", "payment_pressure", "secrecy"}.issubset(
		set(result.tactics_detected)
	)
	evidence = {item.indicator: item for item in result.indicator_evidence}
	assert "సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం" in evidence["authority_claim"].exact_phrases
	assert any(
		"డబ్బు బదిలీ చేయండి" in phrase
		for phrase in evidence["payment_demand"].exact_phrases
	)
	assert evidence["secrecy"].exact_phrases == ["కుటుంబానికి చెప్పకండి"]
	assert evidence["payment_pressure"].exact_phrases == [
		"అరెస్టు తప్పించుకోవడానికి వెంటనే డబ్బు బదిలీ చేయండి"
	]
	assert all(item.explanation and item.potential_risk for item in evidence.values())


def test_telugu_financial_fraud_patterns_keep_payment_demand_separate():
	result = analyze_transcript(
		"మీ బ్యాంకు ఖాతాలో అనుమానాస్పద లావాదేవీలు ఉన్నాయి. "
		"ఖాతా నిలిపివేయకుండా ఉండాలంటే ఇప్పుడే చెల్లించి మీ OTP చెప్పండి."
	)

	assert result.scam_detected is True
	assert "urgency" in result.tactics_detected
	assert "credential_harvesting" in result.tactics_detected
	assert "payment_pressure" in result.tactics_detected
	assert "payment_demand" not in result.stages_detected
	evidence = {item.indicator: item for item in result.indicator_evidence}
	assert evidence["payment_pressure"].exact_phrases == ["ఖాతా నిలిపివేయకుండా ఉండాలంటే"]
	assert evidence["credential_harvesting"].exact_phrases == ["మీ OTP చెప్పండి"]


@pytest.mark.parametrize(
	"transcript",
	[
		"నా బ్యాంకు అధికారిక యాప్‌లో సాధారణ UPI బదిలీ స్థితిని చూశాను. "
		"సహాయకుడు లావాదేవీ పూర్తయిందని తెలిపి OTP ఎవరితోనూ పంచుకోవద్దని గుర్తుచేశాడు.",
		"పాస్‌పోర్ట్ ధృవీకరణ కోసం నిర్ణయించిన సమయంలో పోలీస్ స్టేషన్‌కు వెళ్లాను. "
		"అధికారి గుర్తింపును పరిశీలించి తదుపరి విధానాన్ని వివరించారు.",
		"భద్రతా సూచన: మీ OTP, PIN లేదా పాస్‌వర్డ్‌ను ఫోన్‌లో అడిగే ఎవరికీ చెప్పవద్దు.",
		"సైబర్ భద్రత తరగతిలో డిజిటల్ అరెస్ట్ మోసాల గురించి చర్చించాము. "
		"ఉదాహరణలో కాలర్ పోలీస్ అని చెప్పి డబ్బు అడుగుతాడు.",
	],
)
def test_genuine_telugu_examples_do_not_trigger_scam_indicators(transcript):
	result = analyze_transcript(transcript)

	assert result.scam_detected is False
	assert result.stages_detected == []
	assert result.tactics_detected == []
	assert result.exact_phrases == []


@pytest.mark.parametrize(
	"transcript",
	[
		"Your Aadhaar number is linked to a criminal investigation.",
		"Your bank account was involved in illegal transactions.",
		"Your identity has been used for money laundering.",
		"You are suspected of participating in a financial crime.",
	],
)
def test_accusation_language_variations(transcript):
	result = analyze_transcript(transcript)

	assert "accusation" in result.stages_detected
	assert result.exact_phrases


@pytest.mark.parametrize(
	"transcript",
	[
		"Do not disconnect this call.",
		"Do not contact your family.",
		"You must remain on video call.",
		"Do not discuss this investigation with anyone.",
	],
)
def test_isolation_language_variations(transcript):
	result = analyze_transcript(transcript)

	assert "isolation" in result.stages_detected
	assert result.exact_phrases




def test_account_freeze_until_payment_is_payment_pressure_not_demand():
	result = analyze_transcript("Your account will remain frozen until payment.")

	assert "payment_demand" not in result.stages_detected
	assert "payment_pressure" in result.tactics_detected
	assert result.exact_phrases

@pytest.mark.parametrize(
	"transcript",
	[
		"Transfer fifty thousand rupees.",
		"Send money to this verification account.",
		"Pay the security deposit immediately.",
		"Transfer the amount to avoid arrest.",
	],
)

def test_payment_demand_language_variations(transcript):
	result = analyze_transcript(transcript)

	assert "payment_demand" in result.stages_detected
	assert result.exact_phrases


@pytest.mark.parametrize(
	("transcript", "expected_tactic"),
	[
		("You have ten minutes to respond.", "urgency"),
		(
			"I am calling from the police investigation unit. You are under investigation. Do not tell anyone.",
			"authority_based_coercion",
		),
		("Please provide your OTP.", "credential_harvesting"),
		("Transfer fifty thousand rupees to avoid arrest.", "payment_pressure"),
		("Keep this investigation confidential.", "secrecy"),
	],
)
def test_each_tactic_has_a_contextual_phrase(transcript, expected_tactic):
	result = analyze_transcript(transcript)

	assert expected_tactic in result.tactics_detected
	assert result.exact_phrases


def test_overlapping_matches_prefer_the_complete_supporting_phrase():
	transcript = "You must transfer fifty thousand rupees immediately to avoid arrest."
	result = analyze_transcript(transcript)

	assert result.exact_phrases == [
		"transfer fifty thousand rupees immediately to avoid arrest"
	]
	evidence = {item.indicator: item for item in result.indicator_evidence}
	assert evidence["payment_demand"].exact_phrases == result.exact_phrases
	assert evidence["payment_pressure"].exact_phrases == result.exact_phrases
	assert evidence["urgency"].exact_phrases == result.exact_phrases


def test_independent_evidence_in_same_sentence_is_preserved():
	result = analyze_transcript(
		"This is the police; you are under investigation, and transfer fifty "
		"thousand rupees immediately to avoid arrest."
	)

	assert "This is the police" in result.exact_phrases
	assert "you are under investigation" in result.exact_phrases
	assert any("transfer fifty thousand rupees" in phrase for phrase in result.exact_phrases)


def test_each_detected_stage_and_tactic_has_supporting_explanation():
	result = analyze_transcript(
		"This is the police. You are under investigation. Do not contact your family. "
		"Transfer fifty thousand rupees immediately to avoid arrest. "
		"Keep this confidential. Please provide your OTP."
	)
	evidence = {item.indicator: item for item in result.indicator_evidence}
	detected = set(result.stages_detected + result.tactics_detected)

	assert set(evidence) == detected
	for indicator, item in evidence.items():
		assert item.exact_phrases
		assert all(phrase in result.exact_phrases for phrase in item.exact_phrases)
		assert item.explanation
		assert item.potential_risk


def test_no_explanations_are_created_for_undetected_indicators():
	result = analyze_transcript(
		"I visited the police station to ask about a routine verification."
	)

	assert result.scam_detected is False
	assert result.indicator_evidence == []
	assert result.exact_phrases == []


def test_educational_scam_example_is_not_classified_as_a_live_scam():
	result = analyze_transcript(
		"In a scam-awareness lesson, we discuss an example script: "
		"This is the police, you are under investigation, transfer the money "
		"to avoid arrest."
	)

	assert result.scam_detected is False
	assert result.stages_detected == []
	assert result.tactics_detected == []
	assert result.exact_phrases == []


@pytest.mark.parametrize(
	"transcript",
	[
		"The police checked my identity during a scheduled passport verification.",
		"I use UPI, NEFT, IMPS and RTGS for ordinary bank transactions.",
		"My sister transferred money to me for our household expenses.",
		"Aadhaar and PAN are required for my bank's normal KYC process.",
	],
)
def test_legitimate_verification_finance_and_identity_mentions_are_not_scams(transcript):
	result = analyze_transcript(transcript)

	assert result.scam_detected is False
	assert "credential_harvesting" not in result.tactics_detected
	assert "payment_pressure" not in result.tactics_detected


def test_protective_warning_does_not_hide_a_separate_suspicious_demand():
	result = analyze_transcript(
		"The bank warns customers never share your OTP or PIN. "
		"The caller says transfer fifty thousand rupees to avoid arrest."
	)

	assert result.scam_detected is True
	assert "payment_demand" in result.stages_detected
	assert "payment_pressure" in result.tactics_detected
	assert "credential_harvesting" not in result.tactics_detected
	assert any("transfer fifty thousand rupees" in phrase for phrase in result.exact_phrases)


def test_payment_demand_with_authority_claim_is_detected():
	result = analyze_transcript("This is the police. Transfer the money.")

	assert "authority_claim" in result.stages_detected
	assert "payment_demand" in result.stages_detected
	assert "authority_based_coercion" not in result.tactics_detected
	assert result.scam_detected is True
	assert result.risk_level == RiskLevel.MEDIUM


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
