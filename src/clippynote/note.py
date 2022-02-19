import os
import json
import pyperclip


class Note:
    def __init__(self, init=False):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.db_location = 'db.json'

        if init:
            return self.initialize_db()
        elif not os.path.exists(self.db_location):
            print('❌ You need to initialize the database first with "note init"!')
            exit()

        with open(self.db_location, 'r') as f:
            self.db = json.load(f)

    def initialize_db(self):
        if os.path.exists(self.db_location):
            print('⚠️ Database already exists!')
            exit()
        with open(self.db_location, 'w') as f:
            json.dump({}, f, indent=2)
        print('✅ Database initialized!')

    def get_db_location(self):
        return os.path.abspath(self.db_location)

    def get_note(self, key, clipboard):
        if key not in self.db:
            print(f'❌ {key} does not exist!')
        else:
            if clipboard:
                pyperclip.copy(self.db[key])
                print(f'📋 {key} copied to clipboard!')
            else:
                print(f'{key} = {self.db[key]}')

    def add_note(self, key, new_key, value, clipboard):
        if key in self.db:
            print(f'⚠️ {key} with a value of "{self.db[key]}" is already exists!\n')
            self.edit_note(key, new_key, value, clipboard)
        else:
            if clipboard:
                self.db[key] = pyperclip.paste()
                print(f'📋 Adding value from clipboard to {key}...')
            else:
                self.db[key] = value
            print(f'✅ {key} added!')
            self.save_db()

    def remove_note(self, key):
        if key not in self.db:
            print(f'❌ {key} does not exist!')
        else:
            self.db.pop(key)
            print(f'✅ {key} deleted!')
            self.save_db()

    def edit_note(self, key, new_key, value, clipboard):
        if key not in self.db:
            print(f'❌ {key} does not exist!')
        else:
            try:
                ask = ''
                valid = ['Y', 'y', 'N', 'n']

                while ask not in valid:
                    ask = input(
                        f'❓ Do you want to change {"key" if new_key and not value else "value" if not new_key else "content and key"} of {key}? y/N\n> '
                    )
                    if ask not in valid:
                        print('\nInvalid input!\n')
            except KeyboardInterrupt:
                pass

            if ask in ['Y', 'y']:
                if new_key:
                    old_val = self.db.pop(key)
                    print(f'✅ {key} changed to {new_key}!')
                    key = new_key

                if clipboard:
                    self.db[key] = pyperclip.paste()
                else:
                    if not value:
                        self.db[key] = old_val
                    else:
                        self.db[key] = value
                self.save_db()
                print(f'✅ {key} updated!')
            else:
                print(f'❌ {key} not updated!')

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
            print(f'❌ No notes{f" that matches {search}" if search else ""} found!')
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
                ask = input('❓ Do you really want to clear the database? y/N\n> ')
                if ask not in valid:
                    print('\n❌Invalid input!\n')
        except KeyboardInterrupt:
            pass

        if ask in ['Y', 'y']:
            self.clear_db()
        else:
            print('\n❌ Database not cleared!')

    def clear_db(self):
        self.db = {}
        self.save_db()
        print('✅ Database cleared!')

    def save_db(self):
        with open(self.db_location, 'w') as f:
            json.dump(self.db, f, indent=2)


def run_notepy(
    command: str,
    key: str = None,
    value: list = None,
    new_key: str = None,
    clipboard: bool = False,
    search: str = None,
    many: int = None,
    sort: bool = False,
    force_strict: bool = False,
):

    note = Note(init=True if command == 'init' else False)

    if command == 'loc':
        print(f'📋 Database located at {note.get_db_location()}')
        exit()
    elif (
        command == 'add' and not value or command == 'remove' and not key
    ) and not clipboard:
        print(f'❌ you need a {"value" if command == "add" else "key"} for that!')
        exit()
    elif command == 'list' and not search and force_strict:
        print('❌ you need to add a filter to use strict filter!')
        exit()
    elif command == 'edit' and not value and not new_key and not clipboard:
        print('❌ you need a value to edit!')
        exit()

    if value:
        value = ' '.join(value)

    match command:
        case 'get':
            note.get_note(key, clipboard)
        case 'add':
            note.add_note(key, new_key, value, clipboard)
        case 'remove':
            note.remove_note(key)
        case 'edit':
            note.edit_note(key, new_key, value, clipboard)
        case 'list':
            note.list_notes(search, many, sort, force_strict)
        case 'clear':
            note.clear_notes()
