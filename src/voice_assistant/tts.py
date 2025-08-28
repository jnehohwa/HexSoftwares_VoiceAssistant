from __future__ import annotations
import sys

try:
    import pyttsx3  # type: ignore
except Exception:
    pyttsx3 = None  # fallback to print

from .utils.config import get_settings

_settings = get_settings()
_engine = None

def _init_engine():
    global _engine
    if pyttsx3 is None:
        return None
    if _engine is None:
        _engine = pyttsx3.init()
        try:
            _engine.setProperty("rate", _settings.tts_rate)
            if _settings.tts_voice:
                for v in _engine.getProperty("voices"):
                    if _settings.tts_voice.lower() in (v.name or "").lower():
                        _engine.setProperty("voice", v.id)
                        break
        except Exception:
            pass
    return _engine

def speak(text: str):
    """Speak and print the text. If TTS engine not available, just print."""
    print(text)
    eng = _init_engine()
    if eng:
        try:
            eng.say(text)
            eng.runAndWait()
        except Exception:
            # silent fail to console-only
            pass
