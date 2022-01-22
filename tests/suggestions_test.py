#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from inclusive.suggestions import *

class SuggestionsTestSuite(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_all_language_resources(self):
        resources = get_all_language_resources() # Get resources for all languages
        # There must be at least one language resource
        self.assertTrue(len(resources) > 0)

        # A language resource must not be empty
        for language in resources.keys():
            self.assertTrue(len(resources[language]) > 0)

    def test_en_language_resource(self):
        suggestions = get_suggestions("en") # Get suggestions for "en"
        # There must be at least one suggestion 
        self.assertTrue(len(suggestions) > 0)

    def test_detect_get_suggestions(self):
        text = "Once the user has installed the packages, he can run the application"
        used_suggestions, suggestions, updated_text = detect_and_get_suggestions(text)
        self.assertTrue(updated_text=="Once the user has installed the packages, <change>he</change>  can run the application")
        self.assertTrue("he" in used_suggestions)

if __name__ == '__main__':
    unittest.main()
