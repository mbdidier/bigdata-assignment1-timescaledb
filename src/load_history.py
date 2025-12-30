import random
from datetime import datetime, timedelta, timezone
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from utils import db_conninfo

INSERT_SQL = """
INSERT INTO energy_readings (meter_id, timestamp, power, voltage, current, frequency, energy)
VALUES %s
ON CONFLICT (meter_id, timestamp) DO NOTHING;
"""

def daily_multiplier(hour: int) -> float:
    if 0 <= hour <= 5:
        return 0.55
    if 6 <= hour <= 9:
        return 0.85
    if 10 <= hour <= 16:
        return 0.75
    if 17 <= hour <= 21:
        return 1.00
    return 0.70

def generate_row(meter_id: int, ts: datetime):
    mult = daily_multiplier(ts.hour)
    voltage = random.gauss(230, 5)
    frequency = random.gauss(50, 0.05)
    base_power = random.uniform(0.2, 2.5)
    power = max(0.05, base_power * mult + random.uniform(-0.05, 0.05))
    current = max(0.05, (power * 1000) / max(100, voltage))
    energy = power * (5.0 / 60.0)
    return (meter_id, ts.isoformat(), power, voltage, current, frequency, energy)

def meter_ids(n: int, start: int = 1000000000):
    return [start + i for i in range(n)]

def main():
    # Increase to reach ~4.2M rows.
    # 1000 meters * 288/day * 14 days = 4,032,000 rows (close to 4.2M)
    N_METERS = 1050  # gives ~4.23M rows for 14 days (approx)
    DAYS = 14
    STEP_MINUTES = 5
    BATCH_ROWS = 10000

    end_ts = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    start_ts = end_ts - timedelta(days=DAYS)

    ids = meter_ids(N_METERS)

    conn = psycopg2.connect(db_conninfo())
    cur = conn.cursor()

    total_steps = int((DAYS * 24 * 60) / STEP_MINUTES)
    print(f"Generating ~{N_METERS * total_steps:,} rows ...")

    batch = []
    ts = start_ts

    try:
        for _ in tqdm(range(total_steps)):
            for mid in ids:
                batch.append(generate_row(mid, ts))

                if len(batch) >= BATCH_ROWS:
                    execute_values(cur, INSERT_SQL, batch, page_size=5000)
                    conn.commit()
                    batch = []

            ts += timedelta(minutes=STEP_MINUTES)

        if batch:
            execute_values(cur, INSERT_SQL, batch, page_size=5000)
            conn.commit()

    finally:
        cur.close()
        conn.close()

    print("Done.")
    print("Row count check: run SELECT COUNT(*) FROM energy_readings;")

if __name__ == "__main__":
    main()
