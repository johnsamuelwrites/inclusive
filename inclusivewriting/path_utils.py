#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Helpers for resolving package resource file paths."""

from pathlib import Path


def package_file_path(relative_path: str) -> str:
    """
    Resolve a package-relative file path to an absolute filesystem path.
    """
    cleaned = relative_path.lstrip("./\\")
    return str(Path(__file__).resolve().parent / cleaned)
