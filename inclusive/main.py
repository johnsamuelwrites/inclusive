#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json

import typer
import re
import gettext
import locale
from rich import print
from unicode_utils import get_all_punctuation_separator_characters
from file_utils import read_file

resource = dict()
resource["en"] = "./resources/en/list.json"

app = typer.Typer()

def get_default_locale_message_handler():
    default, encoding = locale.getdefaultlocale()
    lang = gettext.translation('inclusive', localedir='locales', languages=[default])
    lang.install()
    return lang.gettext



@app.command()
def detect(language: str,
           filename: str = typer.Argument(None, 
                  help="File name; if missing, you will be prompted to enter a text")):
    _ = get_default_locale_message_handler()
    suggestions = dict()
    punctuations_separator = get_all_punctuation_separator_characters()
    with open(resource[language], "r") as suggestion_file:
        suggestion = json.load(suggestion_file)
        for key, value in suggestion.items():
            suggestions[key] = value
    text = None
    if filename is None:
        print(_("Enter [bold magenta]a text[/bold magenta]:"))
        text = input()
    else:
        text = read_file(filename)
    punctuations_separator = "|".join(punctuations_separator)
    words = re.split("(" + punctuations_separator + ")", text)
    used_suggestions = set()
    for word in words:
        if word.lower() in suggestions:
            print("[bold green]" + word + " [/bold green]", end="")
            used_suggestions.add(word)
        else:
            print(word, end="")
    print()
    if (len(used_suggestions) > 0):
        print("Following are some suggested replacements:")
        for word in used_suggestions:
            print("[bold green]" + word + " [/bold green]: ", end="")
            for suggestion,references in suggestions[word]["replacement"].items():
                print("[bold blue]" + suggestion + " [/bold blue] ", end="")
            print()
    print()

if __name__ == "__main__":
    app()
