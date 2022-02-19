import argparse

from clippynote import note


def parse_args():
    # initialize the main parser
    notepy_parser = argparse.ArgumentParser(
        prog='notepy',
        description='A simple CLI for taking notes',
        allow_abbrev=False,
    )
    sub_parser = notepy_parser.add_subparsers(dest='command')

    # sub-parser for 'get' command
    get_parser = sub_parser.add_parser('get', help='get a note')
    get_parser.add_argument('key', help='note key')
    get_parser.add_argument(
        '-c', '--clipboard', action='store_true', help='copy to clipboard'
    )

    # subparser for 'add' command
    add_parser = sub_parser.add_parser('add', help='add a new note')
    add_parser.add_argument('key', action='store', type=str, help='note key')
    add_parser.add_argument(
        'value',
        action='store',
        type=str,
        help='content of the note',
        nargs='*',
        default=[],
    )
    add_parser.add_argument(
        '-c', '--clipboard', action='store_true', help='get from clipboard'
    )

    # subparser for 'remove' command
    remove_parser = sub_parser.add_parser('remove', help='remove a note')
    remove_parser.add_argument('key', action='store', type=str, help='note key')

    # parseer for 'edit' command
    edit_parser = sub_parser.add_parser('edit', help='edit a note')
    edit_parser.add_argument('key', action='store', type=str, help='note key')
    edit_parser.add_argument(
        'value',
        action='store',
        type=str,
        help='content of the note',
        nargs='*',
        default=[],
    )
    edit_parser.add_argument(
        '-c', '--clipboard', action='store_true', help='get from clipboard'
    )

    # subparser for 'list' command
    list_parser = sub_parser.add_parser('list', help='show all notes')
    list_parser.add_argument(
        'search',
        action='store',
        type=str,
        help='search notes by key',
        nargs='?',
        default=None,
    )
    list_parser.add_argument(
        '-m',
        '--many',
        metavar='num',
        action='store',
        type=int,
        help='limit how many notes',
    )
    list_parser.add_argument(
        '-s',
        '--sort',
        action='store_true',
        help='sort the notes by key',
    )
    list_parser.add_argument(
        '-f',
        '--force-strict',
        action='store_true',
        help='only show notes that starts with the filter',
    )

    # subparser for 'clear' command
    sub_parser.add_parser('clear', help='clear all notes')

    return [notepy_parser, vars(notepy_parser.parse_args())]


def run_cli():
    [notepy_parser, kwargs] = parse_args()

    if not kwargs['command']:
        notepy_parser.print_help()
        quit()

    note.run_notepy(**kwargs)
