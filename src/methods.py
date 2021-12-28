import json
import os
from src.objects import Flashcard, Session
from src.utils import EnhancedJSONEncoder, deserialize_dataclass, deserialize_dataclass_from_dict

from typing import Dict, List, Any
import urllib.request
import urllib.response
import urllib.parse
from urllib.error import URLError, HTTPError


def load_deck(filename: str) -> List[Flashcard]:
    json_flashcards = []
    if filename.startswith("http://") or filename.startswith("https://"):
        req = urllib.request.Request(url=filename)
        try:
            resp = urllib.request.urlopen(req, timeout=5)
            json_flashcards = json.loads(resp.read().decode())
        except HTTPError as e:
            print(f"error: {e} {e.read().decode()}")
            exit(1)
        except URLError as e:
            print(f"connection error: {e}")
            exit(1)
    else:
        f = open(filename)
        json_flashcards = json.load(f)

    flashcards = list()
    for card in json_flashcards:
        flashcards.append(deserialize_dataclass_from_dict(Flashcard, card))

    print(f"Loaded {len(flashcards)} flashcards from {filename}")
    return flashcards


def get_unique_id(flashcards: List[Flashcard]) -> int:
    max_found = 0
    for el in flashcards:
        if int(el.id) > max_found:
            max_found = int(el.id)
    return max_found+1


def save_deck(filename: str, flashcards: List[Flashcard]):
    with open(filename, 'w') as f:
        content = json.dumps(flashcards, cls=EnhancedJSONEncoder, indent=2)
        f.write(content)


def hash_filename(filename: str) -> str:
    import hashlib
    return str(int(hashlib.sha256(filename.encode('utf-8')).hexdigest(), 16) % 10 ** 8)


def convert_potential_url_to_hash(filename: str) -> str:
    if filename.startswith("http://") or filename.startswith("https://"):
        filename = hash_filename(filename)
    return filename


def save_session_to_file(session: Session, filename: str) -> str:
    filename = convert_potential_url_to_hash(filename)

    with open(filename + ".session", 'w') as f:
        content = json.dumps(session, cls=EnhancedJSONEncoder, indent=2)
        f.write(content)
    return filename


def load_session_from_file(filename: str) -> Session:
    filename = convert_potential_url_to_hash(filename)

    with open(filename + ".session" ) as f:
        file = f.read()
        session = deserialize_dataclass(Session, file)
        return session


def get_session(deck_filename: str, quick_start: bool) -> Session:
    session_filename = convert_potential_url_to_hash(deck_filename)

    if os.path.exists(session_filename + ".session"):
        if not quick_start:
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
            session = load_session_from_file(session_filename)
            print("Continuing session...")
    else:
        session = Session()
        print("Starting new session")
    return session
