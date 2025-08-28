import argparse
from .stt import listen_once
from .tts import speak
from .utils.router import Router
from .utils.config import get_settings
from .skills.time_skill import TimeSkill
from .skills.notes_skill import NotesSkill
from .skills.apps_skill import AppsSkill
from .skills.joke_skill import JokeSkill
from .skills.calc_skill import CalcSkill
from .skills.wikipedia_skill import WikipediaSkill
from .skills.weather_skill import WeatherSkill
from .skills.system_skill import SystemSkill
from .skills.ai_chat_skill import AIChatSkill

def build_router():
    settings = get_settings()
    return Router([
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

def main():
    parser = argparse.ArgumentParser(description="HexSoftwares Voice Assistant")
    parser.add_argument("--voice", action="store_true", help="Use voice I/O (requires extras)")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    args = parser.parse_args()

    if args.gui:
        try:
            from .gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Install customtkinter: pip install customtkinter")
            return
    else:
        router = build_router()
        print("HexSoftwares Voice Assistant. Type 'help' for commands, 'exit' to quit.")
        while True:
            try:
                text = listen_once() if args.voice else input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break
            if not text:
                continue
            lower = text.lower()
            if lower in {"exit", "quit"}:
                print("Bye.")
                break
            if lower == "help":
                print(router.help())
                continue
            reply = router.dispatch(text)
            speak(reply) if args.voice else print(reply)

if __name__ == "__main__":
    main()
