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
from inclusivewriting.unicode_utils import get_all_punctuation_separator_characters
from inclusivewriting.locale_utils import get_default_locale_encoding, get_default_locale_message_handler

class Lexeme:
    def __init__(self, value, links=list()):
        self.value = value
        self.links = links

    def get_value(self):
        return self.value

    def get_links(self):
        return self.links

    def __str__(self):
        return '"' + self.get_value() + '" : ' + "[ " + ", ".join('"{0}"'.format(link) for link in self.get_links())  + " ]"

class Replacement:
    def __init__(self, lexeme, references=list()):
        self.lexeme = lexeme
        self.references = references

    def get_value(self):
        return self.lexeme.get_value()

    def __str__(self):
        return '"' + self.get_value() + '" : ' + '{ "links" : [' + ", ".join('"{0}"'.format(link) for link in self.lexeme.get_links()) + '], "references" : [' + ", ".join('"{0}"'.format(reference) for reference in self.references)  + " ] " "}"

class Suggestion:
    def __init__(self, lexeme, replacement_lexemes):
        self.lexeme = lexeme
        self.replacement_lexemes = replacement_lexemes

    def get_replacement_lexemes(self):
        return self.replacement_lexemes

    def get_lexeme(self):
        return self.lexeme

    def __str__(self):
        return "{ " + '"' + str(self.get_lexeme().get_value()) + '" : {'  + ", ".join(str(replacement) for replacement in self.get_replacement_lexemes())  + "}" "}" 

# File containing links to resources
all_language_resource_file = "./configuration.json"

def get_all_language_resources():
    resources = dict()
    resource_file_string = read_file(all_language_resource_file)
    resources_parsed_data = json.loads(resource_file_string)
    for key, value in resources_parsed_data.items():
        resources[key] = value
    return resources


def get_suggestions(language: str):
    resources = get_all_language_resources()
    suggestions = dict()

    # Load all the suggestion files for a given language
    if language in resources:
        for suggestion_file in resources[language]:
            suggestion_file_data = read_file(suggestion_file)
            suggestion = json.loads(suggestion_file_data)
            for key, value in suggestion.items():
                lexeme =  Lexeme(key, value["lexeme"])
                replacements = list()
                for replacement in value["replacement"]:
                    replacement_lexeme = Lexeme(replacement, value["replacement"][replacement]["lexeme"])
                    replacement = Replacement(replacement_lexeme, value["replacement"][replacement]["references"])
                    replacements.append(replacement)

                suggestion_value = Suggestion(lexeme, replacements)
                suggestions[key] = suggestion_value

    return suggestions

def detect_and_get_suggestions(text):
    language, encoding = get_default_locale_encoding()
    punctuations_separator = get_all_punctuation_separator_characters()
    suggestions = get_suggestions(language)

    punctuations_separator = "|".join(punctuations_separator)
    words = re.split("(" + punctuations_separator + ")", text)
    used_suggestions = set()
    
    updated_text = ""
    for word in words:
        if word.lower() in suggestions:
            updated_text = updated_text + "<change>" + word + "</change>"
            used_suggestions.add(word)
        else:
            updated_text = updated_text +  word 

    return used_suggestions, suggestions, updated_text
