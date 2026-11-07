import React from 'react';

interface ThreatMeterProps {
  score: number;
  scheme: string;
  coercionLevel: string;
  agency?: string | null;
  amount?: string | null;
  clues: string[];
}

export const ThreatMeter: React.FC<ThreatMeterProps> = ({
  score,
  scheme,
  coercionLevel,
  agency,
  amount,
  clues
}) => {
  const isCritical = score >= 75;
  const isSuspicious = score >= 40 && score < 75;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col h-[460px] justify-between">
      <div>
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
            Evon 30B MoE Threat Radar
          </h2>
          <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${
            isCritical
              ? 'bg-red-600/30 text-red-300 border-red-500 animate-pulse'
              : isSuspicious
              ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
              : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
          }`}>
            {coercionLevel}
          </span>
        </div>

        <div className="my-4">
          <div className="flex items-end justify-between mb-1.5 font-mono">
            <span className="text-xs text-slate-400 uppercase">Acoustic Threat Level</span>
            <span className={`text-3xl font-extrabold ${isCritical ? 'text-red-500 animate-pulse' : isSuspicious ? 'text-amber-400' : 'text-emerald-400'}`}>
              {score}%
            </span>
          </div>
          <div className="w-full bg-slate-950 rounded-full h-4 overflow-hidden border border-slate-800 p-0.5">
            <div
              className="bg-gradient-to-r from-emerald-500 via-yellow-500 to-red-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.max(4, score)}%` }}
            />
          </div>
        </div>

        <div className="space-y-2.5 text-xs font-mono">
          <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-[11px] text-slate-400 mb-0.5">Detected Scheme</div>
            <div className="text-slate-200 font-bold text-sm">{scheme.replace(/_/g, ' ')}</div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
              <div className="text-[10px] text-slate-400">Impersonated Entity</div>
              <div className="text-slate-200 font-semibold truncate">{agency || 'None'}</div>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
              <div className="text-[10px] text-slate-400">Demanded Amount</div>
              <div className="text-slate-200 font-semibold truncate">{amount || '₹0'}</div>
            </div>
          </div>

          <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 mb-1">Psychological Coercion Clues</div>
            <div className="flex flex-wrap gap-1">
              {clues.length > 0 ? (
                clues.map((c, i) => (
                  <span key={i} className="text-[10px] font-mono px-2 py-0.5 rounded bg-red-500/20 border border-red-500/40 text-red-300 font-semibold">
                    {c}
                  </span>
                ))
              ) : (
                <span className="text-[10px] text-slate-500">No coercion indicators</span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-800 pt-3">
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1">
          <span>Glass-to-Ear Total Latency</span>
          <span className="text-cyan-400 font-bold font-mono">~1,350 ms (&lt;1.5s Goal)</span>
        </div>
      </div>
    </div>
  );
};
