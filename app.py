"""
Description:
    Example flask test program to demonstrate connectivity to a postgresql database service.
"""
#
# The psycopg library is used for Postgresql access.
#
from flask import Flask
import logging
import os
import psycopg

#
# Setup basic logging.
#
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def hello() -> None:
    """
    Define a top-level route and a REST endpoint.
    Args: None
    Returns: The IP address of the Postgresql service.
    """
    
    logging.info("Calling the hello function.")
    #
    # Grab the environment variables needed for Postgresql authentication.
    #
    dbname = os.getenv('POSTGRESQL_DATABASE')
    user = os.getenv('POSTGRESQL_USER')
    password = os.getenv('POSTGRESQL_PASSWORD')
    host = os.getenv('POSTGRESQL_SERVICE_HOST')
    logging.info(f"POSTGRESQL_DATABASE = {dbname}")
    logging.info(f"POSTGRESQL_USER = {user}")
    logging.info(f"POSTGRESQL_PASSWORD = {password}")
    logging.info(f"POSTGRESQL_SERVICE_HOST = {host}")

    #
    # Create the Postgresql auth string.
    #
    params = {
    'dbname': dbname,
    'user': user,
    'password': password,
    'host': host,
    'port': 5432
    }

    #
    # Make the Postgresql database connection.
    #
    try:
        conn = psycopg.connect(**params)
    except psycopg.OperationalError:
        logging.info("DB Connection Failed!")
        logging.info("Exiting.")
        exit()

    logging.info(f"connection = {conn.info.hostaddr}")

    #
    # Return the IP address of the Postgresql service to the REST client.
    #
    return f"Connected to postgresql at {conn.info.hostaddr}"

#
# Run the webserver.
#
if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')

