#!/usr/bin/env python

# Author   : Henry Huang <keenhenry1109@gmail.com>
# Copyright: This module has been placed in the public domain

"""
A simple command line tool to manage personal todo list, tolearn list, 
toread list, and all sorts of other lists you can imagine.

`pda` makes use of `PyGithub library <https://github.com/jacquev6/PyGithub>`_ 
to communicate with Github Issue API; all the data are stored at Github Issue.

This module includes following several functions:

================
Helper Functions
================

- `convert_priority_to_text()`:
- `convert_milestone_title()`:
- `is_label_created()`: test if a label exists in the Github Issue repository

=======
gettors
=======

=======
settors
=======

=============
Core Function
=============

- `controller()`: bridging function between Github Issue and terminal interface

"""

import argparse
import os
from github import Github

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

def convert_priority_to_text(priority):
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
    '''
    :param db: :class:`github.Repository.Repository`
    :param label_name: string
    :rtype: Boolean
    '''
    created = False

    for label in db.get_labels():
        if label.name == label_name:
            created = True
            break

    return created

def get_milestone_number(db, milestone_name):
    number = None

    for milestone in db.get_milestones():
        if milestone.title == milestone_name:
            number = milestone.number
            break

    return number

def get_issue_number(db, issue_number):
    number = None

    for issue in db.get_issues(state='open'):
        if issue.number == issue_number:
            number = issue.number
            break

    return number

def get_one_label(db, label_name, label_color):

    # get one label if already exists, otherwise create one in list!
    if is_label_created(db, label_name):
        return db.get_label(label_name)
    else:
        return db.create_label(label_name, label_color)

# collect one label into list_of_labels structure
def collect_one_label(db, list_of_labels, label_name, label_color):
    list_of_labels.append(get_one_label(db, label_name, label_color))

# get one milestone if already exists, otherwise create one in list!
def get_one_milestone(db, milestone_title):
    milestone_number = get_milestone_number(db, milestone_title)
    if milestone_number:
        return db.get_milestone(milestone_number)
    else:
        return db.create_milestone(milestone_title)


# assign priority to a task
def assign_priority(args, db, list_of_labels):
    if args.priority:
        prio = convert_priority_to_text(args.priority)
        collect_one_label(db, list_of_labels, prio, YELLOW)

# assign milestone to a task
def assign_milestone(args, db):
    if args.time:
        title      = convert_milestone_title(args.time)
        time_range = get_one_milestone(db, title)

# assign list name to a task
def assign_listname(args, db, list_of_labels):
    if args.listname != '':
        collect_one_label(db, list_of_labels, args.listname, GREEN)

# update milestone information for a task
def update_mildestone(db, issue, time):
    title = convert_milestone_title(time)

    if issue.milestone and issue.milestone.title != title:
        issue.edit(milestone=get_one_milestone(db, title))

# update priority information for a task
def update_one_label(db, issue, label_name, label_color):
    # remove original priority from task
    for label in issue.get_labels():
        if label.color == label_color and label.name != label_name:
            issue.remove_from_labels(label)
            break

    # add new priority to task
    issue.add_to_labels(get_one_label(db, label_name, label_color))

# update summary of a task
def update_summary(issue, summary):
    issue.edit(title=summary)


def controller(db):

    # create instance of ArgumentParser Module 
    p = argparse.ArgumentParser(
            description = 'A Personal Desktop Assistant to manage useful lists, like TODO list.',
            prog        = 'pda',
            usage       = '%(prog)s [OPTION]... [LISTNAME]'
        )

    #=============================#
    # Create Positional Arguments #
    #=============================#
    # positional argument to hold the list name typed on command line
    p.add_argument('listname',
                   nargs='?',
                   type=str,
                   default='',
                   help='tell pda which list to work on')
    
    #================#
    # Create Options #
    #================#

    # option to close a task from todo list
    p.add_argument('-r', '--remove',
                   action="store",
                   type=int,
                   metavar='N',
                   help='remove task numbered N from list')

    # option to add a task into todo list
    p.add_argument('-a', '--add',
                   action="store", 
                   type=str,
                   metavar='SUMMARY',
                   help='add a task summarized with SUMMARY into list')

    # option to add validity period associated with a task
    p.add_argument('-t', '--time',
                   action="store", 
                   type=str,
                   choices='dwmsy',
                   metavar='PERIOD',
                   help='specify the PERIOD for this task')

    # option to assign priority to a task
    p.add_argument('-p', '--priority',
                   action="store", 
                   type=int,
                   choices=[1,2,3,4,5],
                   metavar='PRIO',
                   help='assign priority PRIO to a task in list')

    # options to update a task in list
    p.add_argument('-e', '--edit',
                   action="store",
                   type=int,
                   metavar='N',
                   help='update a task numberd N in list')

    # option assign task summary to a task
    p.add_argument('-s', '--summary',
                   action="store",
                   type=str,
                   default='',
                   metavar='SUMMARY',
                   help='assign SUMMARY to a task in list')

    # options to show tasks in list
    p.add_argument('-l', '--list',
                   action="store_true",
                   help='show the tasks in list')

    #======================#
    # Create Other Options #
    #======================#
    p.add_argument('--version', action='version', version='%(prog)s 0.0.1')

    #=============================================================#
    # Parsing options and perform appropriate actions accordingly #
    #=============================================================#
    args = p.parse_args()

    if args.remove:
        issue_number = get_issue_number(db, args.remove)
        if issue_number:
            issue = db.get_issue(issue_number)
            issue.edit(state='closed')
        else:
            print '{}: error: no such task (#{}) in the list'.format(p.prog, args.edit)
    elif args.add:
        list_of_labels = []
        time_range     = None

        assign_listname (args, db, list_of_labels)
        assign_priority (args, db, list_of_labels)

        if args.time:
            milestone_title = convert_milestone_title(args.time)
            time_range      = get_one_milestone(db, milestone_title)

        # create a task in list
        db.create_issue(args.add, labels=list_of_labels, milestone=time_range)
    elif args.edit:

        issue_number = get_issue_number(db, args.edit)
        if issue_number:
            issue = db.get_issue(issue_number)

            if args.time:
                update_mildestone(db, issue, args.time)
            if args.priority:
                update_one_label(db, issue, convert_priority_to_text(args.priority), YELLOW)
            if args.listname != '':
                update_one_label(db, issue, args.listname, GREEN)
            if args.summary != '':
                update_summary(issue, args.summary)
        else:
            print '{}: error: no such task (#{}) in the list'.format(p.prog, args.edit)
    elif args.list or args.listname:
        list_of_labels = []
        time_range     = None

        # no default value for priority, so we can assign it directly
        assign_priority(args, db, list_of_labels)

        # default value for listname is 'todo'
        list_type = get_one_label(db, 'todo', GREEN) if args.listname == '' else \
                    get_one_label(db, args.listname, GREEN)
        list_of_labels.append(list_type)

        # default value for milestone is 'day'
        time_range = get_one_milestone(db, convert_milestone_title(args.time)) if args.time \
                     else get_one_milestone(db, 'day')

        # print out tasks in a friendly format:
        print
        table_titles = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']
        print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*table_titles)
        print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])
        for issue in db.get_issues(labels=list_of_labels, milestone=time_range, state='open'):
            for label in issue.labels:
                if label.color == YELLOW: prio = label.name
                if label.color ==  GREEN: list_type = label.name
            print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(issue.number, 
                                                              issue.title, 
                                                              list_type, 
                                                              issue.milestone.title, 
                                                              prio)
    else:
        p.print_help()

def main():

    # create a Github object to interact with Github
    token = os.environ['PDA_AUTH']
    g = Github(token)

    # get todo repo
    repo = g.get_repo('keenhenry/todo')
    # repo = g.get_repo('keenhenry/lists')

    # pass github repo object to controller
    controller(repo)

if __name__ == '__main__':
    main()
