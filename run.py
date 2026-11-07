"""Dhan-Rakshak (ధన రక్షక్ / धन रक्षक) — Application Entrypoint.
Starts the FastAPI server with Guardian HUD and real-time streaming pipeline.
"""

import os
import sys

# Ensure UTF-8 output encoding for Windows command line
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 75)
    print("  DHAN-RAKSHAK (Dhan-Rakshak / Indic Voice Scam Interceptor)")
    print("  Sovereign Indic Voice Scam Interceptor & Senior Co-Pilot")
    print("  The Great Indian AI Internship Challenge - Gnani.ai")
    print("=" * 75)
    print("  * Guardian HUD UI:     http://localhost:8000")
    print("  * OpenAPI Docs:        http://localhost:8000/docs")
    print("  * Streaming WebSocket: ws://localhost:8000/ws/stream-call")
    print("=" * 75)

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
