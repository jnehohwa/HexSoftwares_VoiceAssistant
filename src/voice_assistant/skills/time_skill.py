from datetime import datetime
from .base import Skill
import locale

class TimeSkill(Skill):
    def __init__(self, loc: str = "en_ZA"):
        try:
            locale.setlocale(locale.LC_TIME, loc)
        except Exception:
            pass

    def names(self):
        return ["time", "date"]

    def handle(self, cmd: str, args: str) -> str:
        now = datetime.now()
        if cmd == "date":
            return now.strftime("%A, %d %B %Y")
        return now.strftime("%H:%M")
