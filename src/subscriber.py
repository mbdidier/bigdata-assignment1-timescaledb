import json
import time
import psycopg2
from psycopg2.extras import execute_batch
import paho.mqtt.client as mqtt
from utils import db_conninfo, MQTT_HOST, MQTT_PORT, MQTT_TOPIC_SUB

INSERT_SQL = """
INSERT INTO energy_readings (meter_id, timestamp, power, voltage, current, frequency, energy)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (meter_id, timestamp) DO NOTHING;
"""

BATCH_SIZE = 200
FLUSH_SECONDS = 2

buffer = []
last_flush = time.time()

def flush(cur, conn):
    global buffer, last_flush
    if not buffer:
        return
    execute_batch(cur, INSERT_SQL, buffer, page_size=200)
    conn.commit()
    buffer = []
    last_flush = time.time()

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT with result code:", rc)
    client.subscribe(MQTT_TOPIC_SUB)
    print("Subscribed to:", MQTT_TOPIC_SUB)

def on_message(client, userdata, msg):
    global buffer, last_flush
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        row = (
            int(data["meter_id"]),
            data["timestamp"],  # ISO string is OK for psycopg2
            float(data["power"]),
            float(data["voltage"]),
            float(data["current"]),
            float(data["frequency"]),
            float(data["energy"]),
        )
        buffer.append(row)

        # flush by size or time
        now = time.time()
        if len(buffer) >= BATCH_SIZE or (now - last_flush) >= FLUSH_SECONDS:
            cur, conn = userdata["cur"], userdata["conn"]
            flush(cur, conn)

    except Exception as e:
        print("Bad message:", e, "topic:", msg.topic)

def main():
    conn = psycopg2.connect(db_conninfo())
    conn.autocommit = False
    cur = conn.cursor()

    client = mqtt.Client()
    userdata = {"conn": conn, "cur": cur}
    client.user_data_set(userdata)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    print("Subscriber running... Ctrl+C to stop")
    try:
        client.loop_forever()
    finally:
        try:
            flush(cur, conn)
        except Exception:
            pass
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
