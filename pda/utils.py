"""
pda.utils
~~~~~~~~~

This module provides utility functions that are used by ``pda`` and 
also useful for external consumption, for example, unit tests.

"""

import sys

PROG_NAME = 'pda'

def print_header():
    """print pretty header of list content

    The head contains 5 columns, each column has a differnt string length.
    """

    headers = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']

    print
    print '{0:<5}  {1:<60}  {2:<9}  {3:<8}  {4:<8}'.format(*headers)
    print '{0:=<5}  {1:=<60}  {2:=<9}  {3:=<8}  {4:=<8}'.format(*['', '', '', \
                                                                  '', ''])

def cry_msg(prog, err_str="", msg=""):
    """Emit error messages for pda
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """
    print '{0}: {1}{2}'.format(prog, err_str, msg)

def die_msg(prog, msg=''):
    """Crash pda with an error message -> used for more fatal errors
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """

    print '{0}: error: {1}'.format(prog, msg)
    sys.exit(1)
