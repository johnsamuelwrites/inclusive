#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from tests.unicode_utils_test import *
from tests.file_utils_test import *
from tests.locale_utils_test import *
from tests.suggestions_test import *

if __name__ == '__main__':
    unicode_utils_tests = UnicodeUtilsTestSuite()
    file_utils_tests = FileUtilsTestSuite()
    suggestions_tests = SuggestionsTestSuite()
    locales_tests = LocaleUtilsTestSuite()
    tests = unittest.TestSuite([unicode_utils_tests, 
                                file_utils_tests,
                                suggestions_tests,
                                locales_tests])
    unittest.main()
