import json
from random import randrange

default_filename = "python.json"
print(f"Type the name of flashcard file to open and press enter, or press enter for default ({default_filename}):")
filename = input()
if len(filename) == 0:
    filename = default_filename

f = open(filename)
db = json.load(f)

print(f"Loaded flashcards from {filename}")
print(f"Loaded {len(db)} flashcards")
print("Do you want to have random questions (r,R) or go sequentially (press any key) ?")

mode = input()
if mode.lower() == "r":
    linearly = False
else:
    linearly = True

next_flashcard = 0
covered = 0

try:
    while True:
        if linearly:
            next_flashcard += 1
        else:
            next_flashcard = randrange(len(db)-1) + 1

        flashcard = db[str(next_flashcard)]

        question = flashcard["question"]
        if isinstance(question, list):
            for line in question:
                print(line)
        else:
            print("Q: " + question)
        input()

        print("A: " + flashcard["answer"])
        print("\n\n")
        input()

        covered += 1
        if (covered % 10) == 0:
            print(f"You have finished {covered} questions!\n")

except (KeyboardInterrupt, KeyError):
    print(f"You have finished {covered} questions!")
    exit(0)


