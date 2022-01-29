#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

def read_input_from_terminal():
    text = None
    try:
        text = input()
    except EOFError:
        text = ""
        pass

    return text

