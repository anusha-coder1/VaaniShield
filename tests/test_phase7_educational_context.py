import pytest

from services.risk_engine import _is_educational_match


@pytest.mark.parametrize(
    "transcript,target,expected",
    [
        (
            "A scammer might say: let our officer view your screen.",
            "let our officer",
            True,
        ),
        (
            "Scammers may ask you to share your screen.",
            "share your screen",
            True,
        ),
        (
            "A fraudster could claim to be a bank employee.",
            "bank employee",
            True,
        ),
        (
            "Let our officer view your screen while you open your banking app.",
            "Let our officer",
            False,
        ),
        (
            "Scammers may ask for screen access. "
            "Let our officer view your screen while you open your banking app.",
            "Let our officer",
            False,
        ),
    ],
)
def test_phase7_educational_context(transcript, target, expected):
    match_start = transcript.index(target)
    assert _is_educational_match(transcript, match_start) is expected
