import argparse

notepy = argparse.ArgumentParser(
    prog='clipper', description='A simple CLI for taking notes'
)

sub_parser = notepy.add_subparsers(dest='command')

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
    '-m',
    '--many',
    metavar='number',
    action='store',
    type=int,
    help='set how many notes to show',
    default=None,
)

args = notepy.parse_args()

notepy.print_help()

print(args)
