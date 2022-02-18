import argparse

from note import notepy

# initialize the parser
notepy_parser = argparse.ArgumentParser(
    prog='clipper', description='A simple CLI for taking notes'
)
sub_parser = notepy_parser.add_subparsers(dest='command')

# parser for 'get' command
get_parser = sub_parser.add_parser('get', help='get a note')
get_parser.add_argument('key', help='note key')
get_parser.add_argument(
    '-c', '--clipboard', action='store_true', help='copy to clipboard'
)

# parser for 'add' command
add_parser = sub_parser.add_parser('add', help='add a new note')
add_parser.add_argument('key', action='store', type=str, help='note key')
add_parser.add_argument(
    'value', action='store', type=str, help='content of the note', nargs='*', default=[]
)
add_parser.add_argument(
    '-c', '--clipboard', action='store_true', help='get from clipboard'
)

# parser for 'remove' command
remove_parser = sub_parser.add_parser('remove', help='remove a note')
remove_parser.add_argument('key', action='store', type=str, help='note key')

# parseer for 'edit' command
edit_parser = sub_parser.add_parser('edit', help='edit a note')
edit_parser.add_argument('key', action='store', type=str, help='note key')
edit_parser.add_argument(
    'value', action='store', type=str, help='content of the note', nargs='*', default=[]
)
edit_parser.add_argument(
    '-c', '--clipboard', action='store_true', help='get from clipboard'
)

# parser for 'list' command
list_parser = sub_parser.add_parser('list', help='show all notes')
list_parser.add_argument(
    'many',
    action='store',
    type=int,
    help='set how many notes to show',
    nargs='?',
    default=None,
)

# parser for 'clear' command
clear_parser = sub_parser.add_parser('clear', help='clear all notes')

kwargs = vars(notepy_parser.parse_args())

if not kwargs['command']:
    notepy_parser.print_help()
    quit()


notepy(**kwargs)
