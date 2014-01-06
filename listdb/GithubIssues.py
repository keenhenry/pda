#!/usr/bin/env python

"""
`ListDB` is a data model abstraction of the list databse used by `pda`.

================
Helper Functions
================

=======
gettors
=======

=======
settors
=======

"""

import requests
import os
import shelve

# def convert_priority_to_text(priority):
#     """
#     :param priority: integer
#     :rtype: string
#     """
#     prio = ''
# 
#     if   priority == URGENT_MUSTDO: 
#         prio = 'urgmust'
#     elif priority == MUSTDO:
#         prio = 'must'
#     elif priority == HIGH_IMPORTANCE: 
#         prio = 'high'
#     elif priority == MEDIUM_IMPORTANCE: 
#         prio = 'medium'
#     else: 
#         prio = 'low'
# 
#     return prio
# 
# def convert_milestone_title(time):
#     """
#     :param time: string
#     :rtype: string
#     """
#     title = ''
# 
#     if   time == 'd':
#         title = 'day'
#     elif time == 'w':
#         title = 'week'
#     elif time == 'm':
#         title = 'month'
#     elif time == 's':
#         title = 'season'
#     else            :
#         title = 'year'
# 
#     return title
# 
# def is_label_created(db, label_name):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param label_name: string
#     :rtype: Boolean
#     """
#     created = False
# 
#     for label in db.get_labels():
#         if label.name == label_name:
#             created = True
#             break
# 
#     return created
# 
# def get_milestone_number(db, milestone_name):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param milestone_name: string
#     :rtype: None or integer
#     """
#     number = None
# 
#     for milestone in db.get_milestones():
#         if milestone.title == milestone_name:
#             number = milestone.number
#             break
# 
#     return number
# 
# def get_issue_number(db, issue_number):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param issue_number: integer
#     :rtype: None or integer
#     """
#     number = None
# 
#     for issue in db.get_issues(state='open'):
#         if issue.number == issue_number:
#             number = issue.number
#             break
# 
#     return number
# 
# def get_one_label(db, label_name, label_color):
#     """
#     :param db: :class:`github.Repository.Repository`
#     :param label_name: string
#     :param label_color: string
#     :rtype: :class:`github.Label.Label`
#     """
# 
#     if is_label_created(db, label_name):
#         return db.get_label(label_name)
#     else:
#         return db.create_label(label_name, label_color)
# 
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
# 
# def create_priority(args, db, list_of_labels):
#     """
#     :param args: :class:`argparse.Namespace`
#     :param db: :class:`github.Repository.Repository`
#     :param list_of_labels: list of :class:`github.Label.Label`s
#     """
#     if args.priority:
#         prio = convert_priority_to_text(args.priority)
#         collect_one_label(db, list_of_labels, prio, YELLOW)
# 
# def create_milestone(args, db):
#     """
#     :param args: :class:`argparse.Namespace`
#     :param db: :class:`github.Repository.Repository`
#     :rtype: :class:`github.Milestone.Milestone` or `github.GithubObject.NotSet`
#     """
#     if args.time:
#         return get_one_milestone(db, convert_milestone_title(args.time))
#     else:
#         return github.GithubObject.NotSet
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
# def update_summary(issue, summary):
#     """
#     :param issue: :class:`github.Issue.Issue`
#     :param summary: string
#     """
#     issue.edit(title=summary)
# 
# 
        # print
        # table_titles = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']
        # print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*table_titles)
        # print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])
        # for issue in r.json():
        #     for label in issue["labels"]:
        #         if label["color"] == self.YELLOW: prio      = label["name"]
        #         if label["color"] == self.GREEN:  list_type = label["name"]
        #     print u'{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(issue["number"], 
        #                                                        issue["title"], 
        #                                                        list_type, 
        #                                                        issue["milestone"]["title"], 
        #                                                        prio)

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

    @property
    def url_issues(self):
        return self.__url_issues

    @property
    def auth(self):
        return self.__auth

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

    def sync_local_dbstore(self):

        # retrieving OPEN issues from Github Issues
        r = requests.get(self.__url_issues, params={'state': 'open'}, auth=self.__auth)

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

    def add_task(self):
        print

    def edit_task(self):
        print

    def read_tasks(self):

        db_local = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), protocol=-1)

        # print
        # table_titles = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']
        # print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*table_titles)
        # print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])
        # for key in db_local:
        #     if key != 'CMDS_HISTORY':
        #         print u'{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(key, 
        #                                                            db_local[key]["summary"], 
        #                                                            db_local[key]["type"], 
        #                                                            db_local[key]["milestone"], 
        #                                                            db_local[key]["priority"])

        # for cmd in db_local['CMDS_HISTORY']:
        #     print cmd

        db_local.close()

def main():

    # create db object
    db = ListDB()

    db.sync_local_dbstore()

    # db.read_tasks()
    # db.remove_task(37)
    # db.read_tasks()
    # db.remove_task(37)
    # db.remove_task(39)
    # db.read_tasks()
    
    db.sync_remote_dbstore()

if __name__ == '__main__':
    main()
