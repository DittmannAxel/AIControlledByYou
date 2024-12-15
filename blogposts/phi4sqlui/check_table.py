import psycopg2

# For reference, here is the CREATE TABLE statement:
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

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'factory_data'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'

def check_table_and_print_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, 
            port=DB_PORT, 
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if table exists using the information_schema
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'sensor_data'
            );
        """)
        exists = cur.fetchone()[0]

        if not exists:
            print("Table 'sensor_data' does not exist.")
        else:
            # Get total number of rows
            cur.execute("SELECT COUNT(*) FROM sensor_data;")
            total_rows = cur.fetchone()[0]

            # Get column names
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'sensor_data' ORDER BY ordinal_position;")
            columns = [row[0] for row in cur.fetchall()]

            # Print total rows
            print("Total rows in sensor_data:", total_rows)
            
            # Fetch last 10 rows
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10;")
            rows = cur.fetchall()

            # Print table name
            print("Table: sensor_data")

            # Print headers
            print("\t".join(columns))

            # Print rows or <empty> if none
            if len(rows) == 0:
                print("<empty>")
            else:
                for r in rows:
                    # Convert all row values to string for printing
                    print("\t".join([str(x) for x in r]))

        cur.close()
        conn.close()

    except Exception as e:
        # In case of any database connection error or query error
        print("An error occurred:", e)

if __name__ == "__main__":
    check_table_and_print_data()
