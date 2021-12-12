# simple-flashcards
CLI based flashcards for easy remembering practice. You can use it for whatever 
type of domain learning you need.


# Basic usage

Just run it with `python main.py` and it will start to ask questions. 
First how to operate:

```
Type the name of flashcard file to open and press enter, or press enter for default (python.json):
docker.json
Loaded db from docker.json
Loaded 6 flashcards
Do you want to have random questions (r,R) or go sequentially (press any key) ?
```

Then the actual questions from loaded flashcards file: 

```
Q: 4. Which command do you use to find the information about the nodes in the swarm?

A: docker node ls
```

The answer is displayed after pressing enter.

# Flashcard file format

The flashcard file format is json, with simple structure of main dictionary, and
each flashcard is another dict, with two keys, "question" and "answer".

There is attached file harvest.js which creates sample file. 


# TODO

- add mode for interactively adding new questions
- allow user to flag questions which he failed, and the program would return to them
