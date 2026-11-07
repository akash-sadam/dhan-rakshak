import React, { useState } from 'react';
import { Header } from './components/Header';
import { AudioStreamer } from './components/AudioStreamer';
import { TranscriptFeed } from './components/TranscriptFeed';
import { ThreatMeter } from './components/ThreatMeter';
import { VoiceIntervention } from './components/VoiceIntervention';
import { IncidentLogger } from './components/IncidentLogger';
import { useGnaniPipeline } from './hooks/useGnaniPipeline';

export const App: React.FC = () => {
  const [isSosOpen, setIsSosOpen] = useState(false);
  const pipeline = useGnaniPipeline();

  const playAudio = (b64: string | null) => {
    if (!b64) return;
    const snd = new Audio(`data:audio/wav;base64,${b64}`);
    snd.play();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header
        status={pipeline.status}
        onReset={pipeline.reset}
        onOpenSos={() => setIsSosOpen(true)}
        sosCount={pipeline.alerts.length}
      />

      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-5 flex-1 w-full space-y-5">
        {/* Scenario Buttons */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <button
              onClick={() => pipeline.startScenario('digital_arrest')}
              className="p-3 rounded-xl border border-red-500/30 bg-red-950/20 hover:border-red-500/60 transition text-left"
            >
              <div className="text-xs font-bold text-red-400 font-mono">🚨 DIGITAL ARREST</div>
              <p className="text-xs text-slate-300">Fake Police/CBI warrant extortion.</p>
            </button>

            <button
              onClick={() => pipeline.startScenario('power_cut')}
              className="p-3 rounded-xl border border-amber-500/30 bg-amber-950/20 hover:border-amber-500/60 transition text-left"
            >
              <div className="text-xs font-bold text-amber-400 font-mono">⚡ ELECTRICITY CUT</div>
              <p className="text-xs text-slate-300">Urgent 1-hour power disconnection scam.</p>
            </button>

            <button
              onClick={() => pipeline.startScenario('kyc_expiry')}
              className="p-3 rounded-xl border border-yellow-500/30 bg-yellow-950/20 hover:border-yellow-500/60 transition text-left"
            >
              <div className="text-xs font-bold text-yellow-400 font-mono">🏦 BANK KYC EXPOSURE</div>
              <p className="text-xs text-slate-300">SBI account freeze & remote APK install.</p>
            </button>

            <button
              onClick={() => pipeline.startScenario('benign_family')}
              className="p-3 rounded-xl border border-emerald-500/30 bg-emerald-950/20 hover:border-emerald-500/60 transition text-left"
            >
              <div className="text-xs font-bold text-emerald-400 font-mono">🟢 BENIGN FAMILY CALL</div>
              <p className="text-xs text-slate-300">Granddaughter health & sweets check.</p>
            </button>
          </div>
        </section>

        <AudioStreamer
          isCallerSpeaking={pipeline.status === 'ACTIVE_CALL' || pipeline.status === 'COERCION_DETECTED'}
          isSeniorSpeaking={false}
        />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          <div className="lg:col-span-7">
            <TranscriptFeed
              items={pipeline.transcript}
              heuristicWarning={pipeline.heuristicWarning}
            />
          </div>
          <div className="lg:col-span-5">
            <ThreatMeter
              score={pipeline.threatScore}
              scheme={pipeline.detectedScheme}
              coercionLevel={pipeline.coercionLevel}
              agency={pipeline.agency}
              amount={pipeline.amount}
              clues={pipeline.clues}
            />
          </div>
        </div>

        <VoiceIntervention
          whisperText={pipeline.whisperText}
          interceptorText={pipeline.interceptorText}
          onPlayWhisper={() => playAudio(pipeline.whisperAudio)}
          onPlayInterceptor={() => playAudio(pipeline.interceptorAudio)}
        />
      </main>

      <IncidentLogger
        isOpen={isSosOpen}
        onClose={() => setIsSosOpen(false)}
        alerts={pipeline.alerts}
      />
    </div>
  );
};

export default App;
