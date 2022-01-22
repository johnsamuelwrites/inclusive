#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json

import typer
import re
from rich import print
from inclusive.file_utils import read_file
from inclusive.unicode_utils import get_all_punctuation_separator_characters
from inclusive.locale_utils import get_default_locale_encoding, get_default_locale_message_handler


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
                suggestions[key] = value

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
            updated_text = updated_text + "<change>" + word + "</change> "
            used_suggestions.add(word)
        else:
            updated_text = updated_text +  word 

    return used_suggestions, suggestions, updated_text
