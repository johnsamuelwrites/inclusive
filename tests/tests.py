#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from tests.unicode_utils_test import *
from tests.file_utils_test import *

if __name__ == '__main__':
    unicode_utils_tests = UnicodeUtilsTestSuite()
    file_utils_tests = FileUtilsTestSuite()
    tests = unittest.TestSuite([unicode_utils_tests, file_utils_tests])
    unittest.main()
