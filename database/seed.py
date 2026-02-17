import sqlite3
import pandas as pd
import os
from datetime import datetime

def seed_database(db_path, schema_path, cleaned_trips_path, zones_lookup_path):
    """
    Seed the database with cleaned trip data and zone lookup data
    """
    print("Starting database seeding process...")
    start_time = datetime.now()
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute schema
    print("Creating database schema...")
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    print("Schema created successfully!")
    
    # Load zones data
    print("Loading zones data...")
    zones_df = pd.read_csv(zones_lookup_path)
    
    # Insert zones
    zones_inserted = 0
    for _, row in zones_df.iterrows():
        # Handle N/A and empty values
        borough = str(row['Borough']).strip() if pd.notna(row['Borough']) and str(row['Borough']).strip() not in ['N/A', ''] else 'Unknown'
        zone = str(row['Zone']).strip() if pd.notna(row['Zone']) and str(row['Zone']).strip() not in ['N/A', ''] else 'Unknown'
        service_zone = str(row['service_zone']).strip() if pd.notna(row['service_zone']) and str(row['service_zone']).strip() not in ['N/A', ''] else None
        
        cursor.execute("""
            INSERT INTO zones (location_id, borough, zone, service_zone)
            VALUES (?, ?, ?, ?)
        """, (
            int(row['LocationID']),
            borough,
            zone,
            service_zone
        ))
        zones_inserted += 1
    
    print(f"Inserted {zones_inserted} zones")
    
    # Load trips data in chunks (memory efficient for large files)
    print("Loading trips data (this may take a few minutes)...")
    chunk_size = 50000
    trips_inserted = 0
    
    for chunk in pd.read_csv(cleaned_trips_path, chunksize=chunk_size):
        # Prepare data for insertion
        trips_data = []
        for _, row in chunk.iterrows():
            trips_data.append((
                row['tpep_pickup_datetime'],
                row['tpep_dropoff_datetime'],
                int(row['passenger_count']) if pd.notna(row['passenger_count']) else None,
                float(row['trip_distance']),
                int(row['PULocationID']),
                int(row['DOLocationID']),
                float(row['fare_amount']),
                float(row['tip_amount']) if pd.notna(row['tip_amount']) else 0.0,
                float(row['total_amount']),
                float(row['trip_duration_min']),
                float(row['avg_speed_mph']) if pd.notna(row['avg_speed_mph']) else 0.0,
                int(row['pickup_hour'])
            ))
        
        # Bulk insert
        cursor.executemany("""
            INSERT INTO trips (
                pickup_datetime, dropoff_datetime, passenger_count,
                trip_distance, pickup_location_id, dropoff_location_id,
                fare_amount, tip_amount, total_amount,
                trip_duration_min, avg_speed_mph, pickup_hour
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, trips_data)
        
        trips_inserted += len(trips_data)
        print(f"Inserted {trips_inserted:,} trips...")
        
        # Commit periodically
        conn.commit()
    
    # Final commit
    conn.commit()
    
    # Verify data
    cursor.execute("SELECT COUNT(*) FROM zones")
    zone_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM trips")
    trip_count = cursor.fetchone()[0]
    
    # Close connection
    conn.close()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*50)
    print("DATABASE SEEDING COMPLETE!")
    print("="*50)
    print(f"Zones inserted: {zone_count:,}")
    print(f"Trips inserted: {trip_count:,}")
    print(f"Time taken: {duration:.2f} seconds")
    print(f"Database location: {db_path}")
    print("="*50)

if __name__ == '__main__':
    # Get paths relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    db_path = os.path.join(project_root, 'database', 'nyc_taxi.db')
    schema_path = os.path.join(project_root, 'database', 'schema.sql')
    cleaned_trips_path = os.path.join(project_root, 'backend', 'data', 'processed', 'cleaned_trips.csv')
    zones_lookup_path = os.path.join(project_root, 'backend', 'data', 'raw', 'taxi_zone_lookup.csv')
    
    seed_database(db_path, schema_path, cleaned_trips_path, zones_lookup_path)
