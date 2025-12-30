
-- 1) Average power per hour today
SELECT time_bucket('1 hour', timestamp) AS hour,
       AVG(power) AS avg_power
FROM energy_readings
WHERE timestamp >= date_trunc('day', now())
GROUP BY hour
ORDER BY hour;

-- 2) Peak 15-minute periods past week (by avg power)
SELECT time_bucket('15 minutes', timestamp) AS bucket_15m,
       AVG(power) AS avg_power
FROM energy_readings
WHERE timestamp >= now() - INTERVAL '7 days'
GROUP BY bucket_15m
ORDER BY avg_power DESC
LIMIT 20;

-- 3) Monthly consumption per meter (sum energy)
SELECT meter_id,
       time_bucket('1 month', timestamp) AS month,
       SUM(energy) AS total_energy
FROM energy_readings
GROUP BY meter_id, month
ORDER BY month DESC, meter_id
LIMIT 200;

-- 4) Full dataset scan (count/avg/max/min)
SELECT COUNT(*) AS rows,
       AVG(power) AS avg_power,
       MIN(power) AS min_power,
       MAX(power) AS max_power
FROM energy_readings;
