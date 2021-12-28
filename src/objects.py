from random import randrange
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field

# todo put classess in separate files, with their respective methods?

@dataclass 
class Flashcard:
    question: str = ""
    answer: str = ""
    id: int = 0
    category: str = ""
    domc: list = field(default_factory=lambda: [])


@dataclass 
class Params:
    sequential: bool = False  # if false, is random
    ignored_categories: List[str] = field(default_factory=lambda: [])
    avoid_asked: bool = True
    filename: str = ''
    quick_start: bool = False


@dataclass
class Session:
    # both store ids of Flashcards; can't use List[int] because deserialize_dataclass complains
    asked: list = field(default_factory=lambda: [])
    problematic: list = field(default_factory=lambda: [])
    next_flashcard: int = 0
    covered: int = 0


class Program:

    def __init__(self, session: Session, params: Params, flashcards: List[Flashcard]):
        self.session = session
        self.params = params
        self.flashcards = flashcards

    # Returns flashcard and bool whether it was problematic
    def get_next_flashcard(self) -> Tuple[Flashcard, bool]:
        if self.params.sequential:
            self.session.next_flashcard += 1
        else:
            for i in range(10):
                # random.randrange(stop)  -> [0, 1, 2, ..., stop-1]
                if len(self.session.problematic) > 2 and randrange(100) > 50:
                    print("Let's refresh sth...")
                    which = randrange(len(self.session.problematic))
                    self.session.next_flashcard = self.session.problematic[which]
                    flashcard = self.flashcards[self.session.next_flashcard]
                    return flashcard, True

                self.session.next_flashcard = randrange(len(self.flashcards))
                flashcard = self.flashcards[self.session.next_flashcard]
                cat = flashcard.category
                # todo perhaps its better to filter questions at beginning
                if (self.params.avoid_asked and self.session.next_flashcard in self.session.asked) or (
                        cat != "" and cat in self.params.ignored_categories):
                    continue
                else:
                    break

        self.session.asked.append(self.session.next_flashcard)
        flashcard: Flashcard = self.flashcards[self.session.next_flashcard]
        return flashcard, False

    def display_flashcard(self, flashcard: Flashcard):
        print(f"Question {flashcard.id}: " + flashcard.question)
        input()

        if isinstance(flashcard.domc, list) and len(flashcard.domc) > 0:
            letter_code: int = ord("a")
            for line in flashcard.domc:
                print(chr(letter_code) + ") " + line)
                input()
                letter_code += 1

        print("Answer: " + flashcard.answer)
        print("\n")

