#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Test suite for locale utils
"""

import unittest
from inclusivewriting.locale_utils import (
    get_default_locale_encoding,
    get_default_locale_message_handler,
)


class LocaleUtilsTestSuite(unittest.TestCase):
    """
    Test cases for locale utils
    """

    def setUp(self):
        """
        Set up TestSuite
        """

    def test_get_default_locale_message_handler(self):
        """
        Test case to verify that there is a default message handler
        """
        _ = get_default_locale_message_handler()  # get message handler
        # This must return a message handler
        self.assertTrue(_ is not None)

    def test_get_default_locale_encoding(self):
        """
        Test case to verify that there is a default locale information
        """
        language, encoding = get_default_locale_encoding()  # get locale and encoding
        # These values must not be blank
        self.assertTrue(language is not None)
        self.assertTrue(encoding is not None)


if __name__ == "__main__":
    unittest.main()
