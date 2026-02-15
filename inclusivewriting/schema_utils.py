#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Helpers for validating and normalizing resource schema fields."""

from typing import List


def normalize_string_list(field_name: str, value) -> List[str]:
    """Normalize a schema field to a list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError(
        f'Invalid "{field_name}" format: expected string or list of strings'
    )
