import pytest

from services.risk_engine import analyze_transcript


@pytest.mark.parametrize(
    "name,transcript,expected_indicator",
    [
        (
            "C04 scam",
            "Install our support application and let our officer "
            "view your screen while you open your banking app.",
            True,
        ),
        (
            "Educational example",
            "A scammer might say: let our officer view your screen "
            "while you open your banking app.",
            False,
        ),
        (
            "Safety warning",
            "Never let our officer view your screen while you "
            "open your banking app.",
            False,
        ),
        (
            "Demo account",
            "During our scheduled demonstration, let our support "
            "agent view your screen while you open your banking "
            "app using a demo account.",
            False,
        ),
        (
            "Demonstration pretext",
            "During our scheduled demonstration, let our officer "
            "view your screen while you open your banking app "
            "to verify your identity.",
            True,
        ),
        (
            "Ordinary technical support",
            "Let our support agent view your screen to diagnose "
            "the display problem.",
            False,
        ),
        (
            "Scam after educational sentence",
            "Scammers might ask for screen access. "
            "Let our officer view your screen while you open "
            "your banking app.",
            True,
        ),
    ],
)
def test_banking_screen_sharing_indicator(
    name, transcript, expected_indicator
):
    result = analyze_transcript(transcript)
    actual = "remote_access_control" in result.tactics_detected
    assert actual == expected_indicator, name

    if expected_indicator:
        assert result.exact_phrases, name
    else:
        assert not result.scam_detected, name


def test_screen_sharing_alone_does_not_prove_scam():
    transcript = (
        "Let our officer view your screen while you "
        "open your banking app."
    )
    result = analyze_transcript(transcript)

    assert "remote_access_control" in result.tactics_detected
    assert result.scam_detected is False
