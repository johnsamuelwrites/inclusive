#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json

import typer
import re
from rich import print
from inclusivewriting.file_utils import read_file
from inclusivewriting.text_utils import read_input_from_terminal
from inclusivewriting.locale_utils import get_default_locale_message_handler
from inclusivewriting.suggestions import detect_and_get_suggestions

app = typer.Typer()

@app.command()
def detect(language: str,
           config: str = typer.Option(None,
               help="Use a different configuration file"),
           filepath: str = typer.Option(None, 
                  help="File name; if missing, you will be prompted to enter a text")):
    _ = get_default_locale_message_handler()
    text = None
    if filepath is None:
        print(_("Enter [bold magenta]a text[/bold magenta]."), end="")
        print(_(" Press [bold magenta]Ctrl+D[/bold magenta] to exit:"))
        text = read_input_from_terminal()
    else:
        text = read_file(filepath)
    used_suggestions, suggestions, updated_text = detect_and_get_suggestions(text, config)
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
