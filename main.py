import sys
from random import randrange, seed
from typing import Dict, List, Any

from src.methods import get_session, load_flashcards, save_session_to_file
from src.objects import Flashcard, Params, Session


DEFAULT_FILENAME = 'docker copy.json'


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


def program(params: Params):

    db = load_flashcards(params.filename)
    print(f"Loaded {len(db)} flashcards")
    session: Session = get_session(params.filename)
    seed()

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
                    cat = flashcard.category
                    # todo perhaps its better to filter questions at beginning
                    if (params.avoid_asked and session.next_flashcard in session.asked) or (cat != "" and cat in params.ignored_categories):
                        continue
                    else:
                        break

            session.asked.append(session.next_flashcard)
            flashcard: Flashcard = db[(session.next_flashcard)]

            question = flashcard.question
            if isinstance(question, list):
                for line in question:
                    print(line)
            else:
                print(f"Q {flashcard.id}: " + question)
            input()

            print("A: " + flashcard.answer)
            print("\n")
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
        session_filename = params.filename + ".session"
        save_session_to_file(session, session_filename)
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
