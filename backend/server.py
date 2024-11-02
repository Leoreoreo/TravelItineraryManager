from flask import Flask, jsonify, request
from config import Config
import psycopg2
from psycopg2 import pool
import logging
import atexit
from db_utils import *
from flask_cors import CORS

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
    if trips:
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
