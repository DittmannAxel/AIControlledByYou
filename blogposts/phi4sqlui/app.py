import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from llm_query import generate_sql_from_text
from db_schema import get_tables_and_columns
from datetime import datetime
import email.utils  # to parse RFC 2822 formatted timestamps like "Sat, 14 Dec 2024 13:33:44 GMT"

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

app = Flask(__name__)

LAST_GENERATED_SQL = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init_query', methods=['POST'])
def init_query():
    global LAST_GENERATED_SQL
    user_query = request.form.get('user_query', '')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Get the database schema info
    tables_info = get_tables_and_columns()

    # Construct a schema description message
    all_tables = ", ".join(tables_info.keys())
    schema_message = [f"The database has the following tables: {all_tables}."]
    for table, cols in tables_info.items():
        schema_message.append(f"The table '{table}' has columns: {', '.join(cols)}.")

    # Combine the user query with the schema info
    enriched_query = (
        f"User wants: {user_query}. "
        f"{' '.join(schema_message)} "
        "Please return a valid SQL query on the sensor_data table that matches the user request. "
        "Make sure to include the timestamp column in the results even if not asked explicitly. "
        "If the user says 'rpm', map it to 'motor_rpm'. Return only the SQL statement, no extra text."
    )

    sql = generate_sql_from_text(enriched_query)
    if not sql.strip():
        return jsonify({"error": "LLM returned empty SQL"}), 400

    LAST_GENERATED_SQL = sql
    return jsonify({"sql": sql})

@app.route('/run_query', methods=['POST'])
def run_query():
    global LAST_GENERATED_SQL
    # If no SQL available, return empty list
    if not LAST_GENERATED_SQL:
        return jsonify([]), 200

    data = execute_sql_and_return_json(LAST_GENERATED_SQL)
    return jsonify(data)

def execute_sql_and_return_json(sql):
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]

        data = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            if 'timestamp' in row_dict and isinstance(row_dict['timestamp'], str):
                # Attempt to parse the "Sat, 14 Dec 2024 13:33:44 GMT" format
                parsed_time = email.utils.parsedate_to_datetime(row_dict['timestamp'])
                if parsed_time:
                    # Convert to ISO8601 format with 'Z' to indicate UTC
                    row_dict['timestamp'] = parsed_time.isoformat() + 'Z'
            data.append(row_dict)

        cur.close()
        conn.close()
        return data
    except Exception as e:
        if conn:
            conn.close()
        print("[ERROR] SQL Error:", e)
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)