from flask import Flask, jsonify, request
from config import Config
import psycopg2
from psycopg2 import pool
import logging
import atexit
from db_utils import *
from helper import *
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

logging.basicConfig(level=logging.INFO)
atexit.register(free_connection_pool)# register the free_connection_pool function to be called on app shutdown

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/register', methods=['POST'])
def register():
    """ register a new user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        print('Username and password are required.')
        return jsonify({'error': 'Username and password are required.'}), 400

    if register_user(username, password):
        print('User registered successfully.')
        return jsonify({'message': 'User registered successfully.'}), 201
    else:
        print('User registration failed.')
        return jsonify({'error': 'User registration failed.'}), 500

@app.route('/login', methods=['POST'])
def login():
    """ log in an existing user """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    uid = authenticate_user(username, password)
    if uid:
        return jsonify({'message': 'Login successful.', "uid": uid}), 200
    else:
        return jsonify({'error': 'Invalid username or password.'}), 401
    
@app.route('/fetch_all_trip', methods=['GET'])
def fetchAllTrips():
    uid = request.args.get('uid') 

    trips = fetch_all_trips(uid)
    print("trips are", trips)
    if trips != None:
        return jsonify({'message': 'Fetch successful.', "trips": trips}), 200
    else:
        return jsonify({'error': 'Fail to fetch all trips.'}), 401

@app.route('/addtrip', methods=['POST'])
def addTrip():
    data = request.json
    title = data.get('title')
    uid = data.get('uid')

    trip = add_trip_to_db(title, uid)
    if trip:
        return jsonify({"trip": trip}), 200
    return jsonify({'error': 'fail to add trip into database'}), 401

@app.route('/addstop', methods=['POST'])
def addStop():
    data = request.json

    trip_id = data.get('trip_id')
    title = data.get('title')
    type = data.get('type')
    startDate = data.get('startDate')
    startHour = data.get('startHour')
    startMinute = data.get('startMinute')
    endDate = data.get('endDate')
    endHour = data.get('endHour')
    endMinute = data.get('endMinute')
    location = data.get('location')
    link = data.get('link')
    description = data.get('description')

    startDateObj = datetime.strptime(startDate, "%Y-%m-%d")
    start_time = datetime(startDateObj.year, startDateObj.month, startDateObj.day, int(startHour), int(startMinute))
    endDateObj = datetime.strptime(endDate, "%Y-%m-%d")
    end_time = datetime(endDateObj.year, endDateObj.month, endDateObj.day, int(endHour), int(endMinute))

    event_id = add_stop_to_db(trip_id, title, type, start_time, end_time, location, description, link)
    if event_id:
        return jsonify({'message': 'Add Stop successful.', "event_id": event_id}), 200
    return jsonify({'message': 'Fail to stop successful.'}), 401

@app.route('/editstop', methods=['PATCH'])
def editStop():
    data = request.json

    event_id = data.get('event_id')
    title = data.get('title')
    type = data.get('type')
    startDate = data.get('startDate')
    startHour = data.get('startHour')
    startMinute = data.get('startMinute')
    endDate = data.get('endDate')
    endHour = data.get('endHour')
    endMinute = data.get('endMinute')
    location = data.get('location')
    link = data.get('link')
    description = data.get('description')
    
    startDateObj = datetime.strptime(startDate, "%Y-%m-%d")
    start_time = datetime(startDateObj.year, startDateObj.month, startDateObj.day, int(startHour), int(startMinute))
    endDateObj = datetime.strptime(endDate, "%Y-%m-%d")
    end_time = datetime(endDateObj.year, endDateObj.month, endDateObj.day, int(endHour), int(endMinute))

    event_id = edit_stop_to_db(event_id, title, type, start_time, end_time, location, description, link)
    if event_id:
        return jsonify({'message': 'Add Stop successful.', "trip": data}), 200
    return jsonify({'message': 'Fail to stop successful.'}), 401

@app.route('/fetchstops', methods=['GET'])
def fetchStops():
    trip_id = request.args.get('trip_id')

    print("trip_id is ", trip_id)
    stops = fetch_stops(trip_id)
    print("stops are", stops)
    if stops != None:
        return jsonify({'message': 'Fetch successful.', "stops": stops}), 200
    else:
        return jsonify({'error': 'Fail to fetch all stops.'}), 401

@app.route('/removetrip', methods=['DELETE'])
def removeTrip():
    data = request.json
    trip_id = data.get('trip_id')

    trip_id = remove_trip(trip_id)
    if trip_id:
        return jsonify({'message': 'Remove successful.', "trip_id": trip_id}), 200
    return jsonify({'error': 'Fail to remove trip.'}), 401
'''
@app.route('/add_bots', methods=['GET'])
def add_bot_trips():
    preferences = ['Sightseer', 'Adventurer', 'Historian', 'Artist', 'Foodie', 'Family', 'Solo', 'Nature', 'Luxury', 'Budget']
    ages = [18, 21, 30, 45]
    all_trips = []
    i = 0
    uid = 10000
    tid = 10000
    # uid = 17
    # tid = 30
    # for every pref
    for p in preferences:
        # each age
        for a in ages:
            if p in preferences[0:4]: filename = f"/home/ubuntu/trip_data/trip_{p}_{a}_size_200.csv"
            else: filename = f"/home/ubuntu/trip_data/trip_{p}_{a}_size_300.csv"
            curr_trips = csv_to_trips(filename)
            # now for the specific preference and age
            print(i)
            for t in curr_trips:
                i += 1
                # print(t['trip_name'])
                # create user
                if not register_user(f"{p}_{a}_{i}", "1234", uid + i, p, a):
                    print(f"failed to register user {uid + i}")
                    continue
                # create trip
                if not add_trip_to_db(t['trip_name'], uid + i, tid + i, t['start_date'], t['end_date']):
                    print(f"failed to add trip for user {uid + i} for trip {tid + i}")
                    continue
                # create events
                    # stops + commutes
                for ev in t['events']:
                    if ev['type'] == "stop":
                        add_stop_to_db(tid + i, ev['location'], ev['type'], ev['start_time'], ev['end_time'], ev['location'], "", "", weather=ev['preferred_weather'])
                    elif ev['type'] == "commute":
                        add_commute_to_db(tid + i, ev['mode'], ev['type'], ev['start_time'], ev['end_time'], ev['location_start'], ev['location_end'], ev['mode'])
                    else:
                        print(f"failed to add event for user {uid + i} for trip {tid + i}")
                        continue
        
    return curr_trips
                
    
    # data = request.get_json()
    # username = data.get('username')
    # password = data.get('password')

    # if not username or not password:
    #     print('Username and password are required.')
    #     return jsonify({'error': 'Username and password are required.'}), 400

    # if register_user(username, password):
    #     print('User registered successfully.')
    #     return jsonify({'message': 'User registered successfully.'}), 201
    # else:
    #     print('User registration failed.')
    #     return jsonify({'error': 'User registration failed.'}), 500
'''
@app.route('/db_version', methods=['GET'])
def version():
    """Get the PostgreSQL database version."""
    db_version = get_db_version()  # Call the function from db.py
    if db_version:
        return jsonify({'database_version': db_version}), 200
    else:
        return jsonify({'error': 'Could not fetch database version.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8081)
