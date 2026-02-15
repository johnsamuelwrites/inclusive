#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Test suite for CLI behavior
"""

import json
import os
import tempfile
import unittest

from typer.testing import CliRunner

from inclusivewriting.__main__ import app


class CliTestSuite(unittest.TestCase):
    """
    Test cases for CLI behavior
    """

    def setUp(self):
        """
        Set up TestSuite
        """
        self.runner = CliRunner()

    def _write_temp_file(self, content: str) -> str:
        """
        Create a temporary file with the provided content and return its path.
        """
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as temp_file:
            temp_file.write(content)
        return path

    def test_detect_exit_code_when_issues_found(self):
        """
        Detect command should return exit code 1 when issues are found.
        """
        file_path = self._write_temp_file("The user said he will do it.")
        try:
            result = self.runner.invoke(
                app,
                ["en", "--filepath", file_path, "--quiet", "--no-color"],
            )
            self.assertEqual(result.exit_code, 1)
            self.assertTrue("<change>he</change>" not in result.stdout)
            self.assertTrue("he" in result.stdout)
        finally:
            os.unlink(file_path)

    def test_detect_json_output(self):
        """
        Detect command should provide machine-readable JSON output.
        """
        file_path = self._write_temp_file("Estimated man hours.")
        try:
            result = self.runner.invoke(
                app,
                ["en", "--filepath", file_path, "--format", "json"],
            )
            self.assertEqual(result.exit_code, 1)
            output = json.loads(result.stdout)
            self.assertEqual(output["issues_found"], 1)
            self.assertEqual(output["matches"][0]["match"].lower(), "man hours")
            self.assertTrue("person hours" in output["matches"][0]["replacements"])
        finally:
            os.unlink(file_path)

    def test_detect_exit_code_when_no_issues(self):
        """
        Detect command should return exit code 0 when no issues are found.
        """
        file_path = self._write_temp_file("This sentence is inclusive.")
        try:
            result = self.runner.invoke(
                app, ["en", "--filepath", file_path, "--quiet"]
            )
            self.assertEqual(result.exit_code, 0)
        finally:
            os.unlink(file_path)

    def test_detect_invalid_format(self):
        """
        Detect command should return exit code 2 for invalid formats.
        """
        file_path = self._write_temp_file("This sentence is inclusive.")
        try:
            result = self.runner.invoke(
                app, ["en", "--filepath", file_path, "--format", "yaml"]
            )
            self.assertEqual(result.exit_code, 2)
        finally:
            os.unlink(file_path)


if __name__ == "__main__":
    unittest.main()
