-- Create tables
DROP TABLE IF EXISTS energy_readings_3h CASCADE;
DROP TABLE IF EXISTS energy_readings_week CASCADE;

CREATE TABLE energy_readings_3h (LIKE energy_readings INCLUDING ALL);
CREATE TABLE energy_readings_week (LIKE energy_readings INCLUDING ALL);

-- Convert to hypertables with different chunk sizes
SELECT create_hypertable('energy_readings_3h', 'timestamp',
  chunk_time_interval => INTERVAL '3 hours', if_not_exists => TRUE);

SELECT create_hypertable('energy_readings_week', 'timestamp',
  chunk_time_interval => INTERVAL '1 week', if_not_exists => TRUE);
