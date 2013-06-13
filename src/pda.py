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
            usage       = '%(prog)s [-c] lists'
        )

    #========================#
    # Create Options objects #
    #========================#

    # option to create lists
    p.add_argument('-c', '--create',
            action='store_true',
            help='create lists in database')

    # positional argument to hold the lists to be to display
    p.add_argument('lists',
            nargs='*',
            help='tell pda which lists to work on')

    # option to include all the lists available in database for processing
    # p.add_argument('--all',
    #              action='store_true',
    #              default=False,
    #              help='include all the lists in database to be operated on');

    # options to update lists
    # p.add_option('--add','-a', action="store_true", help='gets current IP Address')
    # p.add_option('--update','-u', action="store_true", help='gets current IP Address')
    # p.add_option('--priority','-p', action="store_true", help='gets current IP Address')
    # p.add_option('--delete','-d', action="store_true", help='gets current IP Address')

    # other options
    # p.add_option('--verbose', '-v', action = 'store_true', help='prints verbosely', default=False)
    p.add_argument('--version', action='version', version='%(prog)s 0.1')

    args = p.parse_args()

    # debugging message for options and arguments
    print args

    #=============================================================#
    # Parsing options and perform appropriate actions accordingly #
    #=============================================================#
    if args.create:
        if args.lists:
            print 'create lists:', args.lists
        else:
            # throw an error
            print 'no lists to be created'
    elif args.lists:
        # no optional arguments at all, only positional argument exists
        # this default behavior for this situation is to display contents of
        # lists stored in the database
        print 'show lists:', args.lists
    else:
        p.print_help()

def main():
    controller()

if __name__ == '__main__':
    main()
