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

import argparse
import shelve
import os
import github.GithubObject
from github import Github

def convert_priority_to_text(priority):
    """
    :param priority: integer
    :rtype: string
    """
    prio = ''

    if   priority == URGENT_MUSTDO: 
        prio = 'urgmust'
    elif priority == MUSTDO:
        prio = 'must'
    elif priority == HIGH_IMPORTANCE: 
        prio = 'high'
    elif priority == MEDIUM_IMPORTANCE: 
        prio = 'medium'
    else: 
        prio = 'low'

    return prio

def convert_milestone_title(time):
    """
    :param time: string
    :rtype: string
    """
    title = ''

    if   time == 'd':
        title = 'day'
    elif time == 'w':
        title = 'week'
    elif time == 'm':
        title = 'month'
    elif time == 's':
        title = 'season'
    else            :
        title = 'year'

    return title

def is_label_created(db, label_name):
    """
    :param db: :class:`github.Repository.Repository`
    :param label_name: string
    :rtype: Boolean
    """
    created = False

    for label in db.get_labels():
        if label.name == label_name:
            created = True
            break

    return created

def get_milestone_number(db, milestone_name):
    """
    :param db: :class:`github.Repository.Repository`
    :param milestone_name: string
    :rtype: None or integer
    """
    number = None

    for milestone in db.get_milestones():
        if milestone.title == milestone_name:
            number = milestone.number
            break

    return number

def get_issue_number(db, issue_number):
    """
    :param db: :class:`github.Repository.Repository`
    :param issue_number: integer
    :rtype: None or integer
    """
    number = None

    for issue in db.get_issues(state='open'):
        if issue.number == issue_number:
            number = issue.number
            break

    return number

def get_one_label(db, label_name, label_color):
    """
    :param db: :class:`github.Repository.Repository`
    :param label_name: string
    :param label_color: string
    :rtype: :class:`github.Label.Label`
    """

    if is_label_created(db, label_name):
        return db.get_label(label_name)
    else:
        return db.create_label(label_name, label_color)

def collect_one_label(db, list_of_labels, label_name, label_color):
    """
    :param db: :class:`github.Repository.Repository`
    :param list_of_labels: list of :class:`github.Label.Label`s
    :param label_name: string
    :param label_color: string
    """
    list_of_labels.append(get_one_label(db, label_name, label_color))

def get_one_milestone(db, milestone_title):
    """
    :param db: :class:`github.Repository.Repository`
    :param milestone_title: string
    :rtype: :class:`github.Milestone.Milestone`
    """
    milestone_number = get_milestone_number(db, milestone_title)
    if milestone_number:
        return db.get_milestone(milestone_number)
    else:
        return db.create_milestone(milestone_title)


def create_priority(args, db, list_of_labels):
    """
    :param args: :class:`argparse.Namespace`
    :param db: :class:`github.Repository.Repository`
    :param list_of_labels: list of :class:`github.Label.Label`s
    """
    if args.priority:
        prio = convert_priority_to_text(args.priority)
        collect_one_label(db, list_of_labels, prio, YELLOW)

def create_milestone(args, db):
    """
    :param args: :class:`argparse.Namespace`
    :param db: :class:`github.Repository.Repository`
    :rtype: :class:`github.Milestone.Milestone` or `github.GithubObject.NotSet`
    """
    if args.time:
        return get_one_milestone(db, convert_milestone_title(args.time))
    else:
        return github.GithubObject.NotSet

def create_listname(args, db, list_of_labels):
    """
    :param args: :class:`argparse.Namespace`
    :param db: :class:`github.Repository.Repository`
    :param list_of_labels: list of :class:`github.Label.Label`s
    """
    if args.listname:
        collect_one_label(db, list_of_labels, args.listname, GREEN)

def update_milestone(db, issue, time):
    """
    :param db: :class:`github.Repository.Repository`
    :param issue: :class:`github.Issue.Issue`
    :param time: string
    """
    title = convert_milestone_title(time)

    if issue.milestone and issue.milestone.title != title:
        issue.edit(milestone=get_one_milestone(db, title))

def update_one_label(db, issue, label_name, label_color):
    """
    :param db: :class:`github.Repository.Repository`
    :param issue: :class:`github.Issue.Issue`
    :param label_name: string
    :param label_color: string
    """
    # remove original priority from task
    for label in issue.get_labels():
        if label.color == label_color and label.name != label_name:
            issue.remove_from_labels(label)
            break

    # add new priority to task
    issue.add_to_labels(get_one_label(db, label_name, label_color))

def update_summary(issue, summary):
    """
    :param issue: :class:`github.Issue.Issue`
    :param summary: string
    """
    issue.edit(title=summary)


def print_pretty_tasks_info(db, list_of_labels, time_range):
    """
    :param db: :class:`github.Repository.Repository`
    :param list_of_labels: list of :class:`github.Label.Label`s
    :param time_range: :class:`github.Milestone.Milestone`
    """
    print
    table_titles = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']
    print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*table_titles)
    print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])
    for issue in db.get_issues(labels=list_of_labels, milestone=time_range, state='open'):
        for label in issue.labels:
            if label.color == YELLOW: prio = label.name
            if label.color ==  GREEN: list_type = label.name
        print u'{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(issue.number, 
                                                           issue.title, 
                                                           list_type, 
                                                           issue.milestone.title, 
                                                           prio)

# default github repository name where list database is stored
REPO_NAME = 'keenhenry/lists'
# REPO_NAME = 'keenhenry/todo'

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

    def __init__(self, repo_name=None):
        """
        :param repo_name: string
        """

        assert repo_name is None or isinstance(repo_name, (str, unicode)), repo_name

        # connect to the list database stored on Github
        self.__repo_name = repo_name if repo_name else REPO_NAME
        self.__github    = Github(os.environ['PDA_AUTH'])
        self.__repo      = self.__github.get_repo(self.__repo_name)

    def _has_task(self, task_number):
        """
        :param task_number: integer
        :rtype: True or False
        """

        assert isinstance(task_number, (int, long)), task_number

        hasTask = False

        for issue in self.__repo.get_issues(state='open'):
            if task_number == issue.number:
                hasTask = True
                break

        return hasTask

    def sync_local_dbstore(self):
        """
        """
        print

    def sync_remote_dbstore(self):
        print

    def remove_task(self, task_number):
        print

    def add_task(self):
        print

    def edit_task(self):
        print

    def read_tasks(self):
        print
        
def main():
    # open local persistent object store
    # objstore = os.environ['HOME'] + "/" + ".pdastore"
    # storehdl = shelve.open(objstore, protocol=-1)

    # create a Github Repository object to interact with Github
    # and store that object into a persistent local object store
    # if not storehdl.has_key('GITHUB_REPO'):
    #     g = Github(os.environ['PDA_AUTH']) 
    #     storehdl['GITHUB_REPO'] = g.get_repo(REPO_NAME)

    # retrieve github repo object from local persistent store
    # repo = storehdl['GITHUB_REPO']

    # pass github repo object to controller
    # controller(repo)

    # write the object back to persistent store after done with it
    # storehdl['GITHUB_REPO'] = repo
    # storehdl.close()
    db = ListDB()

if __name__ == '__main__':
    main()
