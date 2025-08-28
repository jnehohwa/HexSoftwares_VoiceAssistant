import random
from .base import Skill

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, it said: 'Going to sleep.'",
    "There are 10 kinds of people: those who understand binary and those who don't.",
]

class JokeSkill(Skill):
    def names(self):
        return ["joke", "funny"]

    def handle(self, cmd: str, args: str) -> str:
        return random.choice(JOKES)
