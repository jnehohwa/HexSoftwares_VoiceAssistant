from .base import Skill
from ..utils.config import get_settings

class WeatherSkill(Skill):
    def __init__(self):
        self.settings = get_settings()
        try:
            import requests  # type: ignore
            self._requests = requests
        except Exception:
            self._requests = None

    def names(self):
        return ["weather", "met"]

    def handle(self, cmd: str, args: str) -> str:
        if not args:
            return "Usage: weather <city>"
        if not self._requests:
            return "Requests module not available. Install 'requests'."
        if not self.settings.openweather_key:
            return "OpenWeather API key missing. Set VA_OPENWEATHER_KEY in .env."

        city = args.strip()
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.settings.openweather_key,
            "units": "metric",
        }
        try:
            resp = self._requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                return f"Weather error: {resp.status_code} {resp.text[:120]}"
            data = resp.json()
            desc = (data.get("weather", [{}])[0].get("description") or "").title()
            temp = data.get("main", {}).get("temp")
            hum = data.get("main", {}).get("humidity")
            wind = data.get("wind", {}).get("speed")
            name = data.get("name") or city
            return f"{name}: {desc}, {temp}°C, humidity {hum}%, wind {wind} m/s"
        except Exception as ex:
            return f"Weather error: {ex}"
