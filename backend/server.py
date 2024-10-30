from flask import Flask, jsonify, g
from config import Config
import psycopg2
from psycopg2 import pool
import logging
import atexit


app = Flask(__name__)
app.config.from_object(Config)

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
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USERNAME'],
            password=app.config['DB_PASSWORD']
        )

def free_connection_pool():
    """ free the connection pool and close all connections """
    global connection_pool
    if connection_pool:
        logging.info("Closing connection pool...")
        connection_pool.closeall()  # close all connections in the pool
        logging.info("Connection pool closed.")
        connection_pool = None  # remove the reference to the pool



@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/db_version', methods=['GET'])
def get_db_version():
    """Get the PostgreSQL database version."""
    connection = None
    cursor = None
    try:
        create_connection_pool()  # Ensure the connection pool is created
        connection = connection_pool.getconn()  # Get a connection from the pool
        cursor = connection.cursor()

        # Execute a query to fetch the database version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        return jsonify({'database_version': db_version[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection_pool.putconn(connection)  # Return the connection to the pool

# Register the free_connection_pool function to be called on app shutdown
atexit.register(free_connection_pool)
'''
@app.teardown_appcontext
def close_db_connection(exception):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
'''
# if __name__ == '__main__':
#     app.run(debug=True)
