#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

def read_file(filename):
    text = None
    with open(filename, "r") as text_file:
        text = text_file.read()
    return text

