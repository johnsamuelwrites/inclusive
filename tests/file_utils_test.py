#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from inclusivewriting.file_utils import read_file

class FileUtilsTestSuite(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_file(self):
        text = read_file(__file__) # Get current filename
        # The length must be greater than 0 
        self.assertTrue(len(text) > 0)

if __name__ == '__main__':
    unittest.main()
