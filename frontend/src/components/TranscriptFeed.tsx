import React from 'react';

export interface TranscriptItem {
  speaker: 'caller' | 'senior' | 'interceptor' | 'whisper';
  text: string;
  timestamp: number;
  language: string;
}

interface TranscriptFeedProps {
  items: TranscriptItem[];
  heuristicWarning?: { flagged: boolean; clues: string[]; latency_ms: number };
}

export const TranscriptFeed: React.FC<TranscriptFeedProps> = ({ items, heuristicWarning }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col h-[460px]">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
          Live Dual Transcript Feed (Prisma v3.0 Code-Mixed)
        </h2>
        <span className="text-[11px] font-mono text-slate-400">{items.length} utterances</span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 py-3 pr-1 text-sm">
        {items.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500 font-mono text-xs">
            Ready to monitor telephony audio stream...
          </div>
        ) : (
          items.map((item, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-xl border ${
                item.speaker === 'caller'
                  ? 'bg-red-950/20 border-red-900/50 text-slate-200'
                  : 'bg-slate-950 border-cyan-900/50 text-slate-100'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-mono mb-1">
                <span className={`font-bold ${item.speaker === 'caller' ? 'text-red-400' : 'text-cyan-400'}`}>
                  {item.speaker === 'caller' ? 'INBOUND CALLER' : 'SENIOR (GRANDFATHER)'}
                </span>
                <span className="text-slate-500 text-[10px]">offset: +{item.timestamp}s [{item.language}]</span>
              </div>
              <p className="text-sm leading-relaxed">{item.text}</p>
            </div>
          ))
        )}
      </div>

      {heuristicWarning && heuristicWarning.flagged && (
        <div className="mt-2 px-3 py-2 rounded-lg bg-amber-950/40 border border-amber-500/40 text-amber-300 text-xs font-mono flex items-center justify-between">
          <span><strong>Pre-Filter Flagged:</strong> {heuristicWarning.clues.join(', ')}</span>
          <span className="text-[10px] text-amber-400/80">{heuristicWarning.latency_ms}ms fast-path</span>
        </div>
      )}
    </div>
  );
};
