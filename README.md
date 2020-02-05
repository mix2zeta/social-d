# social-d

Social processing, Require `docker` , `docker-compose v3`, `Makefile` to run if you don't have Makefile you can copy directly from Makefie

Accept csv format with column
```
id,type,message,time,engagement,channel,owner id,owner name
```

## Table of content

- [Setup & How to use](##Setup)
- [Running test](##test)

## Setup

- Clone this repo
- Place you csv at [src/raw_data](src/raw_data)
- This command will format project and start from fresh again
```
make format
```
- if you can't pull docker image build it with cmd: `docker-compose build`
- PS. I mount database volume to previous directory, if you do this at home it can have permission problem (and please delete volume yourself)

- To start service again
```
make start
```

- To stop
```
make stop
```

## Test
```
make tests
```

## API and Dashboard
[Example Dashboard](jupyter/dashboard.ipynb)

## System design and Explain

This project have 5 container following this list

### social-d-db
Postgres DB for record processed data

### social-d-redis
Redis for

### social-d-scheduler 
### social-d-service
### social-d-worker  
### social-d-jupyter 

## Improvement

