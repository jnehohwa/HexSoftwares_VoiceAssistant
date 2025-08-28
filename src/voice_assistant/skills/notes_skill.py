from .base import Skill
from ..utils.config import get_settings

class NotesSkill(Skill):
    def __init__(self):
        self.settings = get_settings()

    def names(self):
        return ["note", "notes"]

    def handle(self, cmd: str, args: str) -> str:
        if not args:
            return "Usage: note <text>"
        with open(self.settings.notes_file, "a", encoding="utf-8") as f:
            f.write(args.strip() + "\n")
        return "Noted."
