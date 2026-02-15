#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Functions to handle suggestions for different languages."""

from typing import Dict, List, Tuple

from inclusivewriting.configuration import (
    get_all_language_resource_config_file,
    get_all_language_resources as _configuration_language_resources,
)
from inclusivewriting.rulepacks import load_rulepack
from inclusivewriting.schema_utils import normalize_string_list
from inclusivewriting.rules import RuleEngine, RuleMatch


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


def get_all_language_resources(config_file: str = None):
    """Backward-compatible re-export from configuration module."""
    return _configuration_language_resources(config_file)


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

    lexeme = Lexeme(key, normalize_string_list("lexeme", value.get("lexeme")))
    replacements = []
    for replacement_word, replacement_data in value["replacement"].items():
        if not isinstance(replacement_data, dict):
            raise ValueError(
                f'Invalid replacement "{replacement_word}" in "{key}": entry must be an object'
            )

        replacement_lexeme = Lexeme(
            replacement_word,
            normalize_string_list("replacement.lexeme", replacement_data.get("lexeme")),
        )
        references = normalize_string_list(
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
    rules = load_rulepack(language, config_file)
    return _build_suggestions_from_rules(rules)


def _build_suggestions_from_rules(rules) -> Dict[str, Suggestion]:
    """
    Convert loaded rules to backward-compatible suggestion objects.
    """
    suggestions: Dict[str, Suggestion] = {}
    for rule in rules:
        replacement_lexemes = []
        for replacement in rule.replacements:
            replacement_lexeme = Lexeme(replacement.value, [])
            replacement_lexemes.append(
                Replacement(replacement_lexeme, replacement.references)
            )
        suggestions[rule.phrase.lower()] = Suggestion(
            Lexeme(rule.phrase, []), replacement_lexemes
        )
    return suggestions


def _highlighted_text_from_matches(text: str, matches: List[RuleMatch]) -> str:
    """
    Build output text by wrapping matched spans with <change> tags.
    """
    output = ""
    cursor = 0
    for match in matches:
        output += text[cursor : match.start]
        output += "<change>" + match.matched_text + "</change>"
        cursor = match.end
    output += text[cursor:]
    return output


def detect_and_get_rule_matches(
    language: str, text: str, config_file: str = None
) -> Tuple[set, Dict[str, Suggestion], str, List[RuleMatch]]:
    """
    Detect possible issues in text and return rule-level matches.
    """
    config_file = get_all_language_resource_config_file(config_file)
    rules = load_rulepack(language, config_file)
    suggestions = _build_suggestions_from_rules(rules)
    matches = RuleEngine(rules).find_matches(text)
    used_suggestions = {match.matched_text for match in matches}
    updated_text = _highlighted_text_from_matches(text, matches)
    return used_suggestions, suggestions, updated_text, matches


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
    used_suggestions, suggestions, updated_text, _ = detect_and_get_rule_matches(
        language, text, config_file
    )
    return used_suggestions, suggestions, updated_text
