import psycopg2
from psycopg2 import pool
import os
import logging
from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from logger_config import get_logger

logger = get_logger(__name__)
connection_pool = None

def create_connection_pool():
	""" create a connection pool for the application (better scalability also cool ig) """
	global connection_pool
	if connection_pool is None:
		logger.info("Creating connection pool...")
		connection_pool = psycopg2.pool.SimpleConnectionPool(
			1,  # minimum number of connections
		   	4,  # maximum number of connections
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
		logger.info("Closing connection pool...")
		connection_pool.closeall()  # close all connections in the pool
		logger.info("Connection pool closed.")
		connection_pool = None  # remove the reference to the pool

def register_user(username, password, user_id=None, trait=None, age=None):
	""" register a new user """
	create_connection_pool()
	conn = None
	cursor = None
	# logger.info(f'{username}, {password}, {len(username)}, {len(password)}')

	try:
		conn = connection_pool.getconn()  # get a connection from the pool
		cursor = conn.cursor()

		# hash the password
		hashed_password = generate_password_hash(password)
		# logger.info(f'{hashed_password}, {len(hashed_password)}')
		
		# insert the user into the users table
		if not trait:
			sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
			val = (username, hashed_password)
		elif user_id:
			sql = "INSERT INTO users (user_id, username, password, trait, age) VALUES (%s, %s, %s, %s, %s)"
			val = (user_id, username, hashed_password, trait, age)
		else:
			sql = "INSERT INTO users (username, password, trait) VALUES (%s, %s, %s)"
			val = (username, hashed_password, trait)
		cursor.execute(sql, val)
		conn.commit()
		
		logger.info(f"User registered: {username}")
		return True
	except Exception as e:
		logger.error(f"Error registering user: {str(e)}")
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
			logger.info(f"User validated: {username}")
			return user[0]

		# invalid
		logger.info(f"User validation failed: {username}")
		return None

	except Exception as e:
		logger.error(f"Error validating user: {str(e)}")
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
		# logger.debug(f"trips are {trips}")
		# logger.debug(f"Fetch All trips")
		return trips

	except Exception as e:
		logger.error(f"Error fetching trips: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)

def add_trip_embedding(uid, tid, cid, t_emb):
	""" add the trip embedding to the database """
	create_connection_pool()
	conn = None
	cursor = None
	logger.info(f'TRYING TO ADD TRIP EMBEDDING: {uid} {tid} {cid}')
	
	try:
		conn = connection_pool.getconn()  # get a connection from the pool
		cursor = conn.cursor()

		sql = "INSERT INTO trip_embeddings (user_id, trip_id, cluster_id, vector) VALUES (%s, %s, %s, %s)"
		val = (uid, tid, cid, t_emb)

		cursor.execute(sql, val)
		conn.commit()
  
		return True
	except Exception as e:
		logger.error(f"Error adding embedded trip: {str(e)}")
		return False
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)

def recommend_trip(cid, t_emb):
	""" recommends trip based on similarity search on their embedding """
	create_connection_pool()
	conn = None
	cursor = None
	logger.info(f'getting similar trips in cluster: {cid}')
	
	try:
		conn = connection_pool.getconn()  # get a connection from the pool
		cursor = conn.cursor()

		sql = 	"""
				SELECT trip_id, (vector <=> %s::vector) AS similarity_score
				 FROM trip_embeddings WHERE cluster_id = %s
				ORDER BY vector <=> %s::vector
				LIMIT 3
				"""

		val = (t_emb, cid, t_emb)

		cursor.execute(sql, val)
		conn.commit()

		trips = cursor.fetchall()
		return trips
	except Exception as e:
		logger.error(f"Error recommending trips: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)


def add_trip_to_db(title, uid, tid=None, start_date=None, end_date=None):

	""" add the trip to the database"""
	create_connection_pool()
	conn = None
	cursor = None
	logger.info(f'{title}, {uid}')

	try:
		conn = connection_pool.getconn()  # get a connection from the pool
		cursor = conn.cursor()

		# insert the user into the users table
		if not start_date or not end_date:
			sql = "INSERT INTO trips (uid_fk, trip_name) VALUES (%s, %s) RETURNING trip_id, trip_name, start_date, end_date"
			val = (uid, title)
		elif tid:
			sql = "INSERT INTO trips (trip_id, uid_fk, trip_name, start_date, end_date) VALUES (%s, %s, %s, %s, %s) RETURNING trip_id, trip_name, start_date, end_date"
			val = (tid, uid, title, start_date, end_date)
		else:
			sql = "INSERT INTO trips (uid_fk, trip_name, start_date, end_date) VALUES (%s, %s, %s, %s) RETURNING trip_id, trip_name, start_date, end_date"
			val = (uid, title, start_date, end_date)
		cursor.execute(sql, val)
		trip = cursor.fetchone()
		conn.commit()
  
		# Get column names from cursor description
		columns = [desc[0] for desc in cursor.description]

		# Fetch all rows and convert each to a dictionary
		trip = dict(zip(columns, trip))

		logger.info(f"User add trip, trip: {trip}")
		return trip
	except Exception as e:
		logger.error(f"Error adding trip: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)
		  
def return_user_info(uid):
	""" get user info of one user """
	create_connection_pool()
	conn = None
	cursor = None
	
	try:
		conn = connection_pool.getconn()
		cursor = conn.cursor()
		print(f"trying to fetch {uid} info")	
		# fetch the user from the users table
		sql =  "SELECT user_id, username, trait, age FROM users WHERE user_id = %s"
		val = (uid,)
		cursor.execute(sql, val)
		user = cursor.fetchone()
		
	   
		return user # [uid, username, trait, age]

	except Exception as e:
		logger.error(f"Error fetching user: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)

 
def return_users():
	""" get all users of db """
	create_connection_pool()
	conn = None
	cursor = None
	
	try:
		conn = connection_pool.getconn()
		cursor = conn.cursor()
		
		# fetch the user from the users table
		sql =  "SELECT user_id, username, trait, age FROM users"
		val = ()
		cursor.execute(sql, val)
		users = cursor.fetchall()
	   
		return users

	except Exception as e:
		logger.error(f"Error fetching all users: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)

def return_trips():
	""" get all trips of db """
	create_connection_pool()
	conn = None
	cursor = None
	
	try:
		conn = connection_pool.getconn()
		cursor = conn.cursor()
		
		# fetch the trip from the trips table
		sql =  "SELECT trip_id, trip_name, start_date, end_date FROM trips"
		val = ()
		cursor.execute(sql, val)
		trips = cursor.fetchall()
	   
		return trips

	except Exception as e:
		logger.error(f"Error fetching all trips: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)

def create_event(trip_id, start_time, end_time, title, link):
	""" create an event in the database and return its id """
	create_connection_pool()
	conn = None
	cursor = None

	try:
		conn = connection_pool.getconn()
		cursor = conn.cursor()

		sql = """
		INSERT INTO events (trip_id_fk, start_time, end_time, title, link) 
		VALUES (%s, %s, %s, %s, %s) 
		RETURNING event_id
		"""
		
		val = (trip_id, start_time, end_time, title, link)
		cursor.execute(sql, val)
		event_id = cursor.fetchone()[0]
		conn.commit()
		
		return event_id
	except Exception as e:
		if conn:
			conn.rollback()
		logger.error(f"Error creating event: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)
			
def add_stop_to_db(trip_id, title, event_type, start_time, end_time, location, description, link, weather=None):
	"""Add a stop to the trip in the database."""
	create_connection_pool()
	conn = None
	cursor = None
	logger.info(f'{trip_id}, {title}, {location}, {event_type}, {description}, {start_time}, {end_time}')

	try:
		# Use the `create_event` function to handle event creation
		event_id = create_event(trip_id, start_time, end_time, title, "")
		if event_id is None: raise Exception("Failed to create event")

		conn = connection_pool.getconn()
		cursor = conn.cursor()

		# Begin a transaction for the stop insertion
		conn.autocommit = False

		if event_id and location and description and event_type and weather:
			sql = """
			INSERT INTO stops (event_id, location, description, type, preferred_weather) 
			VALUES (%s, %s, %s, %s, %s)
			"""
			val = (event_id, location, description, event_type, weather)
		else: 
			# Insert into the stops table
			sql = """
			INSERT INTO stops (event_id, location, description, type) 
			VALUES (%s, %s, %s, %s)
			"""
			val = (event_id, location, description, event_type)
		cursor.execute(sql, val)
		conn.commit()
		
		logger.info(f"Stop added successfully")
		return event_id
	except Exception as e:
		if conn:
			conn.rollback()
		logger.error(f"Error adding stop: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)
			
def add_commute_to_db(trip_id, title, event_type, start_time, end_time, location_start, location_end=None, vehicle=None):
	"""Add a stop to the trip in the database."""
	create_connection_pool()
	conn = None
	cursor = None
	logger.info(f'{trip_id}, {title}, {event_type}, {start_time}, {end_time}, {location_start}, {location_end} , {vehicle}')

	try:
		# Use the `create_event` function to handle event creation
		event_id = create_event(trip_id, start_time, end_time, title, "")
		if event_id is None: raise Exception("Failed to create event")

		conn = connection_pool.getconn()
		cursor = conn.cursor()

		# Begin a transaction for the stop insertion
		conn.autocommit = False

		if event_id and location_start and location_end and vehicle:
			sql = """
			INSERT INTO commutes (event_id, location_start, location_end, vehicle) 
			VALUES (%s, %s, %s, %s)
			"""
			val = (event_id, location_start, location_end, vehicle)
		else: 
			# Insert into the stops table
			sql = """
			INSERT INTO commutes (event_id, location_start) 
			VALUES (%s, %s)
			"""
			val = (event_id, location_start)
		cursor.execute(sql, val)
		conn.commit()
		
		logger.info(f"Commute added successfully")
		return event_id
	except Exception as e:
		if conn:
			conn.rollback()
		logger.error(f"Error adding commute: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)

# def add_stop_to_db(trip_id, title, type, start_time, end_time, location, description, link):
#	 """ add thestop to the trip in the database"""
#	 create_connection_pool()
#	 conn = None
#	 cursor = None
#	 logger.info(f'{trip_id}, {title}, {location}, {description}, {start_time}, {end_time}')

#	 try:
#		 conn = connection_pool.getconn()  # get a connection from the pool
#		 cursor = conn.cursor()

#		 # Begin a transaction
#		 conn.autocommit = False  # Disable autocommit to manage transactions manually

#		 # insert the user into the events table
#		 sql = "INSERT INTO events (trip_id_fk, start_time, end_time, title, link) VALUES (%s, %s, %s, %s, %s) RETURNING event_id"
#		 val = (trip_id, start_time, end_time, title, link)
#		 cursor.execute(sql, val)
#		 event_id = cursor.fetchone()[0]

#		 # insert the user into the stops table
#		 sql = "INSERT INTO stops (event_id, location, description, type) VALUES (%s, %s, %s, %s)"
#		 val = (event_id, location, description, type)
#		 cursor.execute(sql, val)

#		 conn.commit()
#		 logger.info(f"User add stop successfully")
#		 return event_id
#	 except Exception as e:
#		 if conn:
#			 conn.rollback()
#		 logger.error(f"Error adding stop: {str(e)}")
#		 return None
#	 finally:
#		 if cursor:
#			 cursor.close()
#		 if conn:
#			 connection_pool.putconn(conn)	

def edit_stop_to_db(event_id, title, type, start_time, end_time, location, description, link):
	""" add thestop to the trip in the database"""
	create_connection_pool()
	conn = None
	cursor = None
	logger.info(f'{event_id}, {title}, {location}, {description}, {start_time}, {end_time}')

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
		logger.info(f"User add stop successfully")
		return event_id
	except Exception as e:
		if conn:
			conn.rollback()
		logger.error(f"Error adding stop: {str(e)}")
		return None
	finally:
		if cursor:
			cursor.close()
		if conn:
			connection_pool.putconn(conn)  

def fetch_stops(trip_id):
	""" check all trips of a user from db """
	create_connection_pool()
	conn = None
	cursor = None
	
	try:
		conn = connection_pool.getconn()
		cursor = conn.cursor()
		
		# fetch the user from the users table
		sql =  '''SELECT events.event_id, events.start_time, events.end_time, events.title, events.link, stops.location, stops.description, stops.type
		FROM events, stops
		WHERE events.trip_id_fk = %s AND events.event_id = stops.event_id
		ORDER BY events.start_time, events.end_time
		'''
		val = (trip_id,)
		cursor.execute(sql, val)
		stops = cursor.fetchall()

		# Get column names from cursor description
		columns = [desc[0] for desc in cursor.description]

		# Fetch all rows and convert each to a dictionary
		stops = [dict(zip(columns, row)) for row in stops]
		for stop in stops:
			start_time = stop['start_time']
			stop['startDate'] = start_time.date().isoformat()
			stop['startHour'] = start_time.hour
			stop['startMinute'] = start_time.minute
			del stop['start_time']

			end_time = stop['end_time']
			stop['endDate'] = end_time.date().isoformat()
			stop['endHour'] = end_time.hour
			stop['endMinute'] = end_time.minute
			del stop['end_time']

		logger.info(f"stops are {stops}")
		# valid
		logger.info(f"Fetch All stops")
		return stops

	except Exception as e:
		logger.error(f"Error fetching stops: {str(e)}")
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

		logger.info(f"Remove the trip")
		return trip_id

	except Exception as e:
		logger.error(f"Error remove trip: {str(e)}")
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
