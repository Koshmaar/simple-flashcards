
import json
import os
from src.objects import Flashcard, Session
from src.utils import EnhancedJSONEncoder, deserialize_dataclass, deserialize_dataclass_from_dict

from typing import Dict, List, Any
import urllib.request
import urllib.response
import urllib.parse
from urllib.error import URLError, HTTPError


def save_session_to_file(session: Session, filename: str):
    with open(filename, 'w') as f:
        content = json.dumps(session, cls=EnhancedJSONEncoder, indent=2)
        f.write(content)


def load_session_from_file(filename: str) -> Session:
    with open(filename) as f:
        file = f.read()
        session = deserialize_dataclass(Session, file)
        return session


def load_flashcards(filename: str) -> List[Flashcard]:
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

    flashcards = list()
    for el in db:
        flashcards.append(deserialize_dataclass_from_dict(Flashcard, el))

    return flashcards


def get_session(flashcard_filename: str) -> Session:
    session_filename = flashcard_filename + ".session" 
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
