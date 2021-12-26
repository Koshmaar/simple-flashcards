from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass 
class Flashcard:
    question: str
    answer: str
    id: int
    category: str = ""


@dataclass 
class Params:
    sequential: bool = False  # if false, is random
    ignored_categories: List[str] = field(default_factory=lambda: [])
    avoid_asked: bool = True
    filename: str = ''


@dataclass
class Session:
    # both store ids of Flashcards; can't use List[int] because deserialize_dataclass complains
    asked: list = field(default_factory=lambda: [])
    problematic: list = field(default_factory=lambda: [])
    next_flashcard: int = 0
    covered: int = 0




# class Program:

#     def __init__(self):
#         self.covered = 0
#         self.params = Params()

#     def get_next_flashcard(self) -> Flashcard:
#         pass

#     def display_flashcard(self):
#         pass

