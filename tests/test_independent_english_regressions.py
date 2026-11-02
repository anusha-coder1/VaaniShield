import pytest

from services.risk_engine import analyze_transcript


@pytest.mark.parametrize(
    ("transcript", "expected_stages", "expected_tactics"),
    [
        (
            "This is an officer from the National Investigation Bureau. "
            "Your identity has been linked to an international money laundering case. "
            "You must remain on this video call and must not contact your family. "
            "Transfer the verification deposit to the account I am sending now, "
            "or you will be arrested today.",
            {"authority_claim", "accusation", "isolation", "payment_demand"},
            {"urgency", "authority_based_coercion", "payment_pressure"},
        ),
        (
            "I am calling from the cybercrime police department. "
            "A parcel registered in your name contains illegal documents. "
            "Do not disconnect this call or tell anyone about this investigation. "
            "Pay the security clearance fee immediately using this UPI ID.",
            {"authority_claim", "accusation", "isolation", "payment_demand"},
            {"urgency", "authority_based_coercion", "secrecy"},
        ),
        (
            "I am a senior officer with the central investigation agency. "
            "Your bank account is suspected of funding a criminal network. "
            "Stay alone in front of the camera and do not speak to anybody. "
            "We need you to transfer your savings to our temporary government account.",
            {"authority_claim", "accusation", "isolation", "payment_demand"},
            {"authority_based_coercion"},
        ),
        (
            "I am an officer from the national cyber investigation office. "
            "Your identity documents were used to open a suspicious account. "
            "You are not allowed to discuss this with your relatives. "
            "Transfer the investigation deposit within thirty minutes "
            "to avoid immediate detention.",
            {"authority_claim", "accusation", "isolation", "payment_demand"},
            {"urgency", "authority_based_coercion", "payment_pressure", "secrecy"},
        ),
        (
            "I am from your bank's security team. "
            "Your account will be blocked unless you confirm the OTP you just received. "
            "Read all six digits to me now so I can protect your money.",
            {"authority_claim"},
            {"urgency", "credential_harvesting", "authority_based_coercion"},
        ),
        (
            "I work with the payment support department. "
            "Your refund is waiting for approval. "
            "Enter your UPI PIN into the screen-sharing app so I can release the money.",
            {"authority_claim"},
            {"credential_harvesting", "authority_based_coercion"},
        ),
        (
            "I represent the bank's verification department. "
            "Your account is under review. "
            "Send a small verification transfer to this personal account "
            "and share the transaction screenshot to complete the process.",
            {"authority_claim", "payment_demand"},
            set(),
        ),
    ],
)
def test_independent_english_scam_examples(
    transcript, expected_stages, expected_tactics
):
    result = analyze_transcript(transcript)

    assert result.scam_detected is True
    assert expected_stages.issubset(set(result.stages_detected))
    assert expected_tactics.issubset(set(result.tactics_detected))
