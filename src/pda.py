#!/usr/bin/env python

import subprocess
import optparse
import re

#==========================================================================
#   This file is the pda cli 
#==========================================================================

# VERBOSE = False

# functions to parse options
def create(option, opt_str, value, parser, *args, **kwargs):
    assert value is None
    value = []

    if not parser.rargs:
        parser.error("-c option requires at least one argument")
    else:
        for arg in parser.rargs:
            value.append(arg)

    # consume arguments in rargs
    del parser.rargs[:len(value)]

    # set value for dest variable
    setattr(parser.values, option.dest, value)

def update(option, opt, value, parser):
    print "update lists"

# Function to control option parsing in Python
def controller():
    # global VERBOSE

    # create instance of OptionParser Module 
    p = optparse.OptionParser(description = 'A Personal Desktop Assistant to manage useful lists, like TODO list.',
                              prog        = 'pda',
                              version     = 'pda 0.1',
                              usage       = '%prog [-c <list names>] [-s <list name>]')

    #========================#
    # Create Options objects #
    #========================#

    # option to create lists
    p.add_option('--create', '-c', 
            action='callback', 
            callback=create, 
            dest='create',
            help='create lists in database')

    # option to display the content of a list
    # this option takes ONE argument only
    p.add_option('--show', '-s', 
            action='store', 
            dest='show',
            nargs=1,
            metavar="LISTNAME",
            help='show contents of a list in database')

    # option to include all the lists available in database for processing
    p.add_option('--all', '-a',
                 action='store_true',
                 help='include all the lists in database to be operated on');

    # option to specify list(s)
    # p.add_option('--list', '-l', dest="lists", help='specify the lists to be operated on', default=[]);
    # options to update lists
    # p.add_option('--add','-a', action="store_true", help='gets current IP Address')
    # p.add_option('--update','-u', action="store_true", help='gets current IP Address')
    # p.add_option('--priority','-p', action="store_true", help='gets current IP Address')
    # p.add_option('--delete','-d', action="store_true", help='gets current IP Address')

    # other options
    # p.add_option('--verbose', '-v', action = 'store_true', help='prints verbosely', default=False)

    options, arguments = p.parse_args()

    #=============================================================#
    # Parsing options and perform appropriate actions accordingly #
    #=============================================================#

    # debugging message for options and arguments
    print options, arguments

    if options.create:
        if options.all: print "create all lists"
        else:           print "create lists"
    elif options.show:
        if options.all: print "show all lists"
        else:           print "show list"
    else:
        p.print_help()

def main():
    controller()

if __name__ == '__main__':
    main()
