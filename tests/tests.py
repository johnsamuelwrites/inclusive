#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Main file to run all the test suites
"""

import unittest

from tests.unicode_utils_test import UnicodeUtilsTestSuite
from tests.file_utils_test import FileUtilsTestSuite
from tests.locale_utils_test import LocaleUtilsTestSuite
from tests.suggestions_test import SuggestionsTestSuite
from tests.cli_test import CliTestSuite
from tests.resource_schema_test import ResourceSchemaTestSuite

if __name__ == "__main__":
    unicode_utils_tests = UnicodeUtilsTestSuite()
    file_utils_tests = FileUtilsTestSuite()
    suggestions_tests = SuggestionsTestSuite()
    locales_tests = LocaleUtilsTestSuite()
    cli_tests = CliTestSuite()
    resource_schema_tests = ResourceSchemaTestSuite()
    tests = unittest.TestSuite(
        [
            unicode_utils_tests,
            file_utils_tests,
            suggestions_tests,
            locales_tests,
            cli_tests,
            resource_schema_tests,
        ]
    )
    unittest.main()
