#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Test suite for unicode utils
"""
import unittest
from inclusivewriting.unicode_utils import get_all_punctuation_separator_characters


class UnicodeUtilsTestSuite(unittest.TestCase):
    """
    Test cases for unicode utils
    """

    def setUp(self):
        """
        Set up TestSuite
        """

    def test_all_punctuation_separator_characters(self):
        """
        Test case to check that there are at least one
        separator/punctuation character
        """
        punctuations_separator = get_all_punctuation_separator_characters()
        # Ensure that we have more than zero separator/punctuation characters
        self.assertTrue(len(punctuations_separator) > 0)


if __name__ == "__main__":
    unittest.main()
