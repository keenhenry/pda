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
        self.shelf_path = self.db.DEFAULT_LOCAL_DBPATH
        self.db.sync_local_dbstore()

    def tearDown(self):
        del self.db
        os.remove(self.shelf_path)

    def testSyncLocalDBStore(self):

        # retrieve remote data for testing
        r        = requests.get(self.db.url_issues, params={'state': 'open'}, auth=self.db.auth)

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
            self.assertTrue(self.db.shelf.has_key(task_no))

            # the data stored at local should be the same as remote
            self.assertTrue(self.db.shelf[task_no]["summary"]   == task_summary)
            self.assertTrue(self.db.shelf[task_no]["type"]      == task_type)
            self.assertTrue(self.db.shelf[task_no]["priority"]  == task_prio)
            self.assertTrue(self.db.shelf[task_no]["milestone"] == task_milestone)

    def testRemoveTask(self):

        # first try to collect a list of task numbers you want to remove
        removed_tasks, to_be_removed = [], True
        for task_no in self.db.shelf:
            if task_no != 'CMDS_HISTORY' and to_be_removed:
                removed_tasks.append(task_no)
                to_be_removed = (not to_be_removed)

        # second try to remove the tasks which are to be removed
        for task_no in removed_tasks:
            self.db.remove_task(int(task_no))

        # check if those removed tasks are really removed
        for task_no in removed_tasks:
            self.assertFalse(self.db.shelf.has_key(task_no))

        # remove non-existing task
        num_of_records_before_remove = len(self.db.shelf)
        self.db.remove_task(-1)
        num_of_records_after_remove = len(self.db.shelf)

        self.assertTrue(num_of_records_after_remove == num_of_records_before_remove)

    def testAddTask(self):

        # add one task
        num_of_tasks_before_add = len(self.db.shelf)

        task_no = self.db.add_task('test summary 1', 'todo', 'week', 'must')
        self.assertTrue(self.db.shelf.has_key(str(task_no)))

        num_of_tasks_after_add  = len(self.db.shelf)

        # num_of_tasks_before_add + 1 == num_of_tasks_after_add
        self.assertTrue(num_of_tasks_after_add == (num_of_tasks_before_add+1))

        # check data integrity
        self.assertTrue(self.db.shelf[str(task_no)]['summary'] == 'test summary 1')
        self.assertTrue(self.db.shelf[str(task_no)]['type'] == 'todo')
        self.assertTrue(self.db.shelf[str(task_no)]['milestone'] == 'week')
        self.assertTrue(self.db.shelf[str(task_no)]['priority'] == 'must')
        self.assertTrue(self.db.shelf['CMDS_HISTORY'][-1]['CMD'] == 'ADD')

    def testEditTask(self):

        # edit the first task
        first_task_no = self.db.shelf.keys()[0]

        num_of_tasks_before_edit = len(self.db.shelf) 
        old_prio      = self.db.shelf[first_task_no]['priority']

        self.db.edit_task(int(first_task_no), 'test summary 2')
        self.db.edit_task(int(first_task_no), new_tasktype='tolearn')
        self.db.edit_task(int(first_task_no), new_milestone='year')
        num_of_tasks_after_edit = len(self.db.shelf)

        # check data integrity
        self.assertTrue(self.db.shelf.has_key(first_task_no))
        self.assertTrue(num_of_tasks_after_edit == num_of_tasks_before_edit)

        self.assertTrue(self.db.shelf[first_task_no]['summary']   == 'test summary 2')
        self.assertTrue(self.db.shelf[first_task_no]['type']      == 'tolearn')
        self.assertTrue(self.db.shelf[first_task_no]['milestone'] == 'year')
        self.assertTrue(self.db.shelf[first_task_no]['priority']  == old_prio)
        self.assertTrue(self.db.shelf['CMDS_HISTORY'][-1]['CMD']  == 'EDIT')

    def testSyncRemoteDBStore(self):
        self.assertTrue(True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
