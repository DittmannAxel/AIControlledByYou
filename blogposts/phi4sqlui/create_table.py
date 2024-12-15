import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# SQL statement to create the table if it doesn't exist
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS sensor_data (
    timestamp    TIMESTAMP NOT NULL,
    motor_rpm    DOUBLE PRECISION,
    temperature  DOUBLE PRECISION,
    load         DOUBLE PRECISION,
    pressure     DOUBLE PRECISION,
    humidity     DOUBLE PRECISION
);
"""

def initialize_database():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST, 
        port=DB_PORT, 
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Execute the CREATE TABLE statement
    cur.execute(CREATE_TABLE_SQL)

    # Clean up
    cur.close()
    conn.close()
    print("Database initialized and table created if it did not exist.")

if __name__ == "__main__":
    initialize_database()
