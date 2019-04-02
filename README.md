# DebtTracker

Tool to track my debt among my friends.

#### Dependency 
[Python3](https://www.python.org/downloads/)

### subcommands
- add
- show
- total

#### add
adds transaction to the record based on date
example:
```
$ tracker add -t '<- Ben 800 \\ for my new PC'
$ tracker add -t '-> Ben 100 \\ for his new router' -d '12-03-2019'
```

### show
displays the current record
```
$ tracker show
```

### total
adds the amounts from the transaction record based on either
- name
- date
- name and date
```
$ tracker total
$ tracker total -n Ben
$ tracker total -d '12-03-2001'
```
