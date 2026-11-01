import json
from pathlib import Path
from typing import Any, get_args

from models.schemas import Stage, Tactic
from services.analyzer import analyze


DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "evaluation_dataset.json"
SUPPORTED_LANGUAGES = {
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "Malayalam",
    "Indian code-mixed speech",
}
SUPPORTED_CONVERSATION_TYPES = {
    "digital-arrest scam",
    "financial fraud scam",
    "genuine banking conversation",
    "legitimate police verification discussion",
    "protective OTP/security warning",
    "educational discussion about scams",
}
REQUIRED_SAMPLE_FIELDS = {
    "sample_id",
    "language",
    "conversation_type",
    "transcript",
    "expected_scam",
    "expected_stages",
    "expected_tactics",
    "native_speaker_review_required",
}


class EvaluationDatasetError(ValueError):
    """Raised when evaluation dataset content is missing or invalid."""


def _validate_samples(samples: Any) -> list[dict[str, Any]]:
    if not isinstance(samples, list):
        raise EvaluationDatasetError("Dataset 'samples' must be a list.")

    valid_stages = set(get_args(Stage))
    valid_tactics = set(get_args(Tactic))
    seen_ids = set()

    for index, sample in enumerate(samples):
        if not isinstance(sample, dict):
            raise EvaluationDatasetError(f"Sample at index {index} must be an object.")

        missing_fields = REQUIRED_SAMPLE_FIELDS - sample.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise EvaluationDatasetError(
                f"Sample at index {index} is missing required fields: {missing}."
            )

        sample_id = sample["sample_id"]
        if not isinstance(sample_id, str) or not sample_id.strip():
            raise EvaluationDatasetError(f"Sample at index {index} has an invalid sample_id.")
        if sample_id in seen_ids:
            raise EvaluationDatasetError(f"Duplicate sample_id: {sample_id}.")
        seen_ids.add(sample_id)

        if not isinstance(sample["language"], str) or sample["language"] not in SUPPORTED_LANGUAGES:
            raise EvaluationDatasetError(f"Sample {sample_id} has an unsupported language.")
        if (
            not isinstance(sample["conversation_type"], str)
            or sample["conversation_type"] not in SUPPORTED_CONVERSATION_TYPES
        ):
            raise EvaluationDatasetError(f"Sample {sample_id} has an unsupported conversation_type.")
        if not isinstance(sample["transcript"], str) or not sample["transcript"].strip():
            raise EvaluationDatasetError(f"Sample {sample_id} has an empty or invalid transcript.")
        if type(sample["expected_scam"]) is not bool:
            raise EvaluationDatasetError(f"Sample {sample_id} expected_scam must be a boolean.")
        if type(sample["native_speaker_review_required"]) is not bool:
            raise EvaluationDatasetError(
                f"Sample {sample_id} native_speaker_review_required must be a boolean."
            )

        for field, valid_identifiers in (
            ("expected_stages", valid_stages),
            ("expected_tactics", valid_tactics),
        ):
            values = sample[field]
            if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
                raise EvaluationDatasetError(f"Sample {sample_id} {field} must be a list of strings.")
            unknown = set(values) - valid_identifiers
            if unknown:
                raise EvaluationDatasetError(
                    f"Sample {sample_id} has unknown {field} identifiers: {', '.join(sorted(unknown))}."
                )
            if len(values) != len(set(values)):
                raise EvaluationDatasetError(f"Sample {sample_id} has duplicate values in {field}.")

        has_expected_indicators = bool(sample["expected_stages"] or sample["expected_tactics"])
        if sample["expected_scam"] and not has_expected_indicators:
            raise EvaluationDatasetError(
                f"Scam sample {sample_id} must have at least one expected stage or tactic."
            )
        if not sample["expected_scam"] and has_expected_indicators:
            raise EvaluationDatasetError(
                f"Non-scam sample {sample_id} cannot have expected scam indicators."
            )

    return samples


def load_evaluation_dataset(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load and validate every sample; invalid samples are never silently skipped."""
    dataset_path = Path(path) if path is not None else DATASET_PATH
    try:
        dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise EvaluationDatasetError(f"Evaluation dataset not found: {dataset_path}.") from None
    except json.JSONDecodeError as error:
        raise EvaluationDatasetError(
            f"Evaluation dataset contains invalid JSON at line {error.lineno}."
        ) from None
    except OSError:
        raise EvaluationDatasetError("Evaluation dataset could not be read.") from None

    if not isinstance(dataset, dict):
        raise EvaluationDatasetError("Evaluation dataset root must be an object.")
    if "samples" not in dataset:
        raise EvaluationDatasetError("Evaluation dataset is missing the 'samples' list.")
    return _validate_samples(dataset["samples"])


def _confusion_matrix(expected: list[bool], predicted: list[bool]) -> dict[str, int]:
    true_positive = sum(actual and guess for actual, guess in zip(expected, predicted))
    true_negative = sum(not actual and not guess for actual, guess in zip(expected, predicted))
    false_positive = sum(not actual and guess for actual, guess in zip(expected, predicted))
    false_negative = sum(actual and not guess for actual, guess in zip(expected, predicted))
    return {
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
    }


def _safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _metrics(confusion: dict[str, int]) -> dict[str, float]:
    true_positive = confusion["true_positive"]
    true_negative = confusion["true_negative"]
    false_positive = confusion["false_positive"]
    false_negative = confusion["false_negative"]
    total = true_positive + true_negative + false_positive + false_negative
    precision = _safe_divide(true_positive, true_positive + false_positive)
    recall = _safe_divide(true_positive, true_positive + false_negative)
    return {
        "accuracy": _safe_divide(true_positive + true_negative, total),
        "precision": precision,
        "recall": recall,
        "f1_score": _safe_divide(2 * precision * recall, precision + recall),
        "false_positive_rate": _safe_divide(false_positive, false_positive + true_negative),
        "true_positive_rate": recall,
    }


def _indicator_performance(
    samples: list[dict[str, Any]], predictions: list[Any], field: str, identifiers: tuple[str, ...]
) -> dict[str, dict[str, Any]]:
    performance = {}
    for identifier in identifiers:
        expected = [identifier in sample[field] for sample in samples]
        prediction_field = {
            "expected_stages": "stages_detected",
            "expected_tactics": "tactics_detected",
        }[field]
        predicted = [identifier in getattr(result, prediction_field) for result in predictions]
        confusion = _confusion_matrix(expected, predicted)
        performance[identifier] = {
            "support": sum(expected),
            "predicted_positive": sum(predicted),
            "confusion_matrix": confusion,
            "metrics": _metrics(confusion),
        }
    return performance


def evaluate_samples(samples: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate validated samples with the existing analyzer, without altering it."""
    validated_samples = _validate_samples(samples)
    predictions = [analyze(sample["transcript"]) for sample in validated_samples]
    expected_labels = [sample["expected_scam"] for sample in validated_samples]
    predicted_labels = [result.scam_detected for result in predictions]
    confusion = _confusion_matrix(expected_labels, predicted_labels)

    stage_ids = get_args(Stage)
    tactic_ids = get_args(Tactic)
    languages = sorted({sample["language"] for sample in validated_samples})
    language_performance = {}
    for language in languages:
        matching = [
            (sample, result)
            for sample, result in zip(validated_samples, predictions)
            if sample["language"] == language
        ]
        language_samples = [sample for sample, _ in matching]
        language_predictions = [result for _, result in matching]
        language_expected = [sample["expected_scam"] for sample in language_samples]
        language_predicted = [result.scam_detected for result in language_predictions]
        language_confusion = _confusion_matrix(language_expected, language_predicted)
        language_performance[language] = {
            "total_samples": len(language_samples),
            "scam_samples": sum(language_expected),
            "genuine_samples": len(language_samples) - sum(language_expected),
            "native_speaker_review_required_samples": sum(
                sample["native_speaker_review_required"] for sample in language_samples
            ),
            "confusion_matrix": language_confusion,
            "metrics": _metrics(language_confusion),
        }

    scam_samples = sum(expected_labels)
    return {
        "total_samples": len(validated_samples),
        "scam_samples": scam_samples,
        "genuine_samples": len(validated_samples) - scam_samples,
        "correct_scam_detections": confusion["true_positive"],
        "missed_scams": confusion["false_negative"],
        "false_alarms": confusion["false_positive"],
        "native_speaker_review_required_samples": sum(
            sample["native_speaker_review_required"] for sample in validated_samples
        ),
        "confusion_matrix": confusion,
        "overall_metrics": _metrics(confusion),
        "stage_wise_performance": _indicator_performance(
            validated_samples, predictions, "expected_stages", stage_ids
        ),
        "tactic_wise_performance": _indicator_performance(
            validated_samples, predictions, "expected_tactics", tactic_ids
        ),
        "language_performance": language_performance,
    }


def evaluate_dataset(path: str | Path | None = None) -> dict[str, Any]:
    """Load the configured evaluation set and return its complete summary."""
    return evaluate_samples(load_evaluation_dataset(path))
