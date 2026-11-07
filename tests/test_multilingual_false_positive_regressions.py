import json
from pathlib import Path

import pytest

from services.risk_engine import analyze_transcript


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "independent_evaluation_v1_development.json"
)

with DATASET_PATH.open(encoding="utf-8") as file:
    DATASET = json.load(file)

GENUINE_SAMPLES = [
    sample for sample in DATASET["samples"]
    if sample["expected_scam"] is False
]


@pytest.mark.parametrize(
    "sample",
    GENUINE_SAMPLES,
    ids=lambda sample: sample["sample_id"],
)
def test_multilingual_genuine_conversations_do_not_trigger_scam(sample):
    result = analyze_transcript(sample["transcript"])

    assert result.scam_detected is False
    assert result.stages_detected == []
    assert result.tactics_detected == []
    assert result.exact_phrases == []


def test_genuine_regression_dataset_covers_all_six_language_groups():
    languages = {sample["language"] for sample in GENUINE_SAMPLES}

    assert len(GENUINE_SAMPLES) == 60
    assert languages == {
        "English",
        "Hindi",
        "Telugu",
        "Tamil",
        "Malayalam",
        "Indian code-mixed speech",
    }


def test_gnani_hindi_bank_otp_scam_is_detected():
    transcript = (
        "नमस्ते, मैं बैंक के सुरक्षा विभाग से बोल रहा हूँ। "
        "आपका खाता आज बंद हो जाएगा। कृपया अपना OTP बताइये।"
    )

    result = analyze_transcript(transcript)

    assert result.scam_detected is True
    assert result.risk_level.value in {"HIGH", "CRITICAL"}
    assert "authority_claim" in result.stages_detected
    assert "credential_harvesting" in result.tactics_detected
    assert "urgency" in result.tactics_detected
    assert any("OTP बताइये" in phrase for phrase in result.exact_phrases)


def test_hindi_otp_safety_warning_is_not_a_scam():
    result = analyze_transcript("सुरक्षा के लिए अपना OTP किसी को मत बताइए।")

    assert result.scam_detected is False
    assert "credential_harvesting" not in result.tactics_detected
def test_gnani_telugu_bank_otp_scam_detects_authority_and_urgency():
    transcript = (
        "\u0c28\u0c2e\u0c38\u0c4d\u0c15\u0c3e\u0c30\u0c02, "
        "\u0c28\u0c47\u0c28\u0c41 \u0c2c\u0c4d\u0c2f\u0c3e\u0c02\u0c15\u0c41 "
        "\u0c2d\u0c26\u0c4d\u0c30\u0c24\u0c3e \u0c35\u0c3f\u0c2d\u0c3e\u0c17\u0c02 "
        "\u0c28\u0c41\u0c02\u0c21\u0c3f \u0c2e\u0c3e\u0c1f\u0c4d\u0c32\u0c3e\u0c21\u0c41\u0c24\u0c41\u0c28\u0c4d\u0c28\u0c3e\u0c28\u0c41, "
        "\u0c2e\u0c40 \u0c16\u0c3e\u0c24\u0c3e \u0c08\u0c30\u0c4b\u0c1c\u0c41 "
        "\u0c28\u0c3f\u0c32\u0c3f\u0c2a\u0c3f\u0c35\u0c47\u0c2f\u0c2c\u0c21\u0c41\u0c24\u0c41\u0c02\u0c26\u0c3f. "
        "\u0c26\u0c2f\u0c1a\u0c47\u0c38\u0c3f \u0c2e\u0c40 OTP "
        "\u0c1a\u0c46\u0c2a\u0c4d\u0c2a\u0c02\u0c21\u0c3f."
    )
    result = analyze_transcript(transcript)
    assert result.scam_detected is True
    assert "authority_claim" in result.stages_detected
    assert "urgency" in result.tactics_detected
    assert "credential_harvesting" in result.tactics_detected


def test_telugu_account_suspension_notice_alone_is_not_a_scam():
    transcript = (
        "\u0c2e\u0c40 \u0c16\u0c3e\u0c24\u0c3e \u0c08\u0c30\u0c4b\u0c1c\u0c41 "
        "\u0c28\u0c3f\u0c32\u0c3f\u0c2a\u0c3f\u0c35\u0c47\u0c2f\u0c2c\u0c21\u0c41\u0c24\u0c41\u0c02\u0c26\u0c3f."
    )
    result = analyze_transcript(transcript)
    assert result.scam_detected is False
    assert "credential_harvesting" not in result.tactics_detected
