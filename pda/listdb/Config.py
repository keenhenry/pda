#!/usr/bin/env python

"""
``Config`` module holds all the configuration-related implementations 
used in ``listdb`` package.

"""

try:
    import configparser as ConfigParser # python 3.3, 3.4
except ImportError:
    import ConfigParser # python 2.6, 2.7

import os
from ..utils import die_msg, PROG_NAME

class PdaConfig(object):
    """
    ``PdaConfig`` is a class which implements configuration abstraction 
    for ``ListDB`` class in ``GithubIssues`` module.

    """

    DEFAULTS = {
        'database-path': '/tmp/.pdastore',
        'username'     : None,
        'repo-name'    : None,
        'auth-token'   : None
    }

    def __init__(self, test_cfg=None):
        """
        :param test_cfg: :class: `file <file>` object or None
        """

        try:
            # load configurations from several possible locations
            self.__config = ConfigParser.RawConfigParser(self.DEFAULTS)

            if not test_cfg:
                self.__config.read([os.path.expanduser('~/.pdaconfig')])
            else:
                self.__config.readfp(test_cfg)

        except ConfigParser.ParsingError as err:
            # crash pda when configuration file is ill-formatted
            die_msg(PROG_NAME, msg=err)

    @property
    def local_db_path(self):
        """local_db_path attribute getter
        """

        try:
            path = self.__config.get('pda', 'database-path')
        except ConfigParser.NoSectionError or \
               ConfigParser.DuplicateSectionError:
            path = self.DEFAULTS['database-path']

        return path if path != "" else self.DEFAULTS['database-path']

    @property
    def username(self):
        """username attribute getter
        """

        try:
            name = self.__config.get('github', 'username')
        except ConfigParser.NoSectionError or \
               ConfigParser.DuplicateSectionError:
            name = self.DEFAULTS['username']

        return name if name != "" else self.DEFAULTS['username']

    @property
    def reponame(self):
        """reponame attribute getter
        """

        try:
            name = self.__config.get('github', 'repo-name')
        except ConfigParser.NoSectionError or \
               ConfigParser.DuplicateSectionError:
            name = self.DEFAULTS['repo-name']

        return name if name != "" else self.DEFAULTS['repo-name']

    @property
    def authtoken(self):
        """authtoken attribute getter
        """

        try:
            token = self.__config.get('github', 'auth-token')
        except ConfigParser.NoSectionError or \
               ConfigParser.DuplicateSectionError:
            token = self.DEFAULTS['auth-token']

        return token if token != "" else self.DEFAULTS['auth-token']

    @property
    def remote_mode(self):
        """remote_mode attribute getter
        """

        return (self.username is not None) and \
               (self.reponame is not None) and \
               (self.authtoken is not None)
