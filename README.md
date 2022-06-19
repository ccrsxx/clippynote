# [clippynote](https://github.com/ccrsxx/clippynote) &middot; [![Upload Python Package](https://github.com/ccrsxx/clippynote/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ccrsxx/clippynote/actions/workflows/python-publish.yml) [![PyPI Latest Release](https://img.shields.io/pypi/v/clippynote.svg)](https://pypi.org/project/clippynote) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A CLI for taking notes with key value pairs that uses `.json` file to store its data. It is designed to be used in a terminal. You can use it to take notes on your projects, tasks, or anything else you want.

Also you can copy and paste the note with the `-c / --copy` option, it will use the clipboard data.

Although the package is named `clippynote`, but the CLI is using `note` as the entry point to the CLI. Why? you may ask. Well, it's because `note` is short and easier to type than `clippynote`.

## Installation

Follow all these steps shown below to use the CLI.

1. Install using pip:

   ```bash
   pip install clippynote
   ```

2. Initialize the database:

   ```bash
   note init
   ```

3. Use the CLI:

   ```bash
   note
   ```
