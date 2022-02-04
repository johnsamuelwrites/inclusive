#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Function to read input from the terminal"""


def read_input_from_terminal():
    """
    Read input from the terminal.
    The user needs to enter CTRL+D to stop
    """
    text = None
    try:
        text = input()
    except EOFError:
        text = ""

    return text
