"""Test script verifying Gnani.ai API contract compliance and health checks."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.config import settings
from backend.app.services.gnani_prisma import prisma_client
from backend.app.services.gnani_timbre import timbre_client


class TestGnaniAPIContracts(unittest.IsolatedAsyncioTestCase):

    async def test_gnani_configuration(self):
        self.assertEqual(settings.GNANI_BASE_URL, "https://api.vachana.ai")
        self.assertEqual(settings.PRISMA_MODEL, "prisma-v3.0")
        self.assertEqual(settings.TIMBRE_MODEL, "timbre-v3.0")
        self.assertEqual(settings.EVON_MODEL, "evon-30b-moe")

    async def test_prisma_contract(self):
        res = await prisma_client.transcribe_audio_chunk(
            audio_bytes=b"dummy_bytes_12345",
            language_code="te-IN"
        )
        self.assertNotEqual(res.transcript, "")
        self.assertGreaterEqual(res.confidence, 0.90)
        self.assertTrue(res.is_final)

    async def test_timbre_contract(self):
        res = await timbre_client.synthesize_speech(
            text="Aapka call Cyber Defense dwara record ho raha hai.",
            language_code="hi-IN",
            voice_id="hi-male-authoritative"
        )
        self.assertNotEqual(res.audio_base64, "")
        self.assertEqual(res.audio_format, "wav")


if __name__ == "__main__":
    unittest.main()
