import time
import random
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
# Connection settings
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Example ranges for the data:
# motor_rpm: 1000-2000
# temperature: 20-80 degrees Celsius
# load: 0-100 %
# pressure: 1-10 bar
# humidity: 30-70 %
conn = psycopg2.connect(
    host=DB_HOST, 
    port=DB_PORT, 
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASSWORD
)
conn.autocommit = True
cur = conn.cursor()

while True:
    motor_rpm = random.uniform(1000, 2000)
    temperature = random.uniform(20, 80)
    load = random.uniform(0, 100)
    pressure = random.uniform(1, 10)
    humidity = random.uniform(30, 70)
    ts = datetime.now()

    cur.execute(
        "INSERT INTO sensor_data (timestamp, motor_rpm, temperature, load, pressure, humidity) VALUES (%s, %s, %s, %s, %s, %s)",
        (ts, motor_rpm, temperature, load, pressure, humidity)
    )
    print(f"Inserted: timestamp={ts}, motor_rpm={motor_rpm:.2f}, temperature={temperature:.2f}, load={load:.2f}, pressure={pressure:.2f}, humidity={humidity:.2f}")
    
    time.sleep(1)  # Insert one row per second
