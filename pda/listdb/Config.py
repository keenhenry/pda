#!/usr/bin/env python

"""
``Config`` module holds all the configuration-related implementations 
used in ``listdb`` package.

"""

import ConfigParser
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

    def __init__(self):

        try:
            # load configurations from several possible locations
            self.__config = ConfigParser.RawConfigParser(self.DEFAULTS)
            self.__config.read(['./.pdaconfig', \
                                os.path.expanduser('~/.pdaconfig')])
        except ConfigParser.ParsingError, err:
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

    @reponame.setter
    def reponame(self, new_reponame):
        """reponame attribute setter
        :param new_reponame: string
        """

        assert new_reponame is not None and \
               isinstance(new_reponame, str), new_reponame

        if self.remote_mode:
            self.__config.set('github', 'repo-name', new_reponame)

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
