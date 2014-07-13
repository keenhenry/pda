#!/usr/bin/env python

"""``control.py`` module

This module serve as the 'C' in MVC pattern; it is bridging the view 
(command line interface) and the model (listdb package) to make ``pda``
work.

This module is also the application entry point which should be run as
the **main** script.

"""

import argparse
from .utils import cry_msg, convert_prio_int_to_txt
from .listdb.ListDB import GithubIssues
from .listdb.Config import PdaConfig
from . import __version__


def controller(_db):
    """Bridging function between data model (listdb) and view (command line)
    :param _db: :class:`listdb.ListDB.GithubIssues`
    """

    # create instance of ArgumentParser Module 
    p = argparse.ArgumentParser(
        description = '''A Personal Desktop Assistant to manage useful lists, 
                         such as todo, tolearn, toread, etc. If [OPTION] is 
                         omitted, the default behavior is to print out the 
                         content of the list named [listname]; if both [OPTION] 
                         and [listname] are omitted, default behavior is to 
                         print out contents of all lists.''',
        prog        = 'pda',
        usage       = '%(prog)s [OPTION]... [listname]')

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

    # option to close all the tasks from todo list
    p.add_argument('--clear',
                   action="store_true",
                   help='remove all the tasks in list')

    # option to close tasks from todo list
    p.add_argument('-f', '--finish',
                   action="store",
                   type=int,
                   nargs='+',
                   metavar='N',
                   help='remove tasks numbered N [N ...] from list')

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
    p.add_argument('--version', 
                   action='version', 
                   version='%(prog)s '+__version__)

    #=============================================================#
    # Parsing options and perform appropriate actions accordingly #
    #=============================================================#
    args = p.parse_args()

    if _db.remote_mode and not _db.shelf:
        if args.start:
            _db.sync_local_dbstore()
        else:
            cry_msg(p.prog, 
                    msg='please execute "pda --start" first; and "pda --stop" before leaving pda')
    else:
        if args.clear:
            _db.remove_all_tasks()
        elif args.finish:
            _db.finish_tasks(args.finish)
        elif args.add:
            _db.add_task(args.add, 
                         task_type=args.listname, 
                         milestone=_db.extend_milestone(args.time), 
                         priority=convert_prio_int_to_txt(args.priority))
        elif args.edit:
            _db.edit_task(
                args.edit, 
                new_summary=args.summary, 
                new_tasktype=args.listname,
                new_milestone=_db.extend_milestone(args.time),
                new_priority=convert_prio_int_to_txt(args.priority))
        elif _db.remote_mode and args.stop:
            _db.sync_remote_dbstore()
        else: # print out contents stored in lists
            _db.read_tasks(args.listname, 
                           _db.extend_milestone(args.time), 
                           convert_prio_int_to_txt(args.priority))

def main():
    """``pda`` entry point
    """
    _db = GithubIssues(PdaConfig())
    controller(_db)

if __name__ == '__main__':
    main()
