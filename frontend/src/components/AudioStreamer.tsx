import React, { useEffect, useRef } from 'react';

interface AudioStreamerProps {
  isCallerSpeaking: boolean;
  isSeniorSpeaking: boolean;
}

export const AudioStreamer: React.FC<AudioStreamerProps> = ({ isCallerSpeaking, isSeniorSpeaking }) => {
  const callerCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const seniorCanvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    let animId: number;
    let waveOffset = 0;

    const render = () => {
      waveOffset += 0.08;

      if (callerCanvasRef.current) {
        const c = callerCanvasRef.current;
        const ctx = c.getContext('2d');
        if (ctx) {
          ctx.fillStyle = '#06090e';
          ctx.fillRect(0, 0, c.width, c.height);
          ctx.lineWidth = 2;
          ctx.strokeStyle = isCallerSpeaking ? '#ef4444' : '#334155';
          ctx.beginPath();
          for (let i = 0; i < 40; i++) {
            const amp = isCallerSpeaking ? Math.sin(i * 0.4 + waveOffset) * 20 : Math.sin(i * 0.5 + waveOffset) * 2;
            const x = (i * c.width) / 40;
            const y = c.height / 2 + amp;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.stroke();
        }
      }

      if (seniorCanvasRef.current) {
        const c = seniorCanvasRef.current;
        const ctx = c.getContext('2d');
        if (ctx) {
          ctx.fillStyle = '#06090e';
          ctx.fillRect(0, 0, c.width, c.height);
          ctx.lineWidth = 2;
          ctx.strokeStyle = isSeniorSpeaking ? '#38bdf8' : '#334155';
          ctx.beginPath();
          for (let i = 0; i < 40; i++) {
            const amp = isSeniorSpeaking ? Math.sin(i * 0.35 + waveOffset) * 16 : Math.sin(i * 0.4 + waveOffset) * 1.5;
            const x = (i * c.width) / 40;
            const y = c.height / 2 + amp;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.stroke();
        }
      }

      animId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animId);
  }, [isCallerSpeaking, isSeniorSpeaking]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono font-bold text-slate-300">Channel 1: Inbound Caller</span>
          <span className="text-[11px] font-mono text-red-400 bg-red-950/40 px-2 py-0.5 rounded border border-red-800/40">
            8kHz Telephony (Prisma)
          </span>
        </div>
        <canvas ref={callerCanvasRef} width={400} height={64} className="w-full h-16 bg-slate-950 rounded-lg border border-slate-800/80" />
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono font-bold text-slate-300">Channel 2: Senior Earbud Mic</span>
          <span className="text-[11px] font-mono text-cyan-400 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40">
            16kHz Local Acoustic
          </span>
        </div>
        <canvas ref={seniorCanvasRef} width={400} height={64} className="w-full h-16 bg-slate-950 rounded-lg border border-slate-800/80" />
      </div>
    </div>
  );
};
