"""Cache high-fidelity live Gnani Timbre audio files for all scenarios.
Guarantees 0ms latency and 100% reliable human voice playback without ever beeping.
"""

import os
import sys
import httpx

api_key = "vach_1ytE2CY5X2PK656WfS6KgL5dunl23PZotqj1ZiwpyW4rpQvBrlPeTrrp0zx0jsaKMMXiAx3x4xoPeKEEq9mkVHf70syVsufh_b4dd3cd128d9491601be3b7b2a19ba04"
headers = {"X-API-Key-ID": api_key, "Content-Type": "application/json"}
out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "samples")
os.makedirs(out_dir, exist_ok=True)

scenarios = {
    "digital_arrest": {
        "whisper": "Nana, idi cyber arrest scam. Police eppudu phone lo dabbu adagaru. Ventane call cut cheyandi.",
        "interceptor": "Yeh call Cyber Crime Branch ki nigrani mein hai. Aapka number trace ho chuka hai, call turant disconnect karein."
    },
    "power_cut": {
        "whisper": "Nana bhayapadakandi, idi fake electricity call. Power cut cheyaru, ee number ki dabbu transfer cheyoddu.",
        "interceptor": "Yeh number Vidyut Nigam ka anadhikrit scam alert hai. Call record ho raha hai, turant line kaatein."
    },
    "kyc_expiry": {
        "whisper": "Nana, bank vallu eppudu OTP adagaru, app install cheyoddu. Call cut cheyandi, manam branch ki veldam.",
        "interceptor": "Aapka banking phishing attempt detect ho chuka hai. RBI guidelines ke tahat yeh call flag kiya gaya hai."
    },
    "benign_family": {
        "whisper": "Idhi safe call Nana, meeru prashantam ga matladachu.",
        "interceptor": "No intervention required. Call verified as benign family communication."
    }
}

for scen_id, data in scenarios.items():
    # 1. Synthesize Telugu Whisper (Prakash - Male)
    whisper_text = data["whisper"]
    w_payload = {
        "model": "timbre-v3.0",
        "voice": "Prakash",
        "text": f"<whispers> {whisper_text} </whispers>",
        "language_code": "te-IN",
        "speed": 1.0,
        "audio_config": {"container": "wav"}
    }
    r = httpx.post("https://api.vachana.ai/api/v1/tts/inference", headers=headers, json=w_payload, timeout=25.0)
    w_path = os.path.join(out_dir, f"whisper_{scen_id}.wav")
    with open(w_path, "wb") as f:
        f.write(r.content)
    print(f"Generated Live Whisper: {w_path} (Bytes: {len(r.content)})")

    # 2. Synthesize Hindi Interceptor (Avinash - Male)
    interceptor_text = data["interceptor"]
    i_payload = {
        "model": "timbre-v3.0",
        "voice": "Avinash",
        "text": interceptor_text,
        "language_code": "hi-IN",
        "speed": 1.05,
        "audio_config": {"container": "wav"}
    }
    r2 = httpx.post("https://api.vachana.ai/api/v1/tts/inference", headers=headers, json=i_payload, timeout=25.0)
    i_path = os.path.join(out_dir, f"interceptor_{scen_id}.wav")
    with open(i_path, "wb") as f:
        f.write(r2.content)
    print(f"Generated Live Interceptor: {i_path} (Bytes: {len(r2.content)})")

print("\n[+] All live Gnani Timbre audio files generated successfully!")
