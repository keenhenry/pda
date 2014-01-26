#!/usr/bin/env python

"""
`ListDB` is a data model abstraction of the list databse used by `pda`.

"""

import requests
import os
import shelve


DEFAULT_BASE_URL = "https://api.github.com/repos/"
REPO_NAME = 'keenhenry/todo'
# REPO_NAME = 'keenhenry/lists'

class ListDB(object):
    """Base class for representing list database.
    """

    # COLOR constants
    GREEN  = '009800'
    YELLOW = 'fbca04'
    RED    = 'e11d21'
    BLUE   = '0052cc'
    
    # PRIORITY constants
    URGENT_MUSTDO     = 5
    MUSTDO            = 4
    HIGH_IMPORTANCE   = 3
    MEDIUM_IMPORTANCE = 2
    LOW_IMPORTANCE    = 1

    # default local database mirror path
    DEFAULT_LOCAL_DBPATH = '/tmp/.pdastore'

    def __init__(self):

        self.__url_issues = DEFAULT_BASE_URL + REPO_NAME + "/issues"
        self.__auth       = (os.environ['PDA_AUTH'], '')
        self.__max_taskno = -1
        self.__shelf      = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), 
                                        protocol=-1,
                                        writeback=True)

    def __del__(self):
        self.__shelf.close()

    @property
    def shelf(self):
        return self.__shelf

    @property
    def url_issues(self):
        return self.__url_issues

    @property
    def auth(self):
        return self.__auth

    @property
    def max_task_number(self):
        return self.__max_taskno

    @max_task_number.setter
    def max_task_number(self, value):
        self.__max_taskno = value

    def _has_task(self, task_number):
        """
        :param task_number: integer
        :rtype: True or False
        """

        assert isinstance(task_number, (int, long)), task_number

        return self.shelf.has_key(str(task_number))

    def _get_task_prio_and_type(self, task):
        """
        :param task: dict
        :rtype: tuple
        """

        assert task is not None and isinstance(task, dict), task

        prio, task_type = None, None

        for label in task["labels"]:
            if label["color"] == self.YELLOW:     prio = label["name"]
            if label["color"] == self.GREEN: task_type = label["name"]
        
        return prio, task_type

    def _is_selected(self, task_type_in_db, task_type_requested, 
                           milestone_in_db, milestone_requested, 
                           priority_in_db, priority_requested):

        return (task_type_requested is None or task_type_requested == task_type_in_db) and \
               (milestone_requested is None or milestone_requested == milestone_in_db) and \
               (priority_requested is None or priority_requested == priority_in_db)

    def _is_cmd_history_annihilable(self, task_number):
        """
        :param task_number: integer
        :rtype: True or False
        """

        o_cmd_list = self.shelf['CMDS_HISTORY']
        n_cmd_list = [cmd for cmd in o_cmd_list if \
                          not (cmd['#'] == task_number and cmd['CMD'] != 'REMOVE')]

        self.shelf['CMDS_HISTORY'] = n_cmd_list

        return (len(n_cmd_list) < len(o_cmd_list))


    def _print_header(self):

        headers = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']

        print
        print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*headers)
        print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])

    def _print_task(self, task_number, task_type, milestone, priority):
        """Helper function for read_tasks()
        :param task_number: string
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        if self._is_selected(self.shelf[task_number]['type'], task_type,
                             self.shelf[task_number]['milestone'], milestone,
                             self.shelf[task_number]['priority'], priority):
            print u'{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(
                                                         task_number, 
                                                         self.shelf[task_number]["summary"], 
                                                         self.shelf[task_number]["type"], 
                                                         self.shelf[task_number]["milestone"], 
                                                         self.shelf[task_number]["priority"])


    def sync_local_dbstore(self):

        # retrieving OPEN issues from Github Issues
        r = requests.get(self.url_issues, params={'state': 'open'}, auth=self.auth)

        # write issue data into local db store
        for issue in r.json():

            prio, ltype = self._get_task_prio_and_type(issue)

            issue_data = {
                          "summary"  : issue["title"],
                          "type"     : ltype,
                          "milestone": issue["milestone"]["title"],
                          "priority" : prio
                         }

            self.shelf[str(issue["number"])] = issue_data
            self.max_task_number = issue["number"] if issue["number"] > self.max_task_number \
                                                else self.max_task_number

        # create a list to hold command history records
        self.shelf['CMDS_HISTORY'] = []

        # sync to local store
        self.shelf.sync()

    def sync_remote_dbstore(self):

        # TODO: syncing data to remote (Github Issues)
        # for cmd in self.shelf['CMDS_HISTORY']:
        #     if cmd['CMD'] == 'REMOVE':
        #         print
        #     elif cmd['CMD'] == 'ADD':
        #         print
        #     elif cmd['CMD'] == 'EDIT':
        #         print
        #     else: # should never reach here!
        #         print 'Something must be wrong!'

        # remove local data store after syncing data to remote
        os.remove(self.DEFAULT_LOCAL_DBPATH)
        
    def remove_task(self, task_number):
        """
        :param task_number: integer
        """

        assert isinstance(task_number, (int, long)), task_number

        if self._has_task(task_number):

            # delete task at local store
            del self.shelf[str(task_number)]

            # record remove operation in list 'CMDS_HISTORY' in local store
            if not self._is_cmd_history_annihilable(task_number):
                cmd_history_data = { 'CMD': 'REMOVE', '#': task_number }
                self.shelf['CMDS_HISTORY'].append(cmd_history_data)

            self.shelf.sync()

    def add_task(self, summary, task_type=None, milestone=None, priority=None):
        assert summary   is not None and isinstance(summary,   str), summary
        assert task_type is None or isinstance(task_type, str), task_type
        assert milestone is None or isinstance(milestone, str), milestone
        assert priority  is None or isinstance(priority,  str), priority

        issue_data = {
                      "summary"  : summary,
                      "type"     : task_type,
                      "milestone": milestone,
                      "priority" : priority
                     }

        # the value of the key for local store is not important, as long as it is unique
        self.max_task_number += 1
        self.shelf[str(self.max_task_number)] = issue_data

        # record ADD operation in list 'CMDS_HISTORY' in local store
        cmd_history_data = { '#'        : self.max_task_number,
                             'CMD'      : 'ADD', 
                             'SUMMARY'  : summary,
                             'TYPE'     : task_type,
                             'MILESTONE': milestone,
                             'PRIORITY' : priority }
        self.shelf['CMDS_HISTORY'].append(cmd_history_data)

        self.shelf.sync()

        return self.max_task_number

    def edit_task(self, task_number, 
                  new_summary  =None, 
                  new_tasktype =None, 
                  new_milestone=None, 
                  new_priority =None):
        """
        :param task_number  : integer
        :param new_summary  : string
        :param new_tasktype : string
        :param new_milestone: string
        :param new_priority : string
        """

        assert task_number   is not None and isinstance(task_number, (int,long)), task_number
        assert new_summary   is None or isinstance(new_summary,   str), new_summary
        assert new_tasktype  is None or isinstance(new_tasktype,  str), new_tasktype
        assert new_milestone is None or isinstance(new_milestone, str), new_milestone
        assert new_priority  is None or isinstance(new_priority,  str), new_priority

        if self._has_task(task_number):
            if new_summary: 
                self.shelf[str(task_number)]["summary"] = new_summary
            if new_tasktype: 
                self.shelf[str(task_number)]["type"] = new_tasktype
            if new_milestone: 
                self.shelf[str(task_number)]["milestone"] = new_milestone
            if new_priority: 
                self.shelf[str(task_number)]["priority"] = new_priority

            # record EDIT operation in list 'CMDS_HISTORY' in local store
            cmd_history_data = { 'CMD'      : 'EDIT', 
                                 '#'        : task_number,
                                 'SUMMARY'  : new_summary,
                                 'TYPE'     : new_tasktype,
                                 'MILESTONE': new_milestone,
                                 'PRIORITY' : new_priority }
            self.shelf['CMDS_HISTORY'].append(cmd_history_data)
            self.shelf.sync()

    def read_tasks(self, task_type=None, milestone=None, priority=None):
        """
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        assert task_type is None or isinstance(task_type, str), task_type
        assert milestone is None or isinstance(milestone, str), milestone
        assert priority  is None or isinstance(priority,  str), priority

        self._print_header()
        for key in self.shelf:
            if key != 'CMDS_HISTORY':
                self._print_task(key, task_type, milestone, priority)

        # DEBUG code
        for cmd in self.shelf['CMDS_HISTORY']:
            print cmd

def main():

    # create db object
    db = ListDB()

    db.sync_local_dbstore()

    db.read_tasks()
    db.add_task('task 6', 'tolearn', 'month', 'must')
    db.read_tasks()
    db.edit_task(task_number=44, new_tasktype='toread', new_milestone='year')
    db.read_tasks()
    db.remove_task(41)
    # db.remove_task(44)
    db.read_tasks()
    # db.read_tasks('toread')
    
    db.sync_remote_dbstore()

if __name__ == '__main__':
    main()
