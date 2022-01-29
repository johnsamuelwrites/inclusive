#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json
import pkg_resources


import typer
import re
from rich import print
from inclusivewriting.file_utils import read_file
from inclusivewriting.unicode_utils import get_all_punctuation_separator_characters
from inclusivewriting.locale_utils import get_default_locale_encoding, get_default_locale_message_handler

def get_all_language_resource_config_file(config_file:str=None):
    # File containing links to resources
    if config_file is None or config_file == "":
       all_language_resource_file = pkg_resources.resource_filename('inclusivewriting', 'configuration.json')
       return all_language_resource_file
    return config_file

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


def get_all_language_resources(config_file:str=None):
    """
         This method can be used to obtain all the language resources configured in the configuration 
         file. If the configuration file is not specified, the default configuration file is used

        Parameters
        ----------
          config_file : str
            This parameter contains the file path of a congiguration file

        Returns
        -------
          resources
            language resources

    """
    config_file = get_all_language_resource_config_file(config_file)
    resources = dict()
    resource_file_string = read_file(config_file)
    resources_parsed_data = json.loads(resource_file_string)
    for key, value in resources_parsed_data.items():
        resources[key] = value
    return resources


def get_suggestions(language: str, config_file:str=None):
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
    suggestions = dict()

    # Load all the suggestion files for a given language
    if language in resources:
        for suggestion_file in resources[language]:
            suggestion_file = pkg_resources.resource_filename('inclusivewriting', suggestion_file)
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

def detect_and_get_suggestions(text, config_file:str=None):
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
    language, encoding = get_default_locale_encoding()
    punctuations_separator = get_all_punctuation_separator_characters()
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
            updated_text = updated_text +  word 

    return used_suggestions, suggestions, updated_text
