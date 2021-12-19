import sys
import json
from random import randrange
from typing import Dict, List
import urllib.request
import urllib.response
import urllib.parse
from urllib.error import URLError, HTTPError

DEFAULT_FILENAME = 'python.json'


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


def process_params():

    if len(sys.argv) == 2:
        default_filename = sys.argv[1]
    else:    
        default_filename = DEFAULT_FILENAME

    print(f"Type the name of flashcard file to open and press enter, or press enter for default ({default_filename}):")
    filename = input()
    if len(filename) == 0:
        filename = default_filename

    db = load_flashcards(filename)

    print(f"Loaded flashcards from {filename}")
    print(f"Loaded {len(db)} flashcards")
    print("Do you want to have random questions (press any key) or go sequentially (S, s) ?")

    mode = input()
    if mode.lower() == "s":
        linearly = True
    else:
        linearly = False

    ignored_categories = []
    print(f"Do you want to ignore some category (default = {ignored_categories}) ?")
    cat = input()
    if cat:
        ignored_categories.append(cat)

    avoid_asked = True
    return db, avoid_asked, ignored_categories, linearly


def program(db: Dict, avoid_asked: bool, ignored_categories: List, linearly: bool):

    asked = [] # contains indexes of asked questions
    next_flashcard = 0
    covered = 0

    try:
        while True:
            if linearly:
                next_flashcard += 1
            else:
                for i in range(10):
                    next_flashcard = randrange(len(db)-1) + 1
                    flashcard = db[(next_flashcard)]
                    cat = flashcard.get("category")
                    # todo perhaps its better to filter questions at beginning
                    if (avoid_asked and next_flashcard in asked) or (cat is not None and cat in ignored_categories):
                        continue
                    else:
                        break

            asked.append(next_flashcard)
            flashcard = db[(next_flashcard)]

            question = flashcard["question"]
            if isinstance(question, list):
                for line in question:
                    print(line)
            else:
                print(f"Q {next_flashcard}: " + question)
            input()

            print("A: " + flashcard["answer"])
            print("\n\n")
            input()

            covered += 1
            if (covered % 10) == 0:
                print(f"You have finished {covered} questions out of {len(db)}!\n")

    except (KeyboardInterrupt, KeyError):
        print(f"You have finished {covered} questions!")
        exit(0)


def main():
    params = process_params()
    program(*params)
    
    # from .scripts import process_flashcards
    # db = load_flashcards(filename)
    # process_flashcards(db)
    # convert_flashcards_to_list(db, filename + ".list")

main()


