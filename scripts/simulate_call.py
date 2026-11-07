"""Interactive Telephony Call Simulator for Dhan-Rakshak.
Streams audio/transcript frames into the local or remote Dhan-Rakshak server
and prints real-time threat telemetry to the terminal.
"""

import asyncio
import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import websockets

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.app.services.scenarios import SCENARIOS_DATA


async def simulate_scenario(scenario_id: str = "digital_arrest", server_url: str = "ws://localhost:8000/ws/stream-call"):
    print("=" * 75)
    print(f"  LAUNCHING DHAN-RAKSHAK LIVE TELEPHONY SIMULATOR")
    print(f"  Scenario: {scenario_id.upper()}")
    print(f"  Server:   {server_url}")
    print("=" * 75)

    try:
        async with websockets.connect(server_url) as ws:
            print("[+] WebSocket connection established with Guardian HUD backend.")
            
            # Start scenario
            await ws.send(json.dumps({
                "type": "START_SCENARIO",
                "scenario_id": scenario_id
            }))
            print(f"[>] Scenario trigger dispatched: {scenario_id}\n")

            while True:
                msg_str = await ws.recv()
                msg = json.loads(msg_str)
                msg_type = msg.get("type")

                if msg_type == "TRANSCRIPT_CHUNK":
                    chunk = msg["chunk"]
                    speaker_tag = "[CALLER (8kHz)]" if chunk["speaker"] == "caller" else "[SENIOR (Mic)]"
                    print(f"\n{speaker_tag} (+{chunk['timestamp']}s): \"{chunk['text']}\"")

                elif msg_type == "HEURISTIC_PREVIEW":
                    h = msg.get("data", {})
                    if h.get("flagged"):
                        clues = ", ".join(h.get("detected_clues", []))
                        print(f"  ⚡ Fast Heuristic Flagged (<20ms): [{clues}] (Score: {h.get('preliminary_score')}%)")

                elif msg_type == "THREAT_ASSESSMENT":
                    a = msg["assessment"]
                    score = a["threat_score"]
                    print(f"  🧠 Evon 30B MoE Threat Score: {score}% [{a['coercion_level']}] - Scheme: {a['detected_scheme']}")
                    if a.get("extracted_entities"):
                        agency = a["extracted_entities"].get("impersonated_agency")
                        action = a["extracted_entities"].get("action_demanded")
                        amount = a["extracted_entities"].get("amount_demanded")
                        if agency or action or amount:
                            print(f"     Extracted: Agency='{agency}' | Action='{action}' | Demanded='{amount}'")

                elif msg_type == "SOS_DISPATCHED":
                    alert = msg["alert"]
                    print("\n" + "!" * 75)
                    print(f"  🚨 EMERGENCY SOS DISPATCHED TO FAMILY GUARDIAN: {alert['emergency_contact']}")
                    print(f"  Alert ID: {alert['alert_id']} | Status: {alert['status']}")
                    print("!" * 75)

                elif msg_type == "AUTO_INTERVENTIONS_PREPARED":
                    print(f"\n  🔊 [Timbre Whisper Mode (Telugu)]: \"{msg.get('whisper_text')}\"")
                    print(f"  🚨 [Timbre Speaker Interceptor (Hindi)]: \"{msg.get('interceptor_text')}\"\n")

                elif msg_type == "SCENARIO_COMPLETE":
                    print("\n[+] Call scenario simulation completed successfully.")
                    break

    except ConnectionRefusedError:
        print("[!] ERROR: Could not connect to Dhan-Rakshak server at ws://localhost:8000/ws/stream-call.")
        print("    Please run 'python run.py' in a separate terminal first.")
    except Exception as e:
        print(f"[!] Simulation interrupted: {e}")


def main():
    scenario = "digital_arrest"
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
    asyncio.run(simulate_scenario(scenario))


if __name__ == "__main__":
    main()
