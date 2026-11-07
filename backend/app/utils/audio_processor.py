"""Audio processing utilities for Dhan-Rakshak.
Handles telephony 8kHz/16kHz resampling, noise injection, and PCM format conversions.
"""

import io
import math
import struct
import wave
from typing import Tuple


def add_telephony_noise(pcm_bytes: bytes, noise_level: float = 0.05) -> bytes:
    """Simulates 8kHz Indian telephony line noise, background chatter, and hiss."""
    samples = struct.unpack(f"<{len(pcm_bytes)//2}h", pcm_bytes)
    noisy_samples = []

    for i, s in enumerate(samples):
        # Pink/white noise hybrid
        noise = (math.sin(i * 37.1) + math.cos(i * 91.3)) * 0.5 * 32767 * noise_level
        new_val = int(max(-32768, min(32767, s + noise)))
        noisy_samples.append(new_val)

    return struct.pack(f"<{len(noisy_samples)}h", *noisy_samples)


def create_wav_header(pcm_data: bytes, sample_rate: int = 16000, channels: int = 1, bits_per_sample: int = 16) -> bytes:
    """Wraps raw PCM bytes in a standard RIFF/WAV header."""
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)
    data_size = len(pcm_data)
    total_size = 36 + data_size

    header = bytearray()
    header.extend(b'RIFF')
    header.extend(struct.pack('<I', total_size))
    header.extend(b'WAVEfmt ')
    header.extend(struct.pack('<I', 16))          # Subchunk1Size (16 for PCM)
    header.extend(struct.pack('<H', 1))           # AudioFormat (1 for PCM)
    header.extend(struct.pack('<H', channels))
    header.extend(struct.pack('<I', sample_rate))
    header.extend(struct.pack('<I', byte_rate))
    header.extend(struct.pack('<H', block_align))
    header.extend(struct.pack('<H', bits_per_sample))
    header.extend(b'data')
    header.extend(struct.pack('<I', data_size))

    return bytes(header) + pcm_data
