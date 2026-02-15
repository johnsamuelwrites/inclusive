#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Context-aware rule engine for inclusive language checks."""

from dataclasses import dataclass, field
import re
from typing import List, Pattern


@dataclass
# pylint: disable=too-few-public-methods
class RuleReplacement:
    """A replacement option for a rule."""

    value: str
    references: List[str] = field(default_factory=list)


@dataclass
# pylint: disable=too-many-instance-attributes
class Rule:
    """A context-aware language rule."""

    rule_id: str
    language: str
    phrase: str
    replacements: List[RuleReplacement]
    severity: str = "medium"
    confidence: float = 0.8
    rationale: str = ""
    auto_fix_safe: bool = False
    required_context_patterns: List[str] = field(default_factory=list)
    excluded_context_patterns: List[str] = field(default_factory=list)

    def compile_pattern(self) -> Pattern[str]:
        """Compile a word-boundary aware pattern for this phrase."""
        tokens = self.phrase.split()
        escaped = [re.escape(token) for token in tokens]
        phrase_pattern = r"\s+".join(escaped)
        return re.compile(r"(?<!\w)" + phrase_pattern + r"(?!\w)", re.IGNORECASE)


@dataclass
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class RuleMatch:
    """A match produced by the rule engine."""

    rule_id: str
    start: int
    end: int
    matched_text: str
    replacements: List[str]
    severity: str
    confidence: float
    rationale: str
    auto_fix_safe: bool


class RuleEngine:
    """Runs a set of rules over input text."""

    def __init__(self, rules: List[Rule], context_window: int = 40):
        self.rules = list(rules)
        self.context_window = context_window

    def _context_for_span(self, text: str, start: int, end: int) -> str:
        left = max(0, start - self.context_window)
        right = min(len(text), end + self.context_window)
        return text[left:right]

    def _context_is_valid(self, rule: Rule, context: str) -> bool:
        if rule.required_context_patterns:
            if not any(
                re.search(pattern, context, flags=re.IGNORECASE)
                for pattern in rule.required_context_patterns
            ):
                return False

        if rule.excluded_context_patterns:
            if any(
                re.search(pattern, context, flags=re.IGNORECASE)
                for pattern in rule.excluded_context_patterns
            ):
                return False

        return True

    def find_matches(self, text: str) -> List[RuleMatch]:
        """
        Return non-overlapping matches, prioritizing longer phrases first.
        """
        matches: List[RuleMatch] = []
        occupied_spans: List[tuple] = []
        ordered_rules = sorted(
            self.rules,
            key=lambda current_rule: (
                -len(current_rule.phrase),
                current_rule.rule_id,
            ),
        )

        for rule in ordered_rules:
            pattern = rule.compile_pattern()
            for candidate in pattern.finditer(text):
                start, end = candidate.start(), candidate.end()
                if any(
                    start < other_end and end > other_start
                    for other_start, other_end in occupied_spans
                ):
                    continue

                context = self._context_for_span(text, start, end)
                if not self._context_is_valid(rule, context):
                    continue

                occupied_spans.append((start, end))
                matches.append(
                    RuleMatch(
                        rule_id=rule.rule_id,
                        start=start,
                        end=end,
                        matched_text=candidate.group(0),
                        replacements=[
                            replacement.value for replacement in rule.replacements
                        ],
                        severity=rule.severity,
                        confidence=rule.confidence,
                        rationale=rule.rationale,
                        auto_fix_safe=rule.auto_fix_safe,
                    )
                )

        matches.sort(key=lambda current_match: current_match.start)
        return matches
