from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

def _to_int(val: str | None, default: int) -> int:
    try:
        return int(val) if val else default
    except Exception:
        return default

@dataclass
class Settings:
    voice_enabled: bool = False
    locale: str = os.getenv("VA_LOCALE", "en_ZA")
    notes_file: str = os.getenv("VA_NOTES_FILE", "notes.txt")
    # Voice
    model_path: str = os.getenv("VA_MODEL_PATH", "")
    stt_seconds: int = _to_int(os.getenv("VA_STT_SECONDS"), 4)
    input_device: str | None = os.getenv("VA_INPUT_DEVICE") or None
    tts_rate: int = _to_int(os.getenv("VA_TTS_RATE"), 200)
    tts_voice: str | None = os.getenv("VA_TTS_VOICE") or None
    # APIs
    openweather_key: str | None = os.getenv("VA_OPENWEATHER_KEY") or None
    wiki_lang: str = os.getenv("VA_WIKI_LANG", "en")

def get_settings() -> Settings:
    return Settings()
