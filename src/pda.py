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
            usage       = '%(prog)s [-i DESCRIPTION] [-c|-d|-w|-m|-s|-y] lists'
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

    # option to include all the lists available in database for processing
    # p.add_argument('--all',
    #              action='store_true',
    #              default=False,
    #              help='include all the lists in database to be operated on');

    # options to insert items into lists
    p.add_argument('-i', '--insert',
                   action="store", 
                   type=str,
                   metavar='DESCRIPTION',
                   help='insert an item into lists')

    # options to update items into lists
    # p.add_option('--update','-u', action="store_true", help='gets current IP Address')
    # options to change priorities of items in lists
    # p.add_option('--priority','-p', action="store_true", help='gets current IP Address')
    # options to delete items in lists
    # p.add_option('--remove','-r', action="store_true", help='gets current IP Address')

    # other options
    # p.add_option('--verbose', '-v', action = 'store_true', help='prints verbosely', default=False)
    p.add_argument('--version', action='version', version='%(prog)s 0.1')

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
