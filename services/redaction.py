
import re


# Match 12-digit Aadhaar numbers with optional spaces or hyphens.
_AADHAAR_PATTERN = re.compile(
    r"(?<!\d)(?:\d[ -]?){11}\d(?!\d)"
)

# Match 16-digit card numbers with optional spaces or hyphens.
_CARD_PATTERN = re.compile(
    r"(?<!\d)(?:\d[ -]?){15}\d(?!\d)"
)

# Match Indian 10-digit mobile numbers, optionally with +91.
_PHONE_PATTERN = re.compile(
    r"(?<![\d+])(?:\+?91[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)"
)

# Detect OTPs only when accompanied by a relevant label.
_OTP_PATTERN = re.compile(
    r"\b(?:otp|one[ -]?time\s+password|verification\s+code)\b"
    r"\s*(?:is\s*)?[:=-]?\s*\d{4,8}\b",
    re.IGNORECASE,
)


def redact_sensitive_data(text: str) -> str:
    """Replace common Indian identity and payment details with placeholders."""

    if not text:
        return text

    text = _OTP_PATTERN.sub("[REDACTED_OTP]", text)
    text = _CARD_PATTERN.sub("[REDACTED_CARD]", text)
    text = _PHONE_PATTERN.sub("[REDACTED_PHONE]", text)
    text = _AADHAAR_PATTERN.sub("[REDACTED_AADHAAR]", text)

    return text
