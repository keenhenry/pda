#!/usr/bin/env python

import requests
import shelve
import os
from listdb.GithubIssues import ListDB

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ListDBTests(unittest.TestCase):

    def setUp(self):
        self.db = ListDB()

    def testSyncLocalDBStore(self):

        # sync data before testing
        self.db.sync_local_dbstore()

        # retrieve remote data for testing
        r        = requests.get(self.db.url_issues, params={'state': 'open'}, auth=self.db.auth)
        db_local = shelve.open(os.path.abspath(self.db.DEFAULT_LOCAL_DBPATH), protocol=-1)

        for issue in r.json():

            task_no        = str(issue["number"])
            task_summary   = issue["title"]
            task_milestone = issue["milestone"]["title"] 
            task_prio      = ""
            task_type      = ""

            for label in issue["labels"]:
                if label["color"] == self.db.YELLOW: task_prio = label["name"]
                if label["color"] == self.db.GREEN:  task_type = label["name"]

            # after data syncing, the issue should be present in local store
            self.assertTrue(db_local.has_key(task_no))

            # the data stored at local should be the same as remote
            self.assertTrue(db_local[task_no]["summary"]   == task_summary)
            self.assertTrue(db_local[task_no]["type"]      == task_type)
            self.assertTrue(db_local[task_no]["priority"]  == task_prio)
            self.assertTrue(db_local[task_no]["milestone"] == task_milestone)

        db_local.close()

    def testRemoveTask(self):
        self.assertTrue(True)

    def testSyncRemoteDBStore(self):
        self.assertTrue(os.path.exists(self.db.DEFAULT_LOCAL_DBPATH))
        self.db.sync_remote_dbstore()
        self.assertFalse(os.path.exists(self.db.DEFAULT_LOCAL_DBPATH))

    def tearDown(self):
        del self.db

def main():
    unittest.main()

if __name__ == '__main__':
    main()
