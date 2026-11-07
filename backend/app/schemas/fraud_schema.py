"""Data schemas and Pydantic models for Dhan-Rakshak."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ExtractedEntities(BaseModel):
    impersonated_agency: Optional[str] = Field(None, description="E.g. CBI, Maharashtra Police Cyber Cell, TSSPCL")
    action_demanded: Optional[str] = Field(None, description="E.g. Video call, UPI transfer, APK download")
    amount_demanded: Optional[str] = Field(None, description="E.g. ₹50,000, ₹1,200")


class ThreatAssessment(BaseModel):
    threat_score: int = Field(..., ge=0, le=100, description="Risk level 0-100")
    detected_scheme: Literal[
        "DIGITAL_ARREST",
        "UTILITY_CUT",
        "KYC_EXPIRY",
        "LOTTERY_REWARD",
        "BENIGN"
    ]
    coercion_level: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    extracted_entities: ExtractedEntities
    victim_whisper_telugu: str = Field(..., description="Short, calming guidance in Telugu for the senior")
    interceptor_response_hindi: str = Field(..., description="Authoritative legal deterrent in Hindi/English")
    urgency_clues: List[str] = Field(default_factory=list, description="Keywords or phrases showing coercive pressure")
    latency_breakdown_ms: Optional[dict] = Field(default_factory=dict)


class TranscriptChunk(BaseModel):
    speaker: Literal["caller", "senior", "interceptor", "whisper"]
    text: str
    timestamp: float
    confidence: float = 0.95
    is_final: bool = True
    language: str = "te-IN"


class ScenarioDialogueTurn(BaseModel):
    time_offset: float
    speaker: Literal["caller", "senior"]
    text: str
    language: str


class CallScenario(BaseModel):
    id: str
    name: str
    description: str
    scheme: str
    target_score: int
    audio_sample_url: str
    dialogue: List[ScenarioDialogueTurn]


class EmergencyAlert(BaseModel):
    alert_id: str
    timestamp: str
    victim_name: str
    emergency_contact: str
    phone_number: str
    detected_scheme: str
    threat_score: int
    coercion_level: str
    extracted_agency: Optional[str] = None
    extracted_action: Optional[str] = None
    extracted_amount: Optional[str] = None
    raw_transcript_snippet: str
    whisper_delivered: str
    interceptor_delivered: str
    whatsapp_message: str
    status: Literal["DISPATCHED", "DELIVERED", "ACKNOWLEDGED"] = "DISPATCHED"


class STTInferenceRequest(BaseModel):
    audio_data: str  # Base64 encoded audio chunk
    sampling_rate: int = 16000
    encoding: str = "LINEAR16"
    language_code: str = "te-IN"
    model_version: str = "prisma-v3.0"
    mode: str = "code_mix"
    enable_noise_suppression: bool = True


class STTInferenceResponse(BaseModel):
    transcript: str
    confidence: float
    language_detected: str
    is_final: bool


class TTSInferenceRequest(BaseModel):
    text: str
    language_code: str = "te-IN"
    voice_id: str = "te-female-calm"
    model_version: str = "timbre-v3.0"
    audio_format: str = "wav"
    sampling_rate: int = 24000
    speed: float = 1.0


class TTSInferenceResponse(BaseModel):
    audio_base64: str
    duration_sec: float
    audio_format: str
    model_version: str
