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
            print(f'key {key} with a value of "{self.db[key]}" is already exists!\n')
            self.edit_note(key, value, clipboard)
        else:
            if clipboard:
                self.db[key] = pyperclip.paste()
                print(f'Adding value from clipboard to {key}...')
            else:
                self.db[key] = value
            print(f'{key} added!')
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
                    ask = input(f'Do you want to overwrite {key}? [Y/N]\n> ')
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

    def list_notes(self, search, many, sort, force_strict):
        keys = []

        for key in self.db:
            if search:
                if force_strict and key.startswith(search):
                    keys.append(key)
                elif not force_strict and search in key:
                    keys.append(key)
            else:
                keys.append(key)

        if not keys:
            print('No notes found!')
            exit()

        if sort:
            keys.sort()

        if many:
            keys = keys[:many]

        for key in keys:
            print(f'🔑 {key}\t: {self.db[key]}')

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


def run_notepy(
    command: str,
    key: str = None,
    value: list = None,
    clipboard: bool = False,
    search: str = None,
    many: int = None,
    sort: bool = False,
    force_strict: bool = False,
):

    note = Note()

    if value:
        value = ' '.join(value)

    if command in ['edit', 'remove'] and (not key or not value) and not clipboard:
        print('No key / value or clipboard input!')
        exit()
    elif command == 'list' and not search and force_strict:
        print('You need to add a filter to use strict filter!')
        exit()

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
            note.list_notes(search, many, sort, force_strict)
        case 'clear':
            note.clear_notes()
