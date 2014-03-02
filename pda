#!/usr/bin/env python

"""
A simple command line tool to manage personal todo list, tolearn list, 
toread list, and all sorts of other lists you can imagine.

`pda` makes use of `Requests library <http://docs.python-requests.org/en/latest/>`_
to communicate with Github Issue API; all the data are stored at Github Issue.

=============
Core Function
=============

- `controller()`: bridging function between Github Issue and terminal interface

===============
Helper Function
===============

- `cry_msg()`: emitting console messages

"""

import argparse
from listdb import __version__
from listdb.GithubIssues import ListDB
from listdb.Config import PdaConfig


def cry_msg(prog, err_str="", msg=""):
    """
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """
    print '{}: {}{}'.format(prog, err_str, msg)

def controller(db):
    """
    :param db: :class:`listdb.GithubIssues.ListDB`
    """

    # create instance of ArgumentParser Module 
    p = argparse.ArgumentParser(
            description = '''A Personal Desktop Assistant to manage useful lists, 
                             such as TODO, TOLEARN, TOREAD, etc. If [OPTION] is omitted, 
                             the default behavior is to print out the content of the list 
                             named [listname]; if both [OPTION] and [listname] are omitted, 
                             default behavior is to print out contents of all lists.''',
            prog        = 'pda',
            usage       = '%(prog)s [OPTION]... [listname]'
        )

    #=============================#
    # Create Positional Arguments #
    #=============================#
    # positional argument to hold the list name typed on command line
    p.add_argument('listname',
                   nargs='?',
                   type=str,
                   help='tell pda which list to work on')
    
    #================#
    # Create Options #
    #================#
    p.add_argument('--start',
                   action="store_true",
                   help='start pda and sync with remote')

    p.add_argument('--stop',
                   action="store_true",
                   help='stop pda and sync with remote')

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
                   help='add a task summarized as SUMMARY into list')

    # option to specify validity period associated with a task
    p.add_argument('-t', '--time',
                   action="store", 
                   type=str,
                   choices='dwmsy',
                   metavar='PERIOD',
                   help='specify milestone PERIOD of a task')

    # option to specify priority of a task
    p.add_argument('-p', '--priority',
                   action="store", 
                   type=int,
                   choices=[1,2,3,4,5],
                   metavar='PRIO',
                   help='specify priority PRIO of a task')

    # options to update a task in list
    p.add_argument('-e', '--edit',
                   action="store",
                   type=int,
                   metavar='N',
                   help='update a task numberd N in list')

    # option to specify task summary
    p.add_argument('-s', '--summary',
                   action="store",
                   type=str,
                   metavar='SUMMARY',
                   help='specify SUMMARY of a task')

    #======================#
    # Create Other Options #
    #======================#
    p.add_argument('--version', action='version', version='%(prog)s '+__version__)

    #=============================================================#
    # Parsing options and perform appropriate actions accordingly #
    #=============================================================#
    args = p.parse_args()

    if db.remote_mode and not db.shelf:
        if args.start:
            db.sync_local_dbstore()
        else:
            cry_msg(p.prog, msg='please execute "pda --start" first; and "pda --stop" before leaving pda')
    else:
        if args.remove:
            if db.has_task(args.remove):
                db.remove_task(args.remove)
            else:
                cry_msg(p.prog, 
                        err_str='error: ', 
                        msg='no such task (#'+str(args.remove)+') in the list')
        elif args.add:
            db.add_task(args.add, task_type=args.listname, 
                                  milestone=ListDB.extend_milestone(args.time), 
                                  priority=ListDB.convert_int_prio_to_text_prio(args.priority))
        elif args.edit:
            if db.has_task(args.edit):
                db.edit_task(args.edit, new_summary=args.summary, 
                                        new_tasktype=args.listname,
                                        new_milestone=ListDB.extend_milestone(args.time),
                                        new_priority=ListDB.convert_int_prio_to_text_prio(args.priority))
            else:
                cry_msg(p.prog, 
                        err_str='error: ', 
                        msg='no such task (#'+str(args.edit)+') in the list')
        elif db.remote_mode and args.stop:
            db.sync_remote_dbstore()
        else: # print out contents stored in lists
            db.read_tasks(args.listname, 
                          ListDB.extend_milestone(args.time), 
                          ListDB.convert_int_prio_to_text_prio(args.priority))

def main():
    db = ListDB(PdaConfig())
    controller(db)

if __name__ == '__main__':
    main()
