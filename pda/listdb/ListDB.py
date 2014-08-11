#!/usr/bin/env python

"""
``ListDB`` is a module collecting implementations for data model abstraction of 
the list databse(s) used by ``pda``.

"""
from __future__ import print_function

import os
import shelve
import requests
import json

from ..utils import cry_msg, die_msg, print_header, sorted_tasks, PROG_NAME

class GithubIssues(object):
    """A class representing one list database abstraction for ``pda``.

    ``GithubIssues`` always stores data locally in a permanent data store 
    abstracted by python ``shelve``. And depends on the configuration, data 
    might also be synced/stored on **Github Issues**, if **Github Issues** 
    credentials is provided in the configuration.

    """

    # base url to Github Issues API
    BASE_URL = "https://api.github.com/repos/"

    # COLOR constants
    GREEN  = '009800'
    YELLOW = 'fbca04'
    RED    = 'e11d21'
    BLUE   = '0052cc'
    
    def __init__(self, config):
        """
        :param config: :class: `PdaConfig <PdaConfig>` object.
        """

        # initialize instance attributes based on the loaded configuration
        self.__shelf = shelve.open(os.path.abspath(config.local_db_path), 
                                   protocol=-1,
                                   writeback=True)
        self.__remote_mode  = config.remote_mode
        self.__local_dbpath = config.local_db_path

        if config.remote_mode:
            repo_name = config.username + '/' + config.reponame
            self.__url_issues     = self.BASE_URL + repo_name + "/issues"
            self.__url_milestones = self.BASE_URL + repo_name + "/milestones"
            self.__url_labels     = self.BASE_URL + repo_name + "/labels"
            self.__auth           = (config.authtoken, '')
        else:
            self.__url_issues     = ''
            self.__url_milestones = ''
            self.__url_labels     = ''
            self.__auth           = ('','')

    def __del__(self):
        self.__shelf.close()

    @property
    def local_dbpath(self):
        """the path to the local shelve db store
        :rtype: string
        """
        return self.__local_dbpath

    @property
    def remote_mode(self):
        """Is ``GithubIssues`` in remote mode or not?
        :rtype: bool
        """
        return self.__remote_mode

    @property
    def shelf(self):
        """a handle to shelf object
        :rtype: :class: `shelf <shelf>` object
        """
        return self.__shelf

    @property
    def url_issues(self):
        """the URL to fetch repo issues stored on **Github Issues**
        :rtype: string
        """
        return self.__url_issues

    @property
    def url_milestones(self):
        """the URL to fetch repo milestones stored on **Github Issues**
        :rtype: string
        """
        return self.__url_milestones

    @property
    def url_labels(self):
        """the URL to fetch repo labels stored on **Github Issues**
        :rtype: string
        """
        return self.__url_labels

    @property
    def auth(self):
        """authentication token used to communicate to **Github Issues**
        :rtype: tuple
        """
        return self.__auth

    @property
    def max_task_number(self):
        """current maximum task number in local shelve data store
        :rtype: integer
        """

        max_task_num = 0

        if self.shelf:
            task_numbers = [int(task_no) for task_no in self.shelf \
                                             if task_no != 'CMDS_HISTORY']
            if task_numbers:
                max_task_num = max(task_numbers)

        return max_task_num

    def _is_selected(self, task_no, task_type, milestone, priority):
        """method to check if current task is selected for output printing
        :param task_no: string
        :param task_type: None or string
        :param milestone: None or string
        :param priority: None or string
        :rtype: True or False
        """

        task_type_in_shelf = self.shelf[task_no]['type']
        milestone_in_shelf = self.shelf[task_no]['milestone']
        priority_in_shelf  = self.shelf[task_no]['priority']

        return (task_type is None or task_type == task_type_in_shelf) and \
               (milestone is None or milestone == milestone_in_shelf) and \
               (priority  is None or priority  == priority_in_shelf)

    def _is_cmd_history_annihilable(self, task_number):
        """check if command history stack shrinked by REMOVE command
        :param task_number: integer
        :rtype: True or False
        """

        o_cmd_list = self.shelf['CMDS_HISTORY']
        n_cmd_list = [cmd for cmd in o_cmd_list if not \
                      (cmd['#'] == task_number and cmd['CMD'] != 'REMOVE')]

        self.shelf['CMDS_HISTORY'] = n_cmd_list

        return (len(n_cmd_list) < len(o_cmd_list))

    def _is_added_issue_updated(self, task_number, 
                                new_summary, 
                                new_tasktype, 
                                new_milestone,
                                new_priority):
        """check if issues added by ADD commands also get 'EDIT'ed
        :param task_number: integer
        :param new_summary: None or string
        :param new_tasktype: None or string
        :param new_milestone: None or string
        :param new_priority: None or string
        :rtype: True or False
        """

        o_cmd_list, n_cmd_list = self.shelf['CMDS_HISTORY'], []
        is_added_issue_updated = False

        for cmd in o_cmd_list:
            if cmd['#'] == task_number and cmd['CMD'] == 'ADD':
                if new_summary: 
                    cmd['SUMMARY'] = new_summary
                if new_tasktype: 
                    cmd['TYPE'] = new_tasktype
                if new_priority: 
                    cmd['PRIORITY'] = new_priority
                if new_milestone: 
                    cmd['MILESTONE'] = new_milestone
                is_added_issue_updated = True
            n_cmd_list.append(cmd)

        self.shelf['CMDS_HISTORY'] = n_cmd_list

        return is_added_issue_updated

    def _get_one_label(self, name, color, labels):
        """fetch one **Github Issues** label; create one if not exists
        :param name: string
        :param color: string
        :param labels: list of strings 
        """

        resp = requests.get(self.url_labels+'/'+name, auth=self.auth)

        if resp.status_code == requests.codes.ok: # label found
            labels.append(name)
        else: # label not found, create a new label in Github Issues
            rep = requests.put(self.url_labels, 
                               data=json.dumps({'name': name, 'color': color}), 
                               auth=self.auth)

            if rep.status_code == requests.codes.created:
                labels.append(name)
            else:
                die_msg(PROG_NAME, 'label created failed: ' + name)

    def _update_labels(self, cmd):
        """update **Github Issues** based on the information given by `cmd`
        :param cmd: dict
        :rtype: list of strings
        """

        labels, issue_number, issue_type,  issue_prio = \
        [],     cmd['#'],     cmd['TYPE'], cmd['PRIORITY']

        resp = requests.get(self.url_issues+'/'+str(issue_number)+'/labels', 
                            auth=self.auth)

        if resp.status_code == requests.codes.ok:
            # replacing labels
            for label in resp.json():
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
            die_msg(PROG_NAME, \
                    'failed to retrive labels for current issue: '+str(issue_number))

        return labels

    def _get_labels(self, cmd):
        """fetch **priority** and **type** labels
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
        """fetch milestone id; if milestone not exists yet, 
           create one and return the id of the created milestone.

        :param cmd: dict
        :rtype: integer or None
        """

        milestone_number, milestone_title = None, cmd['MILESTONE']

        # look for existing milestone
        if milestone_title:
            resp = requests.get(self.url_milestones, auth=self.auth)

            if resp.status_code == requests.codes.ok:
                for milestone in resp.json():
                    if milestone['title'] == milestone_title:
                        milestone_number = milestone['number']
                        break
            else:
                die_msg(PROG_NAME, 'retrieving milestone failed')

        # milestone not created yet, create one
        if milestone_title and not milestone_number:
            resp = requests.post(url=self.url_milestones,
                              data=json.dumps({'title': milestone_title}),
                              auth=self.auth)

            if resp.status_code == requests.codes.created:
                milestone_number = resp.json()['number']
            else:
                die_msg(PROG_NAME, 'create milestone failed')

        return milestone_number

    def _get_payload_for_add_or_edit(self, cmd, payload):
        """fill in payload used for HTTPS request to **Github Issues**
        :param cmd: dict
        :param payload: dict
        """

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
        """contruct HTTP requests/query to **Github Issues**
        :param cmd: dict
        :rtype: tuple of (str, dict)
        """

        url, payload = self.url_issues, {}

        if cmd['CMD'] == 'REMOVE':
            url += '/'+str(cmd['#']) 
            payload['state'] = 'closed'
        elif cmd['CMD'] == 'ADD':
            self._get_payload_for_add_or_edit(cmd, payload)
        elif cmd['CMD'] == 'EDIT':
            url += '/'+str(cmd['#']) 
            self._get_payload_for_add_or_edit(cmd, payload)
        else: # should never reach here!
            die_msg(PROG_NAME, 'CMD type unknown in command history')

        return url, payload

    def _exec_cmd_on_remote(self, cmd):
        """send HTTPS requests to **Github Issues** API
        :param cmd: dict
        :rtype: True or False
        """

        success = False

        url, payload = self._prepare_method_url_and_payload(cmd)

        if cmd['CMD'] == 'ADD':
            resp = requests.post(url=url, 
                                 data=json.dumps(payload), 
                                 auth=self.auth)
            success = (resp.status_code == requests.codes.created)
        elif cmd['CMD'] == 'EDIT':
            resp = requests.patch(url=url, 
                                  data=json.dumps(payload), 
                                  auth=self.auth)
            success = (resp.status_code == requests.codes.ok)
        else: # REMOVE
            resp = requests.patch(url=url, 
                                  data=json.dumps(payload), 
                                  auth=self.auth)
            success = (resp.status_code == requests.codes.ok)

        return success

    def _print_task(self, task_number, task_type, milestone, priority):
        """Helper function for read_tasks()
        :param task_number: string
        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        if self._is_selected(task_number, task_type, milestone, priority):
            print ('{0:<5}  {1:<60}  {2:<9}  {3:<8}  {4:<8}'.format(
                   task_number, 
                   self.shelf[task_number]["summary"], 
                   self.shelf[task_number]["type"], 
                   self.shelf[task_number]["milestone"], 
                   self.shelf[task_number]["priority"]))

    @staticmethod
    def extend_milestone(milestone):
        """complete milestone name based on abbreviated milestone names
        :param milestone: string
        :rtype: string
        """

        # dictionary-based 'switch' statement
        # None is default if milestone is not found
        return {'d': 'day',
                'w': 'week',
                'm': 'month',
                's': 'season',
                'y': 'year'}.get(milestone, None) if milestone else None

    def has_task(self, task_number):
        """method checking if a task with task_number already exists 
           in local data store.

        :param task_number: integer
        :rtype: True or False
        """

        return (str(task_number) in self.shelf)

    def get_task_prio_and_type(self, task):
        """fetch task priority and type 
        :param task: dict
        :rtype: tuple
        """

        prio, task_type = None, None

        for label in task["labels"]:
            if label["color"] == self.YELLOW:
                prio = label["name"]
            if label["color"] == self.GREEN:
                task_type = label["name"]
        
        return prio, task_type


    def sync_local_dbstore(self):
        """method to download tasks from **Github Issues** to local data store
        """

        # retrieving OPEN issues from Github Issues
        resp = requests.get(self.url_issues, 
                            params={'state': 'open'}, 
                            auth=self.auth)

        if resp.status_code == requests.codes.ok:
            # write issue data into local db store
            for issue in resp.json():
                prio, ltype = self.get_task_prio_and_type(issue)
                milestone   = issue["milestone"]["title"] if issue["milestone"] else None

                issue_data = {
                              "summary"  : issue["title"],
                              "type"     : ltype,
                              "milestone": milestone,
                              "priority" : prio
                             }

                self.shelf[str(issue["number"])] = issue_data

            # create a list to hold command history records
            self.shelf['CMDS_HISTORY'] = []

            # sync to local store
            self.shelf.sync()
        else:
            die_msg(PROG_NAME, 'syncing to local store failed')

    def sync_remote_dbstore(self):
        """method to sync tasks from local data store with **Github Issues**
        """

        if 'CMDS_HISTORY' in self.shelf:

            # syncing data to remote (Github Issues)
            for cmd in self.shelf['CMDS_HISTORY']:
                _ok = self._exec_cmd_on_remote(cmd)
                if not _ok:
                    die_msg(PROG_NAME, 'syncing remote failed')

        # remove local data store after syncing data to remote
        os.remove(self.local_dbpath)
        
    def remove_task(self, task_number):
        """method to remove a task in local data store
        :param task_number: integer
        """

        if self.has_task(task_number):

            # delete task at local store
            del self.shelf[str(task_number)]

            # record remove operation in list 'CMDS_HISTORY' in local store
            if self.remote_mode and not \
               self._is_cmd_history_annihilable(task_number):
                cmd_history_data = { 'CMD': 'REMOVE', '#': task_number }
                self.shelf['CMDS_HISTORY'].append(cmd_history_data)

            self.shelf.sync()
        else:
            cry_msg(PROG_NAME, 
                    err_str='error: ', 
                    msg='no such task (#'+str(task_number)+') in the list')

    def finish_tasks(self, task_numbers):
        """method to remove tasks specified in ``task_numbers``
        :param task_numbers: list of integers
        """

        for t_id in task_numbers:
            self.remove_task(t_id)

    def remove_all_tasks(self):
        """method to remove all the tasks in local data store
        """

        for key in self.shelf:
            if key != 'CMDS_HISTORY':
                self.remove_task(int(key))

    def add_task(self, summary, task_type=None, milestone=None, priority=None):
        """method to create one task in local data store
        :param summary: string
        :param task_type: None or string
        :param milestone: None or string
        :param priority: None or string
        :rtype: integer
        """

        issue_data = {
                      "summary"  : summary,
                      "type"     : task_type,
                      "milestone": milestone,
                      "priority" : priority
                     }

        # the value of the key for local store is not important, 
        # as long as it is unique
        max_task_number = self.max_task_number + 1
        self.shelf[str(max_task_number)] = issue_data

        # record ADD operation in list 'CMDS_HISTORY' in local store
        if self.remote_mode:
            cmd_history_data = { '#'        : max_task_number,
                                 'CMD'      : 'ADD', 
                                 'SUMMARY'  : summary,
                                 'TYPE'     : task_type,
                                 'MILESTONE': milestone,
                                 'PRIORITY' : priority }
            self.shelf['CMDS_HISTORY'].append(cmd_history_data)

        self.shelf.sync()

        return max_task_number

    def edit_task(self, task_number, 
                  new_summary  =None, 
                  new_tasktype =None, 
                  new_milestone=None, 
                  new_priority =None):
        """method to edit a task created in local data store
        :param task_number  : integer
        :param new_summary  : None or string
        :param new_tasktype : None or string
        :param new_milestone: None or string
        :param new_priority : None or string
        """

        if self.has_task(task_number):
            if new_summary: 
                self.shelf[str(task_number)]["summary"] = new_summary
            if new_tasktype: 
                self.shelf[str(task_number)]["type"] = new_tasktype
            if new_milestone: 
                self.shelf[str(task_number)]["milestone"] = new_milestone
            if new_priority: 
                self.shelf[str(task_number)]["priority"] = new_priority

            # record EDIT operation in list 'CMDS_HISTORY' in local store
            if self.remote_mode and not \
               self._is_added_issue_updated(task_number, 
                                            new_summary, 
                                            new_tasktype, 
                                            new_milestone, 
                                            new_priority):
                cmd_history_data = { 'CMD'      : 'EDIT', 
                                     '#'        : task_number,
                                     'SUMMARY'  : new_summary,
                                     'TYPE'     : new_tasktype,
                                     'MILESTONE': new_milestone,
                                     'PRIORITY' : new_priority }
                self.shelf['CMDS_HISTORY'].append(cmd_history_data)
            self.shelf.sync()
        else:
            cry_msg(PROG_NAME, 
                    err_str='error: ', 
                    msg='no such task (#'+str(task_number)+') in the list')

    def read_tasks(self, task_type=None, milestone=None, priority=None):
        """method to output tasks in pretty format to STDOUT based on selected
           attributes of tasks.

        :param task_type: None or string
        :param milestone: None or string
        :param priority : None or string
        """

        print_header()
        for task_no in sorted_tasks(self.shelf):
            self._print_task(task_no, task_type, milestone, priority)
