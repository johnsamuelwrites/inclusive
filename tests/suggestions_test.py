#

# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Test suite for suggestions
"""

import unittest
from inclusivewriting.suggestions import (
    get_all_language_resources,
    get_suggestions,
    detect_and_get_suggestions,
    Lexeme,
    Replacement,
    Suggestion,
    _validate_and_build_suggestion,
)


class SuggestionsTestSuite(unittest.TestCase):
    """
    Test cases for suggestions
    """

    def setUp(self):
        """
        Set up TestSuite
        """
        self.config_file = "./inclusivewriting/configuration.json"

    def test_get_all_language_resources(self):
        """
        Verify that there is at least one language resource
        """
        resources = get_all_language_resources(
            self.config_file
        )  # Get resources for all languages
        # There must be at least one language resource
        self.assertTrue(len(resources) > 0)

        # A language resource must not be empty
        for _, language_resources in resources.items():
            self.assertTrue(len(language_resources) > 0)

    def test_en_language_resource(self):
        """
        Verify English language resource
        """
        suggestions = get_suggestions(
            "en", self.config_file
        )  # Get suggestions for "en"
        # There must be at least one suggestion
        self.assertTrue(len(suggestions) > 0)

    def test_detect_get_suggestions(self):
        """
        Verify whether the possible issue in the following text
        is detected and the suggestions are obtained
        """
        text = "Once the user has installed the packages, he can run the application"
        used_suggestions, suggestions, updated_text = detect_and_get_suggestions(
            "en", text, self.config_file
        )
        self.assertTrue(
            updated_text
            == "Once the user has installed the packages,"
            + " <change>he</change> can run the application"
        )
        self.assertTrue("he" in used_suggestions)
        self.assertTrue(len(suggestions) > 0)

    def test_get_all_language_resources_without_config(self):
        """
        Verify that there are default language resources
        when the configuration file is missing
        """
        resources = get_all_language_resources(
            ""
        )  # Get resources for all languages and empty configuration file
        # There must be at least one language resource
        self.assertTrue(len(resources) > 0)

        # A language resource must not be empty
        for _, language_resources in resources.items():
            self.assertTrue(len(language_resources) > 0)

    def test_en_language_resource_without_config(self):
        """
        Verify that there is English language resource
        when the configuration file is missing
        """
        suggestions = get_suggestions(
            "en", ""
        )  # Get suggestions for "en" and empty configuration file
        # There must be at least one suggestion
        self.assertTrue(len(suggestions) > 0)

    def test_detect_get_suggestions_without_config(self):
        """
        Verify whether possible issues with the following text is
        detected and some suggestions are obtained.
        """
        text = "Once the user has installed the packages, he can run the application"
        used_suggestions, suggestions, updated_text = detect_and_get_suggestions(
            "en", text, None
        )  # No configuration file
        self.assertTrue(
            updated_text
            == "Once the user has installed the packages,"
            + " <change>he</change> can run the application"
        )
        self.assertTrue("he" in used_suggestions)
        self.assertTrue(len(suggestions) > 0)

    def test_detect_multiword_suggestions(self):
        """
        Verify that multi-word suggestions are detected.
        """
        text = "Estimated man hour and man hours."
        used_suggestions, suggestions, updated_text = detect_and_get_suggestions(
            "en", text, self.config_file
        )
        self.assertTrue(
            updated_text
            == "Estimated <change>man hour</change> and <change>man hours</change>."
        )
        self.assertTrue("man hour" in used_suggestions)
        self.assertTrue("man hours" in used_suggestions)
        self.assertTrue(len(suggestions) > 0)

    def test_suggestion_schema_validation(self):
        """
        Verify that invalid suggestion entries are rejected.
        """
        with self.assertRaises(ValueError):
            _validate_and_build_suggestion(
                "test phrase", {"lexeme": [], "replacement": {}, "unexpected": {}}
            )

    def test_class_lexeme(self):
        """
        Test the Lexeme class
        """
        lexeme = Lexeme("he", ["https://www.wikidata.org/wiki/Lexeme:L485"])
        self.assertEqual(
            str(lexeme), '"he" : [ "https://www.wikidata.org/wiki/Lexeme:L485" ]'
        )

    def test_class_replacement(self):
        """
        Test the Replacement class
        """
        replacement_lexeme = Lexeme(
            "they", ["https://www.wikidata.org/wiki/Lexeme:L371"]
        )
        replacement = Replacement(
            replacement_lexeme, ["https://en.wikipedia.org/wiki/Inclusive_language"]
        )
        self.assertEqual(
            str(replacement),
            '"they" : { "links" : ["https://www.wikidata.org/wiki/Lexeme:L371"],'
            + ' "references" : ["https://en.wikipedia.org/wiki/Inclusive_language" ] }',
        )

    def test_class_suggestion(self):
        """
        Test the Suggestion class
        """
        lexeme = Lexeme("he", ["https://www.wikidata.org/wiki/Lexeme:L485"])
        replacement_lexeme = Lexeme(
            "they", ["https://www.wikidata.org/wiki/Lexeme:L371"]
        )
        replacement = Replacement(
            replacement_lexeme, ["https://en.wikipedia.org/wiki/Inclusive_language"]
        )
        suggestion = Suggestion(lexeme, [replacement])
        self.assertEqual(
            str(suggestion),
            '{ "he" : {"they" : { "links" : ["https://www.wikidata.org/wiki/Lexeme:L371"],'
            + ' "references" : ["https://en.wikipedia.org/wiki/Inclusive_language" ] }}}',
        )


if __name__ == "__main__":
    unittest.main()
