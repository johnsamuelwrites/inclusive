#
# SPDX-FileCopyrightText: 2026 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Test suite for validating resource schema consistency
"""

import json
import unittest

import pkg_resources

from inclusivewriting.configuration import get_all_language_resources
from inclusivewriting.file_utils import read_file
from inclusivewriting.suggestions import _validate_and_build_suggestion


class ResourceSchemaTestSuite(unittest.TestCase):
    """
    Test cases for resource schema validation.
    """

    def test_all_configured_suggestion_resources_are_valid(self):
        """
        Validate all configured JSON suggestion resources.
        """
        resources = get_all_language_resources("./inclusivewriting/configuration.json")
        for resource_type, resource_files in resources.items():
            if resource_type == "separators":
                continue

            for resource_file in resource_files:
                path = pkg_resources.resource_filename("inclusivewriting", resource_file)
                parsed_data = json.loads(read_file(path))
                self.assertTrue(isinstance(parsed_data, dict))
                for key, value in parsed_data.items():
                    self.assertTrue(_validate_and_build_suggestion(key, value) is not None)


if __name__ == "__main__":
    unittest.main()
