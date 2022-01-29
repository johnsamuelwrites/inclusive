#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from inclusivewriting.locale_utils import *

class LocaleUtilsTestSuite(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_default_locale_message_handler(self):
        _ = get_default_locale_message_handler() # get message handler
        # This must return a message handler 
        self.assertTrue(_ != None)

    def test_get_default_locale_encoding(self):
        language, encoding = get_default_locale_encoding() # get locale and encoding
        # These values must not be blank
        self.assertTrue(language != None)
        self.assertTrue(encoding != None)

if __name__ == '__main__':
    unittest.main()
