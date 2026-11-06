"use client";

import { Activity, AudioLines, ScanSearch, ShieldAlert } from "lucide-react";

const signals = [
  { label: "Authority pressure", width: "76%", color: "bg-cyan-300" },
  { label: "Urgency indicators", width: "58%", color: "bg-sky-400" },
  { label: "Secrecy patterns", width: "42%", color: "bg-violet-400" },
];

export default function SignalVisualization() {
  return (
    <div className="relative w-full max-w-md">
      <div className="absolute -inset-5 rounded-3xl bg-cyan-400/10 blur-3xl" />

      <div className="relative overflow-hidden rounded-2xl border border-cyan-300/20 bg-[#081827]/95 p-4 shadow-2xl shadow-black/30 sm:p-5">
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <div className="flex items-center gap-2">
            <ScanSearch size={19} className="text-cyan-300" />
            <span className="text-sm font-semibold text-white">
              Signal intelligence
            </span>
          </div>
          <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-2.5 py-1 text-[10px] font-medium text-cyan-200">
            DEMO PREVIEW
          </span>
        </div>

        <div className="relative my-4 flex h-36 items-center justify-center overflow-hidden rounded-xl bg-[#0a2031]">
          <div className="absolute h-36 w-36 animate-[spin_18s_linear_infinite] rounded-full border border-dashed border-cyan-300/30 motion-reduce:animate-none" />
          <div className="absolute h-24 w-24 rounded-full border border-cyan-300/20" />
          <div className="absolute h-14 w-14 rounded-full border border-cyan-300/20" />

          <div className="absolute h-36 w-36 animate-[spin_7s_linear_infinite] rounded-full border-t-2 border-transparent border-t-cyan-300/70 motion-reduce:animate-none" />

          <div className="relative z-10 flex h-14 w-14 items-center justify-center rounded-full border border-cyan-300/30 bg-cyan-300/10 shadow-lg shadow-cyan-400/10">
            <AudioLines size={25} className="text-cyan-300" />
          </div>

          <div className="absolute left-[24%] top-[28%] h-2 w-2 animate-pulse rounded-full bg-cyan-300 motion-reduce:animate-none" />
          <div className="absolute right-[23%] top-[38%] h-2.5 w-2.5 animate-pulse rounded-full bg-amber-300 motion-reduce:animate-none" />
          <div className="absolute bottom-[22%] right-[35%] h-2 w-2 rounded-full bg-sky-400" />
        </div>

        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
            <Activity size={15} className="text-cyan-300" />
            Example signal patterns
          </div>
          <span className="text-[10px] text-slate-500">
            Illustrative only
          </span>
        </div>

        <div className="space-y-4">
          {signals.map((signal) => (
            <div key={signal.label}>
              <div className="mb-2 text-xs text-slate-300">
                {signal.label}
              </div>
              <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                <div
                  className={`h-full rounded-full ${signal.color}`}
                  style={{ width: signal.width }}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 flex items-start gap-3 rounded-xl border border-amber-300/10 bg-amber-300/5 p-3">
          <ShieldAlert size={17} className="mt-0.5 shrink-0 text-amber-200" />
          <p className="text-xs leading-5 text-slate-400">
            This visualization uses example values, not a real
            conversation assessment.
          </p>
        </div>
      </div>
    </div>
  );
}
