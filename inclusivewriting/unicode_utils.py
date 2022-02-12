#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

""" Get all the punctuation and separator characters in all languages"""

import sys
import re
import unicodedata
import pkg_resources

from inclusivewriting.file_utils import read_file, write_file
from inclusivewriting.configuration import (
    get_all_language_resources,
    get_all_language_resource_config_file,
)


def get_all_punctuation_separator_characters_from_resources(config_file: str = None):
    """
    Get all punctuation and characters, i.e., unicode category
    belonging to P or Z
    """
    punctuations_separator = set()
    config_file = get_all_language_resource_config_file(config_file)
    resources = get_all_language_resources(config_file)

    if "separators" in resources:
        separator_file = pkg_resources.resource_filename(
            "inclusivewriting", resources["separators"][0]
        )
        punctuations_separator = read_file(separator_file)
        punctuations_separator = set(punctuations_separator.split("|"))
    else:
        punctuations_separator = get_all_punctuation_separator_characters()

    return punctuations_separator


def get_all_punctuation_separator_characters():
    """
    Get all punctuation and characters, i.e., unicode category
    belonging to P or Z
    """
    characters = range(sys.maxunicode)

    # Escaping the characters ensures that these can be later used
    # splitting text
    punctuations_separator = set(
        re.escape(chr(i))
        for i in characters
        if unicodedata.category(chr(i)).startswith("P")
        or unicodedata.category(chr(i)).startswith("Z")
    )
    return punctuations_separator


def write_all_punctuation_separator_characters_to_resources(config_file: str = None):
    """
    Write all punctuation and characters to resources file
    """
    config_file = get_all_language_resource_config_file(config_file)
    resources = get_all_language_resources(config_file)
    if "separators" in resources:
        punctuations_separator = get_all_punctuation_separator_characters()
        separator_file = pkg_resources.resource_filename(
            "inclusivewriting", resources["separators"][0]
        )
        write_file( separator_file, "|".join(punctuations_separator))
