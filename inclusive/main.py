#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json

import typer
import sys
import unicodedata
import re
from rich import print

resource = dict()
resource["en"] = "./resources/en/list.json"

app = typer.Typer()

def get_all_punctuation_separator_characters():
    characters = range(sys.maxunicode)
    # Get all punctuation and characters, i.e., unicode category
    # belonging to P or Z
    # Escaping the characters ensures that these can be later used
    # splitting text
    punctuations_separator = set(re.escape(chr(i)) for i in characters
                             if unicodedata.category(chr(i)).startswith("P") or
                                unicodedata.category(chr(i)).startswith("Z"))
    return(punctuations_separator)

@app.command()
def detect(language: str,
           filename: str = typer.Argument(None, 
                  help="File name; if missing, you will be prompted to enter a text")):
    suggestions = dict()
    punctuations_separator = get_all_punctuation_separator_characters()
    with open(resource[language], "r") as suggestion_file:
        suggestion = json.load(suggestion_file)
        for key, value in suggestion.items():
            suggestions[key] = value
    text = None
    if filename is None:
        print("Enter [bold magenta]a text[/bold magenta]:")
        text = input()
    else:
        with open(filename, "r") as text_file:
            text = text_file.read()
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
