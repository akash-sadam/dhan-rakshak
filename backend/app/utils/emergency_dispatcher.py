"""Emergency SOS and Telemetry Dispatcher for Dhan-Rakshak.
Simulates instant WhatsApp and SMS incident dispatch to family members.
"""

from datetime import datetime
import logging
from typing import List, Optional
import uuid
import httpx

from backend.app.config import settings
from backend.app.schemas.fraud_schema import EmergencyAlert, ThreatAssessment

logger = logging.getLogger("dhan_rakshak.sos")


class EmergencyDispatcher:
    """Dispatches real-time SOS alerts to family guardians via WhatsApp & Webhooks."""

    def __init__(self):
        self.dispatched_alerts: List[EmergencyAlert] = []

    async def trigger_emergency_sos(
        self,
        assessment: ThreatAssessment,
        transcript_snippet: str,
        victim_name: str = "Grandfather (Suryanarayana)"
    ) -> EmergencyAlert:
        alert_id = f"SOS-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

        # Format WhatsApp message
        whatsapp_body = (
            f"🚨 *DHAN-RAKSHAK CRITICAL FRAUD INTERCEPTION* 🚨\n\n"
            f"👤 *Family Member:* {victim_name}\n"
            f"⚠️ *Threat Score:* {assessment.threat_score}% [{assessment.coercion_level}]\n"
            f"🎯 *Detected Scheme:* {assessment.detected_scheme.replace('_', ' ')}\n"
            f"🏢 *Impersonated Agency:* {assessment.extracted_entities.impersonated_agency or 'Unknown'}\n"
            f"💳 *Demand:* {assessment.extracted_entities.action_demanded or 'N/A'} ({assessment.extracted_entities.amount_demanded or 'Unspecified'})\n\n"
            f"🛡️ *Interventions Active:*\n"
            f"• *Earbud Whisper:* \"{assessment.victim_whisper_telugu}\"\n"
            f"• *Speaker Deterrent:* \"{assessment.interceptor_response_hindi}\"\n\n"
            f"🕒 *Timestamp:* {now_str}\n"
            f"📍 *Location:* Hyderabad, Telangana\n"
            f"Status: Scammer confrontation active. Please call your elder immediately if needed."
        )

        alert = EmergencyAlert(
            alert_id=alert_id,
            timestamp=now_str,
            victim_name=victim_name,
            emergency_contact=settings.EMERGENCY_CONTACT_NAME,
            phone_number=settings.EMERGENCY_CONTACT_PHONE,
            detected_scheme=assessment.detected_scheme,
            threat_score=assessment.threat_score,
            coercion_level=assessment.coercion_level,
            extracted_agency=assessment.extracted_entities.impersonated_agency,
            extracted_action=assessment.extracted_entities.action_demanded,
            extracted_amount=assessment.extracted_entities.amount_demanded,
            raw_transcript_snippet=transcript_snippet[-200:],
            whisper_delivered=assessment.victim_whisper_telugu,
            interceptor_delivered=assessment.interceptor_response_hindi,
            whatsapp_message=whatsapp_body,
            status="DISPATCHED"
        )

        self.dispatched_alerts.insert(0, alert)
        logger.info(f"Dispatched SOS Alert: {alert_id} for {victim_name} (Score: {assessment.threat_score}%)")

        # Optional external webhook post if configured
        if settings.EMERGENCY_WEBHOOK_URL:
            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    await client.post(settings.EMERGENCY_WEBHOOK_URL, json=alert.model_dump())
            except Exception as e:
                logger.error(f"Failed to post to emergency webhook: {e}")

        return alert

    def get_recent_alerts(self, limit: int = 10) -> List[EmergencyAlert]:
        return self.dispatched_alerts[:limit]


emergency_dispatcher = EmergencyDispatcher()
