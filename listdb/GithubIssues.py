#!/usr/bin/env python

"""
`ListDB` is a data model abstraction of the list databse used by `pda`.

"""

import requests
import os
import shelve

# def collect_one_label(db, list_of_labels, label_name, label_color):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param list_of_labels: list of :class:`github.Label.Label`s
#     :param label_name: string
#     :param label_color: string
#     """
#     list_of_labels.append(get_one_label(db, label_name, label_color))
# 
# def get_one_milestone(db, milestone_title):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param milestone_title: string
#     :rtype: :class:`github.Milestone.Milestone`
#     """
#     milestone_number = get_milestone_number(db, milestone_title)
#     if milestone_number:
#         return db.get_milestone(milestone_number)
#     else:
#         return db.create_milestone(milestone_title)
# 
# def create_listname(args, db, list_of_labels):
#     """
#     :param args: :class:`argparse.Namespace`
#     :param db: :class:`github.Repository.Repository`
#     :param list_of_labels: list of :class:`github.Label.Label`s
#     """
#     if args.listname:
#         collect_one_label(db, list_of_labels, args.listname, GREEN)
# 
# def update_milestone(db, issue, time):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param issue: :class:`github.Issue.Issue`
#     :param time: string
#     """
#     title = convert_milestone_title(time)
# 
#     if issue.milestone and issue.milestone.title != title:
#         issue.edit(milestone=get_one_milestone(db, title))
# 
# def update_one_label(db, issue, label_name, label_color):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param issue: :class:`github.Issue.Issue`
#     :param label_name: string
#     :param label_color: string
#     """
#     # remove original priority from task
#     for label in issue.get_labels():
#         if label.color == label_color and label.name != label_name:
#             issue.remove_from_labels(label)
#             break
# 
#     # add new priority to task
#     issue.add_to_labels(get_one_label(db, label_name, label_color))
# 

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

    @property
    def url_issues(self):
        return self.__url_issues

    @property
    def auth(self):
        return self.__auth

    @property
    def max_task_number(self):
        return self.__max_taskno

    def _has_task(self, db_local, task_number):
        """
        :param db_local: :class:`shelve.Shelf`
        :param task_number: integer
        :rtype: True or False
        """

        assert db_local is not None and isinstance(db_local, shelve.Shelf), db_local
        assert isinstance(task_number, (int, long)), task_number

        return db_local.has_key(str(task_number))

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

    def _print_header(self):

        headers = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']

        print
        print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*headers)
        print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])

    def _print_task(self, db_local, task_number, task_type, milestone, priority):
        """Helper function for read_tasks()
        :param db_local: :class:`shelve.Shelf`
        :param task_number: string
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        assert db_local is not None and isinstance(db_local, shelve.Shelf), db_local

        if self._is_selected(db_local[task_number]['type'], task_type,
                             db_local[task_number]['milestone'], milestone,
                             db_local[task_number]['priority'], priority):
            print u'{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(
                                                         task_number, 
                                                         db_local[task_number]["summary"], 
                                                         db_local[task_number]["type"], 
                                                         db_local[task_number]["milestone"], 
                                                         db_local[task_number]["priority"])


    def sync_local_dbstore(self):

        # retrieving OPEN issues from Github Issues
        r = requests.get(self.url_issues, params={'state': 'open'}, auth=self.auth)

        # prepare a local db store for storing issues locally
        db_local = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), protocol=-1)

        # write issue data into local db store
        for issue in r.json():

            prio, ltype = self._get_task_prio_and_type(issue)

            issue_data = {
                          "summary"  : issue["title"],
                          "type"     : ltype,
                          "milestone": issue["milestone"]["title"],
                          "priority" : prio
                         }

            db_local[str(issue["number"])] = issue_data
            self.__max_taskno = issue["number"] if issue["number"] > self.__max_taskno \
                                                else self.__max_taskno

        # create a list to hold command history records
        db_local['CMDS_HISTORY'] = []

        # close local store
        db_local.close()

    def sync_remote_dbstore(self):

        # TODO: syncing data to remote (Github Issues)

        # remove local data store after syncing data to remote
        os.remove(self.DEFAULT_LOCAL_DBPATH)
        
    def remove_task(self, task_number):
        """
        :param task_number: integer
        """

        assert isinstance(task_number, (int, long)), task_number

        # prepare a local db store for storing issues locally
        db_local = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), 
                               protocol=-1, 
                               writeback=True)

        if self._has_task(db_local, task_number):

            # delete task at local store
            del db_local[str(task_number)]

            # record remove operation in list 'CMDS_HISTORY' in local store
            cmd_history_data = { 'CMD': 'REMOVE', '#': task_number }
            db_local['CMDS_HISTORY'].append(cmd_history_data)

        db_local.close()

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

        db_local = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), 
                               protocol=-1,
                               writeback=True)

        # the value of the key for local store is not important, as long as it is unique
        self.__max_taskno += 1
        db_local[str(self.__max_taskno)] = issue_data

        # record ADD operation in list 'CMDS_HISTORY' in local store
        cmd_history_data = { 'CMD'      : 'ADD', 
                             'SUMMARY'  : summary,
                             'TYPE'     : task_type,
                             'MILESTONE': milestone,
                             'PRIORITY' : priority }
        db_local['CMDS_HISTORY'].append(cmd_history_data)

        db_local.close()

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

        db_local = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), 
                               protocol=-1,
                               writeback=True)

        if self._has_task(db_local, task_number):
            if new_summary: 
                db_local[str(task_number)]["summary"] = new_summary
            if new_tasktype: 
                db_local[str(task_number)]["type"] = new_tasktype
            if new_milestone: 
                db_local[str(task_number)]["milestone"] = new_milestone
            if new_priority: 
                db_local[str(task_number)]["priority"] = new_priority

            # record EDIT operation in list 'CMDS_HISTORY' in local store
            cmd_history_data = { 'CMD'      : 'EDIT', 
                                 '#'        : task_number,
                                 'SUMMARY'  : new_summary,
                                 'TYPE'     : new_tasktype,
                                 'MILESTONE': new_milestone,
                                 'PRIORITY' : new_priority }
            db_local['CMDS_HISTORY'].append(cmd_history_data)

        db_local.close()

    def read_tasks(self, task_type=None, milestone=None, priority=None):
        """
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        assert task_type is None or isinstance(task_type, str), task_type
        assert milestone is None or isinstance(milestone, str), milestone
        assert priority  is None or isinstance(priority,  str), priority

        db_local = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), protocol=-1)

        self._print_header()
        for key in db_local:
            if key != 'CMDS_HISTORY':
                self._print_task(db_local, key, task_type, milestone, priority)

        for cmd in db_local['CMDS_HISTORY']:
            print cmd

        db_local.close()

def main():

    # create db object
    db = ListDB()

    db.sync_local_dbstore()

    db.read_tasks()
    db.add_task('task 6', 'tolearn', 'month', 'must')
    db.read_tasks()
    db.edit_task(task_number=44, new_tasktype='toread', new_milestone='year')
    db.read_tasks()
    # db.read_tasks('todo', 'day', 'high')
    # db.read_tasks('todo', 'day', 'low')
    
    db.sync_remote_dbstore()

if __name__ == '__main__':
    main()
