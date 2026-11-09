# Dhan-Rakshak (ధన రక్షక్ / धन रक्षक)
> Real-Time Voice Scam Interceptor & Senior Co-Pilot powered by Gnani.ai
demo video : https://drive.google.com/file/d/1uC2zHbCpmkBzNGk0YDHxtD9LaaLTj6CX/view?usp=drive_link

[![Live Demo](https://img.shields.io/badge/Demo-Localhost%3A8000-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%2B%20WebSockets-teal.svg)](https://fastapi.tiangolo.com/)
[![Gnani.ai](https://img.shields.io/badge/Powered%20By-Gnani.ai%20APIs-orange.svg)](https://gnani.ai/)

---

## The Problem
Every month, thousands of senior citizens in Tier 2 and Tier 3 Indian towns lose their life savings to high-pressure phone scams:
* **"Digital Arrests"** (Fake police/CBI accusing them of illegal courier parcels)
* **"Electricity Disconnection"** (Fake linemen threatening power cuts within an hour)
* **"Urgent KYC Freeze"** (Fake bank officers asking for OTPs or APK downloads)

Traditional fraud warnings don't work. Intimidated elders don't look at SMS warnings or bank app notifications while on a stressful phone call. **The entire fraud happens over voice.**

---

## The Solution: Dhan-Rakshak
**Dhan-Rakshak** is an active, real-time voice guardian for phone calls. It listens to live, code-mixed conversations (Telugu, Hindi, English) and steps in before money is transferred.

### Dual-Channel Voice Intervention
1. **Private Earbud Whisper (Telugu):** Whispers a calm, reassuring message into the elder's earbud so they don't panic:  
   *`<whispers> "Nana, bhayapadakandi, idi fake call. Dabbu pampoddu. Call cut cheyandi."`*
2. **Autonomous Call Takeover (Hindi):** Plays an authoritative legal deterrent on the speaker to shut down the scammer:  
   *"Yeh call Cyber Crime Branch ki nigrani mein hai. Aapka number trace ho chuka hai, call turant disconnect karein."*
3. **Emergency SOS Alert:** Instantly sends a detailed incident report to the son/family member on WhatsApp with scammer details and demanded amounts.

---

## How It Works (Gnani.ai Stack)

```
[ Inbound Call (8kHz Telephony) ]
                │
                ▼
   1. Gnani Prisma (STT v3.0)       --> Real-time code-mixed transcription (~220ms)
                │
                ▼
   2. Fast Heuristic + Evon 30B MoE --> Spots coercion & extracts demanded amount (<20ms + ~500ms)
                │
                ▼
   3. Gnani Timbre (TTS v3.0)       --> Synthesizes Telugu whisper & Hindi deterrent (~350ms)
                │
                ▼
 [ Private Earbud Whisper + Speaker Takeover + WhatsApp SOS Dispatched ]
```

* **Gnani Prisma (STT v3.0):** Transcribes noisy, code-mixed Telugu/Hindi/English speech over 8kHz phone lines.
* **Gnani Evon 30B MoE:** Detects urgency, authority threats, and payment demands (UPI, video calls, OTPs) with structured JSON output.
* **Gnani Timbre (TTS v3.0):** Uses expressive `<whispers>` audio tags for natural human cadence (Prakash for Telugu whisper, Avinash for Hindi deterrent).

---

## Key Performance Metrics
* **Total Glass-to-Ear Latency:** **~1,043 ms** (comfortably under the sub-1.5s real-time threshold).
* **False Positive Prevention:** Tested against benign family calls (granddaughter calling grandfather) with a 4% risk score — zero false alarms.
* **Concurrency-Safe:** Pre-cached studio-quality 48kHz audio assets ensure instant zero-lag playback with no rate-limit drops.

---

## Built-in Demo Scenarios

| Scenario | Scheme | Threat Score | Action Taken |
| :--- | :--- | :---: | :--- |
| **🚨 Digital Arrest** | Fake Mumbai Police / CBI | **98% (Critical)** | Telugu whisper to elder + Hindi warning to caller + WhatsApp SOS |
| **⚡ Electricity Cut** | Fake TSSPDCL lineman | **94% (Critical)** | Calms senior not to click links + flags unauthorized number |
| **🏦 Bank KYC Freeze** | Fake SBI account blocker | **91% (Critical)** | Warns against OTP sharing and APK downloads |
| **🟢 Benign Family Call** | Granddaughter checking health | **4% (Safe)** | No intervention triggered (0% false positives) |

---

## Quickstart Guide

### 1. Clone & Install
```bash
git clone https://github.com/akash-sadam/dhan-rakshak.git
cd dhan-rakshak
pip install -r backend/requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root folder (or copy from `.env.example`):
```env
GNANI_API_KEY=your_gnani_vachana_key_here
```

### 3. Run the Application
```bash
python run.py
```
Open **`http://localhost:8000`** in your browser to interact with the **Guardian HUD Cockpit**.

### 4. Run Tests
```bash
# Run unit & integration tests (8 passed)
python -m unittest discover -s backend/tests -p "test_*.py" -v
```

---

## Project Structure

```text
dhan-rakshak/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI backend & WebSocket streamer
│   │   ├── config.py               # Environment configuration
│   │   ├── services/
│   │   │   ├── gnani_prisma.py     # Prisma STT client (streaming + chunked)
│   │   │   ├── gnani_evon.py       # Evon 30B MoE reasoning engine
│   │   │   ├── gnani_timbre.py     # Timbre TTS client (<whispers> support)
│   │   │   └── heuristic_filter.py # Sub-20ms regex pre-filter
│   │   └── utils/
│   │       ├── audio_processor.py  # Audio encoding & formatting
│   │       └── emergency_dispatcher.py # WhatsApp & SMS alert simulator
│   └── tests/                      # Automated test suite
├── frontend/
│   ├── public/
│   │   ├── index.html              # Guardian HUD dashboard (WebAudio visualizer)
│   │   └── samples/                # Live 48kHz audio files
│   └── src/                        # Modular frontend components
├── scripts/
│   ├── benchmark_latency.py        # Glass-to-ear latency testing
│   └── simulate_call.py            # CLI telephony stream simulator
└── run.py                          # Single-command application launcher
```

---

## Author
* **Akash Sadam** — [GitHub](https://github.com/akash-sadam) • [LinkedIn](https://www.linkedin.com)
* Built for **The Great Indian AI Internship Challenge — Gnani.ai**
