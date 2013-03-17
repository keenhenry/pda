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

def show(parser, opt, args):

    if not args:
        parser.error("-s option requires at least an argument")
    else:
        print "show lists:", args
    return

def update(option, opt, value, parser):
    print "update lists"


# Function to control option parsing in Python
def controller():
    # global VERBOSE

    # create instance of OptionParser Module 
    p = optparse.OptionParser(description = 'A Personal Desktop Assistant to manage useful lists, like TODO list.',
                              prog        = 'pda',
                              version     = 'pda 0.1',
                              usage       = 'usage: %prog [options] [list(s)]')

    #========================#
    # Create Options objects #
    #========================#

    # option to create lists
    p.add_option('--create', '-c', 
            action='callback', 
            callback=create, 
            dest='create',
            metavar="LISTS",
            help='create list(s) in database')

    # option to display lists
    p.add_option('--show', '-s', action="store_true", help='show contents of a list(s) in database')

    # option to specify list(s)
    # p.add_option('--list', '-l', dest="lists", help='specify the lists to be operated on', default=[]);
    # p.add_option('--all', '-a', nargs=0, dest="lists", help='specify the lists to be operated on', default=['todo','tolearn','note','qa','resolution']);

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
    # if options.verbose:
    #     VERBOSE=True

    if options.create:
        print "create lists"
    elif options.show:
        show(p, options, arguments)
    else:
        p.print_help()

def main():
    controller()

if __name__ == '__main__':
    main()
