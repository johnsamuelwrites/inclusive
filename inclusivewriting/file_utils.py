#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Function to read data from a file"""


def read_file(filename):
    """
    Read input from a file

    parameters:
       filename: name or path of the file to be read
    """
    text = None
    with open(filename, "r", encoding="utf8") as text_file:
        text = text_file.read()
    return text
