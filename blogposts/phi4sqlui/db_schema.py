import psycopg2
import os

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_tables_and_columns():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema='public';
    """)
    tables = [row[0] for row in cur.fetchall()]

    tables_info = {}
    for table in tables:
        cur.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table}'
            ORDER BY ordinal_position;
        """)
        columns = [row[0] for row in cur.fetchall()]
        tables_info[table] = columns

    cur.close()
    conn.close()
    return tables_info