from __future__ import annotations
import json
import sys
from .utils.config import get_settings

_settings = get_settings()

def _can_use_vosk():
    try:
        import vosk  # type: ignore
        import sounddevice as sd  # type: ignore
        return True
    except Exception:
        return False

def listen_once() -> str:
    """
    Try to capture a short utterance using Vosk.
    Falls back to keyboard input if models/libs are missing or any error occurs.
    """
    if not _can_use_vosk() or not _settings.model_path:
        # Text fallback
        return input("> ").strip()

    try:
        import vosk  # type: ignore
        import sounddevice as sd  # type: ignore
        import numpy as np  # type: ignore
        import os

        if not os.path.isdir(_settings.model_path):
            return input("> ").strip()

        model = vosk.Model(_settings.model_path)
        samplerate = 16000
        device = _settings.input_device

        # Prepare stream
        sd.default.samplerate = samplerate
        if device:
            try:
                sd.default.device = int(device) if device.isdigit() else device
            except Exception:
                pass

        rec = vosk.KaldiRecognizer(model, samplerate)
        duration = max(1, _settings.stt_seconds)

        print("🎙️ Speak now...")
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16", channels=1):
            frames = int(duration * samplerate / 8000)
            for _ in range(frames):
                data = sd.raw_input_stream.read(8000)[0]  # type: ignore[attr-defined]
                if rec.AcceptWaveform(data):
                    break
            # Final result
            try:
                res = json.loads(rec.FinalResult())
                text = (res.get("text") or "").strip()
                return text if text else ""
            except Exception:
                return ""
    except KeyboardInterrupt:
        return ""
    except Exception:
        # Any issue → fallback to text input
        return input("> ").strip()
