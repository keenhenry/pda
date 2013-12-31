#!/usr/bin/env python

"""
This is a module to command line tool `pda`
"""

import unittest
from listdb.ListDB import ListDB

# test fixture to test ListDB class
class ListDBTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = ListDB()

    def testHasTaskFalse(self):
        self.assertFalse(self.db._has_task(-1))
        self.assertFalse(self.db._has_task(-2))

    def testHasTaskTrue(self):
        self.assertTrue(self.db._has_task(4))
        self.assertTrue(self.db._has_task(5))
        self.assertTrue(self.db._has_task(6))
        self.assertTrue(self.db._has_task(8))

    @classmethod
    def tearDownClass(cls):
        #cls._db = ListDB()
        # do nothing for now
        print

def main():
    unittest.main()

if __name__ == '__main__':
    main()
