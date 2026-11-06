import pytest

from services.risk_engine import analyze_transcript


@pytest.mark.parametrize(
    "name,transcript,expected",
    [
        (
            "Legitimate demo account",
            "Let our support agent view your screen while you open "
            "your banking app using a demo account.",
            False,
        ),
        (
            "Demo pretext followed by real account",
            "Let our officer view your screen while you open "
            "your banking app using a demo account, then switch "
            "to your real bank account.",
            True,
        ),
        (
            "Real account before demo wording",
            "Let our officer view your screen while you open "
            "your real bank account, then use a demo account.",
            True,
        ),
        (
            "Separate suspicious instruction",
            "We will use a demo account for training. "
            "Let our officer view your screen while you open "
            "your banking app.",
            True,
        ),
        (
            "Safety warning",
            "Never let our officer view your screen while "
            "you open your banking app.",
            False,
        ),
    ],
)
def test_banking_screen_sharing_adversarial(name, transcript, expected):
    result = analyze_transcript(transcript)
    actual = "remote_access_control" in result.tactics_detected
    assert actual == expected, name
