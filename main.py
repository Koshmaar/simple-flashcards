import sys
from random import randrange, seed
from typing import Dict, List, Any

from src.methods import get_session, load_deck, save_session_to_file, save_deck, get_unique_id
from src.objects import Flashcard, Params, Session, Program


def process_params(default_filename: str) -> Params:

    params = Params()
    params.filename = default_filename

    # todo reversed arguments should be also supported
    if len(sys.argv) == 2:
        if sys.argv[1] == '-q':
            params.quick_start = True
            return params
        else:
            params.filename = sys.argv[1]
    if len(sys.argv) == 3:
        if sys.argv[1] == '-q':
            params.quick_start = True
            params.filename = sys.argv[2]
            return params

    print(f"Type the name of flashcard file to open and press enter, or press enter for default ({params.filename}):")
    filename = input()
    if len(filename) != 0:
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


def start_learning(params: Params):
    seed()
    db = load_deck(params.filename)
    session: Session = get_session(params.filename, params.quick_start)
    program = Program(session, params, db)

    try:
        while True:
            flashcard, was_problematic = program.get_next_flashcard()
            program.display_flashcard(flashcard)

            answer = input()
            if answer:
                # typing anything means that the question was answered wrongly
                print("Wrong answer! Will repeat soon.")
                session.problematic.append(session.next_flashcard)
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
        session_filename = save_session_to_file(session, params.filename)
        print(f"Saved session to {session_filename}")
        exit(0)


def add_new_flashcard():
    print("Adding new questions. Type the following:")
    print("Deck filename:")
    filename = input()
    if filename.startswith("http://"):
        print("Can't save flashcard file back to http address. Please type filename on disk:")
        filename = input()
    flashcards = load_deck(filename)

    try:
        while True:
            flashcard = Flashcard()
            print("Question:")
            flashcard.question = input()

            domc = []
            while True:
                print("DOMC:")
                next_domc = input()
                if len(next_domc) == 0:
                    break
                else:
                    domc.append(next_domc)
            flashcard.domc = domc

            print("Answer:")
            flashcard.answer = input()

            flashcard.id = get_unique_id(flashcards)

            print("---------\nGathered data:")
            print(flashcard)

            print("Do you want to add this? Press enter if yes, ctrl+c if not")
            input()
            flashcards.append(flashcard)
            save_deck(filename, flashcards)

    except KeyboardInterrupt:
        exit(0)


def main():

    if len(sys.argv) >= 2:
        first_arg = sys.argv[1]
        if first_arg == "--add" or first_arg == "-a":
            add_new_flashcard()
            sys.exit(0)

    # deprecated logic, but will be useful in future
    if len(sys.argv) >= 2:
        first_arg = sys.argv[1]
        if first_arg == "--script" or first_arg == "-s":
            from scripts import process_flashcards
            filename = sys.argv[2]
            deck = load_deck(filename)
            process_flashcards(deck, filename + ".list")
            # convert_flashcards_to_list(db, filename + ".list")
            sys.exit(0)

    params = process_params('docker copy.json')
    start_learning(params)


main()
