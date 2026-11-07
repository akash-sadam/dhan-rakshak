import os
import time
import httpx

api_key = "vach_1ytE2CY5X2PK656WfS6KgL5dunl23PZotqj1ZiwpyW4rpQvBrlPeTrrp0zx0jsaKMMXiAx3x4xoPeKEEq9mkVHf70syVsufh_b4dd3cd128d9491601be3b7b2a19ba04"
headers = {"X-API-Key-ID": api_key, "Content-Type": "application/json"}
out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "samples")

tasks = [
    ("interceptor_kyc_expiry.wav", "Avinash", "hi-IN", "Aapka banking phishing attempt detect ho chuka hai. RBI guidelines ke tahat yeh call flag kiya gaya hai.", False),
    ("whisper_benign_family.wav", "Prakash", "te-IN", "Idhi safe call Nana, meeru prashantam ga matladachu.", True),
    ("interceptor_benign_family.wav", "Avinash", "hi-IN", "No intervention required. Call verified as benign family communication.", False),
]

for filename, voice, lang, text, is_whisper in tasks:
    time.sleep(2.5)  # Avoid rate limiting
    formatted_text = f"<whispers> {text} </whispers>" if is_whisper else text
    payload = {
        "model": "timbre-v3.0",
        "voice": voice,
        "text": formatted_text,
        "language_code": lang,
        "speed": 1.0 if is_whisper else 1.05,
        "audio_config": {"container": "wav"}
    }
    try:
        r = httpx.post("https://api.vachana.ai/api/v1/tts/inference", headers=headers, json=payload, timeout=25.0)
        out_path = os.path.join(out_dir, filename)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(out_path, "wb") as f:
                f.write(r.content)
            print(f"Generated Live {filename}: {len(r.content)} bytes (Status 200 OK)")
        else:
            print(f"Failed {filename}: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error {filename}: {e}")
