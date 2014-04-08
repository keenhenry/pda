================================
Personal Desktop Assistant - pda
================================

``pda`` is a command line tool used to manage useful lists in your daily ife - such as TODO, 
TOLEARN and TOREAD lists, etc. You can use it to create as many lists as you want.

Install
-------

.. code-block:: bash

    $ sudo pip install pda

Or (but not recommended):

.. code-block:: bash

    $ sudo easy_install pda
    

Synopsis
--------

List names can be any string you want, personally I have **todo**, **tolearn** and **toread**
as available list names. List data is always stored locally. And, depends on the `Configuration 
Setting`_ in your configuration file (``~/.pdaconfig``), list data can also be synced to 
`Github Issue <http://bit.ly/18YAS2p>`_ and accessed through ``pda``; that is how you 
make your todo list(s) portable via web interface.

If no configuration file is provided, ``pda`` assumes it is to be used only locally; in other 
words, no data will be put on **Github Issues**.

For more detailed usage:

CREATE tasks
++++++++++++

To add (``-a`` option) a task in a list. If list with **listname** has not yet created, 
this command will automatically create such list in database. See example below:

.. code-block:: bash

    # Command format:
    #
    # $ pda -a <task summary text> <-t PERIOD> <-p PRIORITY> <listname>
    #
    # ===> add a task in a list named <listname>
    #
    # <-t> specifies the time frame this task is scheduled to
    #      allowed values are => d (day), w (week), m (month), s (season), y (year)
    # 
    # <-p> specifies the priority of this task
    #      allowed values are => 1 (low), 2 (medium), 3 (high), 4 (must), 5 (urgmust)
    #
    # For example: add a 'wash dishes' task with due time current 'day' and 
    #              priority 'must' in 'todo' list

    $ pda -a 'wash dishes' -t d -p 4 todo


UPDATE tasks
++++++++++++

All the attributes of a task can be changed to the specified values in the options. If
a value with an option is not specified in the command, then the corresponding attribute 
of that task will stay unchanged.

.. code-block:: bash

    # Command format:
    #
    # $ pda -r <N> 
    #
    # ===> delete a task numbered <N>
    #
    # For example: remove a task with task number 5 

    $ pda -r 5

    # Command format:
    #
    # $ pda -e <N> -s <task summary text> <-t PERIOD> <-p PRIORITY> <listname>
    #
    # ===> update a task numbered <N> in a list named <listname>
    #
    # <-s> specifies the NEW task summary
    #
    # <-t> specifies the NEW time frame this task is scheduled to
    #      allowed values are => d (day), w (week), m (month), s (season), y (year)
    #
    # <-p> specifies the NEW priority of this task
    #      allowed values are => 1 (low), 2 (medium), 3 (high), 4 (must), 5 (urgmust)
    #
    # <lisname> specifies the NEW list this task belongs to
    #
    # For example: edit/update a task number 3 with a new task summary 
    #              'vacuum floor this week' and its due time to current week

    $ pda -e 3 -s 'vacuum floor this week' -t w


QUERY lists
+++++++++++

To list ALL the tasks stored in the database:

.. code-block:: bash

    $ pda

To list ALL the tasks belongs to the list named **todo**:

.. code-block:: bash

    $ pda todo

To list ALL the tasks belongs to time frame **month**:

.. code-block:: bash

    $ pda -tm

To list ALL the tasks which have priority **urgmust** (urgent must):

.. code-block:: bash

    $ pda -p5

To list ALL the tasks which belongs to time frame **week** and 
have priority **high** and belongs to the list named **toread**:

.. code-block:: bash

    $ pda -tw -p3 toread


Syncing Data With Github Issues
+++++++++++++++++++++++++++++++

When ``pda`` is in **remote mode**, it can communicate with **Github Issues** to 
upload/download list data.

Once ``pda`` is in remote mode, you can only start using ``pda`` by downloading data 
from **Github Issues** to local data store first:

.. code-block:: bash

    $ pda --start

Once you have finished using ``pda`` and want to upload all the data created during 
current *section* (between ``--start`` and ``--stop``) to **Github Issues**, try:

.. code-block:: bash

    $ pda --stop


Configuration Setting
---------------------

``pda`` can be configured by a configuration file named ``.pdaconfig`` reside in your 
home directory. If no such file is present, then ``pda`` simply use some *default settings*
internally, and behave only in **local mode**; meaning data is only stored locally.

To make ``pda`` operate in **remote mode** (meaning the data is stored both locally and 
remotely on **Github Issues**), you need to set several parameters in the configuration file.

See an example configuration file below:

.. code-block:: cfg

    # a typical configuration file contains two sections: [pda] and [github]

    [pda]
    ; the local database where pda will store its data
    database-path = /tmp/.pdastore

    [github]
    ; username on github
    username   = your_github_username

    ; the name of the repository where you want to store your list data
    repo-name  = your_github_reponame

    ; authentication token for a Github application which pda will use
    ; to communitcate with Github Issues API, see link below:
    ; https://help.github.com/articles/creating-an-access-token-for-command-line-use
    auth-token = your_github_app_token
