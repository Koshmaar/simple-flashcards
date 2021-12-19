import json


def process_flashcards(db: dict, save_filename: str): 
    # could be used for various purposes, just change logic
    # in this case it was used for removing unnecessary indexes from question body
    
    for key,value in db.items():
        s = key + "."
        if s in value["question"]:
            value["question"] = value["question"].replace(s, "").strip()

        s = str(int(key)+1) + "."
        if s in value["question"]:
            value["question"] = value["question"].replace(s, "").strip()

        value["id"] = key

    new_db = json.dumps(db, indent=2) 
    with open(save_filename + ".mod", 'w') as file:
        file.write(new_db)


def convert_flashcards_to_list(db: dict, save_filename: str): 
    # used to transform old dictionary based flashcard file to array based
    new_db = []
    for key,value in db.items():
        value["id"] = key
        new_db.append(value)

    new_db_str = json.dumps(new_db, indent=2) 
    with open(save_filename, 'w') as file:
        file.write(new_db_str)