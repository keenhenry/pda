#!/usr/bin/env python

import requests
import os
import io
from pda.listdb.ListDB import GithubIssues
from pda.listdb.Config import PdaConfig

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ConfigLocalModeTests(unittest.TestCase):

    localmode_test_config = """
[pda]
database-path = /tmp/.pdastore
[github]
username   = someone
repo-name  = todo
"""

    cfg = PdaConfig(io.BytesIO(localmode_test_config))

    def testLocalDBPath(self):
        self.assertTrue(ConfigLocalModeTests.cfg.local_db_path == '/tmp/.pdastore')

    def testUserName(self):
        self.assertTrue(ConfigLocalModeTests.cfg.username == 'someone')

    def testRepoName(self):
        self.assertTrue(ConfigLocalModeTests.cfg.reponame == 'todo')

    def testAuthToken(self):
        self.assertTrue(ConfigLocalModeTests.cfg.authtoken is None)

    def testRemoteMode(self):
        self.assertTrue(ConfigLocalModeTests.cfg.remote_mode == False)


class ConfigRemoteModeTests(unittest.TestCase):

    remotemode_test_config = """
[pda]
database-path = /tmp/.pdastore
[github]
username   = someoneelse
repo-name  = todo
auth-token = lalala
"""

    cfg = PdaConfig(io.BytesIO(remotemode_test_config))

    def testLocalDBPath(self):
        self.assertTrue(ConfigRemoteModeTests.cfg.local_db_path == '/tmp/.pdastore')

    def testUserName(self):
        self.assertTrue(ConfigRemoteModeTests.cfg.username == 'someoneelse')

    def testRepoName(self):
        self.assertTrue(ConfigRemoteModeTests.cfg.reponame == 'todo')

    def testAuthToken(self):
        self.assertTrue(ConfigRemoteModeTests.cfg.authtoken == 'lalala')

    def testRemoteMode(self):
        self.assertTrue(ConfigRemoteModeTests.cfg.remote_mode == True)


class ListDBTests(unittest.TestCase):

    def setUp(self):

        localmode_test_config = """
[pda]
database-path = /tmp/.pdateststore
"""

        cfg = PdaConfig(io.BytesIO(localmode_test_config))
        self.db = GithubIssues(cfg)

        # populate local data store with some data
        self.tl = [str(self.db.add_task('test summary 1', 'todo', 'week', 'must')),
                   str(self.db.add_task('test summary 2', 'tolearn', 'month', 'high')),
                   str(self.db.add_task('test summary 3', 'toread', 'day', 'urgmust'))]

    def tearDown(self):

        if os.path.exists(self.db.local_dbpath):
            os.remove(self.db.local_dbpath)

        del self.db

    def testAddTask(self):

        # initially the local data store should have 3 tasks
        self.assertTrue(len(self.db.shelf) == 3)

        # check tasks existence
        self.assertTrue(self.db.shelf.has_key(self.tl[0]))
        self.assertTrue(self.db.shelf.has_key(self.tl[1]))
        self.assertTrue(self.db.shelf.has_key(self.tl[2]))

        # check data integrity
        self.assertTrue(self.db.shelf[self.tl[0]]['summary'] == 'test summary 1')
        self.assertTrue(self.db.shelf[self.tl[1]]['type'] == 'tolearn')
        self.assertTrue(self.db.shelf[self.tl[1]]['milestone'] == 'month')
        self.assertTrue(self.db.shelf[self.tl[2]]['milestone'] == 'day')
        self.assertTrue(self.db.shelf[self.tl[2]]['priority'] == 'urgmust')
        self.assertFalse(self.db.shelf.has_key('CMDS_HISTORY'))

    def testRemoveTask(self):

        # initially the local data store should have 3 tasks
        self.assertTrue(len(self.db.shelf) == 3)

        # remove task 1
        self.db.remove_task(int(self.tl[0]))
        self.assertFalse(self.db.shelf.has_key(self.tl[0]))
        self.assertTrue(len(self.db.shelf) == 2)

        # remove non-existing task
        self.db.remove_task(-1)
        self.assertTrue(len(self.db.shelf) == 2)
        self.assertFalse(self.db.shelf.has_key('CMDS_HISTORY'))

    def testEditTask(self):

        # initially the local data store should have 3 tasks
        self.assertTrue(len(self.db.shelf) == 3)

        # edit the first and the third task
        self.db.edit_task(self.tl[0], 
                          new_summary='test summary 4',
                          new_tasktype='totest',
                          new_milestone='season')
        self.db.edit_task(self.tl[2], 
                          new_priority='low')

        # check data integrity
        self.assertTrue(len(self.db.shelf) == 3)

        self.assertTrue(self.db.shelf[self.tl[0]]['summary']   == 'test summary 4')
        self.assertTrue(self.db.shelf[self.tl[0]]['type']      == 'totest')
        self.assertTrue(self.db.shelf[self.tl[0]]['milestone'] == 'season')
        self.assertTrue(self.db.shelf[self.tl[0]]['priority']  == 'must')

        self.assertTrue(self.db.shelf[self.tl[2]]['type']     == 'toread')
        self.assertTrue(self.db.shelf[self.tl[2]]['priority'] == 'low')

        self.assertTrue(self.db.shelf[self.tl[1]]['summary'] == 'test summary 2')

        self.assertFalse(self.db.shelf.has_key('CMDS_HISTORY'))


class ListDBSyncingTests(unittest.TestCase):

    def setUp(self):
        cfg = PdaConfig(io.FileIO('.pdaconfig'))
        self.db = GithubIssues(cfg)
        self.db.sync_local_dbstore()

    def tearDown(self):
        if os.path.exists(self.db.local_dbpath):
            os.remove(self.db.local_dbpath)

        del self.db

    def testSyncLocalDBStore(self):

        # retrieve remote data for testing
        r = requests.get(self.db.url_issues, params={'state': 'open'}, auth=self.db.auth)

        for issue in r.json():
            task_no        = str(issue["number"])
            task_summary   = issue["title"]
            task_milestone = issue["milestone"]["title"] 
            task_prio      = ""
            task_type      = ""

            for label in issue["labels"]:
                if label["color"] == GithubIssues.YELLOW:
                    task_prio = label["name"]
                if label["color"] == GithubIssues.GREEN:
                    task_type = label["name"]

            # after data syncing, the issue should be present in local store
            self.assertTrue(self.db.shelf.has_key(task_no))

            # the data stored at local should be the same as remote
            self.assertTrue(self.db.shelf[task_no]["summary"]   == task_summary)
            self.assertTrue(self.db.shelf[task_no]["type"]      == task_type)
            self.assertTrue(self.db.shelf[task_no]["priority"]  == task_prio)
            self.assertTrue(self.db.shelf[task_no]["milestone"] == task_milestone)

        self.assertTrue(self.db.shelf.has_key('CMDS_HISTORY'))

    def testSyncRemoteDBStore(self):

        if self.db.shelf:

            task_numbers = [number for number in self.db.shelf.keys() \
                                              if number != 'CMDS_HISTORY']

            # (1) remove tasks
            if task_numbers:
                number = task_numbers.pop()
                self.db.remove_task(int(number))

            if task_numbers:
                number = task_numbers.pop()
                self.db.remove_task(int(number))

            # (2) add a task locally
            self.db.add_task('first added', 'tolearn', 'month', 'low')

            # (3) add another task
            added_2nd = self.db.add_task('secondly added', 'todo', 'year', 'high')

            # (4) edit a locally added task
            self.db.edit_task(int(added_2nd), new_milestone='season', new_tasktype='toread')

            # (5) edit a remotely imported task
            if task_numbers:
                number = task_numbers.pop()
                self.db.edit_task(int(number), new_priority='urgmust')

        # a data structure in memory to hold all the records before data is synced to remote
        records = [self.db.shelf[k] for k in self.db.shelf if k != 'CMDS_HISTORY']

        # syncing data to remote
        self.db.sync_remote_dbstore()

        # retrieving remote data to local memory
        r = requests.get(self.db.url_issues, params={'state': 'open'}, auth=self.db.auth)
        if r.status_code == requests.codes.ok:
            remote_records = r.json()

        # check if data is equivalent by making use of sets!
        local, remote = set([]), set([])

        for rec in records:
            local.add((rec['summary'], rec['type'], rec['milestone'], rec['priority']))

        for rec in remote_records:
            prio, ltype = self.db.get_task_prio_and_type(rec)
            remote.add((rec['title'], ltype, rec['milestone']['title'], prio))

        # finally test if local and remote contents are synced!
        self.assertTrue(local==remote)


class pdaTests(unittest.TestCase):
    pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
