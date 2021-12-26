import os
import sys
import json
from random import randrange
from typing import Dict, List, Any
import dataclasses
from dataclasses import dataclass, field

import urllib.request
import urllib.response
import urllib.parse
from urllib.error import URLError, HTTPError

DEFAULT_FILENAME = 'docker copy.json'


class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)


def deserialize_dataclass(DataClass, json_string) -> Any:
    """ Convert the JSON object represented by the string into the dataclass
        specified.
    """
    json_obj = json.loads(json_string)
    dc_data = {field.name: field.type(json_obj[field.name])
                    for field in dataclasses.fields(DataClass)}
    return DataClass(**dc_data)


@dataclass 
class Flashcard:
    question: str
    answer: str
    id: int


@dataclass 
class Params:
    sequential: bool = False  # if false, is random
    # ignored_categories: List[str] = []
    ignored_categories: List[str] = field(default_factory=lambda: [])

    avoid_asked: bool = True
    filename: str = ''


@dataclass
class Session:
    # both store ids of Flashcards
    asked: list = field(default_factory=lambda: [])
    problematic: list = field(default_factory=lambda: [])
    next_flashcard: int = 0
    covered: int = 0

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            content = json.dumps(self, cls=EnhancedJSONEncoder)
            f.write(content)


def load_session_from_file(filename: str) -> Session:
    with open(filename) as f:
        file = f.read()
        session = deserialize_dataclass(Session, file)
        return session


# class Program:

#     def __init__(self):
#         self.covered = 0
#         self.params = Params()


#     def get_next_flashcard(self) -> Flashcard:
#         pass


#     def display_flashcard(self):
#         pass




def load_flashcards(filename: str) -> Dict:

    if filename.startswith("http://"):
        req = urllib.request.Request(url=filename)
        try:
            resp = urllib.request.urlopen(req, timeout=5)
        except HTTPError as e:
            print(f"error: {e} {e.read().decode()}")
            exit(1)
        except URLError as e:
            print(f"connection error: {e}")
            exit(1)
        else:
            db = json.loads(resp.read().decode())
    else:
        f = open(filename)
        db = json.load(f)
    return db



def process_params() -> Params:

    params = Params()

    if len(sys.argv) == 2:
        default_filename = sys.argv[1]
    else:    
        default_filename = DEFAULT_FILENAME

    print(f"Type the name of flashcard file to open and press enter, or press enter for default ({default_filename}):")
    filename = input()
    if len(filename) == 0:
        filename = default_filename
    params.filename = filename

    print(f"Loading flashcards from {params.filename}")
    print("Do you want to have random questions (press any key) or go sequentially (S, s) ?")

    mode = input()
    if mode.lower() == "s":
        params.sequential = True
    else:
        params.sequential = False

    params.ignored_categories = []
    print(f"Do you want to ignore some category (default = {params.ignored_categories}) ?")
    cat = input()
    if cat:
        params.ignored_categories.append(cat)

    params.avoid_asked = True
    return params 

def get_session(flashcard_filename: str) -> Session:
    session_filename = flashcard_filename + ".session" 
    continue_session = False
    if os.path.exists(session_filename):
        print(f"Do you want to continue session from {session_filename}? Enter for Yes, anything else for No.")
        session = load_session_from_file(session_filename)
        print(session)
        continue_session = input()
        if continue_session != "":
            session = Session()
            print("Starting new session")
        else:
            print("Continuing...")
    else:
        session = Session()
        print("Starting new session")
    return session


def program(params: Params):

    db = load_flashcards(params.filename)
    print(f"Loaded {len(db)} flashcards")
    session = get_session(params.filename)

    try:
        while True:

            was_problematic = False
            if params.sequential:
                session.next_flashcard += 1
            else:
                for i in range(10):
                    # random.randrange(stop)  -> [0, 1, 2, ..., stop-1]                  
                    if len(session.problematic) > 2 and randrange(100) > 50:
                        print("Let's refresh sth...")
                        which = randrange(len(session.problematic))
                        session.next_flashcard = session.problematic[which]
                        flashcard = db[session.next_flashcard]
                        was_problematic = True
                        break

                    session.next_flashcard = randrange(len(db))
                    flashcard = db[session.next_flashcard]
                    cat = flashcard.get("category")
                    # todo perhaps its better to filter questions at beginning
                    if (params.avoid_asked and session.next_flashcard in session.asked) or (cat is not None and cat in params.ignored_categories):
                        continue
                    else:
                        break

            session.asked.append(session.next_flashcard)
            flashcard = db[(session.next_flashcard)]

            question = flashcard["question"]
            if isinstance(question, list):
                for line in question:
                    print(line)
            else:
                print(f"Q {flashcard['id']}: " + question)
            input()

            print("A: " + flashcard["answer"])
            print("\n")
            answer = input()
            if answer:
                # typing anything means that the question was answered wrongly
                print("Wrong answer! Will repeat soon.")
                session.problematic.append(session.next_flashcard)
            else:
                if was_problematic:
                    session.problematic.remove(session.next_flashcard)           

            print("\n")            
            session.covered += 1
            if (session.covered % 10) == 0:
                print(f"You have finished {session.covered} questions out of {len(db)}!\n")

    except (KeyboardInterrupt, KeyError):
        print(f"You have finished {session.covered} questions!")
        session_filename = params.filename + ".session"
        session.save_to_file(session_filename)
        print(f"Saved session to {session_filename}")
        exit(0)


def main():
    params = process_params()
    program(params)
    
    # from .scripts import process_flashcards
    # db = load_flashcards(filename)
    # process_flashcards(db)
    # convert_flashcards_to_list(db, filename + ".list")

main()


