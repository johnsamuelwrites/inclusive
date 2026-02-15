#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Functions to handle suggestions for different languages
"""

import json
import re
from typing import Dict, List, Tuple

import pkg_resources

from inclusivewriting.file_utils import read_file
from inclusivewriting.configuration import (
    get_all_language_resources,
    get_all_language_resource_config_file,
)


class Lexeme:
    """
    A lexeme has a value and associated links.
    Each link points to a source related to the lexeme.
    """

    def __init__(self, value, links: list = None):
        self.value = value
        self.links = links or []

    def get_value(self) -> str:
        """
        Returns the lexeme value (a string)
        """
        return self.value

    def get_links(self) -> list:
        """
        Returns all the source links related to a lexeme
        """
        return self.links

    def __str__(self):
        return (
            '"'
            + self.get_value()
            + '" : '
            + "[ "
            + ", ".join(f'"{link}"' for link in self.get_links())
            + " ]"
        )


class Replacement:
    """
    A replacement lexeme and the associated references.
    Each reference points to a source related to the lexeme.
    """

    def __init__(self, lexeme, references: list = None):
        self.lexeme = lexeme
        self.references = references or []

    def get_value(self) -> str:
        """
        Returns the lexeme value (a string)
        """
        return self.lexeme.get_value()

    def __str__(self):
        return (
            '"'
            + self.get_value()
            + '" : '
            + '{ "links" : ['
            + ", ".join(f'"{link}"' for link in self.lexeme.get_links())
            + '], "references" : ['
            + ", ".join(f'"{reference}"' for reference in self.references)
            + " ] "
            "}"
        )


class Suggestion:
    """
    A suggestion consists of one or more replacement lexemes for a given lexeme.
    """

    def __init__(self, lexeme, replacement_lexemes):
        self.lexeme = lexeme
        self.replacement_lexemes = replacement_lexemes

    def get_replacement_lexemes(self):
        """
        Returns the replacement lexemes for a given lexeme
        """
        return self.replacement_lexemes

    def get_lexeme(self):
        """
        Returns a lexeme for the suggestion
        """
        return self.lexeme

    def __str__(self):
        return (
            "{ "
            + '"'
            + str(self.get_lexeme().get_value())
            + '" : {'
            + ", ".join(
                str(replacement) for replacement in self.get_replacement_lexemes()
            )
            + "}"
            "}"
        )


def _normalize_link_list(field_name: str, value) -> List[str]:
    """
    Normalize a link-like field to a list of strings.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError(
        f'Invalid "{field_name}" format: expected string or list of strings'
    )


def _validate_and_build_suggestion(key: str, value: dict) -> Suggestion:
    """
    Validate and convert a resource entry into an in-memory Suggestion.
    """
    if not isinstance(value, dict):
        raise ValueError(f'Invalid suggestion "{key}": entry must be an object')

    allowed_entry_fields = {"lexeme", "replacement"}
    extra_fields = set(value.keys()) - allowed_entry_fields
    if extra_fields:
        raise ValueError(
            f'Invalid suggestion "{key}": unexpected fields {sorted(extra_fields)}'
        )

    if "replacement" not in value or not isinstance(value["replacement"], dict):
        raise ValueError(
            f'Invalid suggestion "{key}": "replacement" must be an object'
        )

    lexeme = Lexeme(key, _normalize_link_list("lexeme", value.get("lexeme")))
    replacements = []
    for replacement_word, replacement_data in value["replacement"].items():
        if not isinstance(replacement_data, dict):
            raise ValueError(
                f'Invalid replacement "{replacement_word}" in "{key}": entry must be an object'
            )

        replacement_lexeme = Lexeme(
            replacement_word,
            _normalize_link_list("replacement.lexeme", replacement_data.get("lexeme")),
        )
        references = _normalize_link_list(
            "replacement.references", replacement_data.get("references")
        )
        replacements.append(Replacement(replacement_lexeme, references))

    return Suggestion(lexeme, replacements)


def get_suggestions(language: str, config_file: str = None):
    """
     This method can be used to obtain the suggestions for a given language as
     configured in the configuration
     file. If the configuration file is not specified, the default configuration file is used

    Parameters
    ----------
      language : str
        This parameter is the language code or locale (en: English)
      config_file : str
        This parameter contains the file path of a congiguration file

    Returns
    -------
      suggestions
        suggestions for a given language

    """
    config_file = get_all_language_resource_config_file(config_file)
    resources = get_all_language_resources(config_file)
    suggestions: Dict[str, Suggestion] = {}

    # Load all the suggestion files for a given language
    if language in resources:
        for suggestion_file in resources[language]:
            suggestion_file = pkg_resources.resource_filename(
                "inclusivewriting", suggestion_file
            )
            suggestion_file_data = read_file(suggestion_file)
            parsed_suggestions = json.loads(suggestion_file_data)
            if not isinstance(parsed_suggestions, dict):
                raise ValueError(
                    f"Invalid suggestion resource format in file: {suggestion_file}"
                )

            for key, value in parsed_suggestions.items():
                suggestion_key = key.lower()
                suggestion_value = _validate_and_build_suggestion(key, value)
                suggestions[suggestion_key] = suggestion_value

    return suggestions


def _build_phrase_pattern(phrase: str) -> str:
    """
    Build a regex for a phrase where spaces are treated as flexible whitespace.
    """
    tokens = phrase.split()
    return r"\s+".join(re.escape(token) for token in tokens)


def _find_suggestion_spans(
    text: str, suggestion_keys: List[str]
) -> List[Tuple[int, int, str]]:
    """
    Find non-overlapping phrase spans in text, preferring longer phrases first.
    """
    spans: List[Tuple[int, int, str]] = []
    occupied: List[Tuple[int, int]] = []
    ordered_keys = sorted(set(suggestion_keys), key=lambda key: (-len(key), key))

    for key in ordered_keys:
        pattern = re.compile(
            r"(?<!\w)" + _build_phrase_pattern(key) + r"(?!\w)",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            start, end = match.start(), match.end()
            if any(
                start < current_end and end > current_start
                for current_start, current_end in occupied
            ):
                continue
            occupied.append((start, end))
            spans.append((start, end, match.group(0)))

    spans.sort(key=lambda span: span[0])
    return spans


def detect_and_get_suggestions(language: str, text, config_file: str = None):
    """
     This method detects the language/locale and
     returns the suggestions for the language and the given text.
     If the configuration file is not specified, the default configuration file is used

    Parameters
    ----------
      text : str
        The text for which the suggestions are required
      config_file : str
        This parameter contains the file path of a congiguration file

    Returns
    -------
      suggestions
        suggestions for the current locale and the given text

    """
    config_file = get_all_language_resource_config_file(config_file)
    suggestions = get_suggestions(language, config_file)

    used_suggestions = set()
    spans = _find_suggestion_spans(text, list(suggestions.keys()))

    updated_text = ""
    cursor = 0
    for start, end, matched_text in spans:
        updated_text += text[cursor:start]
        updated_text += "<change>" + matched_text + "</change>"
        used_suggestions.add(matched_text)
        cursor = end
    updated_text += text[cursor:]

    return used_suggestions, suggestions, updated_text
