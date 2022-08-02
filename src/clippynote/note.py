import os
import json
import pyperclip


class Note:
    def __init__(self, init: bool, imported: bool):
        self.db_location = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'db.json'
        )

        if init:
            return self.initialize_db()

        if not os.path.exists(self.db_location) and not imported:
            print('❌ You need to initialize the database first with "note init"!')
            exit()

        self.db = self.load_db(imported)

    def load_db(self, imported: bool):
        if not imported:
            with open(self.db_location, 'r') as f:
                return json.load(f)
        else:
            return {}

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
                print(f'🔑 {key} : {self.db[key]}')

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

    def list_notes(self, search, many, sort, force_strict, full_key):
        keys = []

        format_string = lambda x: x.replace(' ', '').lower()

        for key in self.db:
            formatted_search, formatted_key = [
                format_string(text) if text else '' for text in (search, key)
            ]
            if search:
                if force_strict and key.startswith(search):
                    keys.append(key)
                elif not force_strict and formatted_search in formatted_key:
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

        format_spacing = lambda x, y: y - len(x)
        max_len = max([len(x) for x in keys])

        if max_len > 20:
            max_len = 20

        for key in keys:
            new_key, over_space = '', False
            key_space = format_spacing(key, max_len)
            if key_space < 0:
                key_space = ''
                new_key = f'{key[:17]}...' if not full_key else key
                over_space = True
            print(
                f'🔑 {key if not over_space else new_key}{"":{key_space}} : {self.db[key]}'
            )

    def import_db(self, path: str):
        if not os.path.isfile(path):
            return print(f'❌ {path} is not a file!')

        if not os.path.basename(path).endswith('.json'):
            return print(f'❌ {path} is not a json file!')

        with open(path, 'r') as f:
            data: dict = json.load(f)

        if not data:
            return print(f'❌ {path} is empty!')

        filtered_data = {
            key: value
            for key, value in data.items()
            if all(isinstance(item, str) for item in [key, value])
        }

        if not filtered_data:
            return print(f'❌ {path} is not a valid json file!')

        self.db = filtered_data

        self.save_db()

        print(f'✅ {path} imported!')

    def export_db(self, path: str):
        if path and not os.path.isdir(path):
            return print(f'❌ {path} is not a directory!')

        with open(self.db_location, 'r') as og, open(
            os.path.join(path, 'db.json') if path else 'db.json', 'w'
        ) as new:
            data = json.load(og)
            json.dump(data, new, indent=2)

        print(
            f"✅ Database exported to {os.path.join(path if path else os.getcwd(), 'db.json')}!"
        )

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


def run_note(
    command: str,
    key: str = None,
    value: list = None,
    new_key: str = None,
    clipboard: bool = False,
    search: str = None,
    path: str = None,
    many: int = None,
    sort: bool = False,
    force_strict: bool = False,
    full_key: bool = False,
):
    note = Note(
        init=True if command == 'init' else False,
        imported=True if command == 'import' else False,
    )

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
        value = ' '.join(value)  # type: ignore

    if command == 'get':
        note.get_note(key, clipboard)
    elif command == 'add':
        note.add_note(key, new_key, value, clipboard)
    elif command == 'remove':
        note.remove_note(key)
    elif command == 'edit':
        note.edit_note(key, new_key, value, clipboard)
    elif command == 'list':
        note.list_notes(search, many, sort, force_strict, full_key)
    elif command == 'import':
        note.import_db(path)  # type: ignore
    elif command == 'export':
        note.export_db(path)  # type: ignore
    elif command == 'clear':
        note.clear_notes()
