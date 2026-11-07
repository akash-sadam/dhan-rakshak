import React from 'react';

interface VoiceInterventionProps {
  whisperText: string;
  interceptorText: string;
  onPlayWhisper: () => void;
  onPlayInterceptor: () => void;
}

export const VoiceIntervention: React.FC<VoiceInterventionProps> = ({
  whisperText,
  interceptorText,
  onPlayWhisper,
  onPlayInterceptor
}) => {
  return (
    <section className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 mb-4 border-b border-slate-800">
        <h2 className="text-sm font-mono font-bold uppercase tracking-wider text-white">
          Active Counter-Measures (Gnani Timbre Expressive Synthesis)
        </h2>
        <div className="text-xs font-mono text-slate-400">
          Dual Audio Routing: <span className="text-cyan-300">Earbud (Private)</span> vs <span className="text-red-300">Speaker (Intercept)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Channel 1: Telugu Whisper Mode */}
        <div className="p-4 rounded-xl border border-cyan-500/30 bg-cyan-950/20 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono font-bold text-cyan-300 uppercase">1. Earbud Whisper Mode (Telugu)</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300">
                &lt;whispers&gt; tag
              </span>
            </div>
            <p className="text-sm text-slate-200 italic bg-slate-950/80 p-3 rounded-lg border border-cyan-800/40">
              "{whisperText}"
            </p>
          </div>
          <div className="flex items-center justify-between mt-3 pt-3 border-t border-cyan-900/40">
            <button
              onClick={onPlayWhisper}
              className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-mono font-bold transition"
            >
              Whisper In Senior's Earbud
            </button>
            <span className="text-[11px] font-mono text-slate-400">Voice: <strong className="text-cyan-300">te-female-calm</strong></span>
          </div>
        </div>

        {/* Channel 2: Authoritative Speaker Interceptor */}
        <div className="p-4 rounded-xl border border-red-500/30 bg-red-950/20 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono font-bold text-red-300 uppercase">2. Speaker Interceptor (Deterrent)</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-red-500/20 text-red-300">
                Authoritative Legal Voice
              </span>
            </div>
            <p className="text-sm text-slate-200 italic bg-slate-950/80 p-3 rounded-lg border border-red-800/40 font-mono">
              "{interceptorText}"
            </p>
          </div>
          <div className="flex items-center justify-between mt-3 pt-3 border-t border-red-900/40">
            <button
              onClick={onPlayInterceptor}
              className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-mono font-bold transition"
            >
              Intercept Scammer On Speaker
            </button>
            <span className="text-[11px] font-mono text-slate-400">Voice: <strong className="text-red-300">hi-male-authoritative</strong></span>
          </div>
        </div>
      </div>
    </section>
  );
};
