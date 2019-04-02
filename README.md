# DebtTracker

Tool to track my debt among my friends.

#### Dependency 
[Python3](https://www.python.org/downloads/)

### subcommand
- add
- show
- total

#### add
adds transaction to the record based on date
example:
```
$ tracker add -t '<- Ben 100'
$ tracker add -t '<- Ben 100' -d '23-05-2019'
```

### show
displays the current record
example:
```
$ tracker show
```

### total
adds the amounts from the transaction record based on either
- name
- date
- name and date
example:
```
$ tracker total
$ tracker total -n Ben
```
