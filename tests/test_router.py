from src.voice_assistant.utils.router import Router
from src.voice_assistant.skills.time_skill import TimeSkill
from src.voice_assistant.skills.notes_skill import NotesSkill
from src.voice_assistant.skills.apps_skill import AppsSkill
from src.voice_assistant.skills.joke_skill import JokeSkill
from src.voice_assistant.skills.calc_skill import CalcSkill

def make_router():
    return Router([TimeSkill(), NotesSkill(), AppsSkill(), JokeSkill(), CalcSkill()])

def test_unknown():
    r = make_router()
    assert "Unknown" in r.dispatch("foobar")

def test_calc():
    r = make_router()
    assert r.dispatch("calc 2+2") == "4"

def test_help():
    r = make_router()
    help_text = r.help()
    assert "calc" in help_text and "time" in help_text and "date" in help_text
