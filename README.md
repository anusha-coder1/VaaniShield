# VaaniShield

Explainable multilingual scam detection using Gnani Prisma speech-to-text, a rule-based detection engine, and optional Gemini AI comparison.

## Overview

VaaniShield is a working prototype that analyzes typed conversations or short audio recordings for potential scam indicators. It provides risk assessments, supporting evidence, and optional independent AI analysis.

## Technology

- Frontend: Next.js 16, React 19, TypeScript
- Backend: Python, FastAPI, Pydantic
- Speech-to-text: Gnani Prisma v3 via gnani-vachana
- Detection: Explainable multilingual rules
- Optional AI: Gemini REST API
- Testing: pytest

## Local Setup

Requirements: Python, Node.js, npm, and a Gnani API key for audio transcription.

### Backend

From the project root, create a virtual environment and install dependencies:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

Copy .env.example to .env and configure GNANI_API_KEY. GEMINI_API_KEY is optional. Never commit real API keys.

Start FastAPI:

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8765

Health check: http://127.0.0.1:8765/api/health

### Frontend

In a separate terminal:

    cd frontend
    npm install

Create frontend/.env.local with:

    NEXT_PUBLIC_API_URL=http://127.0.0.1:8765

Start Next.js:

    npm run dev

Open http://localhost:3000.

## Gnani Prisma Integration

VaaniShield uses the Gnani Vachana SDK to transcribe uploaded audio with these settings:

- Model: prisma-v3.0
- Language detection: indic-auto
- Transcription format: codemix
- Language hints: en-IN, hi-IN, te-IN, ta-IN
- Supported formats: WAV, MP3, M4A, AAC, FLAC, OGG
- Maximum audio duration: 30 seconds
- Maximum upload size: 15 MB

Synthetic English, Hindi, and Telugu recordings have been successfully tested through the live Gnani transcription pipeline. These tests demonstrate integration functionality, not real-world recognition accuracy.

## Demo Workflow

1. Open http://localhost:3000.
2. Enter a conversation transcript or upload a supported audio recording.
3. For audio, wait for Gnani Prisma to return the transcript.
4. Review or edit the transcript.
5. Run the rule-based scam analysis.
6. Inspect the risk assessment, detected indicators, and supporting evidence.
7. Optionally enable Gemini comparison to view an independent AI assessment.

Gemini comparison is optional and sends a redacted transcript to an external API. If Gemini fails, the application retains the rule-based result.

## API Endpoints

- GET /api/health - backend health check
- POST /api/analyze - rule-based transcript analysis
- POST /api/analyze-hybrid - rule-based and Gemini comparison
- POST /api/transcribe - Gnani Prisma audio transcription

## Evaluation Evidence

### Multilingual development evaluation

- Dataset: 120 synthetic conversations across English, Hindi, Telugu, Tamil, Malayalam, and Indian code-mixed speech.
- Composition: 60 scam and 60 genuine examples.
- Result: 120/120 correct overall scam classifications on this development dataset.
- Limitations: Rules were refined using this dataset; it is not an untouched held-out benchmark. Annotations were AI-assisted, and 100 samples require native-speaker review.

Full report: docs/phase4_evaluation_summary.md

### Hybrid challenge

- Dataset: 12 frozen, synthetic, AI-authored English conversations.
- Rule engine: 9/12 correct classifications.
- Gemini: 12/12 correct after retries.
- Gemini completed 11/12 cases on the first attempt.
- Gemini recovered three scam examples missed by the rule engine, but tactic extraction was incomplete on some cases.

Full report: docs/hybrid_challenge_v1_report.md

These evaluations do not establish real-world detection accuracy.

### Automated tests

The latest full test run passed 240 pytest tests, including multilingual regression tests.

    python -m pytest -q

## Known Limitations

- Evaluation data is synthetic and not representative of real-world scam calls.
- Independent native-speaker validation is still needed.
- Speech recognition may be affected by accents, background noise, and code-mixing.
- Rule-based detection can miss unfamiliar scam language.
- Gemini availability, latency, and extracted indicators may vary.
- Risk assessments are not calibrated probabilities or definitive proof of fraud.
- Gnani transcription requires network access and a valid API key.

## Responsible Use

VaaniShield is a research and scam-awareness prototype. Verify suspicious requests through trusted channels and do not rely on its output alone for consequential decisions.
