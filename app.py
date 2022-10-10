from flask import Flask
import logging
import psycopg
import os


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def hello():
    logging.info("called hello endpoint")

    dbname = os.getenv('POSTGRESQL_DATABASE')
    user = os.getenv('POSTGRESQL_USER')
    password = os.getenv('POSTGRESQL_PASSWORD')
    host = os.getenv('POSTGRESQL_SERVICE_HOST')
    logging.info(f"POSTGRESQL_DATABASE = {dbname}")
    logging.info(f"POSTGRESQL_USER = {user}")
    logging.info(f"POSTGRESQL_PASSWORD = {password}")
    logging.info(f"POSTGRESQL_SERVICE_HOST = {host}")

    params = {
    'dbname': dbname,
    'user': user,
    'password': password,
    'host': host,
    'port': 5432
    }

    try:
        conn = psycopg.connect(**params)
    except psycopg.OperationalError:
        logging.info("DB Connection Failed!")
        logging.info("Exiting.")
        exit()

    logging.info(f"connection = {conn.info.hostaddr}")


    return f"Connected to postgresql at {conn.info.hostaddr}"

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')

