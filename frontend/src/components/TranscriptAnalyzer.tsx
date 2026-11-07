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

type GeminiAssessment = {
  scam_detected: boolean;
  risk_level: AnalysisResult["risk_level"];
  stages_detected: string[];
  tactics_detected: string[];
  indicator_evidence: IndicatorEvidence[];
  explanation: string;
  uncertainty_note: string;
};

type HybridResponse = {
  rule_analysis: AnalysisResult;
  ai_analysis: GeminiAssessment | null;
  ai_status: "available" | "fallback";
  verdict_agreement: boolean | null;
  risk_agreement: boolean | null;
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
  const [hybridResult, setHybridResult] = useState<HybridResponse | null>(null);
  const [useAi, setUseAi] = useState(false);
  const [aiConsent, setAiConsent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runAnalysis() {
    if (!transcript.trim() || loading) return;
    if (useAi && !aiConsent) {
      setError("Please confirm consent before using Gemini AI analysis.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setHybridResult(null);

    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL;

      if (!baseUrl) {
        throw new Error("Analysis API URL is not configured.");
      }

      const response = await fetch(`${baseUrl}${useAi ? "/api/analyze-hybrid" : "/api/analyze"}`, {
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

      if (useAi) {
        const data: HybridResponse = await response.json();
        setResult(data.rule_analysis);
        setHybridResult(data);
      } else {
        const data: AnalysisResult = await response.json();
        setResult(data);
      }
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

        <div className="mt-5 space-y-3 rounded-xl border border-white/10 bg-[#071421] p-4">
          <label className="flex cursor-pointer items-start gap-3">
            <input
              type="checkbox"
              checked={useAi}
              onChange={(event) => {
                setUseAi(event.target.checked);
                setAiConsent(false);
                setResult(null);
                setHybridResult(null);
                setError("");
              }}
              className="mt-1 h-4 w-4 accent-cyan-300"
            />
            <span>
              <span className="block text-sm font-semibold text-slate-100">
                Enable Gemini AI comparison
              </span>
              <span className="mt-1 block text-xs leading-5 text-slate-400">
                Compare contextual AI findings with VaaniShield's rule-based assessment.
              </span>
            </span>
          </label>

          {useAi && (
            <div className="space-y-3 border-t border-white/10 pt-3">
              <p className="text-xs leading-5 text-amber-200/90">
                Privacy notice: Your transcript will be redacted by the VaaniShield
                backend before being sent to Google's Gemini service.
                Redaction may not remove every sensitive detail. Avoid submitting
                real personal or confidential conversations during this demo.
              </p>
              <label className="flex cursor-pointer items-start gap-3">
                <input
                  type="checkbox"
                  checked={aiConsent}
                  onChange={(event) => {
                    setAiConsent(event.target.checked);
                    setError("");
                  }}
                  className="mt-1 h-4 w-4 accent-cyan-300"
                />
                <span className="text-xs leading-5 text-slate-300">
                  I understand and agree to external AI processing of the
                  redacted transcript.
                </span>
              </label>
            </div>
          )}
        </div>

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

      {hybridResult && (
        <section aria-live="polite" className="rounded-2xl border border-cyan-300/20 bg-[#0e1d2e] p-6 sm:p-8">
          <div className="mb-5">
            <h2 className="text-xl font-semibold text-cyan-200">
              Gemini AI comparison
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Independent contextual assessment compared with the rule engine.
            </p>
          </div>

          {hybridResult.ai_status === "fallback" || !hybridResult.ai_analysis ? (
            <div className="rounded-xl border border-amber-300/20 bg-amber-300/5 p-4 text-sm text-amber-100">
              Gemini is currently unavailable. The rule-based assessment below
              remains available.
            </div>
          ) : (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl border border-white/10 bg-[#071421] p-4">
                  <p className="text-xs text-slate-400">Rule engine risk</p>
                  <p className="mt-2 text-lg font-semibold">
                    {hybridResult.rule_analysis.risk_level}
                  </p>
                </div>
                <div className="rounded-xl border border-white/10 bg-[#071421] p-4">
                  <p className="text-xs text-slate-400">Gemini AI risk</p>
                  <span className={`mt-2 inline-block rounded-full border px-3 py-1 text-sm font-semibold ${riskColors[hybridResult.ai_analysis.risk_level]}`}>
                    {hybridResult.ai_analysis.risk_level}
                  </span>
                </div>
              </div>

              <p className="text-sm text-slate-300">
                Scam verdict: {hybridResult.verdict_agreement ? "Both systems agree." : "The systems disagree."}
                {" "}Risk level: {hybridResult.risk_agreement ? "Both systems agree." : "The systems disagree."}
              </p>

              <div>
                <h3 className="mb-2 text-sm font-semibold text-cyan-200">
                  Gemini explanation
                </h3>
                <p className="text-sm leading-6 text-slate-300">
                  {hybridResult.ai_analysis.explanation}
                </p>
              </div>

              <div>
                <h3 className="mb-3 text-sm font-semibold text-cyan-200">
                  Gemini detected tactics
                </h3>
                <div className="flex flex-wrap gap-2">
                  {hybridResult.ai_analysis.tactics_detected.length ? (
                    hybridResult.ai_analysis.tactics_detected.map((tactic) => (
                      <span key={tactic} className="rounded-lg border border-cyan-300/20 bg-cyan-300/10 px-3 py-2 text-xs capitalize text-cyan-200">
                        {readable(tactic)}
                      </span>
                    ))
                  ) : (
                    <p className="text-sm text-slate-400">None detected.</p>
                  )}
                </div>
              </div>

              <div>
                <h3 className="mb-3 text-sm font-semibold text-cyan-200">
                  Gemini verified evidence
                </h3>
                {hybridResult.ai_analysis.indicator_evidence.length ? (
                  <div className="space-y-3">
                    {hybridResult.ai_analysis.indicator_evidence.map((item, index) => (
                      <div key={`${item.indicator}-${index}`} className="rounded-xl border border-white/10 bg-[#071421] p-4">
                        <p className="text-sm font-semibold capitalize text-cyan-200">
                          {readable(item.indicator)}
                        </p>
                        {item.exact_phrases.map((phrase, phraseIndex) => (
                          <blockquote key={phraseIndex} className="mt-2 border-l-2 border-cyan-300/50 pl-3 text-sm italic text-slate-200">
                            {phrase}
                          </blockquote>
                        ))}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-slate-400">
                    No transcript-matched evidence was returned.
                  </p>
                )}
              </div>

              <p className="text-xs leading-5 text-slate-400">
                {hybridResult.ai_analysis.uncertainty_note}
                {" "}AI findings are not proof of fraud.
              </p>
            </div>
          )}
        </section>
      )}

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
