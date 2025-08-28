from .base import Skill
from ..utils.config import get_settings

class WikipediaSkill(Skill):
    def __init__(self):
        self.settings = get_settings()
        try:
            import wikipedia  # type: ignore
            wikipedia.set_lang(self.settings.wiki_lang or "en")
            self._wikipedia = wikipedia
        except Exception:
            self._wikipedia = None

    def names(self):
        return ["wiki", "wikipedia"]

    def handle(self, cmd: str, args: str) -> str:
        if not args:
            return "Usage: wiki <search terms>"
        if not self._wikipedia:
            return "Wikipedia module not available. Install 'wikipedia'."

        try:
            # Try direct summary, else search then summary
            try:
                return self._wikipedia.summary(args, sentences=2)
            except self._wikipedia.DisambiguationError as e:
                choice = e.options[0] if e.options else None
                if not choice:
                    return "Too many results. Refine your query."
                return self._wikipedia.summary(choice, sentences=2)
            except self._wikipedia.PageError:
                results = self._wikipedia.search(args, results=1)
                if not results:
                    return "No results."
                return self._wikipedia.summary(results[0], sentences=2)
        except Exception as ex:
            return f"Wikipedia error: {ex}"
