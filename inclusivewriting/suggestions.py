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

import pkg_resources

from inclusivewriting.file_utils import read_file
from inclusivewriting.unicode_utils import (
    get_all_punctuation_separator_characters_from_resources,
)
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
        self.links = links

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
        self.references = references

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
    suggestions = {}

    # Load all the suggestion files for a given language
    if language in resources:
        for suggestion_file in resources[language]:
            suggestion_file = pkg_resources.resource_filename(
                "inclusivewriting", suggestion_file
            )
            suggestion_file_data = read_file(suggestion_file)
            suggestion = json.loads(suggestion_file_data)
            for key, value in suggestion.items():
                lexeme = Lexeme(key, value["lexeme"])
                replacements = []
                for replacement in value["replacement"]:
                    replacement_lexeme = Lexeme(
                        replacement, value["replacement"][replacement]["lexeme"]
                    )
                    replacement = Replacement(
                        replacement_lexeme,
                        value["replacement"][replacement]["references"],
                    )
                    replacements.append(replacement)

                suggestion_value = Suggestion(lexeme, replacements)
                suggestions[key] = suggestion_value

    return suggestions


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
    # punctuations_separator = get_all_punctuation_separator_characters()
    punctuations_separator = get_all_punctuation_separator_characters_from_resources(
        config_file
    )
    suggestions = get_suggestions(language, config_file)

    punctuations_separator = "|".join(punctuations_separator)
    words = re.split("(" + punctuations_separator + ")", text)
    used_suggestions = set()

    updated_text = ""
    for word in words:
        if word.lower() in suggestions:
            updated_text = updated_text + "<change>" + word + "</change>"
            used_suggestions.add(word)
        else:
            updated_text = updated_text + word

    return used_suggestions, suggestions, updated_text
