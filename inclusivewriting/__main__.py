#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Functions to detect posssible issues with an input text
and to suggest possible replacements.
"""

import typer
import rich
from inclusivewriting.file_utils import read_file
from inclusivewriting.text_utils import read_input_from_terminal
from inclusivewriting.locale_utils import (
    get_default_locale_message_handler,
    get_default_locale_encoding,
)
from inclusivewriting.suggestions import detect_and_get_suggestions

app = typer.Typer()


@app.command()
def detect(
    language: str,
    config: str = typer.Option(None, help="Use a different configuration file"),
    filepath: str = typer.Option(
        None, help="File name; if missing, you will be prompted to enter a text"
    ),
):
    """
    Detect possible issues in an input text or from a file and
    show possible suggestions
    """
    _ = get_default_locale_message_handler()
    if language is None:
        language, _ = get_default_locale_encoding()
    text = None
    if filepath is None:
        rich.print(_("Enter [bold magenta]a text[/bold magenta]."), end="")
        rich.print(_(" Press [bold magenta]Ctrl+D[/bold magenta] to exit:"))
        text = read_input_from_terminal()
    else:
        text = read_file(filepath)
    used_suggestions, suggestions, updated_text = detect_and_get_suggestions(
        language, text, config
    )
    updated_text = updated_text.replace("<change>", "[bold green]")
    updated_text = updated_text.replace("</change>", "[/bold green]")
    rich.print(updated_text)
    rich.print()
    if len(used_suggestions) > 0:
        rich.print("Following are some suggested replacements:")
        for word in used_suggestions:
            rich.print("[bold green]" + word + " [/bold green]: ", end="")
            for replacement_lexeme in suggestions[
                word.lower()
            ].get_replacement_lexemes():
                rich.print(
                    "[bold blue]" + replacement_lexeme.get_value() + "[/bold blue]",
                    end="; ",
                )
            rich.print()
    rich.print()


if __name__ == "__main__":
    app()
