from flask import Flask, jsonify, request
from config import Config
import psycopg2
from psycopg2 import pool
import logging
import atexit
from db_utils import *
from recommend import *
from chatbot import *
from helper import *
from logger_config import get_logger
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# logger.basicConfig(level=logger.INFO)
logger = get_logger(__name__)

atexit.register(free_connection_pool)# register the free_connection_pool function to be called on app shutdown

@app.route('/')
def hello():
	return 'Hello, World!'
'''
@app.route('/a')
def smth():
	init_models()
	return 'initialized models'
'''

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

    user_date = authenticate_user(username, password)
    if user_date:
        return jsonify({'message': 'Login successful.', "data": user_date}), 200
    else:
        return jsonify({'error': 'Invalid username or password.'}), 401
    

@app.route('/updatebod', methods=['PATCH'])
def updateBod():
    data = request.json

    uid = data.get('uid')
    newBod = data.get('newBod')

    result = update_bod_to_db(uid, newBod)
    if result:
        return jsonify({'message': 'Update BOD successful.', "result": result}), 200
    return jsonify({'message': 'Fail to update BOD.', "result": result}), 401

@app.route('/updatetrait', methods=['PATCH'])
def updateTrait():
    data = request.json

    uid = data.get('uid')
    newTrait = data.get('newTrait')

    result = update_trait_to_db(uid, newTrait)
    if result:
        return jsonify({'message': 'Update BOD successful.', "result": result}), 200
    return jsonify({'message': 'Fail to update BOD.', "result": result}), 401
    
@app.route('/fetch_all_trip', methods=['GET'])
def fetchAllTrips():
	uid = request.args.get('uid') 

	trips = fetch_all_trips(uid)
	# print("trips are", trips)
	if trips != None:
		return jsonify({'message': 'Fetch successful.', "trips": trips}), 200
	else:
		return jsonify({'error': 'Fail to fetch all trips.'}), 401

@app.route('/addtrip', methods=['POST'])
def addTrip():
	data = request.json
	title = data.get('title')
	startDate = data.get('startDate')
	endDate = data.get('endDate')
	uid = data.get('uid')
	
	trip = add_trip_to_db(title, uid, tid=None, start_date=startDate, end_date=endDate)
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

# @app.route('/fetchstops', methods=['GET'])
# def fetchStops():
# 	trip_id = request.args.get('trip_id')

# 	print("trip_id is ", trip_id)
# 	stops = fetch_stops(trip_id)
# 	print("stops are", stops)
# 	if stops != None:
# 		return jsonify({'message': 'Fetch successful.', "stops": stops}), 200
# 	else:
# 		return jsonify({'error': 'Fail to fetch all stops.'}), 401
  
@app.route('/deleteevent', methods=['DELETE'])
def deleteEvent():
    data = request.json

    event_id = data.get('event').get('event_id')

    result = delete_event_from_db(event_id)
    if result:
        return jsonify({'message': 'delete event.'}), 200
    else:
        return jsonify({'message': 'Fail to delete event.'}), 401

@app.route('/fetchevents', methods=['GET'])
def fetchEvents():
    trip_id = request.args.get('trip_id')

    print("trip_id is ", trip_id)
    events = fetch_events(trip_id)
    if events != None:
        return jsonify({'message': 'Fetch successful.', "events": events}), 200
    else:
        return jsonify({'error': 'Fail to fetch all events.'}), 401

@app.route('/addcommute', methods=['POST'])
def addCommute():
    data = request.json

    trip_id = data.get('trip_id')
    vehicle = data.get('vehicle')
    start_stop = data.get('start_stop')
    end_stop = data.get('end_stop')
    print(trip_id, vehicle, start_stop, end_stop)
    commute = add_commute_to_db(trip_id, vehicle, start_stop, end_stop)
    if commute:
        return jsonify({'message': 'Add Commute successful.', "commute": commute}), 200
    return jsonify({'message': 'Fail to add commute.'}), 401

  
@app.route('/removetrip', methods=['DELETE'])
def removeTrip():
	data = request.json
	trip_id = data.get('trip_id')

	trip_id = remove_trip(trip_id)
	if trip_id:
		return jsonify({'message': 'Remove successful.', "trip_id": trip_id}), 200
	return jsonify({'error': 'Fail to remove trip.'}), 401


@app.route('/all_users', methods=['GET'])
def all_users():
	users = return_users()

	if users != None:
		return jsonify({'message': 'Fetch successful.', "users": users}), 200
	else:
		return jsonify({'error': 'Fail to fetch all users.'}), 401

@app.route('/all_trips', methods=['GET'])
def all_trips():
	trips = return_trips()

	if trips != None:
		return jsonify({'message': 'Fetch successful.', "trips": trips}), 200
	else:
		return jsonify({'error': 'Fail to fetch all trips.'}), 401


@app.route('/insert_embedded_trip', methods=['POST'])
def insert_embedded_trip():
	""" insert embedded trip into db """
	data = request.get_json()
	uid, tid, pid, emb_trip = data.get('uid'), data.get('tid'), data.get('cid'), data.get('emb_trip')
	
	status = add_trip_embedding(uid, tid, pid, emb_trip)

	if status: return jsonify({'message': 'Embedded trip added successfully.'}), 201
	else: return jsonify({'message': 'Embedded trip failed to be added.'}), 500
	
@app.route('/recommend_trips', methods=['POST'])
def recommend_trips():
	data = request.get_json()
	uid = data.get('uid')
	tid = data.get('tid')

	# print(cid)
	# print(t_emb)

	trips = rec_recommend_trip(uid, tid)
	tid_recs = [t[0] for t in trips]

	if trips != None:
		return jsonify({'message': 'Recommend successful.', "tid_recs": tid_recs}), 200
	else:
		return jsonify({'error': 'Fail to recommend trips.'}), 401


@app.route('/generate_gpt_trip', methods=['POST'])
def gen_trip():
	data = request.get_json()
	uid = data.get('uid')
	user_input = data.get('user_input')

	tid = generate_trip(uid, user_input)

	if tid != None:
		return jsonify({'message': 'Trip generation successful.', "tid": tid}), 200
	else:
		return jsonify({'error': 'Fail to generate trip.'}), 401




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
	#	 print('Username and password are required.')
	#	 return jsonify({'error': 'Username and password are required.'}), 400

	# if register_user(username, password):
	#	 print('User registered successfully.')
	#	 return jsonify({'message': 'User registered successfully.'}), 201
	# else:
	#	 print('User registration failed.')
	#	 return jsonify({'error': 'User registration failed.'}), 500
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
