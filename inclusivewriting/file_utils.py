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
    with open(filename, "r", encoding="utf-8") as text_file:
        text = text_file.read()
    return text


def write_file(filename, text):
    """
    Write text to a file

    parameters:
       filename: name or path of the file to write
       text: text to write
    """
    with open(filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)
