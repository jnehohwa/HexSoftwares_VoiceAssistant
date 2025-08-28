import subprocess, sys
from .base import Skill

class AppsSkill(Skill):
    def names(self):
        return ["open"]

    def handle(self, cmd: str, args: str) -> str:
        if not args:
            return "Usage: open <AppName> (e.g., open Safari)"
        if sys.platform == "darwin":
            try:
                subprocess.check_call(["open", "-a", args])
                return f"Opening {args}"
            except Exception:
                return f"Couldn't open app: {args}"
        return "Open app is currently supported on macOS only."
