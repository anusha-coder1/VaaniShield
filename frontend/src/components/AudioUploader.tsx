"use client";

import { useRef, useState } from "react";
import { AlertCircle, CheckCircle2, LoaderCircle, Mic, Upload } from "lucide-react";

const MAX_BYTES = 15 * 1024 * 1024;
const SUPPORTED = [".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"];

type Transcription = {
  transcript: string;
  detected_language: string | null;
  request_id: string | null;
};

export default function AudioUploader({ onTranscriptReady }: { onTranscriptReady: (text: string) => void }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<Transcription | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function chooseFile(selected: File | undefined) {
    setResult(null);
    setError("");
    setFile(null);

    if (!selected) return;

    const extension = "." + (selected.name.split(".").pop() || "").toLowerCase();

    if (!SUPPORTED.includes(extension)) {
      setError("Unsupported format. Choose WAV, MP3, M4A, AAC, FLAC, or OGG.");
      return;
    }

    if (selected.size > MAX_BYTES) {
      setError("File exceeds the 15 MB upload limit.");
      return;
    }

    if (selected.size === 0) {
      setError("The selected audio file is empty.");
      return;
    }

    setFile(selected);
  }

  async function transcribe() {
    if (!file || loading) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!baseUrl) throw new Error("Analysis API URL is not configured.");

      const form = new FormData();
      form.append("file", file);

      const response = await fetch(`${baseUrl}/api/transcribe`, {
        method: "POST",
        body: form,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : `Transcription failed (HTTP ${response.status}).`
        );
      }

      if (typeof data.transcript !== "string" || !data.transcript.trim()) {
        throw new Error("The transcription service returned no transcript.");
      }

      setResult(data as Transcription);
      onTranscriptReady(data.transcript);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to transcribe audio."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0e1d2e] p-6 sm:p-8">
      <div className="mb-7 flex items-center gap-3">
        <div className="rounded-xl bg-cyan-300/10 p-3 text-cyan-300">
          <Mic size={23} />
        </div>
        <div>
          <h2 className="text-lg font-semibold">Voice intelligence</h2>
          <p className="text-sm text-slate-400">Gnani Prisma transcription</p>
        </div>
      </div>

      <div className="rounded-xl border border-dashed border-white/15 bg-[#071421] p-6 text-center">
        <Upload size={28} className="mx-auto mb-4 text-cyan-300" />
        <h3 className="font-semibold">Upload a conversation recording</h3>
        <p className="mt-2 text-xs leading-6 text-slate-400">
          WAV, MP3, M4A, AAC, FLAC, OGG. Maximum 30 seconds and 15 MB.
        </p>

        <input
          ref={inputRef}
          type="file"
          accept={SUPPORTED.join(",")}
          className="hidden"
          onChange={(event) => chooseFile(event.target.files?.[0])}
        />

        <button
          type="button"
          onClick={() => {
            if (inputRef.current) inputRef.current.value = "";
            inputRef.current?.click();
          }}
          className="mt-5 rounded-xl border border-cyan-300/30 px-5 py-3 text-sm font-semibold text-cyan-200 hover:bg-cyan-300/10"
        >
          Choose audio file
        </button>

        {file && (
          <div className="mt-4 break-all text-sm text-slate-300">
            Selected: {file.name}
          </div>
        )}

        <button
          type="button"
          disabled={!file || loading}
          onClick={transcribe}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-300 px-4 py-3 text-sm font-semibold text-[#071421] hover:bg-cyan-200 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {loading ? (
            <>
              <LoaderCircle size={17} className="animate-spin" />
              Transcribing...
            </>
          ) : (
            "Transcribe audio"
          )}
        </button>
      </div>

      {error && (
        <div role="alert" className="mt-4 flex items-start gap-2 rounded-xl border border-red-400/20 bg-red-400/10 p-4 text-sm text-red-200">
          <AlertCircle size={18} className="shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="mt-5 rounded-xl border border-emerald-300/20 bg-emerald-300/5 p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-emerald-300">
            <CheckCircle2 size={18} />
            Transcription complete
          </div>

          <p className="mt-3 text-xs text-slate-400">
            Detected language: {result.detected_language || "Not provided"}
          </p>

          <h3 className="mt-5 text-sm font-semibold text-slate-200">
            Transcript
          </h3>

          <p className="mt-2 whitespace-pre-wrap break-words text-sm leading-7 text-slate-300">
            {result.transcript}
          </p>

          <button
            type="button"
            onClick={() => {
              navigator.clipboard.writeText(result.transcript).catch(() => {
                setError("Unable to copy. Select the transcript manually.");
              });
            }}
            className="mt-4 rounded-lg border border-cyan-300/30 px-4 py-2 text-xs font-semibold text-cyan-200 hover:bg-cyan-300/10"
          >
            Copy transcript for analysis
          </button>
        </div>
      )}
    </section>
  );
}
