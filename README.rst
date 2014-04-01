================================
Personal Desktop Assistant - pda
================================

``pda`` is a command line tool used to manage useful lists in your daily ife - such as TODO, 
TOLEARN and TOREAD lists, etc. You can use it to create as many lists as you want.

Install
-------
::

    $ sudo pip install pda


Synopsis
--------

List names can be any string you want, personally I have **todo**, **tolearn** and **toread**
as available list names. Lists data is stored on `Github Issue <http://bit.ly/18YAS2p>`_ and 
accessed through ``pda`` command line interface, which is explained below:


CREATE tasks
++++++++++++

::

    # add a task in a list named <listname>:
    #
    # <-t> specifies the time frame this task is scheduled to
    #      allowed values are => d (day), w (week), m (month), s (season), y (year)
    # <-p> specifies the priority of this task
    #      allowed values are => 1 (low), 2 (medium), 3 (high), 4 (must), 5 (urgent must)
    # 
    # if list <listname> has not yet created in database (Github Issue)
    # this command will automatically create such list in the database
    $ pda -a <task summary text> <-t PERIOD> <-p PRIORITY> <listname>


UPDATE tasks
++++++++++++

::

    # delete a task numbered <N>
    $ pda -r <N>

    # update a task numbered <N> in a list named <listname>
    #
    # all the attributes of a task can be changed to the specified values:
    #
    # <-s> specifies the NEW task summary
    # <-t> specifies the NEW time frame this task is scheduled to
    #      allowed values are => d (day), w (week), m (month), s (season), y (year)
    # <-p> specifies the NEW priority of this task
    #      allowed values are => 1 (low), 2 (medium), 3 (high), 4 (must), 5 (urgent must)
    # <lisname> specifies the NEW list this task belongs to
    $ pda -e <N> -s <task summary text> <-t PERIOD> <-p PRIORITY> <listname>


QUERY lists
+++++++++++

::

    # list ALL the tasks stored in the database (Github Issue)
    $ pda

    # list ALL the tasks belongs to the list named <listname>
    $ pda <listname>

    # list ALL the tasks belongs to time frame PERIOD
    $ pda <-t PERIOD>

    # list ALL the tasks which have priority PRIORITY
    $ pda <-p PRIORITY>

    # list ALL the tasks which belongs to time frame PERIOD
    #                      and have priority PRIORITY
    #                      and belongs to the list named <listname>
    $ pda <-t PERIOD> <-p PRIORITY> <listname>
