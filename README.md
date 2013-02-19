pda - Personal Desktop Assistant
================================

pda is a commandline tool used to manage several useful lists in your life - namely, TODO, TOLEARN, NOTE, QA and RESOLUTIONS. Lists are 
stored in a database, and are accessed through pda commandline interface, which is explained below:

## Synopsis

List names can be abbreviated as D, L, N, Q, R, respectively.

### CREATE lists 
```bash
# to create {todo|tolearn|note|qa|resolution} list(s) in the database
$ pda -c <list name(s)>

# to create all the lists in the database
$ pda -ca 

# import a file into a list, the type of file supported will need to be determined
# the syntax of the content of the file also needs to be determined
$ pda -ci <list name> <filepath>
```

### QUERY lists

```bash
# to list daily, weekly, weekendly, monthly, seasonly, yearly contents of 
# {todo|tolearn|note|qa|resolution} list on commandline
$ pda -l <list name> -[d|w|e|m|s|y]

# to list daily, weekly, weekendly, monthly, seasonly, yearly contents of 
# all the list{s} on commandline
$ pda -la -[d|w|e|m|s|y]
```

### UPDATE lists

```bash
# to add an item in {todo|tolearn|note|qa|resolution} list
# -d meaning daily plan, -w weekly, -e weekend, -m monthly, -s seasonly, -y yearly
# for list 'note' and 'qa', only daily is allowed and defaulted.
$ pda -a <list name> -[d|w|e|m|s|y] <a description of the thing you want to note down>

# to update an item in {todo|tolearn|note|qa|resolution} list
$ pda -u <list name> <item number> <item content in text>

# to update the priority of an item in {todo|tolearn|note|qa|resolution} list
$ pda -p <list name> <item number> <priority #>

# to delete items in {todo|tolearn|note|qa|resolution} list
$ pda -d <list name> <a list of item numbers>
```
