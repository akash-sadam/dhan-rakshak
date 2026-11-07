"""FastAPI entrypoint and WebSocket streaming controller for Dhan-Rakshak.
Coordinates Gnani Prisma STT, Evon 30B MoE semantic reasoning, Timbre TTS synthesis,
and real-time Guardian HUD telemetry.
"""

import asyncio
from datetime import datetime
import json
import logging
import os
import time
from typing import Dict, Any, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.app.config import settings
from backend.app.schemas.fraud_schema import (
    ThreatAssessment,
    TranscriptChunk,
    EmergencyAlert,
    STTInferenceRequest,
    STTInferenceResponse,
    TTSInferenceRequest,
    TTSInferenceResponse
)
from backend.app.services.heuristic_filter import heuristic_filter
from backend.app.services.gnani_evon import evon_engine
from backend.app.services.gnani_prisma import prisma_client, RollingUtteranceBuffer
from backend.app.services.gnani_timbre import timbre_client
from backend.app.services.scenarios import SCENARIOS_DATA, get_scenario_by_id
from backend.app.utils.emergency_dispatcher import emergency_dispatcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("dhan_rakshak.main")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sovereign Indic Voice Scam Interceptor & Senior Co-Pilot powered by Gnani.ai"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount samples directory
samples_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "public", "samples")
if os.path.exists(samples_dir):
    app.mount("/samples", StaticFiles(directory=samples_dir), name="samples")

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "gnani_endpoints": {
            "prisma_stt": settings.PRISMA_STT_URL,
            "evon_moe": settings.EVON_BASE_URL,
            "timbre_tts": settings.TIMBRE_TTS_URL
        },
        "mode": "Live Hybrid / Sovereign MoE Ready",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/scenarios")
async def list_scenarios():
    return SCENARIOS_DATA


@app.get("/api/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    return get_scenario_by_id(scenario_id)


@app.post("/api/analyze", response_model=ThreatAssessment)
async def analyze_transcript_endpoint(payload: Dict[str, str]):
    text = payload.get("transcript", "")
    if not text:
        raise HTTPException(status_code=400, detail="Transcript is required")
    assessment = await evon_engine.analyze_transcript(text)
    return assessment


@app.post("/api/stt", response_model=STTInferenceResponse)
async def stt_endpoint(req: STTInferenceRequest):
    import base64
    audio_bytes = base64.b64decode(req.audio_data)
    result = await prisma_client.transcribe_audio_chunk(
        audio_bytes=audio_bytes,
        language_code=req.language_code,
        sampling_rate=req.sampling_rate
    )
    return result


@app.post("/api/tts", response_model=TTSInferenceResponse)
async def tts_endpoint(req: TTSInferenceRequest):
    result = await timbre_client.synthesize_speech(
        text=req.text,
        language_code=req.language_code,
        voice_id=req.voice_id,
        speed=req.speed,
        whisper_mode="<whispers>" in req.text.lower()
    )
    return result


@app.get("/api/sos/recent", response_model=List[EmergencyAlert])
async def get_recent_sos_alerts():
    return emergency_dispatcher.get_recent_alerts()


@app.post("/api/sos/trigger", response_model=EmergencyAlert)
async def manual_trigger_sos(payload: Dict[str, Any]):
    scenario_id = payload.get("scenario_id", "digital_arrest")
    text = payload.get("transcript", "Sunye, Maharashtra Police Cyber Cell se bol rahe hain. Arrest warrant issue hua hai.")
    assessment = await evon_engine.analyze_transcript(text)
    alert = await emergency_dispatcher.trigger_emergency_sos(assessment, text)
    return alert


@app.websocket("/ws/stream-call")
async def websocket_call_stream(websocket: WebSocket):
    """Real-time bi-directional streaming for Guardian HUD."""
    await websocket.accept()
    buffer = RollingUtteranceBuffer(max_words=30)
    current_scenario_task = None
    logger.info("Guardian HUD WebSocket connected.")

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            msg_type = data.get("type")

            if msg_type == "START_SCENARIO":
                scenario_id = data.get("scenario_id", "digital_arrest")
                scenario = get_scenario_by_id(scenario_id)
                buffer.clear()

                # Cancel running scenario simulation task if any
                if current_scenario_task and not current_scenario_task.done():
                    current_scenario_task.cancel()

                await websocket.send_json({
                    "type": "CALL_STATUS",
                    "status": "ACTIVE_CALL",
                    "scenario": scenario.model_dump()
                })

                # Stream dialogue turns asynchronously
                current_scenario_task = asyncio.create_task(
                    _simulate_scenario_stream(websocket, scenario, buffer)
                )

            elif msg_type == "MANUAL_UTTERANCE":
                speaker = data.get("speaker", "caller")
                text = data.get("text", "")
                chunk = TranscriptChunk(
                    speaker=speaker,
                    text=text,
                    timestamp=time.time(),
                    language=data.get("language", "te-IN")
                )
                buffer.add_chunk(chunk)
                await websocket.send_json({
                    "type": "TRANSCRIPT_CHUNK",
                    "chunk": chunk.model_dump()
                })
                # Re-evaluate
                rolling_context = buffer.get_full_transcript_text()
                assessment = await evon_engine.analyze_transcript(rolling_context)
                await websocket.send_json({
                    "type": "THREAT_ASSESSMENT",
                    "assessment": assessment.model_dump()
                })

            elif msg_type == "TRIGGER_WHISPER":
                # Synthesize Telugu calming earbud whisper (Male voice - Prakash)
                text = data.get("text", "Nana, idi fake call. Dabbu pampoddu. Ventane call cut cheyandi.")
                tts_res = await timbre_client.synthesize_speech(
                    text=text,
                    language_code="te-IN",
                    voice_id="te-male-calm",
                    speed=1.0,
                    whisper_mode=True
                )
                await websocket.send_json({
                    "type": "WHISPER_AUDIO_READY",
                    "audio_base64": tts_res.audio_base64,
                    "text": text,
                    "channel": "earbud_whisper"
                })

            elif msg_type == "TRIGGER_INTERCEPT":
                # Synthesize authoritative speaker intercept
                text = data.get("text", "Yeh call Cyber Crime Branch ki nigrani mein hai. Aapka number trace ho chuka hai, call turant disconnect karein.")
                tts_res = await timbre_client.synthesize_speech(
                    text=text,
                    language_code="hi-IN",
                    voice_id="hi-male-authoritative",
                    speed=1.05,
                    whisper_mode=False
                )
                await websocket.send_json({
                    "type": "INTERCEPTOR_AUDIO_READY",
                    "audio_base64": tts_res.audio_base64,
                    "text": text,
                    "channel": "speaker_interceptor"
                })

            elif msg_type == "RESET_CALL":
                if current_scenario_task and not current_scenario_task.done():
                    current_scenario_task.cancel()
                buffer.clear()
                await websocket.send_json({
                    "type": "CALL_STATUS",
                    "status": "STANDBY"
                })

    except WebSocketDisconnect:
        logger.info("Guardian HUD WebSocket disconnected.")
        if current_scenario_task and not current_scenario_task.done():
            current_scenario_task.cancel()
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if current_scenario_task and not current_scenario_task.done():
            current_scenario_task.cancel()


async def _simulate_scenario_stream(websocket: WebSocket, scenario, buffer: RollingUtteranceBuffer):
    """Simulates realistic timing, acoustic recognition, and progressive threat escalation."""
    sos_dispatched = False

    for i, turn in enumerate(scenario.dialogue):
        await asyncio.sleep(2.0 if i > 0 else 1.0)

        chunk = TranscriptChunk(
            speaker=turn.speaker,
            text=turn.text,
            timestamp=turn.time_offset,
            language=turn.language
        )
        buffer.add_chunk(chunk)

        # 1. Send Transcript Chunk
        await websocket.send_json({
            "type": "TRANSCRIPT_CHUNK",
            "chunk": chunk.model_dump()
        })

        # 2. Fast Heuristic Pre-filter check (<20ms)
        h_res = heuristic_filter.scan_transcript(turn.text)
        await websocket.send_json({
            "type": "HEURISTIC_PREVIEW",
            "data": h_res
        })

        # 3. Evon 30B MoE Reasoning (Full Context)
        rolling_context = buffer.get_full_transcript_text()
        assessment = await evon_engine.analyze_transcript(rolling_context)

        await websocket.send_json({
            "type": "THREAT_ASSESSMENT",
            "assessment": assessment.model_dump()
        })

        # 4. If Threat Score >= 75 and SOS not yet sent, trigger emergency dispatch
        if assessment.threat_score >= 75 and not sos_dispatched:
            sos_dispatched = True
            alert = await emergency_dispatcher.trigger_emergency_sos(
                assessment=assessment,
                transcript_snippet=rolling_context
            )
            await websocket.send_json({
                "type": "SOS_DISPATCHED",
                "alert": alert.model_dump()
            })

            # Broadcast pre-prepared scenario intervention texts
            await websocket.send_json({
                "type": "AUTO_INTERVENTIONS_PREPARED",
                "whisper_audio": None,
                "whisper_text": assessment.victim_whisper_telugu,
                "interceptor_audio": None,
                "interceptor_text": assessment.interceptor_response_hindi
            })

    await asyncio.sleep(1.0)
    await websocket.send_json({
        "type": "SCENARIO_COMPLETE"
    })


# Fallback / Direct root serving for HTML Guardian HUD
@app.get("/")
async def serve_index():
    index_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "public", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Dhan-Rakshak API Active", "version": settings.VERSION})
