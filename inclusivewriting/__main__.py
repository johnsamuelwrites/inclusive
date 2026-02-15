#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Functions to detect posssible issues with an input text
and to suggest possible replacements.
"""

import json

import typer
import rich
from rich.console import Console
from inclusivewriting.file_utils import read_file
from inclusivewriting.text_utils import read_input_from_terminal
from inclusivewriting.locale_utils import (
    get_default_locale_message_handler,
    get_default_locale_encoding,
)
from inclusivewriting.suggestions import detect_and_get_rule_matches

app = typer.Typer()


@app.command()
def detect(
    language: str,
    config: str = typer.Option(None, help="Use a different configuration file"),
    filepath: str = typer.Option(
        None, help="File name; if missing, you will be prompted to enter a text"
    ),
    output_format: str = typer.Option(
        "text", "--format", "-f", help="Output format: text or json"
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Show only the result"),
    no_color: bool = typer.Option(
        False, "--no-color", help="Disable colored output in text mode"
    ),
):
    """
    Detect possible issues in an input text or from a file and
    show possible suggestions
    """
    output_format = output_format.lower()
    if output_format not in {"text", "json"}:
        rich.print('Invalid format. Use "text" or "json".')
        raise typer.Exit(code=2)

    console = Console(no_color=no_color)
    _ = get_default_locale_message_handler()
    if language is None:
        language, _ = get_default_locale_encoding()

    try:
        if filepath is None:
            if not quiet and output_format == "text":
                console.print(_("Enter [bold magenta]a text[/bold magenta]."), end="")
                console.print(_(" Press [bold magenta]Ctrl+D[/bold magenta] to exit:"))
            text = read_input_from_terminal()
        else:
            text = read_file(filepath)

        used_suggestions, suggestions, updated_text, matches = detect_and_get_rule_matches(
            language, text, config
        )
    except Exception as error:
        rich.print(f"Error: {error}")
        raise typer.Exit(code=2) from error

    sorted_used_suggestions = sorted(used_suggestions, key=str.lower)
    if output_format == "json":
        output = {
            "language": language,
            "issues_found": len(matches),
            "updated_text": updated_text,
            "matches": [
                {
                    "rule_id": match.rule_id,
                    "start": match.start,
                    "end": match.end,
                    "match": match.matched_text,
                    "replacements": match.replacements,
                    "severity": match.severity,
                    "confidence": match.confidence,
                    "rationale": match.rationale,
                    "auto_fix_safe": match.auto_fix_safe,
                }
                for match in matches
            ],
        }
        rich.print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        updated_text_markup = updated_text.replace("<change>", "[bold green]")
        updated_text_markup = updated_text_markup.replace("</change>", "[/bold green]")
        console.print(updated_text_markup)
        if not quiet:
            console.print()
        if len(sorted_used_suggestions) > 0 and not quiet:
            console.print("Following are some suggested replacements:")
            for word in sorted_used_suggestions:
                console.print("[bold green]" + word + " [/bold green]: ", end="")
                for replacement_lexeme in suggestions[
                    word.lower()
                ].get_replacement_lexemes():
                    console.print(
                        "[bold blue]" + replacement_lexeme.get_value() + "[/bold blue]",
                        end="; ",
                    )
                console.print()
        if not quiet:
            console.print()

    if len(matches) > 0:
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
