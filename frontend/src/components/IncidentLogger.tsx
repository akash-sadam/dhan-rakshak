import React from 'react';

export interface EmergencyAlertData {
  alert_id: string;
  timestamp: string;
  victim_name: string;
  emergency_contact: string;
  phone_number: string;
  detected_scheme: string;
  threat_score: number;
  whatsapp_message: string;
}

interface IncidentLoggerProps {
  isOpen: boolean;
  onClose: () => void;
  alerts: EmergencyAlertData[];
}

export const IncidentLogger: React.FC<IncidentLoggerProps> = ({ isOpen, onClose, alerts }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-5 shadow-2xl relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white">
          ✕
        </button>

        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-red-600/20 border border-red-500/40 flex items-center justify-center text-red-400">
            ⚠️
          </div>
          <div>
            <h3 className="text-sm font-bold font-mono text-white">Emergency WhatsApp SOS Incident Dispatch</h3>
            <p className="text-xs text-slate-400">Automated Guardian notification to family member</p>
          </div>
        </div>

        {alerts.length > 0 ? (
          <div className="bg-[#0b141a] rounded-xl p-4 border border-[#202c33] text-sm text-[#e9edef] font-mono shadow-inner mb-4 space-y-2 whitespace-pre-line text-xs">
            {alerts[0].whatsapp_message}
          </div>
        ) : (
          <p className="text-xs text-slate-400 font-mono mb-4">No critical incidents dispatched yet.</p>
        )}

        <div className="flex gap-2">
          <button
            onClick={() => alert("Simulating outbound call to family member...")}
            className="flex-1 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-mono font-bold transition"
          >
            Call Family Guardian Immediately
          </button>
          <button onClick={onClose} className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono">
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
