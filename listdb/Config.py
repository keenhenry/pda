#!/usr/bin/env python

"""
`Config` is a module which implements configuration for `ListDB`.

"""

from ConfigParser import ConfigParser, NoSectionError, DuplicateSectionError
import os

class PdaConfig(object):

    DEFAULTS = {
        'database-path': '/tmp/.pdastore',
        'username'     : None,
        'repo-name'    : None,
        'auth-token'   : None
    }

    def __init__(self, fp=None):

        assert fp is None or isinstance(fp, file), fp

        self.__config = ConfigParser(self.DEFAULTS, allow_no_value=True)
        if fp is not None:
            self.__config.readfp(fp)

    @property
    def local_db_path(self):
        try:
            path = self.__config.get('pda', 'database-path')
        except NoSectionError or DuplicateSectionError:
            path = self.DEFAULTS['database-path']
        return path

    @property
    def username(self):
        try:
            name = self.__config.get('github', 'username')
        except NoSectionError or DuplicateSectionError:
            name = self.DEFAULTS['username']
        return name

    @property
    def reponame(self):
        try:
            name = self.__config.get('github', 'repo-name')
        except NoSectionError or DuplicateSectionError:
            name = self.DEFAULTS['repo-name']
        return name

    @property
    def authtoken(self):
        try:
            token = self.__config.get('github', 'auth-token')
        except NoSectionError or DuplicateSectionError:
            token = self.DEFAULTS['auth-token']
        return token

    @property
    def remote_mode(self):
        try:
            mode = (self.__config.get('github', 'username')   is not None) and \
                   (self.__config.get('github', 'repo-name')  is not None) and \
                   (self.__config.get('github', 'auth-token') is not None)
        except NoSectionError or DuplicateSectionError:
            mode = False
        return mode

def main():

    cfg_path = os.path.expanduser('~/.pdaconfig')
    if os.path.exists(cfg_path):
        cfg = PdaConfig(open(cfg_path))
        print cfg.username
        print cfg.reponame
        print cfg.authtoken
        print cfg.local_db_path
        print cfg.remote_mode
    

if __name__ == '__main__':
    main()
