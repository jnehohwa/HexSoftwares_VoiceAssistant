from abc import ABC, abstractmethod
from typing import List

class Skill(ABC):
    @abstractmethod
    def names(self) -> List[str]:
        ...

    @abstractmethod
    def handle(self, cmd: str, args: str) -> str:
        ...
