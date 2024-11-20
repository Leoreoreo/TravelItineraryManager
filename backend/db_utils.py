import psycopg2
from psycopg2 import pool
import os
import logging
from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

logging.basicConfig(level=logging.INFO)
connection_pool = None

def create_connection_pool():
    """ create a connection pool for the application (better scalability also cool ig) """
    global connection_pool
    if connection_pool is None:
        logging.info("Creating connection pool...")
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,  # minimum number of connections
            10,  # maximum number of connections
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            database=current_app.config['DB_NAME'],
            user=current_app.config['DB_USERNAME'],
            password=current_app.config['DB_PASSWORD']
        )

def free_connection_pool():
    """ free the connection pool and close all connections """
    global connection_pool
    if connection_pool:
        logging.info("Closing connection pool...")
        connection_pool.closeall()  # close all connections in the pool
        logging.info("Connection pool closed.")
        connection_pool = None  # remove the reference to the pool

def register_user(username, password):
    """ register a new user """
    create_connection_pool()
    conn = None
    cursor = None
    logging.info(f'{username}, {password}, {len(username)}, {len(password)}')

    try:
        conn = connection_pool.getconn()  # get a connection from the pool
        cursor = conn.cursor()

        # hash the password
        hashed_password = generate_password_hash(password)
        logging.info(f'{hashed_password}, {len(hashed_password)}')

        # insert the user into the users table
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, hashed_password)
        cursor.execute(sql, val)
        conn.commit()
        
        logging.info(f"User registered: {username}")
        return True
    except Exception as e:
        logging.error(f"Error registering user: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def authenticate_user(username, password):
    """ check if user + pw pair exists in db """
    create_connection_pool()
    conn = None
    cursor = None
    
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # fetch the user from the users table
        sql =  "SELECT user_id, password FROM users WHERE username = %s"
        val = (username,)
        cursor.execute(sql, val)
        user = cursor.fetchone()
        
        # valid
        if user and check_password_hash(user[1], password):  # Check the password
            logging.info(f"User validated: {username}")
            return user[0]

        # invalid
        logging.info(f"User validation failed: {username}")
        return None

    except Exception as e:
        logging.error(f"Error validating user: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def fetch_all_trips(uid):
    """ check all trips of a user from db """
    create_connection_pool()
    conn = None
    cursor = None
    
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # fetch the user from the users table
        sql =  "SELECT trip_id, trip_name, start_date, end_date FROM trips WHERE uid_fk = %s"
        val = (uid,)
        cursor.execute(sql, val)
        trips = cursor.fetchall()

        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert each to a dictionary
        trips = [dict(zip(columns, row)) for row in trips]
        logging.info(f"trips are {trips}")
        logging.info(f"Fetch All trips")
        return trips

    except Exception as e:
        logging.error(f"Error fetching trips: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def add_trip_to_db(title, uid, startDate, endDate):
    """ add the trip to the database"""
    create_connection_pool()
    conn = None
    cursor = None
    logging.info(f'{title}, {uid}')

    try:
        conn = connection_pool.getconn()  # get a connection from the pool
        cursor = conn.cursor()

        # insert the user into the users table
        sql = "INSERT INTO trips (uid_fk, trip_name, start_date, end_date) VALUES (%s, %s, %s, %s) RETURNING trip_id, trip_name, start_date, end_date"
        val = (uid, title, startDate, endDate)
        cursor.execute(sql, val)
        trip = cursor.fetchone()
        conn.commit()
  
        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert each to a dictionary
        trip = dict(zip(columns, trip))

        logging.info(f"User add trip, trip: {trip}")
        return trip
    except Exception as e:
        logging.error(f"Error adding trip: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def add_stop_to_db(trip_id, title, type, start_time, end_time, location, description, link):
    """ add thestop to the trip in the database"""
    create_connection_pool()
    conn = None
    cursor = None
    logging.info(f'{trip_id}, {title}, {location}, {description}, {start_time}, {end_time}')

    try:
        conn = connection_pool.getconn()  # get a connection from the pool
        cursor = conn.cursor()

        # Begin a transaction
        conn.autocommit = False  # Disable autocommit to manage transactions manually

        # insert the user into the events table
        sql = "INSERT INTO events (trip_id_fk, start_time, end_time, title, link) VALUES (%s, %s, %s, %s, %s) RETURNING event_id"
        val = (trip_id, start_time, end_time, title, link)
        cursor.execute(sql, val)
        event_id = cursor.fetchone()[0]

        # insert the user into the stops table
        sql = "INSERT INTO stops (event_id, location, description, type) VALUES (%s, %s, %s, %s)"
        val = (event_id, location, description, type)
        cursor.execute(sql, val)

        conn.commit()
        logging.info(f"User add stop successfully")
        return event_id
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error adding stop: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)    

def edit_stop_to_db(event_id, title, type, start_time, end_time, location, description, link):
    """ add thestop to the trip in the database"""
    create_connection_pool()
    conn = None
    cursor = None
    logging.info(f'{event_id}, {title}, {location}, {description}, {start_time}, {end_time}')

    try:
        conn = connection_pool.getconn()  # get a connection from the pool
        cursor = conn.cursor()

        # Begin a transaction
        conn.autocommit = False  # Disable autocommit to manage transactions manually

        # insert the user into the events table
        sql = "UPDATE events set start_time = %s, end_time = %s, title = %s, link = %s WHERE event_id = %s"
        val = (start_time, end_time, title, link, event_id)
        cursor.execute(sql, val)

        # insert the user into the stops table
        sql = "UPDATE stops set location = %s, description = %s, type = %s WHERE event_id = %s"
        val = (location, description, type, event_id)
        cursor.execute(sql, val)

        conn.commit()
        logging.info(f"User add stop successfully")
        return event_id
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error adding stop: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)  
    
def delete_event_from_db(event_id):
    create_connection_pool()
    conn = None
    cursor = None
    
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # fetch the user from the users table
        sql =  "DELETE FROM events WHERE event_id = %s"
        val = (event_id,)
        cursor.execute(sql, val)
        conn.commit()

        logging.info(f"Remove the event")
        return event_id

    except Exception as e:
        logging.error(f"Error remove trip: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def fetch_events(trip_id):
    """ check all trips of a user from db """
    create_connection_pool()
    conn = None
    cursor = None
    
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # fetch the stops from the stops table
        sql =  '''SELECT events.event_id, events.start_time, events.end_time, events.title, events.link, stops.location, stops.description, stops.type
        FROM events, stops
        WHERE events.trip_id_fk = %s AND events.event_id = stops.event_id
        '''
        val = (trip_id,)
        cursor.execute(sql, val)
        stops = cursor.fetchall()

        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert each to a dictionary
        stops = [dict(zip(columns, row)) for row in stops]

        # fetch the commutes from the commutes table
        sql =  '''SELECT events.event_id, events.start_time, events.end_time, commutes.location_start, commutes.location_end, commutes.vehicle
        FROM events, commutes
        WHERE events.trip_id_fk = %s AND events.event_id = commutes.event_id
        '''
        val = (trip_id,)
        cursor.execute(sql, val)
        commutes = cursor.fetchall()

        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert each to a dictionary
        commutes = [dict(zip(columns, row)) for row in commutes]

        events = []
        events.extend(stops)
        events.extend(commutes)

        for event in events:
            start_time = event['start_time']
            event['startDate'] = start_time.date().isoformat()
            event['startHour'] = int(start_time.hour)
            event['startMinute'] = int(start_time.minute)
            del event['start_time']

            end_time = event['end_time']
            event['endDate'] = end_time.date().isoformat()
            event['endHour'] = int(end_time.hour)
            event['endMinute'] = int(end_time.minute)
            del event['end_time']

        # sort the trips in order of start time
        events = sorted(events, key=lambda s: (s['startDate'], s['startHour'], s['startMinute'], s['endDate'], s['endHour'], s['endMinute']))

        logging.info(f"events are {events}")
        # valid
        logging.info(f"Fetch All stops")
        return events

    except Exception as e:
        logging.error(f"Error fetching stops: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def add_commute_to_db(trip_id, vehicle, start_stop, end_stop):
    """ add the commute to the trip in the database, return the commute object"""
    create_connection_pool()
    conn = None
    cursor = None
    logging.info(f'{trip_id}, {vehicle}, {start_stop}, {end_stop}')

    startDateObj = datetime.strptime(start_stop.get('endDate'), "%Y-%m-%d")
    start_time = datetime(startDateObj.year, startDateObj.month, startDateObj.day, int(start_stop.get('endHour')), int(start_stop.get('endMinute')))
    endDateObj = datetime.strptime(end_stop.get('startDate'), "%Y-%m-%d")
    end_time = datetime(endDateObj.year, endDateObj.month, endDateObj.day, int(end_stop.get('startHour')), int(end_stop.get('startMinute')))

    try:
        conn = connection_pool.getconn()  # get a connection from the pool
        cursor = conn.cursor()

        # Begin a transaction
        conn.autocommit = False  # Disable autocommit to manage transactions manually

        # insert the user into the events table
        sql = "INSERT INTO events (trip_id_fk, start_time, end_time) VALUES (%s, %s, %s) RETURNING event_id"
        val = (trip_id, start_time, end_time)
        cursor.execute(sql, val)
        event_id = cursor.fetchone()[0]

        # insert the user into the stops table
        sql = "INSERT INTO commutes (event_id, location_start, location_end, vehicle) VALUES (%s, %s, %s, %s)"
        val = (event_id, start_stop.get('location'), end_stop.get('location'), vehicle)
        cursor.execute(sql, val)

        conn.commit()

        commute = {
            "event_id": event_id,
            "startDate": start_stop.get('endDate'),
            "startHour": int(start_stop.get('endHour')),
            "startMinute": int(start_stop.get('endMinute')),
            "endDate": end_stop.get('startDate'),
            "endHour": int(end_stop.get('startHour')),
            "endMinute": int(end_stop.get('startMinute')),
            "location_start": start_stop.get('location'),
            "location_end": end_stop.get('location'),
            "vehicle": vehicle,
        }
        logging.info(f"User add stop successfully")
        return commute
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error adding stop: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)  

def remove_trip(trip_id):
    """ delete trip from db """
    create_connection_pool()
    conn = None
    cursor = None
    
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # fetch the user from the users table
        sql =  "DELETE FROM trips WHERE trip_id = %s"
        val = (trip_id,)
        cursor.execute(sql, val)
        conn.commit()

        logging.info(f"Remove the trip")
        return trip_id

    except Exception as e:
        logging.error(f"Error remove trip: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)
        

    
        

















def get_db_version():
    """Get the PostgreSQL database version."""
    create_connection_pool()  # make sure connection pool is created
    connection = None
    cursor = None
    try:
        connection = connection_pool.getconn()  # get a connection from the pool
        cursor = connection.cursor()

        # execute a sql query to fetch the database version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        return db_version[0] if db_version else "NONE"
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection_pool.putconn(connection)  # Return the connection to the pool
