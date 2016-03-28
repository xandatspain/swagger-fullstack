#Rundeck-Helper

##What is installed?

- Python 3.5.1.

##Build instructions

```bash
[rundeck-helper] $ docker build -t rundeck-helper:<tag> .
```

##Instructions

This docker image is a helper for rundeck choices retrivied via API REST.

__Start__:

```
[rundeck-helper] $ docker run -d --name rundeck_helper -p 127.0.0.1:5000:5000 registry.geniac.com/rundeck-helper:1.0.0
```




