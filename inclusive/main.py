#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json

import typer
from rich import print

resource = dict()
resource["en"] = "./resources/en/list.json"

app = typer.Typer()

@app.command()
def detect(language: str,
           filename: str = typer.Argument(None, 
                  help="File name; if missing, you will be prompted to enter a text")):
    suggestions = dict()
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
    words = text.split(" ")
    used_suggestions = set()
    for word in words:
        if word in suggestions:
            print("[bold green]" + word + " [/bold green]", end="")
            used_suggestions.add(word)
        else:
            print(word + " ", end="")
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
