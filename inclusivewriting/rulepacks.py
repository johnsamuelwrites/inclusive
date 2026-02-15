#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Multilingual rule-pack loading and validation."""

import json
from typing import Dict, List

import pkg_resources

from inclusivewriting.configuration import (
    get_all_language_resource_config_file,
    get_all_language_resources,
)
from inclusivewriting.file_utils import read_file
from inclusivewriting.schema_utils import normalize_string_list
from inclusivewriting.rules import Rule, RuleReplacement


def _build_rule(language: str, phrase: str, payload: Dict) -> Rule:
    if not isinstance(payload, dict):
        raise ValueError(f'Invalid rule "{phrase}": entry must be an object')
    if "replacement" not in payload or not isinstance(payload["replacement"], dict):
        raise ValueError(f'Invalid rule "{phrase}": "replacement" must be an object')

    replacements = []
    for replacement_value, replacement_payload in payload["replacement"].items():
        if not isinstance(replacement_payload, dict):
            raise ValueError(
                f'Invalid replacement "{replacement_value}" in "{phrase}": entry must be an object'
            )
        replacements.append(
            RuleReplacement(
                value=replacement_value,
                references=normalize_string_list(
                    "replacement.references", replacement_payload.get("references")
                ),
            )
        )

    rule_id = f"{language}:{phrase.lower().replace(' ', '_')}"
    return Rule(
        rule_id=rule_id,
        language=language,
        phrase=phrase,
        replacements=replacements,
    )


def list_available_languages(config_file: str = None) -> List[str]:
    """List all configured languages with rule resources."""
    config_file = get_all_language_resource_config_file(config_file)
    resources = get_all_language_resources(config_file)
    return sorted(language for language in resources if language != "separators")


def load_rulepack(language: str, config_file: str = None) -> List[Rule]:
    """Load a language rule-pack from configured resource files."""
    config_file = get_all_language_resource_config_file(config_file)
    resources = get_all_language_resources(config_file)

    rules: List[Rule] = []
    for relative_path in resources.get(language, []):
        full_path = pkg_resources.resource_filename("inclusivewriting", relative_path)
        parsed = json.loads(read_file(full_path))
        if not isinstance(parsed, dict):
            raise ValueError(f"Invalid resource format in file: {relative_path}")

        for phrase, payload in parsed.items():
            rules.append(_build_rule(language, phrase, payload))

    return rules


def validate_rulepack(language: str, config_file: str = None) -> List[str]:
    """
    Validate a language rule-pack and return a list of errors.
    An empty list means the rule-pack is valid.
    """
    errors = []
    try:
        rules = load_rulepack(language, config_file)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]

    seen_ids = set()
    for rule in rules:
        if rule.rule_id in seen_ids:
            errors.append(f"Duplicate rule id: {rule.rule_id}")
        seen_ids.add(rule.rule_id)
        if len(rule.replacements) == 0:
            errors.append(f"Rule without replacements: {rule.rule_id}")

    return errors
