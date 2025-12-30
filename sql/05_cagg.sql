-- 15-minute cagg
DROP MATERIALIZED VIEW IF EXISTS energy_15min CASCADE;
CREATE MATERIALIZED VIEW energy_15min
WITH (timescaledb.continuous) AS
SELECT time_bucket('15 minutes', timestamp) AS bucket,
       meter_id,
       AVG(power) AS avg_power,
       SUM(energy) AS sum_energy
FROM energy_readings
GROUP BY bucket, meter_id;

-- Hourly cagg
DROP MATERIALIZED VIEW IF EXISTS energy_hourly CASCADE;
CREATE MATERIALIZED VIEW energy_hourly
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', timestamp) AS bucket,
       meter_id,
       AVG(power) AS avg_power,
       SUM(energy) AS sum_energy
FROM energy_readings
GROUP BY bucket, meter_id;

-- Daily cagg
DROP MATERIALIZED VIEW IF EXISTS energy_daily CASCADE;
CREATE MATERIALIZED VIEW energy_daily
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', timestamp) AS bucket,
       meter_id,
       AVG(power) AS avg_power,
       SUM(energy) AS sum_energy
FROM energy_readings
GROUP BY bucket, meter_id;

-- Refresh policy example
SELECT add_continuous_aggregate_policy('energy_15min',
  start_offset => INTERVAL '1 month',
  end_offset   => INTERVAL '1 minute',
  schedule_interval => INTERVAL '5 minutes');
