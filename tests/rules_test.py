#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Test suite for context-aware rule engine."""

import unittest

from inclusivewriting.rules import Rule, RuleEngine, RuleReplacement


class RulesTestSuite(unittest.TestCase):
    """Test cases for rule engine behavior."""

    def test_longer_phrase_wins_for_overlap(self):
        """
        Overlapping candidates should keep the longer phrase match.
        """
        rules = [
            Rule(
                rule_id="en:man",
                language="en",
                phrase="man",
                replacements=[RuleReplacement("person")],
            ),
            Rule(
                rule_id="en:man_hour",
                language="en",
                phrase="man hour",
                replacements=[RuleReplacement("person hour")],
            ),
        ]
        engine = RuleEngine(rules)
        matches = engine.find_matches("Estimated man hour effort")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].matched_text.lower(), "man hour")
        self.assertEqual(matches[0].rule_id, "en:man_hour")

    def test_excluded_context_prevents_match(self):
        """
        Excluded context patterns should suppress matches.
        """
        rules = [
            Rule(
                rule_id="en:master",
                language="en",
                phrase="master",
                replacements=[RuleReplacement("primary")],
                excluded_context_patterns=[r"master\s+of\s+science"],
            )
        ]
        engine = RuleEngine(rules, context_window=20)
        matches = engine.find_matches("She completed a master of science degree.")
        self.assertEqual(matches, [])

    def test_match_contains_metadata(self):
        """
        Rule metadata should be propagated to matches.
        """
        rule = Rule(
            rule_id="en:blacklist",
            language="en",
            phrase="blacklist",
            replacements=[RuleReplacement("blocklist")],
            severity="high",
            confidence=0.95,
            rationale="Term can carry exclusionary connotations.",
            auto_fix_safe=True,
        )
        engine = RuleEngine([rule])
        matches = engine.find_matches("Please update the blacklist.")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].severity, "high")
        self.assertEqual(matches[0].confidence, 0.95)
        self.assertTrue(matches[0].auto_fix_safe)


if __name__ == "__main__":
    unittest.main()
