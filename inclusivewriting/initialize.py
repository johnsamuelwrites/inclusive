#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

""" Initialize the separators"""

from inclusivewriting.unicode_utils import (
    write_all_punctuation_separator_characters_to_resources,
)


def initialize(config_file: str = None):
    """
    Initialize the application (if required) by
    writing the separators/punctuation characters to a file
    """
    write_all_punctuation_separator_characters_to_resources(config_file)


if __name__ == "__main__":
    initialize()
