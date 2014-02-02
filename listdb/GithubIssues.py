#!/usr/bin/env python

"""
`ListDB` is a data model abstraction of the list databse used by `pda`.

"""

import requests
import os
import shelve
import json
import sys


DEFAULT_BASE_URL = "https://api.github.com/repos/"
REPO_NAME = 'keenhenry/todo'
# REPO_NAME = 'keenhenry/lists'

class ListDB(object):
    """Base class for representing list database.
    """

    # COLOR constants
    GREEN  = '009800'
    YELLOW = 'fbca04'
    RED    = 'e11d21'
    BLUE   = '0052cc'
    
    # PRIORITY constants
    URGENT_MUSTDO     = 5
    MUSTDO            = 4
    HIGH_IMPORTANCE   = 3
    MEDIUM_IMPORTANCE = 2
    LOW_IMPORTANCE    = 1

    # default local database mirror path
    DEFAULT_LOCAL_DBPATH = '/tmp/.pdastore'

    def __init__(self):

        self.__url_issues     = DEFAULT_BASE_URL + REPO_NAME + "/issues"
        self.__url_milestones = DEFAULT_BASE_URL + REPO_NAME + "/milestones"
        self.__url_labels     = DEFAULT_BASE_URL + REPO_NAME + "/labels"
        self.__auth           = (os.environ['PDA_AUTH'], '')
        self.__max_taskno     = -1
        self.__shelf          = shelve.open(os.path.abspath(self.DEFAULT_LOCAL_DBPATH), 
                                            protocol=-1,
                                            writeback=True)

    def __del__(self):
        self.__shelf.close()

    @property
    def shelf(self):
        return self.__shelf

    @property
    def url_issues(self):
        return self.__url_issues

    @property
    def url_milestones(self):
        return self.__url_milestones

    @property
    def url_labels(self):
        return self.__url_labels

    @property
    def auth(self):
        return self.__auth

    @property
    def max_task_number(self):
        return self.__max_taskno

    @max_task_number.setter
    def max_task_number(self, value):
        self.__max_taskno = value

    def _has_task(self, task_number):
        """
        :param task_number: integer
        :rtype: True or False
        """

        assert isinstance(task_number, (int, long)), task_number

        return self.shelf.has_key(str(task_number))

    def _get_task_prio_and_type(self, task):
        """
        :param task: dict
        :rtype: tuple
        """

        assert task is not None and isinstance(task, dict), task

        prio, task_type = None, None

        for label in task["labels"]:
            if label["color"] == self.YELLOW:     prio = label["name"]
            if label["color"] == self.GREEN: task_type = label["name"]
        
        return prio, task_type

    def _is_selected(self, task_type_in_db, task_type_requested, 
                           milestone_in_db, milestone_requested, 
                           priority_in_db, priority_requested):

        return (task_type_requested is None or task_type_requested == task_type_in_db) and \
               (milestone_requested is None or milestone_requested == milestone_in_db) and \
               (priority_requested is None or priority_requested == priority_in_db)

    def _is_cmd_history_annihilable(self, task_number):
        """
        :param task_number: integer
        :rtype: True or False
        """

        o_cmd_list = self.shelf['CMDS_HISTORY']
        n_cmd_list = [cmd for cmd in o_cmd_list if \
                          not (cmd['#'] == task_number and cmd['CMD'] != 'REMOVE')]

        self.shelf['CMDS_HISTORY'] = n_cmd_list

        return (len(n_cmd_list) < len(o_cmd_list))

    def _is_locally_created_issue_updated(self, task_number, 
                                                new_summary, 
                                                new_tasktype, 
                                                new_milestone,
                                                new_priority):
        """
        :param task_number: integer
        :param new_summary  : None or string
        :param new_tasktype : None or string
        :param new_milestone: None or string
        :param new_priority : None or string
        :rtype: True or False
        """

        o_cmd_list, n_cmd_list = self.shelf['CMDS_HISTORY'], []
        is_local_created_issue_updated = False

        for cmd in o_cmd_list:
            if cmd['#'] == task_number and cmd['CMD'] == 'ADD':
                if new_summary: cmd['SUMMARY'] = new_summary
                if new_tasktype: cmd['TYPE'] = new_tasktype
                if new_priority: cmd['PRIORITY'] = new_priority
                if new_milestone: cmd['MILESTONE'] = new_milestone
                is_local_created_issue_updated = True
            n_cmd_list.append(cmd)

        self.shelf['CMDS_HISTORY'] = n_cmd_list

        return is_local_created_issue_updated

    def _get_one_label(self, name, color, labels):
        """
        :param name: string
        :param color: string
        :param labels: list of strings 
        """

        r = requests.get(self.url_labels+'/'+name, auth=self.auth)

        if r.status_code == requests.codes.ok: # label found
            labels.append(name)
        else: # label not found, create a new label in Github Issues
            rep = requests.put(self.url_labels, 
                               data=json.dumps({'name': name, 'color': color}), 
                               auth=self.auth)

            if rep.status_code == requests.codes.created:
                labels.append(name)
            else:
                self.die_msg('label created failed: '+ name)

    def _update_labels(self, cmd):
        """
        :param cmd: dict
        :rtype: list of strings
        """

        labels, issue_number, issue_type, issue_prio = [], cmd['#'], cmd['TYPE'], cmd['PRIORITY']

        r = requests.get(self.url_issues+'/'+str(issue_number)+'/labels', auth=self.auth)

        if r.status_code == requests.codes.ok:
            # replacing labels
            for label in r.json():
                if label['color'] == self.GREEN:
                    if issue_type and issue_type != label['name']: 
                        labels.append(issue_type)
                    else:
                        labels.append(label['name'])
                elif label['color'] == self.YELLOW:
                    if issue_prio and issue_prio != label['name']: 
                        labels.append(issue_prio)
                    else:
                        labels.append(label['name'])
                else: # for other colors, still keep original labels
                    labels.append(label['name'])

            # adding labels if not already present in labels after replacing
            if issue_type and issue_type not in labels:
                labels.append(issue_type)
            if issue_prio and issue_prio not in labels:
                labels.append(issue_prio)
        else:
            self.die_msg('failed to retrive labels for current issue: '+str(issue_number))

        return labels

    def _get_labels(self, cmd):
        """
        :param cmd: dict
        :rtype: list of strings
        """

        labels = []

        if cmd['TYPE']:
            self._get_one_label(cmd['TYPE'], self.GREEN, labels)

        if cmd['PRIORITY']:
            self._get_one_label(cmd['PRIORITY'], self.YELLOW, labels)

        return labels

    def _get_milestone_number(self, cmd):
        """
        :param cmd: dict
        :rtype: integer or None
        """

        milestone_number, milestone_title = None, cmd['MILESTONE']

        # look for existing milestone
        if milestone_title:
            r = requests.get(self.url_milestones, auth=self.auth)

            if r.status_code == requests.codes.ok:
                for milestone in r.json():
                    if milestone['title'] == milestone_title:
                        milestone_number = milestone['number']
                        break
            else:
                self.die_msg('retrieving milestone failed')

        # milestone not created yet, create one
        if milestone_title and not milestone_number:
            r = requests.post(url=self.url_milestones,
                              data=json.dumps({'title': milestone_title}),
                              auth=self.auth)

            if r.status_code == requests.codes.created:
                milestone_number = r.json()['number']
            else:
                self.die_msg('create milestone failed')

        return milestone_number

    def _prepare_payload_for_add_or_edit(self, cmd, payload):
        """
        :param cmd: dict
        :param payload: dict
        """

        assert payload is not None and isinstance(payload, dict), payload

        milestone_number = self._get_milestone_number(cmd) 
        labels           = self._get_labels(cmd) if cmd['CMD'] == 'ADD' \
                                                 else self._update_labels(cmd)

        if cmd['SUMMARY']: 
            payload['title'] = cmd['SUMMARY']
        if cmd['MILESTONE'] and milestone_number: 
            payload['milestone'] = milestone_number
        if labels: 
            payload['labels'] = labels

    def _prepare_method_url_and_payload(self, cmd):
        """
        :param cmd: dict
        :rtype: tuple of (str, dict)
        """

        url, payload = self.url_issues, {}

        if cmd['CMD'] == 'REMOVE':
            url += '/'+str(cmd['#']) 
            payload['state'] = 'closed'
        elif cmd['CMD'] == 'ADD':
            self._prepare_payload_for_add_or_edit(cmd, payload)
        elif cmd['CMD'] == 'EDIT':
            url += '/'+str(cmd['#']) 
            self._prepare_payload_for_add_or_edit(cmd, payload)
        else: # should never reach here!
            self.die_msg('CMD type unknown in command history')

        return url, payload

    def _exec_cmd_on_remote(self, cmd):
        """
        :param cmd: dict
        :rtype: True or False
        """

        assert cmd is not None and isinstance(cmd, dict), cmd

        success = False

        url, payload = self._prepare_method_url_and_payload(cmd)

        if cmd['CMD'] == 'ADD':
            r = requests.post(url=url, data=json.dumps(payload), auth=self.auth)
            success = (r.status_code == requests.codes.created)
        elif cmd['CMD'] == 'EDIT':
            r = requests.patch(url=url, data=json.dumps(payload), auth=self.auth)
            success = (r.status_code == requests.codes.ok)
        else: # REMOVE
            r = requests.patch(url=url, data=json.dumps(payload), auth=self.auth)
            success = (r.status_code == requests.codes.ok)

        return success

    def _print_header(self):

        headers = ['TASK#', 'SUMMARY', 'LIST TYPE', 'DUE TIME', 'PRIORITY']

        print
        print '{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(*headers)
        print '{:=<5}  {:=<60}  {:=<9}  {:=<8}  {:=<8}'.format(*['','','','',''])

    def _print_task(self, task_number, task_type, milestone, priority):
        """Helper function for read_tasks()
        :param task_number: string
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        if self._is_selected(self.shelf[task_number]['type'], task_type,
                             self.shelf[task_number]['milestone'], milestone,
                             self.shelf[task_number]['priority'], priority):
            print u'{:<5}  {:<60}  {:<9}  {:<8}  {:<8}'.format(
                                                         task_number, 
                                                         self.shelf[task_number]["summary"], 
                                                         self.shelf[task_number]["type"], 
                                                         self.shelf[task_number]["milestone"], 
                                                         self.shelf[task_number]["priority"])


    def sync_local_dbstore(self):

        # retrieving OPEN issues from Github Issues
        r = requests.get(self.url_issues, params={'state': 'open'}, auth=self.auth)

        if r.status_code == requests.codes.ok:
            # write issue data into local db store
            for issue in r.json():
                prio, ltype = self._get_task_prio_and_type(issue)
                milestone   = issue["milestone"]["title"] if issue["milestone"] else None

                issue_data = {
                              "summary"  : issue["title"],
                              "type"     : ltype,
                              "milestone": milestone,
                              "priority" : prio
                             }

                self.shelf[str(issue["number"])] = issue_data
                self.max_task_number = issue["number"] if issue["number"] > self.max_task_number \
                                                    else self.max_task_number

            # create a list to hold command history records
            self.shelf['CMDS_HISTORY'] = []

            # sync to local store
            self.shelf.sync()
        else:
            die_msg('syncing to local store failed')

    def sync_remote_dbstore(self):

        # syncing data to remote (Github Issues)
        for cmd in self.shelf['CMDS_HISTORY']:
            ok = self._exec_cmd_on_remote(cmd)
            if not ok:
                self.die_msg('syncing remote failed'), repr(cmd)

        # remove local data store after syncing data to remote
        os.remove(self.DEFAULT_LOCAL_DBPATH)
        
    def remove_task(self, task_number):
        """
        :param task_number: integer
        """

        assert isinstance(task_number, (int, long)), task_number

        if self._has_task(task_number):

            # delete task at local store
            del self.shelf[str(task_number)]

            # record remove operation in list 'CMDS_HISTORY' in local store
            if not self._is_cmd_history_annihilable(task_number):
                cmd_history_data = { 'CMD': 'REMOVE', '#': task_number }
                self.shelf['CMDS_HISTORY'].append(cmd_history_data)

            self.shelf.sync()

    def add_task(self, summary, task_type=None, milestone=None, priority=None):
        assert summary   is not None and isinstance(summary,   str), summary
        assert task_type is None or isinstance(task_type, str), task_type
        assert milestone is None or isinstance(milestone, str), milestone
        assert priority  is None or isinstance(priority,  str), priority

        issue_data = {
                      "summary"  : summary,
                      "type"     : task_type,
                      "milestone": milestone,
                      "priority" : priority
                     }

        # the value of the key for local store is not important, as long as it is unique
        self.max_task_number += 1
        self.shelf[str(self.max_task_number)] = issue_data

        # record ADD operation in list 'CMDS_HISTORY' in local store
        cmd_history_data = { '#'        : self.max_task_number,
                             'CMD'      : 'ADD', 
                             'SUMMARY'  : summary,
                             'TYPE'     : task_type,
                             'MILESTONE': milestone,
                             'PRIORITY' : priority }
        self.shelf['CMDS_HISTORY'].append(cmd_history_data)

        self.shelf.sync()

        return self.max_task_number

    def edit_task(self, task_number, 
                  new_summary  =None, 
                  new_tasktype =None, 
                  new_milestone=None, 
                  new_priority =None):
        """
        :param task_number  : integer
        :param new_summary  : string
        :param new_tasktype : string
        :param new_milestone: string
        :param new_priority : string
        """

        assert task_number   is not None and isinstance(task_number, (int,long)), task_number
        assert new_summary   is None or isinstance(new_summary,   str), new_summary
        assert new_tasktype  is None or isinstance(new_tasktype,  str), new_tasktype
        assert new_milestone is None or isinstance(new_milestone, str), new_milestone
        assert new_priority  is None or isinstance(new_priority,  str), new_priority

        if self._has_task(task_number):
            if new_summary: 
                self.shelf[str(task_number)]["summary"] = new_summary
            if new_tasktype: 
                self.shelf[str(task_number)]["type"] = new_tasktype
            if new_milestone: 
                self.shelf[str(task_number)]["milestone"] = new_milestone
            if new_priority: 
                self.shelf[str(task_number)]["priority"] = new_priority

            # record EDIT operation in list 'CMDS_HISTORY' in local store
            if not self._is_locally_created_issue_updated(task_number, new_summary, new_tasktype,
                    new_milestone, new_priority):
                cmd_history_data = { 'CMD'      : 'EDIT', 
                                     '#'        : task_number,
                                     'SUMMARY'  : new_summary,
                                     'TYPE'     : new_tasktype,
                                     'MILESTONE': new_milestone,
                                     'PRIORITY' : new_priority }
                self.shelf['CMDS_HISTORY'].append(cmd_history_data)
            self.shelf.sync()

    def read_tasks(self, task_type=None, milestone=None, priority=None):
        """
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        assert task_type is None or isinstance(task_type, str), task_type
        assert milestone is None or isinstance(milestone, str), milestone
        assert priority  is None or isinstance(priority,  str), priority

        self._print_header()
        for key in self.shelf:
            if key != 'CMDS_HISTORY':
                self._print_task(key, task_type, milestone, priority)

        # DEBUG: check CMDS_HISTORY
        # print 'History:', repr(self.shelf['CMDS_HISTORY'])

    def die_msg(self, msg=''):
        """
        :param msg: string
        """

        print '{}: error: {}'.format('pda', msg)
        sys.exit(1)

def main():

    # create db object
    db = ListDB()

    db.sync_local_dbstore()
    # db.read_tasks()
    # db.edit_task(task_number=50, new_tasktype='tolearn')
    # db.read_tasks()
    # number = db.add_task('2nd wrong formatted issue', task_type='todo')
    # db.read_tasks()
    # db.edit_task(task_number=number, new_milestone='week', new_priority='urgmust')
    # db.read_tasks()
    # db.remove_task(42)
    # db.remove_task(44)
    # db.remove_task(46)
    # db.remove_task(48)
    db.read_tasks()
    db.sync_remote_dbstore()

if __name__ == '__main__':
    main()
