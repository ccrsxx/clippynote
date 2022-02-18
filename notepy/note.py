import os
import json


class Note:
    def __init__(self):
        self.location = 'db.json'

        if not os.path.exists(self.location):
            self.clear()
        else:
            with open(self.location, 'r') as f:
                self.db = json.load(f)

    def add_note(self, key, value):
        if key in self.db:
            print(f'{key} already exists!')
        else:
            self.db[key] = value
            self.save()

    def remove_note(self, key):
        if key not in self.db:
            print(f'{key} does not exist!')
        else:
            self.db.pop(key)
            print(f'{key} deleted!')
            self.save()

    def edit_note(self, key, value):
        if key not in self.db:
            print('Note does not exist!')
        else:
            self.db[key] = value
            self.save()

    def list_notes(self, many=None):
        if many:
            for n, (key, value) in enumerate(self.db.items(), 1):
                print(f'{n}. {key} = {value}')
                if n == many:
                    break
        else:
            for key, value in self.db.items():
                print(f'{key} = {value}')

    def clear(self):
        self.db = {}
        self.save()

    def save(self):
        with open(self.location, 'w') as f:
            json.dump(self.db, f)
