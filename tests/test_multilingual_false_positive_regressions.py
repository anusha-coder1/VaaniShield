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
