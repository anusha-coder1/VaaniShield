from io import BytesIO
from types import SimpleNamespace
import wave

import pytest

from services import speech_to_text


class NamedAudio(BytesIO):
	def __init__(self, name, content=None):
		super().__init__(content if content is not None else make_wav_bytes(1.0))
		self.name = name


def make_wav_bytes(duration_seconds):
	frame_rate = 8000
	frame_count = round(duration_seconds * frame_rate)
	buffer = BytesIO()
	with wave.open(buffer, "wb") as audio:
		audio.setnchannels(1)
		audio.setsampwidth(2)
		audio.setframerate(frame_rate)
		audio.writeframes(b"\x00\x00" * frame_count)
	return buffer.getvalue()


def test_transcribes_supported_audio_using_prisma_v3(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	observed = {}

	class FakeClient:
		def __init__(self, api_key):
			assert api_key == "test-only-key"

		def transcribe(
			self,
			audio,
			language_code,
			model,
			format,
			keywords,
			topic,
			language_candidates,
		):
			observed.update(
				{
					"audio": audio.read(),
					"language_code": language_code,
					"model": model,
					"format": format,
					"keywords": keywords,
					"topic": topic,
					"language_candidates": language_candidates,
				}
			)
			return {
				"success": True,
				"transcript": "synthetic transcript",
				"detected_language_code": "en-IN",
				"request_id": "synthetic-request-id",
			}

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)
	audio = NamedAudio("call.wav")
	audio.seek(0, 2)

	result = speech_to_text.transcribe_audio(audio)

	assert observed["audio"].startswith(b"RIFF")
	assert {key: observed[key] for key in ("language_code", "model", "format")} == {
		"language_code": "indic-auto",
		"model": "prisma-v3.0",
		"format": "codemix",
	}
	assert observed["keywords"] == list(speech_to_text.TRANSCRIPTION_KEYWORDS)
	assert len(observed["keywords"]) <= 200
	assert observed["topic"] == speech_to_text.TRANSCRIPTION_TOPIC
	assert len(observed["topic"]) <= 1600
	assert observed["language_candidates"] == list(
		speech_to_text.TRANSCRIPTION_LANGUAGE_CANDIDATES
	)
	assert speech_to_text.TRANSCRIPTION_LANGUAGE_CANDIDATES == (
		"en-IN",
		"hi-IN",
		"te-IN",
		"ta-IN",
	)
	assert 2 <= len(observed["language_candidates"]) <= 4
	assert result == {
		"transcript": "synthetic transcript",
		"detected_language": "en-IN",
		"request_id": "synthetic-request-id",
	}


@pytest.mark.parametrize("extension", speech_to_text.SUPPORTED_AUDIO_FORMATS)
def test_accepts_documented_audio_formats(extension, monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	monkeypatch.setattr(
		speech_to_text,
		"MutagenFile",
		lambda audio: SimpleNamespace(info=SimpleNamespace(length=5.0)),
	)

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			return {"success": True, "transcript": "synthetic transcript"}

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)

	result = speech_to_text.transcribe_audio(NamedAudio(f"call.{extension}"))

	assert result["transcript"] == "synthetic transcript"


def test_accepts_audio_under_30_seconds(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	client_calls = []

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			client_calls.append(True)
			return {"success": True, "transcript": "synthetic transcript"}

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)
	result = speech_to_text.transcribe_audio(NamedAudio("call.wav", make_wav_bytes(29.5)))

	assert result["transcript"] == "synthetic transcript"
	assert client_calls == [True]


def test_accepts_audio_exactly_30_seconds(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	client_calls = []

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			client_calls.append(True)
			return {"success": True, "transcript": "synthetic transcript"}

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)
	result = speech_to_text.transcribe_audio(NamedAudio("call.wav", make_wav_bytes(30.0)))

	assert result["transcript"] == "synthetic transcript"
	assert client_calls == [True]


def test_rejects_audio_over_30_seconds_before_calling_gnani(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	monkeypatch.setattr(
		speech_to_text,
		"GnaniSTTClient",
		lambda **kwargs: pytest.fail("Gnani client must not be constructed for overlength audio"),
	)

	with pytest.raises(ValueError, match="maximum of 30 seconds"):
		speech_to_text.transcribe_audio(NamedAudio("call.wav", make_wav_bytes(30.1)))


def test_rejects_unsupported_audio_format():
	with pytest.raises(ValueError, match="Unsupported audio format"):
		speech_to_text.transcribe_audio(NamedAudio("call.txt"))


def test_rejects_unreadable_audio_before_calling_gnani(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	monkeypatch.setattr(
		speech_to_text,
		"GnaniSTTClient",
		lambda **kwargs: pytest.fail("Gnani client must not be constructed for unreadable audio"),
	)

	with pytest.raises(ValueError, match="Could not determine audio duration"):
		speech_to_text.transcribe_audio(NamedAudio("call.wav", b"not a readable WAV file"))


def test_reports_missing_api_key(monkeypatch):
	monkeypatch.delenv("GNANI_API_KEY", raising=False)

	with pytest.raises(RuntimeError, match="API key is not configured"):
		speech_to_text.transcribe_audio(NamedAudio("call.wav"))


def test_reports_empty_transcription(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			return {"success": True, "transcript": "  "}

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)

	with pytest.raises(RuntimeError, match="No speech could be transcribed"):
		speech_to_text.transcribe_audio(NamedAudio("call.wav"))


def test_converts_network_failure_to_safe_error(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			raise ConnectionError("sensitive request details")

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)

	with pytest.raises(RuntimeError, match="network error") as error:
		speech_to_text.transcribe_audio(NamedAudio("call.wav"))

	assert "sensitive request details" not in str(error.value)


def test_converts_api_failure_without_exposing_response_body(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")

	class FakeAPIError(Exception):
		status_code = 503

		def __str__(self):
			return "sensitive response body"

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			raise FakeAPIError()

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)

	with pytest.raises(RuntimeError, match="HTTP status 503") as error:
		speech_to_text.transcribe_audio(NamedAudio("call.wav"))

	assert "sensitive response body" not in str(error.value)


def test_context_vocabulary_covers_required_domain_terms():
	keywords = set(speech_to_text.TRANSCRIPTION_KEYWORDS)

	assert {
		"Aadhaar",
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
		"PIN",
		"CVV",
		"password",
		"credentials",
		"cybercrime department",
		"police",
		"CBI",
		"investigation",
		"digital arrest",
		"arrest warrant",
		"Reserve Bank of India",
		"Income Tax Department",
		"Ministry of Home Affairs",
	}.issubset(keywords)
	assert len(keywords) <= 200
	assert len(speech_to_text.TRANSCRIPTION_TOPIC) <= 1600
	for topic in (
		"suspicious calls",
		"customer-support conversations",
		"financial fraud",
		"digital-arrest scam claims",
	):
		assert topic.casefold() in speech_to_text.TRANSCRIPTION_TOPIC.casefold()


def test_transcription_does_not_run_scam_analysis(monkeypatch):
	monkeypatch.setenv("GNANI_API_KEY", "test-only-key")
	analysis_calls = []
	monkeypatch.setattr(
		"services.analyzer.analyze",
		lambda transcript: analysis_calls.append(transcript),
	)

	class FakeClient:
		def __init__(self, api_key):
			pass

		def transcribe(self, **kwargs):
			return {
				"success": True,
				"transcript": "synthetic spoken content",
				"detected_language_code": "te-IN",
			}

	monkeypatch.setattr(speech_to_text, "GnaniSTTClient", FakeClient)
	result = speech_to_text.transcribe_audio(NamedAudio("call.wav"))

	assert result["transcript"] == "synthetic spoken content"
	assert result["detected_language"] == "te-IN"
	assert analysis_calls == []