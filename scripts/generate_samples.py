"""Generate synthetic PCM WAV audio files for Dhan-Rakshak demo and testing scenarios.
Produces telephony-bandpassed modulated audio representing caller and senior dialogues.
"""

import math
import os
import struct
import wave


def generate_scenario_wav(filename: str, duration_sec: float = 6.0, sample_rate: int = 16000, voice_type: str = "caller"):
    num_samples = int(duration_sec * sample_rate)
    wav_file = wave.open(filename, 'w')
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(sample_rate)

    # Base frequencies depending on voice type
    if voice_type == "caller":
        f0 = 140.0  # Male intimidating caller
        formants = [500, 1500, 2500]
    elif voice_type == "senior":
        f0 = 110.0  # Elderly male
        formants = [600, 1700, 2400]
    elif voice_type == "whisper":
        f0 = 220.0  # Female calming whisper (breath-heavy)
        formants = [400, 2000, 3200]
    else:  # Interceptor
        f0 = 160.0  # Authoritative male
        formants = [500, 1400, 2600]

    raw_data = bytearray()

    for i in range(num_samples):
        t = i / sample_rate
        # Syllabic envelope modulation (approx 3.5 syllables per sec)
        envelope = 0.5 + 0.45 * math.sin(2 * math.pi * 3.5 * t)
        
        # Periodic speech pulse
        signal = 0.0
        for harm in range(1, 10):
            freq = f0 * harm
            # Formant shaping
            gain = 0.0
            for form in formants:
                bw = 150.0
                gain += math.exp(-((freq - form) ** 2) / (2 * (bw ** 2)))
            signal += gain * math.sin(2 * math.pi * freq * t)

        # Subtle noise to simulate telephony line (bandpassed)
        noise = (math.sin(i * 12345.67) % 1.0) * 0.05
        
        # Whisper mode: higher noise, lower pitch resonance
        if voice_type == "whisper":
            sample_val = (signal * 0.2 + noise * 0.3) * envelope * 0.6
        else:
            sample_val = (signal * 0.7 + noise * 0.1) * envelope * 0.7

        # Clamp sample to 16-bit signed integer
        int_val = int(max(-32767, min(32767, sample_val * 32767)))
        raw_data.extend(struct.pack('<h', int_val))

    wav_file.writeframes(raw_data)
    wav_file.close()
    print(f"Generated: {filename} ({duration_sec}s @ {sample_rate}Hz)")


def main():
    target_dir = os.path.join("frontend", "public", "samples")
    os.makedirs(target_dir, exist_ok=True)

    scenarios = [
        ("scenario_digital_arrest.wav", 8.0, 16000, "caller"),
        ("scenario_power_cut.wav", 6.5, 16000, "caller"),
        ("scenario_kyc_expiry.wav", 7.0, 16000, "caller"),
        ("scenario_benign_family.wav", 6.0, 16000, "senior"),
        ("whisper_telugu_sample.wav", 3.5, 24000, "whisper"),
        ("interceptor_hindi_sample.wav", 4.0, 24000, "interceptor"),
    ]

    for fname, dur, sr, vtype in scenarios:
        out_path = os.path.join(target_dir, fname)
        generate_scenario_wav(out_path, dur, sr, vtype)

    print("\nAll sample WAV files successfully generated!")


if __name__ == "__main__":
    main()
