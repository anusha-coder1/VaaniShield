import json
from unittest.mock import Mock, patch

from services.gemini_analyzer import analyze_with_gemini


def test_gemini_evidence_matching_preserves_transcript_capitalization():
    transcript = "Share the OTP immediately to prevent account suspension."

    assessment = {
        "scam_detected": True,
        "risk_level": "CRITICAL",
        "stages_detected": [],
        "tactics_detected": ["credential_harvesting"],
        "indicator_evidence": [
            {
                "indicator": "credential_harvesting",
                "exact_phrases": ["share the OTP"],
                "explanation": "The caller requests an authentication code.",
                "potential_risk": "Account compromise.",
            }
        ],
        "explanation": "The caller demands an OTP.",
        "uncertainty_note": "Automated assessment.",
    }

    mock_response = Mock()
    mock_response.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": json.dumps(assessment)}]}}
        ]
    }

    with patch.dict("os.environ", {"GEMINI_API_KEY": "synthetic-test-key"}):
        with patch(
            "services.gemini_analyzer.requests.post",
            return_value=mock_response,
        ):
            result = analyze_with_gemini(transcript)

    assert result.scam_detected is True
    assert result.tactics_detected == ["credential_harvesting"]
    assert len(result.indicator_evidence) == 1
    assert result.indicator_evidence[0].exact_phrases == ["Share the OTP"]


def test_gemini_prompt_requires_evidence_for_each_indicator():
    transcript = "Share the OTP immediately to prevent account suspension."

    assessment = {
        "scam_detected": True,
        "risk_level": "CRITICAL",
        "stages_detected": [],
        "tactics_detected": ["credential_harvesting"],
        "indicator_evidence": [
            {
                "indicator": "credential_harvesting",
                "exact_phrases": ["Share the OTP"],
                "explanation": "An authentication code is requested.",
                "potential_risk": "Account compromise.",
            }
        ],
        "explanation": "The caller requests an OTP.",
        "uncertainty_note": "Automated assessment.",
    }

    mock_response = Mock()
    mock_response.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": json.dumps(assessment)}]}}
        ]
    }

    with patch.dict("os.environ", {"GEMINI_API_KEY": "synthetic-test-key"}):
        with patch(
            "services.gemini_analyzer.requests.post",
            return_value=mock_response,
        ) as mock_post:
            analyze_with_gemini(transcript)

    instructions = mock_post.call_args.kwargs["json"]["systemInstruction"]["parts"][0]["text"]

    assert "For every reported stage or tactic" in instructions
    assert "matching indicator" in instructions
    assert "Do not invent evidence" in instructions
