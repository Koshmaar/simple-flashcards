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
Do you want to have random questions (r,R) or go sequentially (press any key) ?
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

The flashcard file format is json, with simple structure of main dictionary, and
each flashcard is another dict, with two keys, "question" and "answer".

Optional key is "category".

There is attached file harvest.js which creates sample file. 


# TODO
+ make it possible to download flashcard files from internet, for easy sharing
+ change dictionary with keys, to array
- allow user to flag questions which he failed, and the program would return to them more often (even accross restarts)
- stronger typing: FlashcardDb and Flashcard classess
- make it support DMOC type of questions (line by line rendering), when answer is in list format
- make "answer" store the potential answers, and new field "correct" would store the correct answer
- add mode for interactively adding new questions
- add ability to tag questions (better than categorization?)