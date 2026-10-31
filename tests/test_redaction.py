import pytest

from services.redaction import redact_sensitive_data


def test_redacts_aadhaar_number():
	result = redact_sensitive_data("Aadhaar: 123456789012")

	assert result == "Aadhaar: [REDACTED_AADHAAR]"


def test_redacts_card_number():
	result = redact_sensitive_data("Card: 4111111111111111")

	assert result == "Card: [REDACTED_CARD]"


def test_redacts_indian_phone_number():
	result = redact_sensitive_data("Call 9876543210")

	assert result == "Call [REDACTED_PHONE]"


def test_redacts_phone_number_with_country_code():
	result = redact_sensitive_data("Call +91 9876543210")

	assert result == "Call [REDACTED_PHONE]"


def test_redacts_otp_with_otp_context():
	result = redact_sensitive_data("Your OTP is 482731")

	assert result == "Your [REDACTED_OTP]"


@pytest.mark.parametrize("number", ["1234", "654321"])
def test_keeps_numbers_without_otp_context(number):
	text = f"Reference number: {number}"

	assert redact_sensitive_data(text) == text


def test_empty_input_returns_empty_string():
	assert redact_sensitive_data("") == ""


def test_normal_text_remains_unchanged():
	text = "Please review the details and call back tomorrow."

	assert redact_sensitive_data(text) == text
