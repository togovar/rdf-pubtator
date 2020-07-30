# rdf-pubtator

## Installation 

```bash
$ docker build --tag rdf-pubtator .
```

## Run

```bash
$ docker run --rm -v [WORK]:/work -v [DATA]:/data rdf-pubtator [OPTION]
```
[WORK]: Download file location

[DATA]: Converted file location

[OPTION]: 
-f Convert local files when no new remote files are available .  
-P Specifires the maximum number of processes that can be executed simulataneously .

