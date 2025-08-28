#!/usr/bin/env python3
"""
HexSoftwares Voice Assistant Demo
This script demonstrates the voice assistant capabilities
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from voice_assistant.utils.router import Router
from voice_assistant.utils.config import get_settings
from voice_assistant.skills.time_skill import TimeSkill
from voice_assistant.skills.notes_skill import NotesSkill
from voice_assistant.skills.apps_skill import AppsSkill
from voice_assistant.skills.joke_skill import JokeSkill
from voice_assistant.skills.calc_skill import CalcSkill
from voice_assistant.skills.wikipedia_skill import WikipediaSkill
from voice_assistant.skills.weather_skill import WeatherSkill
from voice_assistant.skills.system_skill import SystemSkill
from voice_assistant.skills.ai_chat_skill import AIChatSkill

def demo():
    print("🎤 HexSoftwares Voice Assistant Demo")
    print("=" * 50)
    
    # Initialize router
    settings = get_settings()
    router = Router([
        TimeSkill(settings.locale),
        NotesSkill(),
        AppsSkill(),
        JokeSkill(),
        CalcSkill(),
        WikipediaSkill(),
        WeatherSkill(),
        SystemSkill(),
        AIChatSkill(),
    ])
    
    # Demo commands
    demo_commands = [
        "time",
        "date", 
        "calc 2*(3+4)**2",
        "calc 15/3 + 7*2",
        "calc sqrt(16) + 5**2",
        "joke",
        "note This is a demo note for HexSoftwares",
        "note Meeting with team at 3 PM tomorrow",
        "wiki Python programming",
        "weather London",
        "system info",
        "system cpu",
        "system memory",
        "chat hello",
        "chat what can you do",
        "help"
    ]
    
    for command in demo_commands:
        print(f"\n👤 User: {command}")
        response = router.dispatch(command)
        print(f"🤖 Assistant: {response}")
        print("-" * 30)
    
    print("\n✨ Demo completed! Try the GUI with: python run_gui.py")

if __name__ == "__main__":
    demo()
