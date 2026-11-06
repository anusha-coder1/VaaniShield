"use client";

import { useState } from "react";
import {
  AlertCircle, ArrowRight, CheckCircle2, LoaderCircle,
  ScanSearch, ShieldAlert
} from "lucide-react";

type IndicatorEvidence = {
  indicator: string;
  exact_phrases: string[];
  explanation: string;
  potential_risk: string;
};

type AnalysisResult = {
  scam_detected: boolean;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  stages_detected: string[];
  tactics_detected: string[];
  exact_phrases: string[];
  indicator_evidence: IndicatorEvidence[];
  confidence: number;
  uncertainty_note: string;
};

const riskColors = {
  LOW: "border-emerald-400/30 bg-emerald-400/10 text-emerald-300",
  MEDIUM: "border-yellow-400/30 bg-yellow-400/10 text-yellow-300",
  HIGH: "border-orange-400/30 bg-orange-400/10 text-orange-300",
  CRITICAL: "border-red-400/30 bg-red-400/10 text-red-300",
};

function readable(value: string) {
  return value.replaceAll("_", " ");
}

export default function TranscriptAnalyzer({ initialTranscript = "" }: { initialTranscript?: string }) {
  const [transcript, setTranscript] = useState(initialTranscript);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runAnalysis() {
    if (!transcript.trim() || loading) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL;

      if (!baseUrl) {
        throw new Error("Analysis API URL is not configured.");
      }

      const response = await fetch(`${baseUrl}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript: transcript.trim() }),
      });

      if (!response.ok) {
        throw new Error(
          response.status === 422
            ? "Please enter a transcript between 1 and 20,000 characters."
            : `Analysis failed (HTTP ${response.status}).`
        );
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to analyze the transcript."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-[#0e1d2e] p-6 sm:p-8">
        <div className="mb-6 flex items-center gap-3">
          <div className="rounded-xl bg-cyan-300/10 p-3 text-cyan-300">
            <ScanSearch size={23} />
          </div>
          <div>
            <h2 className="text-lg font-semibold">Transcript analysis</h2>
            <p className="text-sm text-slate-400">
              Analyze suspicious conversation patterns
            </p>
          </div>
        </div>

        <label htmlFor="transcript" className="mb-3 block text-sm font-medium text-slate-300">
          Conversation transcript
        </label>

        <textarea
          id="transcript"
          value={transcript}
          onChange={(event) => {
            setTranscript(event.target.value);
            setResult(null);
            setError("");
          }}
          maxLength={20000}
          placeholder="Paste a suspicious conversation here..."
          className="min-h-56 w-full resize-y rounded-xl border border-white/10 bg-[#071421] p-5 text-sm leading-7 text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-cyan-300/50"
        />

        <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs text-slate-500">
            {transcript.length.toLocaleString()} / 20,000 characters
          </span>

          <button
            type="button"
            onClick={runAnalysis}
            disabled={!transcript.trim() || loading}
            className="inline-flex items-center gap-2 rounded-xl bg-cyan-300 px-5 py-3 text-sm font-semibold text-[#07111e] transition hover:bg-cyan-200 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading ? (
              <>
                <LoaderCircle size={17} className="animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                Analyze transcript <ArrowRight size={17} />
              </>
            )}
          </button>
        </div>

        {error && (
          <div role="alert" className="mt-5 flex items-start gap-3 rounded-xl border border-red-400/20 bg-red-400/10 p-4 text-sm text-red-200">
            <AlertCircle size={18} className="mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </section>

      {result && (
        <section aria-live="polite" className="space-y-5">
          <div className="rounded-2xl border border-white/10 bg-[#0e1d2e] p-6 sm:p-8">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                {result.scam_detected ? (
                  <ShieldAlert size={28} className="text-orange-300" />
                ) : (
                  <CheckCircle2 size={28} className="text-emerald-300" />
                )}
                <div>
                  <h2 className="text-xl font-semibold">
                    {result.scam_detected
                      ? "Potential scam indicators detected"
                      : "No scam indicators detected"}
                  </h2>
                  <p className="mt-1 text-xs text-slate-400">
                    Automated pattern-based assessment
                  </p>
                </div>
              </div>

              <span className={`rounded-full border px-4 py-2 text-xs font-bold ${riskColors[result.risk_level]}`}>
                {result.risk_level} RISK
              </span>
            </div>

            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              <div className="rounded-xl border border-white/10 bg-[#071421] p-5">
                <div className="text-xs text-slate-400">Engine confidence score</div>
                <div className="mt-2 text-3xl font-bold text-white">
                  {(result.confidence * 100).toFixed(0)}%
                </div>
                <p className="mt-2 text-xs leading-5 text-slate-500">
                  Not a calibrated probability of fraud.
                </p>
              </div>
              <div className="rounded-xl border border-white/10 bg-[#071421] p-5">
                <div className="text-xs text-slate-400">Evidence indicators</div>
                <div className="mt-2 text-3xl font-bold text-white">
                  {result.indicator_evidence?.length ?? 0}
                </div>
                <p className="mt-2 text-xs text-slate-500">
                  Indicators identified by the detection engine.
                </p>
              </div>
            </div>
          </div>

          <div className="grid gap-5 md:grid-cols-2">
            {[
              { title: "Detected tactics", values: result.tactics_detected },
              { title: "Detected stages", values: result.stages_detected },
            ].map(({ title, values }) => (
              <div key={title} className="rounded-2xl border border-white/10 bg-[#0e1d2e] p-6">
                <h3 className="mb-4 font-semibold">{title}</h3>
                {values.length ? (
                  <div className="flex flex-wrap gap-2">
                    {values.map((value) => (
                      <span key={value} className="rounded-lg border border-cyan-300/20 bg-cyan-300/10 px-3 py-2 text-xs capitalize text-cyan-200">
                        {readable(value)}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-slate-400">None detected.</p>
                )}
              </div>
            ))}
          </div>

          <div className="rounded-2xl border border-white/10 bg-[#0e1d2e] p-6 sm:p-8">
            <h3 className="mb-5 text-lg font-semibold">Supporting evidence</h3>

            {result.indicator_evidence?.length ? (
              <div className="space-y-4">
                {result.indicator_evidence.map((item, index) => (
                  <article key={`${item.indicator}-${index}`} className="rounded-xl border border-white/10 bg-[#071421] p-5">
                    <h4 className="font-semibold capitalize text-cyan-200">
                      {readable(item.indicator)}
                    </h4>

                    {item.exact_phrases.length > 0 && (
                      <div className="mt-3 space-y-2">
                        {item.exact_phrases.map((phrase, phraseIndex) => (
                          <blockquote key={phraseIndex} className="border-l-2 border-cyan-300/50 pl-3 text-sm italic text-slate-200">
                            {phrase}
                          </blockquote>
                        ))}
                      </div>
                    )}

                    <p className="mt-4 text-sm leading-6 text-slate-300">
                      {item.explanation}
                    </p>
                    <p className="mt-2 text-sm leading-6 text-amber-200/80">
                      {item.potential_risk}
                    </p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">
                No supporting evidence was identified.
              </p>
            )}
          </div>

          <div className="flex items-start gap-3 rounded-xl border border-amber-300/20 bg-amber-300/5 p-5">
            <AlertCircle size={19} className="mt-0.5 shrink-0 text-amber-200" />
            <div>
              <h3 className="text-sm font-semibold text-amber-200">
                Assessment limitations
              </h3>
              <p className="mt-2 text-sm leading-6 text-slate-300">
                {result.uncertainty_note}
              </p>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
