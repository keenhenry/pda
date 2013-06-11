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
            usage       = '%(prog)s [-c <list names>] lists'
        )

    #========================#
    # Create Options objects #
    #========================#

    # option to create lists
    p.add_argument('-c', '--create',
            nargs='+',
            metavar='<list name>',
            help='create lists in database')

    # option to display the content of lists
    p.add_argument('show',
            nargs='*',
            metavar="lists",
            help='show content of a lists in database')

    # option to include all the lists available in database for processing
    # p.add_argument('--all',
    #              action='store_true',
    #              default=False,
    #              help='include all the lists in database to be operated on');

    # option to specify list(s)
    # p.add_option('--list', '-l', dest="lists", help='specify the lists to be operated on', default=[]);
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
        print args.create
    elif args.show:
        print args.show
    #     if options.all: print "create all lists"
    #     else:           print "create lists"
    # elif args.show:
    #     if options.all: print "show all lists"
    #     else:           print "show list"
    else:
        p.print_help()

def main():
    controller()

if __name__ == '__main__':
    main()
