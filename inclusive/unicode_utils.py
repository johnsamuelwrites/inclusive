#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
import re
import unicodedata

def get_all_punctuation_separator_characters():
    characters = range(sys.maxunicode)
    # Get all punctuation and characters, i.e., unicode category
    # belonging to P or Z
    # Escaping the characters ensures that these can be later used
    # splitting text
    punctuations_separator = set(re.escape(chr(i)) for i in characters
                             if unicodedata.category(chr(i)).startswith("P") or
                                unicodedata.category(chr(i)).startswith("Z"))
    return(punctuations_separator)

