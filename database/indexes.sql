-- Additional Performance Indexes
-- Run this after initial data load for optimal query performance

-- Composite indexes for common query patterns

-- Time + Location analysis
CREATE INDEX IF NOT EXISTS idx_time_pickup_loc ON trips(pickup_datetime, pickup_location_id);
CREATE INDEX IF NOT EXISTS idx_hour_pickup_loc ON trips(pickup_hour, pickup_location_id);

-- Fare + Distance analysis
CREATE INDEX IF NOT EXISTS idx_fare_distance ON trips(fare_amount, trip_distance);

-- Speed analysis
CREATE INDEX IF NOT EXISTS idx_speed ON trips(avg_speed_mph);

-- Duration analysis
CREATE INDEX IF NOT EXISTS idx_duration ON trips(trip_duration_min);

-- Passenger count analysis
CREATE INDEX IF NOT EXISTS idx_passenger_count ON trips(passenger_count);

-- Date range queries (covering index)
CREATE INDEX IF NOT EXISTS idx_datetime_range ON trips(pickup_datetime, dropoff_datetime);

-- Analyze tables for query optimizer
ANALYZE trips;
ANALYZE zones;
