#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

""" Get all the punctuation and separator characters in all languages"""

import sys
import re
import unicodedata


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
