from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


def test_hybrid_api_falls_back_to_rules_when_gemini_fails():
    client = TestClient(app)

    transcript = (
        "Hello, I am from your bank. "
        "Share your OTP immediately to prevent account suspension."
    )

    with patch(
        "services.gemini_analyzer.analyze_with_gemini",
        side_effect=RuntimeError("Simulated Gemini outage"),
    ) as mock_gemini:
        response = client.post(
            "/api/analyze-hybrid",
            json={"transcript": transcript},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["ai_status"] == "fallback"
    assert data["ai_analysis"] is None
    assert data["verdict_agreement"] is None
    assert data["risk_agreement"] is None

    assert data["rule_analysis"]["scam_detected"] is True
    assert data["rule_analysis"]["risk_level"] in ("HIGH", "CRITICAL")

    mock_gemini.assert_called_once()
