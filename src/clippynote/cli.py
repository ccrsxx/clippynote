import argparse

from .note import run_note


def parse_args():
    # initialize the main parser
    notepy_parser = argparse.ArgumentParser(
        prog='note',
        description='A simple CLI for taking notes',
        allow_abbrev=False,
    )
    sub_parser = notepy_parser.add_subparsers(dest='command')

    # init-parser for 'init' command
    sub_parser.add_parser('init', help='initialize a new database')

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

    # subparser for 'edit' command
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
        '-k',
        '--key',
        metavar='key',
        help='edit key (optional)',
        action='store',
        type=str,
        dest='new_key',
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
    list_parser.add_argument(
        '-fk',
        '--full-key',
        action='store_true',
        help='show max length of key',
    )

    # subparser for 'import' command
    import_parser = sub_parser.add_parser('import', help='import notes from a file')
    import_parser.add_argument(
        'path',
        action='store',
        type=str,
        help='path to the file',
    )

    # subparser for 'export' command
    export_parser = sub_parser.add_parser('export', help='export notes to a file')
    export_parser.add_argument(
        'path',
        action='store',
        type=str,
        help='path to the file',
        nargs='?',
        default=None,
    )

    # subparser for 'clear' command
    sub_parser.add_parser('clear', help='clear all notes')

    # subparser for 'loc' command
    sub_parser.add_parser('loc', help='get the database location')

    return notepy_parser, vars(notepy_parser.parse_args())


def run_cli():
    notepy_parser, kwargs = parse_args()

    if not kwargs['command']:
        notepy_parser.print_help()
        quit()

    run_note(**kwargs)
