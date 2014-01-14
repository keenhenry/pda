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

    @classmethod
    def setUpClass(cls):
        cls.db = ListDB()

    @classmethod
    def tearDownClass(cls):
        del cls.db

    def setUp(self):
        self.db.sync_local_dbstore()
        # pass

    def tearDown(self):
        self.db.sync_remote_dbstore()
        # pass

    def testSyncLocalDBStore(self):

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

        # first try to collect a list of task numbers you want to remove
        removed_tasks = []
        to_be_removed = True
        db_local = shelve.open(os.path.abspath(self.db.DEFAULT_LOCAL_DBPATH), protocol=-1)
        for task_no in db_local:
            if task_no != 'CMDS_HISTORY' and to_be_removed:
                removed_tasks.append(task_no)
                to_be_removed = (not to_be_removed)
        db_local.close()

        # second try to remove the tasks which are to be removed
        for task_no in removed_tasks:
            self.db.remove_task(int(task_no))

        # check if those removed tasks are really removed
        db_local = shelve.open(os.path.abspath(self.db.DEFAULT_LOCAL_DBPATH), protocol=-1)
        for task_no in removed_tasks:
            self.assertFalse(db_local.has_key(task_no))
        db_local.close()

    def testSyncRemoteDBStore(self):
        self.assertTrue(True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
