import json


def process_flashcards(db: list, save_filename: str): 
    # could be used for various purposes, just change logic
    # in this case it was used for removing unnecessary indexes from question body
    
    for card in db:
        s = card["id"] + "."
        if s in card["question"]:
            card["question"] = card["question"].replace(s, "").strip()

        s = str(int(card["id"])+1) + "."
        if s in card["question"]:
            card["question"] = card["question"].replace(s, "").strip()

        card["id"] = card["id"]

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
