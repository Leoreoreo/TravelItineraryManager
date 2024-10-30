# TravelItineraryManager

[Figma](https://www.figma.com/design/9pcbmqmcjLAdZCZgRIo05Z/TIM-Design?node-id=0-1&node-type=canvas&t=WAw5u0Sfunfb5rfX-0)

### Usage (python environment)
0. try to use python 3.12.3 (if you are working on the aws server, should be default this)
1. $ python -m venv venv   <--  creates virtual environment
2. $ source venv/bin/activate  <--  activates venv
3. $ pip install -r requirements.txt <-- downloads all dependencies 
4. $ pip list  <--  just to check if everything is downloaded

* if python doesn't work, try python3
## FRONTEND
ReactJS

### Usage
Default: http://localhost:3000/
```
$ cd frontend
$ npm install
$ npm start
```

## BACKEND
Python (Flask)
Postgresql (should be always on since the server is on 24/7, so you can remote access)

### Usage (postgresql)
1. $ psql --host 18.222.124.5 --username db\_user1 --password --dbname tim\_db
2. will ask for pw so enter it
3. you can do any kind of sql stuff you want here (e.g. create, alter, insert, select)

### Usage (flask server)
1. you will not need to change the config file i believe as that is only for connecting to the db
2. $ flask run  <--  will run the server, should be on localhost

## Infrastructure
AWS (EC2)

### Production
1. Ports open specificaly 8080-8085
2. Host = ip address of it
