-- NYC Taxi Trip Database Schema
-- Normalized relational design for urban mobility data

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS zones;

-- ============================================
-- DIMENSION TABLE: Taxi Zones
-- ============================================
CREATE TABLE zones (
    location_id INTEGER PRIMARY KEY,
    borough VARCHAR(50) NOT NULL,
    zone VARCHAR(100) NOT NULL,
    service_zone VARCHAR(50)
);

-- ============================================
-- FACT TABLE: Trip Records
-- ============================================
CREATE TABLE trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_datetime TIMESTAMP NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,
    passenger_count INTEGER,
    trip_distance REAL NOT NULL,
    pickup_location_id INTEGER NOT NULL,
    dropoff_location_id INTEGER NOT NULL,
    fare_amount REAL NOT NULL,
    tip_amount REAL,
    total_amount REAL NOT NULL,
    trip_duration_min REAL NOT NULL,
    avg_speed_mph REAL,
    pickup_hour INTEGER NOT NULL,
    
    -- Foreign key constraints
    FOREIGN KEY (pickup_location_id) REFERENCES zones(location_id),
    FOREIGN KEY (dropoff_location_id) REFERENCES zones(location_id),
    
    -- Data integrity constraints
    CHECK (trip_distance > 0),
    CHECK (fare_amount >= 2.50),
    CHECK (total_amount > 0),
    CHECK (trip_duration_min > 0),
    CHECK (pickup_hour >= 0 AND pickup_hour <= 23),
    CHECK (dropoff_datetime > pickup_datetime)
);

-- ============================================
-- PERFORMANCE INDEXES
-- ============================================

-- Index for time-based queries (most common)
CREATE INDEX idx_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX idx_pickup_hour ON trips(pickup_hour);

-- Index for location-based queries
CREATE INDEX idx_pickup_location ON trips(pickup_location_id);
CREATE INDEX idx_dropoff_location ON trips(dropoff_location_id);

-- Composite index for zone-to-zone analysis
CREATE INDEX idx_pickup_dropoff ON trips(pickup_location_id, dropoff_location_id);

-- Index for fare analysis
CREATE INDEX idx_fare_amount ON trips(fare_amount);

-- Index for distance queries
CREATE INDEX idx_trip_distance ON trips(trip_distance);

-- Zone lookup optimization
CREATE INDEX idx_zone_borough ON zones(borough);
