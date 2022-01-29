#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from inclusivewriting.unicode_utils import get_all_punctuation_separator_characters

class UnicodeUtilsTestSuite(unittest.TestCase):
    def setUp(self):
        pass

    def test_all_punctuation_separator_characters(self):
        punctuations_separator = get_all_punctuation_separator_characters()
        # Ensure that we have more than zero separator/punctuation characters
        self.assertTrue(len(punctuations_separator) > 0)

if __name__ == '__main__':
    unittest.main()
