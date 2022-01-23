#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json

import typer
import re
from rich import print
from inclusive.file_utils import read_file
from inclusive.locale_utils import get_default_locale_message_handler
from inclusive.suggestions import detect_and_get_suggestions

resource = dict()
resource["en"] = "./resources/en/list.json"

app = typer.Typer()


@app.command()
def detect(language: str,
           filename: str = typer.Argument(None, 
                  help="File name; if missing, you will be prompted to enter a text")):
    _ = get_default_locale_message_handler()
    text = None
    if filename is None:
        print(_("Enter [bold magenta]a text[/bold magenta]:"))
        text = input()
    else:
        text = read_file(filename)
    used_suggestions, suggestions, updated_text = detect_and_get_suggestions(text)
    updated_text = updated_text.replace("<change>", "[bold green]")
    updated_text = updated_text.replace("</change>", "[/bold green]")
    print(updated_text)
    print()
    if (len(used_suggestions) > 0):
        print("Following are some suggested replacements:")
        for word in used_suggestions:
            print("[bold green]" + word + " [/bold green]: ", end="")
            for replacement_lexeme in suggestions[word.lower()].get_replacement_lexemes():
                print("[bold blue]" + replacement_lexeme.get_value() + "[/bold blue]", end="; ")
            print()
    print()

if __name__ == "__main__":
    app()
