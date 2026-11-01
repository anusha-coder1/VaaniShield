import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from models.schemas import AnalysisResult, RiskLevel
from services import evaluation


def make_sample(
    sample_id,
    language,
    expected_scam,
    expected_stages=None,
    expected_tactics=None,
    transcript="Synthetic test transcript.",
):
    return {
        "sample_id": sample_id,
        "language": language,
        "conversation_type": "digital-arrest scam" if expected_scam else "genuine banking conversation",
        "transcript": transcript,
        "expected_scam": expected_scam,
        "expected_stages": expected_stages or [],
        "expected_tactics": expected_tactics or [],
        "native_speaker_review_required": False,
    }


def make_result(scam_detected, stages=None, tactics=None):
    return AnalysisResult(
        scam_detected=scam_detected,
        risk_level=RiskLevel.HIGH if scam_detected else RiskLevel.LOW,
        stages_detected=stages or [],
        tactics_detected=tactics or [],
        exact_phrases=[],
        confidence=0.5,
        uncertainty_note="Synthetic test result.",
    )


def test_loads_dataset_and_validates_all_samples():
    samples = evaluation.load_evaluation_dataset()

    assert len(samples) == 36
    assert len({sample["sample_id"] for sample in samples}) == 36
    assert {sample["language"] for sample in samples} == evaluation.SUPPORTED_LANGUAGES


def test_invalid_dataset_fields_are_rejected(tmp_path):
    missing_field = make_sample("INVALID-001", "English", False)
    del missing_field["expected_tactics"]
    dataset_path = tmp_path / "invalid.json"
    dataset_path.write_text(json.dumps({"samples": [missing_field]}), encoding="utf-8")

    with pytest.raises(evaluation.EvaluationDatasetError, match="missing required fields"):
        evaluation.load_evaluation_dataset(dataset_path)


def test_unknown_stage_identifier_is_rejected():
    sample = make_sample("INVALID-002", "English", True, expected_stages=["not_a_stage"])

    with pytest.raises(evaluation.EvaluationDatasetError, match="unknown expected_stages"):
        evaluation.evaluate_samples([sample])


def test_binary_metrics_and_confusion_matrix(monkeypatch):
    samples = [
        make_sample(
            "M-1", "English", True,
            expected_stages=["authority_claim"],
            transcript="predicted scam",
        ),
        make_sample(
            "M-2", "English", True,
            expected_stages=["accusation"],
            transcript="predicted genuine",
        ),
        make_sample("M-3", "Hindi", False, transcript="predicted scam"),
        make_sample("M-4", "Hindi", False, transcript="predicted genuine"),
    ]
    predictions = {"predicted scam": True, "predicted genuine": False}
    monkeypatch.setattr(
        evaluation,
        "analyze",
        lambda text: make_result(predictions[text]),
    )

    report = evaluation.evaluate_samples(samples)

    assert report["confusion_matrix"] == {
        "true_positive": 1,
        "true_negative": 1,
        "false_positive": 1,
        "false_negative": 1,
    }
    assert report["overall_metrics"] == {
        "accuracy": 0.5,
        "precision": 0.5,
        "recall": 0.5,
        "f1_score": 0.5,
        "false_positive_rate": 0.5,
        "true_positive_rate": 0.5,
    }
    assert report["correct_scam_detections"] == 1
    assert report["missed_scams"] == 1
    assert report["false_alarms"] == 1


def test_zero_division_and_empty_dataset_are_safe():
    report = evaluation.evaluate_samples([])

    assert report["total_samples"] == 0
    assert report["confusion_matrix"] == {
        "true_positive": 0,
        "true_negative": 0,
        "false_positive": 0,
        "false_negative": 0,
    }
    assert set(report["overall_metrics"].values()) == {0.0}
    assert report["language_performance"] == {}
    assert all(
        set(item["metrics"].values()) == {0.0}
        for item in report["stage_wise_performance"].values()
    )


def test_stage_wise_and_tactic_wise_metrics(monkeypatch):
    samples = [
        make_sample(
            "I-1",
            "English",
            True,
            expected_stages=["authority_claim"],
            expected_tactics=["authority_based_coercion"],
            transcript="stage-and-tactic",
        ),
        make_sample("I-2", "Hindi", False, transcript="no-indicators"),
    ]
    monkeypatch.setattr(
        evaluation,
        "analyze",
        lambda text: make_result(
            text == "stage-and-tactic",
            stages=["authority_claim"] if text == "stage-and-tactic" else [],
            tactics=["authority_based_coercion"] if text == "stage-and-tactic" else [],
        ),
    )

    report = evaluation.evaluate_samples(samples)
    stage = report["stage_wise_performance"]["authority_claim"]
    tactic = report["tactic_wise_performance"]["authority_based_coercion"]

    assert stage["confusion_matrix"]["true_positive"] == 1
    assert stage["metrics"]["recall"] == 1.0
    assert tactic["confusion_matrix"]["true_positive"] == 1
    assert tactic["metrics"]["precision"] == 1.0
    assert report["stage_wise_performance"]["accusation"]["support"] == 0


def test_language_grouping_and_review_counts(monkeypatch):
    samples = [
        make_sample(
            "L-1", "English", True,
            expected_tactics=["authority_based_coercion"],
            transcript="positive",
        ),
        make_sample("L-2", "Hindi", False, transcript="negative"),
    ]
    samples[1]["native_speaker_review_required"] = True
    monkeypatch.setattr(
        evaluation,
        "analyze",
        lambda text: make_result(text == "positive"),
    )

    report = evaluation.evaluate_samples(samples)

    assert report["language_performance"]["English"]["scam_samples"] == 1
    assert report["language_performance"]["Hindi"]["genuine_samples"] == 1
    assert report["language_performance"]["Hindi"]["native_speaker_review_required_samples"] == 1


def test_evaluator_integrates_with_existing_analyzer():
    sample = make_sample(
        "REAL-ENGINE-1",
        "English",
        False,
        transcript="I checked a routine UPI transaction in my bank app.",
    )

    report = evaluation.evaluate_samples([sample])

    assert report["total_samples"] == 1
    assert report["confusion_matrix"]["true_negative"] == 1


def test_evaluation_page_is_navigable_and_disclaims_synthetic_scope():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()
    next(button for button in app.button if button.label == "Evaluation").click().run()

    assert not app.exception
    assert any(item.value == "Detection evaluation" for item in app.title)
    assert any("not real-world validated performance" in item.value for item in app.warning)
    assert any(item.label == "Accuracy" for item in app.metric)

