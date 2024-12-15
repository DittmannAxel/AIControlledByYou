import psycopg2

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'factory_data'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'

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
