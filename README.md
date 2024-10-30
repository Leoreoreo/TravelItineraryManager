# TravelItineraryManager

[Figma](https://www.figma.com/design/9pcbmqmcjLAdZCZgRIo05Z/TIM-Design?node-id=0-1&node-type=canvas&t=WAw5u0Sfunfb5rfX-0)

## FRONTEND
- ReactJS

### Usage
#### Install Dependencies
```
$ cd frontend
$ npm install
```
#### Run 
```
$ npm start
```
Default: http://localhost:3000/

## BACKEND
- Python (Flask)

### Usage
#### Install Dependencies
* if `python` doesn't work, try `python3`
0. try to use python 3.12.3 (if you are working on the aws server, should be default this)
```
$ python -m venv venv               // create virtual environment
$ source venv/bin/activate          // activate venv
$ pip install -r requirements.txt   // downloads dependencies
$ pip list                          // check if everything is downloaded
```

#### Run
* you will not need to change the config file i believe as that is only for connecting to the db
```
$ source venv/bin/activate  // activate venv
$ flask run                 // run the server, should be on localhost
```
Default: http://127.0.0.1:8081

## Database 
- Postgresql (should be always on since the server is on 24/7, so you can remote access)
- Infrastructure: AWS (EC2)

### Usage 
1. `$ psql --host 18.222.124.5 --username db\_user1 --password --dbname tim\_db`
2. will ask for pw so enter it
3. you can do any kind of sql stuff you want here (e.g. create, alter, insert, select)
### Production
1. Ports open specificaly 8080-8085
2. Host = ip address of it
