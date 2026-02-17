# Database Setup

## Schema Overview

The database uses a **normalized relational design** with two main tables:

### Tables

1. **zones** (Dimension Table)
   - `location_id` (PK): Unique zone identifier
   - `borough`: NYC borough name
   - `zone`: Zone name
   - `service_zone`: Service classification

2. **trips** (Fact Table)
   - `trip_id` (PK): Auto-incrementing unique identifier
   - `pickup_datetime`: Trip start timestamp
   - `dropoff_datetime`: Trip end timestamp
   - `passenger_count`: Number of passengers
   - `trip_distance`: Distance in miles
   - `pickup_location_id` (FK): References zones
   - `dropoff_location_id` (FK): References zones
   - `fare_amount`: Base fare
   - `tip_amount`: Tip amount
   - `total_amount`: Total fare
   - `trip_duration_min`: Calculated duration
   - `avg_speed_mph`: Calculated average speed
   - `pickup_hour`: Hour of pickup (0-23)

## Setup Instructions

### 1. Ensure cleaned data exists
```bash
cd backend/script
python clean_data.py
```

### 2. Run the seed script
```bash
cd database
python seed.py
```

This will:
- Create `nyc_taxi.db` SQLite database
- Create tables with schema
- Load zones data (~265 zones)
- Load trips data (~7.6M trips)
- Create performance indexes

**Note**: Seeding may take 5-10 minutes depending on your system.

### 3. Verify database
```bash
sqlite3 nyc_taxi.db "SELECT COUNT(*) FROM trips;"
sqlite3 nyc_taxi.db "SELECT COUNT(*) FROM zones;"
```

## Performance Optimizations

- **Indexes** on frequently queried columns (datetime, location, fare)
- **Composite indexes** for common query patterns
- **Foreign key constraints** for data integrity
- **Check constraints** for data validation

## Database Location

`database/nyc_taxi.db` (ignored in Git - too large)
