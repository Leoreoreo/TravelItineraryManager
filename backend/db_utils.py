import psycopg2
from psycopg2 import pool
import os
import logging
from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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
        # valid
        if trips:  # Check the password
            logging.info(f"Fetch All trips")
            return trips

        # invalid
        logging.info(f"Fetch all trips failed")
        return None

    except Exception as e:
        logging.error(f"Error fetching trips: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

def add_trip_to_db(title, uid):
    """ add the trip to the database"""
    create_connection_pool()
    conn = None
    cursor = None
    logging.info(f'{title}, {uid}')

    try:
        conn = connection_pool.getconn()  # get a connection from the pool
        cursor = conn.cursor()

        # insert the user into the users table
        sql = "INSERT INTO trips (uid_fk, trip_name) VALUES (%s, %s) RETURNING trip_id, trip_name, start_date, end_date"
        val = (uid, title)
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
