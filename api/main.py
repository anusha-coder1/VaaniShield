from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from io import BytesIO
from pathlib import Path
from services.speech_to_text import SUPPORTED_AUDIO_FORMATS, transcribe_audio

from models.schemas import AnalysisResult
from services.analyzer import analyze


app = FastAPI(
    title="VaaniShield API",
    version="0.1.0",
    description="Explainable multilingual scam detection API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class AnalyzeRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=20000)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "VaaniShield API"}


@app.post("/api/analyze", response_model=AnalysisResult)
def analyze_conversation(request: AnalyzeRequest):
    return analyze(request.transcript)


@app.post("/api/analyze-hybrid")
def analyze_hybrid_conversation(request: AnalyzeRequest):
    """Return independent rule and AI assessments with a safe rules fallback."""
    from services.gemini_analyzer import analyze_with_gemini
    from services.redaction import redact_sensitive_data

    rule_result = analyze(request.transcript)

    try:
        redacted = redact_sensitive_data(request.transcript)
        ai_result = analyze_with_gemini(redacted)
    except RuntimeError:
        return {
            "rule_analysis": rule_result.model_dump(mode="json"),
            "ai_analysis": None,
            "ai_status": "fallback",
            "verdict_agreement": None,
            "risk_agreement": None,
        }

    return {
        "rule_analysis": rule_result.model_dump(mode="json"),
        "ai_analysis": ai_result.model_dump(mode="json"),
        "ai_status": "available",
        "verdict_agreement": rule_result.scam_detected == ai_result.scam_detected,
        "risk_agreement": rule_result.risk_level == ai_result.risk_level,
    }


MAX_AUDIO_BYTES = 15 * 1024 * 1024


@app.post("/api/transcribe")
async def transcribe_conversation(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.removeprefix(".").lower()

    if extension not in SUPPORTED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format. Use WAV, MP3, M4A, AAC, FLAC, or OGG.",
        )

    content = await file.read(MAX_AUDIO_BYTES + 1)
    await file.close()

    if not content:
        raise HTTPException(status_code=400, detail="Audio file is empty.")

    if len(content) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio file exceeds the 15 MB limit.")

    audio = BytesIO(content)
    audio.name = filename

    try:
        return transcribe_audio(audio)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from None
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from None
