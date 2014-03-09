"""
pda.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within pda,
that are also useful for external consumption, for example, unit tests.

"""

def cry_msg(prog, err_str="", msg=""):
    """Emit error messages for pda
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """
    print '{}: {}{}'.format(prog, err_str, msg)
