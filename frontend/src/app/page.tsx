"use client";

import { useState } from "react";
import SignalVisualization from "@/components/SignalVisualization";
import TranscriptAnalyzer from "@/components/TranscriptAnalyzer";
import AudioUploader from "@/components/AudioUploader";
import {
  Activity, ArrowRight, ArrowUpRight, AudioLines, CheckCircle2,
  FileText, Fingerprint, LayoutDashboard, Menu, Mic,
  ScanSearch, ShieldCheck, Sparkles, X
} from "lucide-react";

const navigation = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "Analyze", icon: AudioLines },
  { name: "Threat Intelligence", icon: ScanSearch },
  { name: "Reports", icon: FileText },
];

const features = [
  {
    icon: Fingerprint,
    title: "Evidence-led insights",
    description: "Understand which phrases and indicators contributed to an assessment.",
  },
  {
    icon: Activity,
    title: "Manipulation patterns",
    description: "Explore signals such as urgency, authority pressure, and secrecy.",
  },
  {
    icon: ShieldCheck,
    title: "Explainable results",
    description: "See the reasoning behind flagged conversation patterns.",
  },
];

export default function Home() {
  const [audioTranscript, setAudioTranscript] = useState("");
  const [audioTranscriptVersion, setAudioTranscriptVersion] = useState(0);
  const [active, setActive] = useState("Overview");
  const [menuOpen, setMenuOpen] = useState(false);
  const [transcript, setTranscript] = useState("");

  function navigate(page: string) {
    setActive(page);
    setMenuOpen(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="min-h-screen bg-[#07111e] text-slate-100 selection:bg-cyan-300/30">
      <header className="sticky top-0 z-50 border-b border-white/10 bg-[#091522]/90 backdrop-blur-xl">
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between gap-5 px-5 sm:px-8">
          <button
            onClick={() => navigate("Overview")}
            className="flex shrink-0 items-center gap-3 text-left"
            aria-label="VaaniShield home"
          >
            <div className="rounded-xl border border-cyan-300/15 bg-cyan-300/10 p-2.5 text-cyan-300">
              <ShieldCheck size={26} />
            </div>
            <div>
              <div className="text-lg font-bold tracking-tight">VaaniShield</div>
              <div className="text-[9px] font-medium uppercase tracking-[0.2em] text-slate-400">
                Voice Fraud Intelligence
              </div>
            </div>
          </button>

          <nav className="hidden items-center gap-1 rounded-full border border-white/10 bg-white/[0.03] p-1 lg:flex">
            {navigation.map(({ name, icon: Icon }) => (
              <button
                key={name}
                onClick={() => navigate(name)}
                className={`flex items-center gap-2 rounded-full px-4 py-2.5 text-sm transition-all duration-200 ${
                  active === name
                    ? "bg-cyan-300/10 font-semibold text-cyan-200"
                    : "text-slate-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <Icon size={16} />
                {name}
              </button>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate("Analyze")}
              className="hidden items-center gap-2 rounded-xl bg-cyan-300 px-4 py-2.5 text-sm font-semibold text-[#07111e] transition hover:-translate-y-0.5 hover:bg-cyan-200 sm:inline-flex"
            >
              Start analysis <ArrowUpRight size={16} />
            </button>
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="rounded-xl border border-white/10 p-2.5 text-slate-200 lg:hidden"
              aria-label={menuOpen ? "Close menu" : "Open menu"}
              aria-expanded={menuOpen}
            >
              {menuOpen ? <X size={21} /> : <Menu size={21} />}
            </button>
          </div>
        </div>

        {menuOpen && (
          <nav className="border-t border-white/10 bg-[#0b1929] px-5 py-4 lg:hidden">
            <div className="mx-auto grid max-w-7xl gap-2">
              {navigation.map(({ name, icon: Icon }) => (
                <button
                  key={name}
                  onClick={() => navigate(name)}
                  className={`flex items-center gap-3 rounded-xl px-4 py-3 text-left text-sm ${
                    active === name
                      ? "bg-cyan-300/10 text-cyan-200"
                      : "text-slate-300 hover:bg-white/5"
                  }`}
                >
                  <Icon size={18} />
                  {name}
                </button>
              ))}
            </div>
          </nav>
        )}
      </header>

      <main className="mx-auto max-w-7xl px-5 pb-12 pt-9 sm:px-8">
        {active === "Overview" && (
          <div className="animate-[fadeIn_500ms_ease-out] space-y-8">
            <section className="relative overflow-hidden rounded-[28px] border border-cyan-300/15 bg-gradient-to-br from-[#12384c] via-[#10263a] to-[#0b1b2d] px-7 py-9 sm:px-10 lg:px-12 lg:py-11">
              <div className="pointer-events-none absolute -right-20 -top-28 h-96 w-96 rounded-full bg-cyan-300/10 blur-3xl" />

              <div className="relative grid items-center gap-8 lg:grid-cols-[1.15fr_0.85fr]">
                <div>
                  <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-medium text-cyan-200">
                    <Sparkles size={15} />
                    Multilingual fraud intelligence
                  </div>

                  <h1 className="max-w-2xl text-4xl font-bold leading-[1.15] tracking-tight sm:text-5xl xl:text-[3.5rem]">
                    Hear the words.
                    <br />
                    <span className="bg-gradient-to-r from-cyan-300 to-sky-400 bg-clip-text text-transparent">
                      See the warning signs.
                    </span>
                  </h1>

                  <p className="mt-5 max-w-xl text-base leading-7 text-slate-300">
                    Analyze multilingual conversations, identify manipulation
                    tactics, and understand the evidence behind potential fraud.
                  </p>

                  <div className="mt-7 flex flex-wrap items-center gap-4">
                    <button
                      onClick={() => navigate("Analyze")}
                      className="inline-flex items-center gap-2 rounded-xl bg-cyan-300 px-6 py-3.5 text-sm font-semibold text-[#07111e] shadow-lg shadow-cyan-400/10 transition duration-200 hover:-translate-y-1 hover:bg-cyan-200"
                    >
                      Analyze a conversation <ArrowRight size={18} />
                    </button>
                    <span className="flex items-center gap-2 text-sm text-slate-400">
                      <CheckCircle2 size={16} className="text-cyan-300" />
                      Explainable insights
                    </span>
                  </div>
                </div>

                <div className="flex justify-center lg:justify-end">
                  <SignalVisualization />
                </div>
              </div>
            </section>

            <section className="grid gap-5 md:grid-cols-3">
              {features.map(({ icon: Icon, title, description }) => (
                <article
                  key={title}
                  className="group rounded-2xl border border-white/10 bg-[#0e1d2e] p-7 transition duration-300 hover:-translate-y-1 hover:border-cyan-300/30 hover:bg-[#112439]"
                >
                  <div className="mb-5 inline-flex rounded-xl bg-cyan-300/10 p-3 text-cyan-300 transition group-hover:bg-cyan-300/15">
                    <Icon size={24} />
                  </div>
                  <h2 className="text-lg font-semibold">{title}</h2>
                  <p className="mt-3 text-sm leading-7 text-slate-400">{description}</p>
                </article>
              ))}
            </section>

            <section className="flex flex-col justify-between gap-6 rounded-2xl border border-white/10 bg-[#0e1d2e] p-7 sm:flex-row sm:items-center sm:p-9">
              <div>
                <div className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">
                  Analysis workspace
                </div>
                <h2 className="text-2xl font-semibold">Ready to investigate a conversation?</h2>
                <p className="mt-2 max-w-xl text-sm leading-7 text-slate-400">
                  Start with a transcript. Voice transcription and live detection results
                  will be connected to the existing Python services.
                </p>
              </div>
              <button
                onClick={() => navigate("Analyze")}
                className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl border border-cyan-300/30 px-5 py-3 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-300/10"
              >
                Open workspace <ArrowUpRight size={17} />
              </button>
            </section>
          </div>
        )}

        {active === "Analyze" && (
          <div className="animate-[fadeIn_500ms_ease-out] space-y-7">
            <div className="max-w-3xl">
              <div className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">
                Analysis workspace
              </div>
              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                Investigate a conversation
              </h1>
              <p className="mt-3 text-sm leading-7 text-slate-400 sm:text-base">
                Examine transcripts for suspicious patterns and explore the evidence
                behind potential fraud indicators.
              </p>
            </div>

            <div className="space-y-6">
              <AudioUploader onTranscriptReady={(text) => { setAudioTranscript(text); setAudioTranscriptVersion((v) => v + 1); }} />

              <TranscriptAnalyzer key={audioTranscriptVersion} initialTranscript={audioTranscript} />
            </div>
          </div>
        )}

        {active === "Threat Intelligence" && (
          <div className="animate-[fadeIn_500ms_ease-out]">
            <div className="mb-8 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">
              Threat intelligence
            </div>
            <h1 className="text-3xl font-bold sm:text-4xl">Understand the tactics</h1>
            <p className="mt-4 max-w-2xl text-slate-400">
              Explore common conversation patterns associated with impersonation,
              coercion, secrecy, and payment pressure.
            </p>
            <div className="mt-9 grid gap-5 md:grid-cols-3">
              {[
                ["Authority impersonation", "Attempts to create trust or fear through claims of official authority."],
                ["Urgency and pressure", "Language designed to rush decisions and discourage verification."],
                ["Secrecy and isolation", "Requests to avoid consulting trusted people or independent sources."],
              ].map(([title, description]) => (
                <article key={title} className="rounded-2xl border border-white/10 bg-[#0e1d2e] p-7">
                  <ScanSearch className="mb-5 text-cyan-300" size={24} />
                  <h2 className="font-semibold">{title}</h2>
                  <p className="mt-3 text-sm leading-7 text-slate-400">{description}</p>
                </article>
              ))}
            </div>
          </div>
        )}

        {active === "Reports" && (
          <div className="animate-[fadeIn_500ms_ease-out]">
            <div className="mb-8 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">
              Reports
            </div>
            <h1 className="text-3xl font-bold sm:text-4xl">Analysis reports</h1>
            <p className="mt-4 max-w-2xl text-slate-400">
              Review explainable findings from analyzed conversations.
            </p>
            <div className="mt-9 rounded-2xl border border-dashed border-white/15 bg-[#0e1d2e] px-6 py-16 text-center">
              <FileText className="mx-auto mb-5 text-cyan-300" size={36} />
              <h2 className="text-lg font-semibold">No reports available yet</h2>
              <p className="mx-auto mt-3 max-w-md text-sm leading-7 text-slate-400">
                Reports will become available after we connect the analysis engine.
                No results are being generated or stored by this preview.
              </p>
              <button
                onClick={() => navigate("Analyze")}
                className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-cyan-300 hover:text-cyan-200"
              >
                Go to analysis <ArrowRight size={17} />
              </button>
            </div>
          </div>
        )}

        <footer className="mt-14 flex flex-wrap items-center justify-between gap-3 border-t border-white/10 pt-7 text-xs text-slate-500">
          <span>VaaniShield / Explainable multilingual fraud intelligence</span>
          <span>Live scam analysis powered by Python and Gnani Prisma</span>
        </footer>
      </main>

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        html { scroll-behavior: smooth; }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
          }
        }
      `}</style>
    </div>
  );
}
