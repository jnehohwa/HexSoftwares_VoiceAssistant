from typing import Dict, List
from ..skills.base import Skill

class Router:
    def __init__(self, skills: List[Skill]):
        self._skills: Dict[str, Skill] = {}
        for s in skills:
            for name in s.names():
                self._skills[name.lower()] = s

    def dispatch(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return "Say something (try 'time', 'date', 'joke', 'calc 1+1')."
        head, *tail = text.split()
        cmd = head.lower()
        args = " ".join(tail)
        
        # Handle help command
        if cmd == "help":
            return self.help()
        
        skill = self._skills.get(cmd)
        if not skill:
            return f"Unknown command: {cmd}"
        try:
            return skill.handle(cmd, args)
        except Exception as e:
            return f"Error: {e}"

    def help(self) -> str:
        cmds = sorted(set(name for name in self._skills.keys()))
        return "Available: " + ", ".join(cmds)
