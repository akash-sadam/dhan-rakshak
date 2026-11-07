import { useState, useEffect, useRef } from 'react';
import { TranscriptItem } from '../components/TranscriptFeed';
import { EmergencyAlertData } from '../components/IncidentLogger';

export function useGnaniPipeline() {
  const [status, setStatus] = useState<'STANDBY' | 'ACTIVE_CALL' | 'COERCION_DETECTED'>('STANDBY');
  const [transcript, setTranscript] = useState<TranscriptItem[]>([]);
  const [threatScore, setThreatScore] = useState<number>(0);
  const [detectedScheme, setDetectedScheme] = useState<string>('BENIGN');
  const [coercionLevel, setCoercionLevel] = useState<string>('STANDBY');
  const [agency, setAgency] = useState<string | null>(null);
  const [amount, setAmount] = useState<string | null>(null);
  const [clues, setClues] = useState<string[]>([]);
  const [whisperText, setWhisperText] = useState<string>('Nana bhayapadakandi, idi fake call. Call cut cheyandi.');
  const [interceptorText, setInterceptorText] = useState<string>('Yeh call Cyber Crime Branch ki nigrani mein hai.');
  const [whisperAudio, setWhisperAudio] = useState<string | null>(null);
  const [interceptorAudio, setInterceptorAudio] = useState<string | null>(null);
  const [alerts, setAlerts] = useState<EmergencyAlertData[]>([]);
  const [heuristicWarning, setHeuristicWarning] = useState<any>(null);

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const loc = window.location;
    const wsProto = loc.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${wsProto}//${loc.host}/ws/stream-call`);
    wsRef.current = ws;

    ws.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      if (data.type === 'TRANSCRIPT_CHUNK') {
        setTranscript((prev) => [...prev, data.chunk]);
      } else if (data.type === 'THREAT_ASSESSMENT') {
        const a = data.assessment;
        setThreatScore(a.threat_score);
        setDetectedScheme(a.detected_scheme);
        setCoercionLevel(a.coercion_level);
        if (a.threat_score >= 75) setStatus('COERCION_DETECTED');
        if (a.extracted_entities) {
          setAgency(a.extracted_entities.impersonated_agency);
          setAmount(a.extracted_entities.amount_demanded);
        }
        if (a.urgency_clues) setClues(a.urgency_clues);
        if (a.victim_whisper_telugu) setWhisperText(a.victim_whisper_telugu);
        if (a.interceptor_response_hindi) setInterceptorText(a.interceptor_response_hindi);
      } else if (data.type === 'HEURISTIC_PREVIEW') {
        setHeuristicWarning(data.data);
      } else if (data.type === 'SOS_DISPATCHED') {
        setAlerts((prev) => [data.alert, ...prev]);
      } else if (data.type === 'AUTO_INTERVENTIONS_PREPARED') {
        setWhisperAudio(data.whisper_audio);
        setInterceptorAudio(data.interceptor_audio);
      }
    };

    return () => ws.close();
  }, []);

  const startScenario = (id: string) => {
    setTranscript([]);
    setThreatScore(0);
    setDetectedScheme('ANALYZING...');
    setCoercionLevel('STANDBY');
    setStatus('ACTIVE_CALL');
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'START_SCENARIO', scenario_id: id }));
    }
  };

  const reset = () => {
    setTranscript([]);
    setThreatScore(0);
    setDetectedScheme('BENIGN');
    setCoercionLevel('STANDBY');
    setStatus('STANDBY');
    setClues([]);
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'RESET_CALL' }));
    }
  };

  return {
    status,
    transcript,
    threatScore,
    detectedScheme,
    coercionLevel,
    agency,
    amount,
    clues,
    whisperText,
    interceptorText,
    whisperAudio,
    interceptorAudio,
    alerts,
    heuristicWarning,
    startScenario,
    reset
  };
}
