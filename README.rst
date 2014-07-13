================================
Personal Desktop Assistant - pda
================================

.. image:: https://travis-ci.org/keenhenry/pda.svg?branch=master
   :target: https://travis-ci.org/keenhenry/pda

``pda`` is a command line todo list manager. Unlike other todo list tools, ``pda``
strives to find a balance between usability and functionality: a todo list manager 
should be easy to use and learn while offering enough features to accomplish what 
has to be done and to support more advance (however convenient and useful) usecases.

Features
--------

``pda`` is simple to use, yet more powerful than you think.

CREATE tasks
++++++++++++

Just like any other todo list tool, you can add a task in a list. Use command:

``pda -a [task summary text] -t [due time frame] -p [priority] [name of the list]``

Option ``-t`` specifies the due time frame for this task; only values among ``d`` (due today), 
``w`` (due this week), ``m`` (due this month), ``s`` (due this season) and ``y`` (due this year) 
are allowed.

Option ``-p`` specifies the priority for this task; only values among ``1`` (low), 
``2`` (medium), ``3`` (high), ``4`` (must do) and ``5`` (urgent and must do) are allowed.

Positional argument ``[name of the list]`` specifies the name of the list this task belongs 
to. The name can be any string you find appropriate, for example **todo**, **toread** or 
**tohack**; and it's perfectly okay to have different lists exist at the same time.

Option ``-t``, ``-p`` and positional argument ``[name of the list]`` are all *optional* 
attributes of a task, they will be ``None`` if not provided. Option ``-a``, however, is
compulsory to have a value.

.. code-block:: bash

    $ pda -a 'wash dishes' -t d -p 4 todo
    $ pda -a 'house cleaning' -t d -p 5 todo
    $ pda -a 'write a technical blog post' -tw -p2 towrite
    $ pda -a 'read Free Fall' -tm -p3 toread


LIST tasks
++++++++++

Tasks are **sorted** by *due time*, then by *priority*, then by alphabetical 
order of *list names* and last by *task number*, before listed on the command line.

To list **ALL** the tasks, do ``pda``:

.. code-block:: bash

    $ pda

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    2      house cleaning               todo       day       urgmust 
    1      wash dishes                  todo       day       must    
    3      write a technical blog post  towrite    week      medium  
    4      read Free Fall               toread     month     high    


To list only **toread** list's tasks, do ``pda toread``:

.. code-block:: bash

    $ pda toread

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    4      read Free Fall               toread     month     high    


To list the tasks due at the *end of this month*, use ``pda -tm``:

.. code-block:: bash

    $ pda -tm

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    4      read Free Fall               toread     month     high    


To list the tasks with priority *urgent and must do*, use ``pda -p5``:

.. code-block:: bash

    $ pda -p5

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    2      house cleaning               todo       day       urgmust 


To list the tasks due at the *end of today* and have priority **must** and 
belongs to **todo** list, use ``pda -td -p4 todo``:

.. code-block:: bash

    $ pda -td -p4 todo

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    1      wash dishes                  todo       day       must    


UPDATE tasks
++++++++++++

Often, you might want to change the due time, priority, task summary, or even list it belongs
to of a task. You may do so with the following syntax:

``pda -e [task number] -s [new task summary text] -t [new due time frame] -p [new priority] [new list name]``

Option ``-e`` specifies the **task number** (the task id) of the task to be updated.

Option ``-s`` specifies the new task summary of the task to be updated. It should be a **quoted
string** (either double or single quote).

Option ``-t``, Option ``-p`` and positional argument ``[new list name]`` are identical as 
those in the `CREATE tasks`_ part.

If an option or argument is not provided in the command, then the value associated with that
option or argument will stay unchanged for that task.

Let's postpone the **due time** to the end of this season for task number 4:

.. code-block:: bash

    $ pda -e4 -ts
    $ pda toread

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    4      read Free Fall               toread     season    high    


Now modify summary text of *task number 2*:

.. code-block:: bash

    $ pda -e2 -s 'clean study room'
    $ pda todo

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    2      clean study room             todo       day       urgmust 
    1      wash dishes                  todo       day       must    


Now modify several attributes of *task number 3*:

.. code-block:: bash

    $ pda -e3 -td -p3 todo
    $ pda

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    2      clean study room             todo       day       urgmust 
    1      wash dishes                  todo       day       must    
    3      write a technical blog post  todo       day       high    
    4      read Free Fall               toread     season    high    


FINISH tasks
++++++++++++

The best part of a todo list tool is you can remove a task after you finish it:

``pda -f [list of task numbers]`` 

Now, say I have already finished *wash dishes* and *clean study room* tasks 
therefore I would like to delete them from my **todo** list:

.. code-block:: bash

    $ pda -f 1 2
    $ pda

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========
    3      write a technical blog post  todo       day       high    
    4      read Free Fall               toread     season    high    


Sometimes, you might want to empty all your tasks and restart:

.. code-block:: bash

    $ pda --clear
    $ pda

    TASK#  SUMMARY                      LIST TYPE  DUE TIME  PRIORITY
    =====  ===========================  =========  ========  ========


Syncing Data With Github Issues
+++++++++++++++++++++++++++++++

It is also possible to make your todo list(s) *portable* through web interface!
``pda`` can sync your local list data to `Github Issue <http://bit.ly/18YAS2p>`_;
The choice of **Github Issues** is a nice one, since an issue tracker is also a todo
list manager! **Github Issues** actually provides decent visualization over some
statistics of tasks. But, of course, you need to have a Github account before using 
this feature.  In addition, ``pda`` needs to be configured to be in **remote mode** 
to communicate with **Github Issues**. For more detail, see `Configuration Setting`_ 
section.

Once ``pda`` is configured correctly, you can start using ``pda`` by downloading data 
from **Github Issues** to local data store: 

.. code-block:: bash

    $ pda --start

After finishing using ``pda`` in the current 'session' (all the updates in 
between ``--start`` and ``--stop`` commands) and want to upload the updates to 
**Github Issues**, do:

.. code-block:: bash

    $ pda --stop


Now you shall see the exact same copy of your local list data shown on **Github Issues**!


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


Install
-------

.. code-block:: bash

    $ sudo pip install pda

Or (but not recommended):

.. code-block:: bash

    $ sudo easy_install pda
