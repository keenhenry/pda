#!/usr/bin/env python

"""
This is a module to unit-test `ListDB` class.
"""

from ListDB import ListDB
import unittest

class ListDBTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = ListDB()

    def testHasTaskFalse(self):
        self.assertFalse(self.db._has_task(-1))
        self.assertFalse(self.db._has_task(-2))
        self.assertFalse(self.db._has_task('why'))

    def testHasTaskTrue(self):
        self.assertFalse(self.db._has_task(4))
        self.assertFalse(self.db._has_task(5))
        self.assertFalse(self.db._has_task(6))
        self.assertFalse(self.db._has_task(8))

    @classmethod
    def tearDownClass(cls):
        #cls._db = ListDB()
        # do nothing for now
        print

def main():
    unittest.main()

if __name__ == '__main__':
    main()
