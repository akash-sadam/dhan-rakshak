"""Automated integration tests for Dhan-Rakshak fraud detection scenarios.
Validates the Fast-Path Heuristic Filter, Evon 30B MoE Reasoning Engine,
and Timbre Expressive Synthesis against benchmark call transcripts.
Uses standard library unittest.IsolatedAsyncioTestCase for zero external test dependencies.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.services.heuristic_filter import heuristic_filter
from backend.app.services.gnani_evon import evon_engine
from backend.app.services.gnani_timbre import timbre_client


class TestDhanRakshakScenarios(unittest.IsolatedAsyncioTestCase):

    async def test_digital_arrest_scenario(self):
        """Test 1: Digital Arrest / CBI Extortion detection."""
        transcript = (
            "Main Maharashtra Police Cyber Cell se Inspector Shinde bol raha hoon. "
            "Aapke naam pe illegal narcotics parcel mila hai Mumbai airport par. "
            "Turant Skype video call pe aaiye aur ₹50,000 security verification fee jama kijiye warna warrant nikal raha hai."
        )

        # 1. Heuristic Pre-filter check (<20ms)
        h_res = heuristic_filter.scan_transcript(transcript)
        self.assertTrue(h_res["flagged"])
        self.assertEqual(h_res["top_scheme"], "DIGITAL_ARREST")
        self.assertLess(h_res["latency_ms"], 25.0)

        # 2. Evon 30B MoE Deep Reasoning
        assessment = await evon_engine.analyze_transcript(transcript)
        self.assertGreaterEqual(assessment.threat_score, 90)
        self.assertEqual(assessment.detected_scheme, "DIGITAL_ARREST")
        self.assertEqual(assessment.coercion_level, "CRITICAL")
        self.assertIsNotNone(assessment.extracted_entities.impersonated_agency)
        self.assertTrue(
            "₹50000" in assessment.extracted_entities.amount_demanded or 
            "₹50,000" in assessment.extracted_entities.amount_demanded
        )
        self.assertTrue(
            "fake call" in assessment.victim_whisper_telugu.lower() or 
            "cyber arrest" in assessment.victim_whisper_telugu.lower()
        )

    async def test_power_cut_scenario(self):
        """Test 2: Electricity disconnection fraud detection."""
        transcript = (
            "Dear consumer, aapka TSSPDCL current bill update nahi hua hai. "
            "Aaj raat 9:30 baje aapka meter connection permanently cut ho jayega. "
            "Turant iss official link meeda ₹1,450 payment cheyandi warna line cut chestaru."
        )

        h_res = heuristic_filter.scan_transcript(transcript)
        self.assertTrue(h_res["flagged"])
        self.assertEqual(h_res["top_scheme"], "UTILITY_CUT")

        assessment = await evon_engine.analyze_transcript(transcript)
        self.assertGreaterEqual(assessment.threat_score, 85)
        self.assertEqual(assessment.detected_scheme, "UTILITY_CUT")
        self.assertTrue(
            "₹1450" in assessment.extracted_entities.amount_demanded or 
            "₹1,450" in assessment.extracted_entities.amount_demanded
        )
        self.assertTrue(
            "fake" in assessment.victim_whisper_telugu.lower() or 
            "electricity" in assessment.victim_whisper_telugu.lower()
        )

    async def test_kyc_expiry_scenario(self):
        """Test 3: Urgent Bank KYC & remote APK fraud."""
        transcript = (
            "Attention! SBI customer care se bol rahe hain. "
            "Aapka bank account KYC update expire ho gaya hai, aaj freeze ho jayega. "
            "Turant verification APK install kijiye aur phone pe aaya OTP share kijiye."
        )

        h_res = heuristic_filter.scan_transcript(transcript)
        self.assertTrue(h_res["flagged"])
        self.assertEqual(h_res["top_scheme"], "KYC_EXPIRY")

        assessment = await evon_engine.analyze_transcript(transcript)
        self.assertGreaterEqual(assessment.threat_score, 80)
        self.assertEqual(assessment.detected_scheme, "KYC_EXPIRY")
        self.assertTrue(
            "otp" in assessment.victim_whisper_telugu.lower() or 
            "app" in assessment.victim_whisper_telugu.lower()
        )

    async def test_benign_family_scenario(self):
        """Test 4: Benign family call (False-Positive Prevention Check)."""
        transcript = (
            "Namaskaram Thatha garu! Ela vunnaru? Blood pressure tablets tinnara? "
            "Weekend pandaga ki intiki vasthunnava Divya thalli? Avunu Saturday sweets thestha."
        )

        h_res = heuristic_filter.scan_transcript(transcript)
        self.assertFalse(h_res["flagged"])
        self.assertEqual(h_res["top_scheme"], "BENIGN")

        assessment = await evon_engine.analyze_transcript(transcript)
        self.assertLessEqual(assessment.threat_score, 15)
        self.assertEqual(assessment.detected_scheme, "BENIGN")
        self.assertEqual(assessment.coercion_level, "LOW")

    async def test_timbre_synthesis_tags(self):
        """Test 5: Timbre Expressive Synthesis with <whispers> tag formatting."""
        res = await timbre_client.synthesize_speech(
            text="Nana idi fake call, dabbu pampoddu.",
            language_code="te-IN",
            whisper_mode=True
        )
        self.assertIsNotNone(res.audio_base64)
        self.assertGreater(len(res.audio_base64), 100)
        self.assertGreater(res.duration_sec, 1.0)


if __name__ == "__main__":
    unittest.main()
