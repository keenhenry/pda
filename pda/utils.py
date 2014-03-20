"""
pda.utils
~~~~~~~~~

This module provides utility functions that are used within pda,
that are also useful for external consumption, for example, unit tests.

"""

import sys


def print_header():

    headers = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']

    # TODO: should remove magic numbers below, give them some symbolic constants
    print
    print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*headers)
    print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])

def cry_msg(prog, err_str="", msg=""):
    """Emit error messages for pda
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """
    print '{}: {}{}'.format(prog, err_str, msg)

def die_msg(prog, msg=''):
    """
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """

    print '{}: error: {}'.format(prog, msg)
    sys.exit(1)
