#!/usr/bin/env python

"""
`Config` is a module which implements configuration for `ListDB`.

"""

import ConfigParser
import os

class PdaConfig(object):

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
            self.__config.read(['./.pdaconfig', os.path.expanduser('~/.pdaconfig')])
        except ConfigParser.ParsingError, err:
            print 'pda:', err
            print 'pda:', 'using default settings instead ...'

    @property
    def local_db_path(self):
        try:
            path = self.__config.get('pda', 'database-path')
        except ConfigParser.NoSectionError or ConfigParser.DuplicateSectionError:
            path = self.DEFAULTS['database-path']

        return path if path != "" else self.DEFAULTS['database-path']

    @property
    def username(self):
        try:
            name = self.__config.get('github', 'username')
        except ConfigParser.NoSectionError or ConfigParser.DuplicateSectionError:
            name = self.DEFAULTS['username']

        return name if name != "" else self.DEFAULTS['username']

    @property
    def reponame(self):
        try:
            name = self.__config.get('github', 'repo-name')
        except ConfigParser.NoSectionError or ConfigParser.DuplicateSectionError:
            name = self.DEFAULTS['repo-name']

        return name if name != "" else self.DEFAULTS['repo-name']

    @reponame.setter
    def reponame(self, new_reponame):

        assert new_reponame is not None and isinstance(new_reponame, str), new_reponame

        if self.remote_mode:
            self.__config.set('github', 'repo-name', new_reponame)

    @property
    def authtoken(self):
        try:
            token = self.__config.get('github', 'auth-token')
        except ConfigParser.NoSectionError or ConfigParser.DuplicateSectionError:
            token = self.DEFAULTS['auth-token']

        return token if token != "" else self.DEFAULTS['auth-token']

    @property
    def remote_mode(self):
        return (self.username is not None) and \
               (self.reponame is not None) and \
               (self.authtoken is not None)

def main():
    cfg = PdaConfig()
    cfg.reponame = 'todo'
    print cfg.username
    print cfg.reponame
    print cfg.authtoken
    print cfg.local_db_path
    print cfg.remote_mode

if __name__ == '__main__':
    main()
