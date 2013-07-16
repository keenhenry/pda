#!/usr/bin/env python

import subprocess
import re
import argparse

#==========================================================================
#   This file is the pda cli 
#==========================================================================

# Function to control option parsing in Python
def controller():

    # create instance of ArgumentParser Module 
    p = argparse.ArgumentParser(
            description = 'A Personal Desktop Assistant to manage useful lists, like TODO list.',
            prog        = 'pda',
            usage       = '%(prog)s [-i DESCRIPTION] [-r LIST] [-u LIST] [-p LIST] [-n N ...] [-c|-d|-w|-m|-s|-y] lists'
        )

    #========================#
    # Create Options objects #
    #========================#

    # option to create lists
    p.add_argument('-c', '--create',
            action='store_true',
            help='create lists in database')

    # positional argument to hold the lists to be displayed
    p.add_argument('lists',
            nargs='*',
            help='tell pda which lists to work on')

    # options to insert items into lists
    p.add_argument('-i', '--insert',
                   action="store", 
                   type=str,
                   metavar='DESCRIPTION',
                   help='insert an item into lists')

    # options to update items in a list
    p.add_argument('-u', '--update',
                   action="store", 
                   metavar='LIST',
                   help='update an item in a list')

    # options to change priorities of items in lists
    p.add_argument('-p', '--priority',
                   action="store", 
                   metavar='LIST',
                   help='change the priority of an item in a list')

    # options to remove items from lists
    p.add_argument('-r', '--remove',
                   action="store",
                   metavar='LIST',
                   help='remove items from a list')

    # other options
    # p.add_option('--verbose', '-v', action = 'store_true', help='prints verbosely', default=False)
    p.add_argument('--version', action='version', version='%(prog)s 0.1')
    p.add_argument('-n', 
                    action='store', 
                    nargs='+',
                    help='specify item numbers from a list')

    # time period optional arguments
    p.add_argument('-d', action='store_true', help='daily content in a list')       # daily
    p.add_argument('-w', action='store_true', help='weekly content in a list')      # weekly
    p.add_argument('-m', action='store_true', help='monthly content in a list')     # monthly
    p.add_argument('-s', action='store_true', help='seasonally content in a list')  # seasonally
    p.add_argument('-y', action='store_true', help='yearly content in a list')      # yearly

    # debugging message for options and arguments
    args = p.parse_args()
    print args

    #=============================================================#
    # Parsing options and perform appropriate actions accordingly #
    #=============================================================#
    if args.create:
        if args.lists:
            print 'create lists:', args.lists
        else:
            # throw an error
            # you probably need an full blown Error object
            print 'no lists to be created'
    elif args.insert:
        print 'insert "' + args.insert + '" into lists:', args.lists
    elif args.update:
        if args.n is None:
            print 'Error: no item numer is specified; nothing is updated'
        else:
            if len(args.n) == 1:
                print 'update item', repr(args.n), 'from list:', args.update
            else:
                print 'Error: too many items specified; only ONE item is allowed to be updated at one time'
    elif args.priority:
        if args.n is None:
            print 'Error: no item numer is specified; nothing is updated'
        else:
            if len(args.n) == 1:
                print 'change priority of item', repr(args.n), 'from list:', args.priority
            else:
                print 'Error: too many items specified; only ONE item is allowed to be updated at one time'
    elif args.remove:
        if args.n is None:
            print 'remove all the items from list:', args.remove
        else:
            print 'remove items', repr(args.n), 'from list:', args.remove
    elif args.lists:
        # this default behavior is to display contents of
        # lists stored in the database, the following conditional
        # branches can be implemented in DB model instead of here
        if args.d:
            print 'show daily contents in lists:', args.lists
        if args.w:
            print 'show weekly contents in lists:', args.lists
        if args.m:
            print 'show monthly contents in lists:', args.lists
        if args.s:
            print 'show seasonally contents in lists:', args.lists
        if args.y:
            print 'show yearly contents in lists:', args.lists
        if not (args.d or args.w or args.m or args.s or args.y):
            print 'show daily and weekly contents (default) in lists:', args.lists
    else:
        p.print_help()

def main():
    controller()

if __name__ == '__main__':
    main()
