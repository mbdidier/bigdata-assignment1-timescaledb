-- Enable compression on all hypertables
ALTER TABLE energy_readings SET (timescaledb.compress, timescaledb.compress_segmentby = 'meter_id');

ALTER TABLE energy_readings_3h SET (timescaledb.compress, timescaledb.compress_segmentby = 'meter_id');

ALTER TABLE energy_readings_week SET (timescaledb.compress, timescaledb.compress_segmentby = 'meter_id');

-- Compress chunks older than 7 days (policy)
SELECT add_compression_policy('energy_readings', INTERVAL '7 days');
SELECT add_compression_policy('energy_readings_3h', INTERVAL '7 days');
SELECT add_compression_policy('energy_readings_week', INTERVAL '7 days');

-- Measure sizes
SELECT hypertable_name,
       pg_size_pretty(pg_total_relation_size(format('%I.%I', hypertable_schema, hypertable_name)::regclass)) AS total_size
FROM timescaledb_information.hypertables
WHERE hypertable_name IN ('energy_readings','energy_readings_3h','energy_readings_week')
ORDER BY hypertable_name;
