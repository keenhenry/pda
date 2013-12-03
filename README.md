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
# add a task in a list
$ pda -a <task summary text> [-t PERIOD] [-p PRIORITY] <listname>
```

### UPDATE lists

```bash
# delete a task numbered N
$ pda -r N

# to update an item in list
$ pda -e <list name> <item number> <item content in text>
```

### QUERY list contents

```bash
# 
$ pda <listname>
```
