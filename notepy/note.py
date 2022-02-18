import os
import json
import pyperclip


class Note:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.db_location = 'db.json'

        if not os.path.exists(self.db_location):
            self.clear_db()
        else:
            with open(self.db_location, 'r') as f:
                self.db = json.load(f)
            self.get_db_location()

    def get_db_location(self):
        return self.db_location

    def get_note(self, key, clipboard):
        if key not in self.db:
            print(f'{key} does not exist!')
        else:
            if clipboard:
                pyperclip.copy(self.db[key])
                print(f'{key} copied to clipboard!')
            else:
                print(f'{key} = {self.db[key]}')

    def add_note(self, key, value, clipboard):
        if key in self.db:
            print(f'key {key} with a value of "{self.db[key]}" already exists!')
            self.edit_note(key, value, clipboard)
        else:
            if clipboard:
                self.db[key] = pyperclip.paste()
                print(f'{key} added!')
            else:
                self.db[key] = value
            self.save_db()

    def remove_note(self, key):
        if key not in self.db:
            print(f'{key} does not exist!')
        else:
            self.db.pop(key)
            print(f'{key} deleted!')
            self.save_db()

    def edit_note(self, key, value, clipboard):
        if key not in self.db:
            print(f'{key} does not exist!')
        else:
            try:
                ask = ''
                valid = ['Y', 'y', 'N', 'n']

                while ask not in valid:
                    ask = input('Do you want to overwrite? [Y/N]\n> ')
                    if ask not in valid:
                        print('\nInvalid input!\n')
            except KeyboardInterrupt:
                pass

            if ask in ['Y', 'y']:
                if clipboard:
                    self.db[key] = pyperclip.paste()
                else:
                    self.db[key] = value
                self.save_db()
                print(f'\n{key} updated!')
            else:
                print(f'\n{key} not updated!')

    def list_notes(self, many):
        if many:
            for n, (key, value) in enumerate(self.db.items(), 1):
                print(f'{n}. {key} = {value}')
                if n == many:
                    break
        else:
            for key, value in self.db.items():
                print(f'- {key}\t: {value}')

    def clear_notes(self):
        try:
            ask = ''
            valid = ['Y', 'y', 'N', 'n']

            while ask not in valid:
                ask = input('Do you really want to clear the database? [Y/N]\n> ')
                if ask not in valid:
                    print('\nInvalid input!\n')
        except KeyboardInterrupt:
            pass

        if ask in ['Y', 'y']:
            self.clear_db()
        else:
            print('\nDatabase not cleared!')

    def clear_db(self):
        print('Database cleared!, creating new one...')
        self.db = {}
        self.save_db()

    def save_db(self):
        with open(self.db_location, 'w') as f:
            json.dump(self.db, f, indent=2)


def notepy(
    command: str,
    key: str = None,
    value: list = None,
    clipboard: bool = False,
    many: int = None,
):

    note = Note()

    if value:
        value = ' '.join(value)

    if command in ['edit', 'remove'] and not value and not clipboard:
        return print('No value or clipboard input!')

    match command:
        case 'get':
            note.get_note(key, clipboard)
        case 'add':
            note.add_note(key, value, clipboard)
        case 'remove':
            note.remove_note(key)
        case 'edit':
            note.edit_note(key, value, clipboard)
        case 'list':
            note.list_notes(many)
        case 'clear':
            note.clear_notes()
