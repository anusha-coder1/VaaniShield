
import os
from math import isfinite
from pathlib import Path

from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from mutagen import File as MutagenFile


load_dotenv()

SUPPORTED_AUDIO_FORMATS = ("wav", "mp3", "m4a", "aac", "flac", "ogg")
MAX_AUDIO_DURATION_SECONDS = 30.0
TRANSCRIPTION_KEYWORDS = (
    "Aadhaar",
    "Aadhar",
    "PAN",
    "UIDAI",
    "bank account",
    "UPI",
    "NEFT",
    "IMPS",
    "RTGS",
    "transaction",
    "verification",
    "transfer",
    "OTP",
    "one-time password",
    "PIN",
    "CVV",
    "password",
    "credentials",
    "cybercrime department",
    "cybercrime",
    "police",
    "CBI",
    "investigation",
    "digital arrest",
    "arrest warrant",
    "Reserve Bank of India",
    "RBI",
    "Income Tax Department",
    "Ministry of Home Affairs",
    "KYC",
    "debit card",
    "credit card",
    "net banking",
    "UPI ID",
    "account frozen",
    "money laundering",
    "legal notice",
)
TRANSCRIPTION_TOPIC = (
    "Suspicious calls and customer-support conversations involving Indian identity and "
    "government services, banking, financial transactions, verification, financial fraud, "
    "cybercrime investigations, impersonation, and digital-arrest scam claims."
)
# Prisma allows 2-4 candidate hints; indic-auto remains enabled and unrestricted.
TRANSCRIPTION_LANGUAGE_CANDIDATES = ("en-IN", "hi-IN", "te-IN", "ta-IN")


def _validate_audio_duration(audio_file) -> float:
    """Read duration metadata without writing or estimating from file size."""
    try:
        audio_file.seek(0)
        audio = MutagenFile(audio_file)
    except Exception:
        audio = None
    finally:
        try:
            audio_file.seek(0)
        except Exception:
            pass

    if audio is None or getattr(audio, "info", None) is None:
        supported_formats = ", ".join(
            format_name.upper() for format_name in SUPPORTED_AUDIO_FORMATS
        )
        raise ValueError(
            "Could not determine audio duration. Upload a readable "
            f"{supported_formats} audio file."
        )

    try:
        duration = float(audio.info.length)
    except (AttributeError, TypeError, ValueError, OverflowError):
        raise ValueError("Could not determine audio duration from this file.") from None

    if not isfinite(duration) or duration < 0:
        raise ValueError("Could not determine a valid audio duration from this file.")

    if duration > MAX_AUDIO_DURATION_SECONDS:
        raise ValueError(
            f"Audio is {duration:.1f} seconds long. Prisma v3 accepts "
            "a maximum of 30 seconds per transcription request."
        )

    return duration


def transcribe_audio(audio_file):
    """Convert uploaded audio into text using Gnani Prisma v3."""

    audio_name = str(getattr(audio_file, "name", "") or "")
    extension = Path(audio_name).suffix.removeprefix(".").lower()
    if extension not in SUPPORTED_AUDIO_FORMATS:
        supported_formats = ", ".join(format_name.upper() for format_name in SUPPORTED_AUDIO_FORMATS)
        raise ValueError(f"Unsupported audio format. Upload one of: {supported_formats}.")

    _validate_audio_duration(audio_file)

    api_key = os.getenv("GNANI_API_KEY")

    if not api_key:
        raise RuntimeError("Gnani API key is not configured.")

    client = GnaniSTTClient(api_key=api_key)

    if hasattr(audio_file, "seek"):
        audio_file.seek(0)

    try:
        response = client.transcribe(
            audio=audio_file,
            language_code="indic-auto",
            model="prisma-v3.0",
            format="codemix",
            keywords=list(TRANSCRIPTION_KEYWORDS),
            topic=TRANSCRIPTION_TOPIC,
            language_candidates=list(TRANSCRIPTION_LANGUAGE_CANDIDATES),
        )
    except Exception as error:
        exception_names = {error_type.__name__.lower() for error_type in type(error).__mro__}
        network_errors = {
            "connectionerror",
            "connecterror",
            "connecttimeout",
            "networkerror",
            "readtimeout",
            "timeout",
            "timeouterror",
        }
        if exception_names.intersection(network_errors):
            raise RuntimeError(
                "A network error interrupted transcription. Check your connection and try again."
            ) from None

        status_code = getattr(error, "status_code", None)
        if isinstance(status_code, int):
            raise RuntimeError(
                f"Gnani transcription failed with HTTP status {status_code}. Check the service and API key."
            ) from None

        raise RuntimeError(
            "Gnani transcription failed. Check the service connection and try again."
        ) from None

    if not isinstance(response, dict):
        raise RuntimeError("Gnani returned an unexpected transcription response.")

    if not response.get("success"):
        raise RuntimeError("Gnani transcription was unsuccessful.")

    transcript = response.get("transcript", "").strip()

    if not transcript:
        raise RuntimeError("No speech could be transcribed from this audio.")

    return {
        "transcript": transcript,
        "detected_language": response.get("detected_language_code"),
        "request_id": response.get("request_id"),
    }
