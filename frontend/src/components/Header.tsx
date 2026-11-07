import React from 'react';

interface HeaderProps {
  status: 'STANDBY' | 'ACTIVE_CALL' | 'COERCION_DETECTED';
  onReset: () => void;
  onOpenSos: () => void;
  sosCount: number;
}

export const Header: React.FC<HeaderProps> = ({ status, onReset, onOpenSos, sosCount }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-4 lg:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <span className="text-xl">🛡️</span>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-extrabold tracking-tight text-white flex items-center gap-1.5">
                DHAN-RAKSHAK <span className="text-cyan-400 text-sm font-semibold">(ధన రక్షక్ / धन रक्षक)</span>
              </h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-500/20 border border-indigo-500/40 text-indigo-300">
                Sovereign Indic MoE
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono">
              Acoustic Telephony Guardian & Real-Time Voice Interceptor • Gnani.ai Challenge
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-full border text-xs font-mono font-bold ${
            status === 'COERCION_DETECTED'
              ? 'border-red-500/40 bg-red-950/40 text-red-400 animate-pulse'
              : status === 'ACTIVE_CALL'
              ? 'border-amber-500/40 bg-amber-950/40 text-amber-400 animate-pulse'
              : 'border-emerald-500/40 bg-emerald-950/40 text-emerald-400'
          }`}>
            <span className="w-2.5 h-2.5 rounded-full bg-current"></span>
            <span>{status === 'COERCION_DETECTED' ? 'COERCION DETECTED 🔴' : status === 'ACTIVE_CALL' ? 'CALL ENGAGED ⚠️' : 'MONITORING ACTIVE'}</span>
          </div>

          <button onClick={onReset} className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-xs font-mono text-slate-300 transition">
            Reset
          </button>

          <button onClick={onOpenSos} className="relative px-3.5 py-1.5 rounded-lg bg-red-600/20 border border-red-500/40 hover:bg-red-600/30 text-red-300 text-xs font-mono font-bold transition">
            SOS Log {sosCount > 0 && <span className="ml-1 px-1.5 py-0.2 bg-red-600 text-white rounded-full text-[10px]">{sosCount}</span>}
          </button>
        </div>
      </div>
    </header>
  );
};
