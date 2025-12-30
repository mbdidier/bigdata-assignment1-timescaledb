
CREATE EXTENSION IF NOT EXISTS timescaledb;

DROP TABLE IF EXISTS energy_readings CASCADE;

CREATE TABLE energy_readings (
  meter_id BIGINT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  power DOUBLE PRECISION NOT NULL,
  voltage DOUBLE PRECISION NOT NULL,
  current DOUBLE PRECISION NOT NULL,
  frequency DOUBLE PRECISION NOT NULL,
  energy DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (meter_id, timestamp)
);

CREATE INDEX IF NOT EXISTS idx_energy_readings_time ON energy_readings (timestamp DESC);
