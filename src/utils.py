import os
from dotenv import load_dotenv

load_dotenv()

def db_conninfo() -> str:
    # Use env values and the docker-mapped port
    db = os.getenv("TS_DB", "energy")
    user = os.getenv("TS_USER", "energy_user")
    pwd = os.getenv("TS_PASSWORD", "K1g@li2025!")
    host = "localhost"
    port = int(os.getenv("TS_PORT", "5433"))
    # psycopg2 uses separate fields, so special chars in password are fine
    return f"dbname={db} user={user} password={pwd} host={host} port={port}"

MQTT_HOST = "localhost"
MQTT_PORT = 1884
MQTT_TOPIC_SUB = "energy/meters/#"
MQTT_TOPIC_PUB_PREFIX = "energy/meters/"
