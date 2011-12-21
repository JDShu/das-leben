import json
import copy

class CharacterCatalog:

    def __init__(self):
        self.catalog = {}

    def load_textfile(self, filepath):
        character_file = open(filepath)
        character_data =json.load(character_file)
        character_file.close()

        for entry in character_data:
            name = entry["name"]
            profile = Profile(name)
            position = (entry["pos"]["x"], entry["pos"]["y"])
            character = Character(profile, position)
            character_id = entry["id"]
            self.catalog[character_id] = character

    def get_catalog(self):
        return copy.deepcopy(self.catalog)


class Character:
    
    def __init__(self, profile, position):
        self.profile = profile
        self.position = position


class Profile:
    
    def __init__(self, name):
        self.name = name
