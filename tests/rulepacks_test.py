#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Test suite for multilingual rule-packs."""

import unittest

from inclusivewriting.rulepacks import (
    list_available_languages,
    load_rulepack,
    validate_rulepack,
)


class RulepacksTestSuite(unittest.TestCase):
    """Test cases for loading and validating rule-packs."""

    def setUp(self):
        self.config_file = "./inclusivewriting/configuration.json"

    def test_list_available_languages(self):
        """
        Configured languages should include English.
        """
        languages = list_available_languages(self.config_file)
        self.assertTrue("en" in languages)
        self.assertTrue("en_US" in languages)

    def test_load_rulepack(self):
        """
        Loading a configured rule-pack should return rules.
        """
        rules = load_rulepack("en", self.config_file)
        self.assertTrue(len(rules) > 0)
        self.assertTrue(all(rule.language == "en" for rule in rules))

    def test_validate_rulepack(self):
        """
        Configured English rule-pack should validate successfully.
        """
        errors = validate_rulepack("en", self.config_file)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
