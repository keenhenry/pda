pda - Personal Desktop Assistant
================================

pda is a commandline tool used to manage several useful lists in your life - namely, TODO, TOLEARN, NOTE, QA and RESOLUTIONS.

Those lists are stored in a database, and are accessed through pda commandline interface, which is explained below:

## pda CLI (Command-line interfaces)

### CREATE lists 
```bash
# to create [todo|tolearn|note|qa|resolution] list(s) in the database
$ pda -c <list name(s)>

# to create all the lists in the database
$ pda -ca 
```

### READ lists

```bash
# to list [todo|tolearn|note|qa|resolution] list on commandline 
$ pda -l <list name>

# to list all the lists in X-window
$ pda -la 
```

### UPDATE lists

## License
