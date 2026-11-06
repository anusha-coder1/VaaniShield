import json
from pathlib import Path

import pytest

from services.analyzer import analyze


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "phase7_challenge_v2_development.json"
)


def load_samples():
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    return dataset["samples"]


@pytest.mark.parametrize(
    "sample",
    load_samples(),
    ids=lambda sample: sample["sample_id"],
)
def test_phase7_challenge_classification(sample):
    result = analyze(sample["transcript"])

    assert result.scam_detected == sample["expected_scam"], (
        f"{sample['sample_id']}: "
        f"expected scam={sample['expected_scam']}, "
        f"got scam={result.scam_detected}; "
        f"stages={result.stages_detected}; "
        f"tactics={result.tactics_detected}"
    )


def test_phase7_challenge_dataset_size():
    samples = load_samples()

    assert len(samples) == 12
    assert sum(sample["expected_scam"] for sample in samples) == 6
    assert sum(not sample["expected_scam"] for sample in samples) == 6
