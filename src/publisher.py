import json
import math
import random
import time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from utils import MQTT_HOST, MQTT_PORT, MQTT_TOPIC_PUB_PREFIX

def meter_ids(n: int, start: int = 1000000000):
    # 10-digit IDs (1,000,000,000 is 10 digits)
    return [start + i for i in range(n)]

def daily_multiplier(hour: int) -> float:
    # low at night, peaks morning and evening
    if 0 <= hour <= 5:
        return 0.55
    if 6 <= hour <= 9:
        return 0.85
    if 10 <= hour <= 16:
        return 0.75
    if 17 <= hour <= 21:
        return 1.00
    return 0.70

def generate_reading(meter_id: int, ts: datetime) -> dict:
    hour = ts.hour
    mult = daily_multiplier(hour)

    # realistic-ish ranges
    voltage = random.gauss(230, 5)          # around 230V
    frequency = random.gauss(50, 0.05)      # around 50Hz (adjust if you want 60)
    base_power = random.uniform(0.2, 2.5)   # kW-ish
    power = max(0.05, base_power * mult + random.uniform(-0.05, 0.05))

    # I = P / V (approx), keep it plausible
    current = max(0.05, (power * 1000) / max(100, voltage))  # watts/volts

    # energy here is incremental (kWh for 5 minutes)
    energy = power * (5.0 / 60.0)

    return {
        "meter_id": meter_id,
        "timestamp": ts.isoformat(),
        "power": round(power, 4),
        "voltage": round(voltage, 3),
        "current": round(current, 3),
        "frequency": round(frequency, 4),
        "energy": round(energy, 6),
    }

def main():
    N_METERS = 500  # change to 1000+ later for bigger dataset
    INTERVAL_SECONDS = 5 * 60

    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    ids = meter_ids(N_METERS)

    print(f"Publishing {N_METERS} meters every 5 minutes. Ctrl+C to stop.")
    try:
        while True:
            now = datetime.now(timezone.utc)
            for mid in ids:
                payload = generate_reading(mid, now)
                topic = f"{MQTT_TOPIC_PUB_PREFIX}{mid}"
                client.publish(topic, json.dumps(payload), qos=0)
            print("Published batch at:", now.isoformat(), "count:", len(ids))
            time.sleep(INTERVAL_SECONDS)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
