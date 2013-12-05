Personal Desktop Assistant - pda
================================

pda is a command line tool used to manage useful lists in your daily ife - such as TODO, 
TOLEARN and TOREAD lists, etc. You can use it to create as many lists as you want.

Lists data are stored on [Github Issue](bit.ly/18YAS2p) and accessed through pda command 
line interface, which is explained below:

## Synopsis

List names can be any string you want, I currently have __todo__, __tolearn__ and __toread__ 
as available list names stored on _Github Issue_ database.

### CREATE tasks in a list

```bash
# add a task in a list named <listname>:
#
# <-t> specifies the time frame this task is scheduled to
#      allowed values are => d (day), w (week), m (month), s (season), y (year)
# <-p> specifies the priority of this task
#      allowed values are => 1 (low), 2 (medium), 3 (high), 4 (must), 5 (urgent and must)
# 
# if list <listname> has not yet created in database (_Github Issue_)
# this command will automatically create such list in the database
$ pda -a <task summary text> <-t PERIOD> <-p PRIORITY> <listname>
```

### UPDATE lists

```bash
# delete a task numbered <N>
$ pda -r <N>

# update a task numbered <N> in a list named <listname>
#
# all the attributes of a task can be changed to specified values:
#
# <-s> specifies the new task summary
# <-t> specifies the new time frame this task is scheduled to
#      allowed values are => d (day), w (week), m (month), s (season), y (year)
# <-p> specifies the new priority of this task
#      allowed values are => 1 (low), 2 (medium), 3 (high), 4 (must), 5 (urgent and must)
# <lisname> specifies the new list this task belongs to
$ pda -e <N> -s <task summary text> <-t PERIOD> <-p PRIORITY> <listname>
```

### QUERY lists

```bash
# list ALL the tasks _stored in the database_ (_Github Issue_)
$ pda

# list ALL the tasks _belongs to the list named <listname>_
$ pda <listname>

# list ALL the tasks _belongs to time frame PERIOD_
$ pda <-t PERIOD>

# list ALL the tasks _which have priority PRIORITY_
$ pda <-p PRIORITY>
```
