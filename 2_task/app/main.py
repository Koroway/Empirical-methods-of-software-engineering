import time
import threading
import sqlite3
import random
import datetime
from flask import Flask, request, jsonify, Response
from prometheus_client import start_http_server, Counter, Gauge, generate_latest, Histogram
from pymongo import MongoClient

app = Flask(__name__)

TEMP_GAUGE = Gauge('iot_temperature_celsius', 'Current Temperature', ['room'])
HUMIDITY_GAUGE = Gauge('iot_humidity_percent', 'Current Humidity', ['room'])

DB_LATENCY = Histogram('mongodb_insert_latency_seconds', 'Time taken to insert data into MongoDB')
LOGIN_COUNTER = Counter('auth_login_total', 'Total login attempts', ['status'])


def get_mongo_db():
    client = MongoClient("mongodb://mongo:27017/")
    return client.iot_db


def init_sqlite():
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admins (login text, password text)''')
    c.execute("INSERT OR IGNORE INTO admins VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()


def sensor_simulation():
    rooms = ["Kitchen", "Bedroom", "ServerRoom"]
    db = get_mongo_db()
    collection = db.sensor_data

    while True:
        for room in rooms:
            temp = random.uniform(18.0, 30.0)
            hum = random.uniform(30.0, 60.0)

            TEMP_GAUGE.labels(room=room).set(temp)
            HUMIDITY_GAUGE.labels(room=room).set(hum)

            doc = {
                "room": room,
                "temperature": temp,
                "humidity": hum,
                "timestamp": datetime.datetime.utcnow()
            }

            with DB_LATENCY.time():
                collection.insert_one(doc)

            print(f"Recorded: {room} T:{temp:.1f} H:{hum:.1f}")

        time.sleep(5)


@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE login=? AND password=?", (login, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        LOGIN_COUNTER.labels(status='success').inc()
        return jsonify({"msg": "Welcome to Smart Home Panel"}), 200
    else:
        LOGIN_COUNTER.labels(status='fail').inc()
        return jsonify({"msg": "Access Denied"}), 403


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


if __name__ == '__main__':
    init_sqlite()
    t = threading.Thread(target=sensor_simulation)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', port=5000)