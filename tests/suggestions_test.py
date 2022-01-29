#

# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from inclusivewriting.suggestions import *

class SuggestionsTestSuite(unittest.TestCase):
    def setUp(self):
        self.config_file = "./inclusivewriting/configuration.json"
        pass

    def test_get_all_language_resources(self):
        resources = get_all_language_resources(self.config_file) # Get resources for all languages
        # There must be at least one language resource
        self.assertTrue(len(resources) > 0)

        # A language resource must not be empty
        for language in resources.keys():
            self.assertTrue(len(resources[language]) > 0)

    def test_en_language_resource(self):
        suggestions = get_suggestions("en", self.config_file) # Get suggestions for "en"
        # There must be at least one suggestion 
        self.assertTrue(len(suggestions) > 0)

    def test_detect_get_suggestions(self):
        text = "Once the user has installed the packages, he can run the application"
        used_suggestions, suggestions, updated_text = detect_and_get_suggestions(text, self.config_file)
        self.assertTrue(updated_text=="Once the user has installed the packages, <change>he</change> can run the application")
        self.assertTrue("he" in used_suggestions)

    def test_get_all_language_resources_without_config(self):
        resources = get_all_language_resources("") # Get resources for all languages and empty configuration file
        # There must be at least one language resource
        self.assertTrue(len(resources) > 0)

        # A language resource must not be empty
        for language in resources.keys():
            self.assertTrue(len(resources[language]) > 0)

    def test_en_language_resource_without_config(self):
        suggestions = get_suggestions("en", "") # Get suggestions for "en" and empty configuration file
        # There must be at least one suggestion 
        self.assertTrue(len(suggestions) > 0)

    def test_detect_get_suggestions_without_config(self):
        text = "Once the user has installed the packages, he can run the application"
        used_suggestions, suggestions, updated_text = detect_and_get_suggestions(text, None) # No configuration file
        self.assertTrue(updated_text=="Once the user has installed the packages, <change>he</change> can run the application")
        self.assertTrue("he" in used_suggestions)
    def test_class_Lexeme(self):
        lexeme = Lexeme("he", ["https://www.wikidata.org/wiki/Lexeme:L485"])
        self.assertEqual(str(lexeme), '"he" : [ "https://www.wikidata.org/wiki/Lexeme:L485" ]')

    def test_class_Replacement(self):
        replacement_lexeme = Lexeme("they", ["https://www.wikidata.org/wiki/Lexeme:L371"])
        replacement = Replacement(replacement_lexeme,
                   ["https://en.wikipedia.org/wiki/Inclusive_language"])
        self.assertEqual(str(replacement), '"they" : { "links" : ["https://www.wikidata.org/wiki/Lexeme:L371"], "references" : ["https://en.wikipedia.org/wiki/Inclusive_language" ] }')

    def test_class_Suggestion(self):
        lexeme = Lexeme("he", ["https://www.wikidata.org/wiki/Lexeme:L485"])
        replacement_lexeme = Lexeme("they", ["https://www.wikidata.org/wiki/Lexeme:L371"])
        replacement = Replacement(replacement_lexeme,
                   ["https://en.wikipedia.org/wiki/Inclusive_language"])
        suggestion = Suggestion(lexeme, [replacement])
        self.assertEqual(str(suggestion), '{ "he" : {"they" : { "links" : ["https://www.wikidata.org/wiki/Lexeme:L371"], "references" : ["https://en.wikipedia.org/wiki/Inclusive_language" ] }}}')

if __name__ == '__main__':
    unittest.main()
