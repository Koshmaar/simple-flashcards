# simple-flashcards
CLI based flashcards for easy remembering practice. You can use it for whatever 
type of domain learning you need.


# Basic usage

Just run it with `python main.py <flashard.json>` and it will start to ask questions. 
As the flashcard file you can pass http:// address. Program will download it. 
First how to operate:

```
Type the name of flashcard file to open and press enter, or press enter for default (python.json):
docker.json
Loaded db from docker.json
Loaded 6 flashcards
Do you want to have random questions (press any key) or go sequentially (s, S) ?
r
Do you want to ignore some category (default = []) ?
```

Then the actual questions from loaded flashcards file: 

```
Q 4: Which command do you use to find the information about the nodes in the swarm?

A: docker node ls
```

The answer is displayed after pressing enter.


# Flashcard file format

The flashcard file format is json, with simple structure of list, and
each flashcard is dict, with three keys, "id", "question" and "answer".

Optional key is "category".

There are attached sample harvest js files, which take content from html websites to create sample file. 


# Characteristic

Simple, and therefore very adaptable. 
Doesn't use any non-standard python libraries - so no venv or dependencies installation needs.
Uses Python 3.6+ compatible syntax.
It's free :)


# TODO
- refactor logic, add stronger typing: FlashcardDb and Flashcard classess
- simple view (screen is cleared after every question, so there's no history view)
- make it support DMOC type of questions (line by line rendering), when answer is in list format
- make "answer" store the potential answers, and new field "correct" would store the correct answer
- add mode for interactively adding new questions
- add ability to tag questions (better than categorization?)
- maybe some nice curses-based screen UI, with menus for easy navigation, with default etc.
- dockerize it and add API, so that it can be run on backend and controlled by some frontend

## Done
+ save sessions, which remember failed questions (accross restarts) and other settings
+ make it possible to download flashcard files from internet, for easy sharing
+ allow user to flag questions which he failed, and the program would return to them more often
+ change dictionary with keys, to array