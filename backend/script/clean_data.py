import pandas as pd
import datetime
import os

def process_nyc_taxi_data(csv_path, lookup_path, output_path, log_path):
    #  DATA INTEGRATION
    print("Loading data...")
    # Read the CSV file and the lookup CSV
    df = pd.read_csv(csv_path)
    lookup = pd.read_csv(lookup_path)
    
    initial_count = len(df)
    log_entries = []

    # DATA INTEGRITY (The Cleaning part) 
    #  Remove impossible timestamps 
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    
    mask_time = df['tpep_dropoff_datetime'] > df['tpep_pickup_datetime']
    time_anomalies = initial_count - mask_time.sum()
    df = df[mask_time]
    log_entries.append(f"Removed {time_anomalies} records with invalid timestamps (Dropoff <= Pickup).")

    # Remove zero or negative distances
    mask_dist = df['trip_distance'] > 0
    dist_anomalies = len(df) - mask_dist.sum()
    df = df[mask_dist]
    log_entries.append(f"Removed {dist_anomalies} records with zero or negative distance.")

    #  Remove fare outliers (Minimum NYC fare is $2.50)
    mask_fare = df['fare_amount'] >= 2.50
    fare_anomalies = len(df) - mask_fare.sum()
    df = df[mask_fare]
    log_entries.append(f"Removed {fare_anomalies} records with fare < $2.50.")

    #  FEATURE ENGINEERING (The 3 Derived Features) 
    print("Engineering features...")
    
    # Feature 1:  (How long was the ride in minutes?)
    df['trip_duration_min'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # Feature 2:  (How fast was the taxi moving in MPH?)
    df['avg_speed_mph'] = df['trip_distance'] / (df['trip_duration_min'] / 60)
    # Handle any math errors (like dividing by 0 duration)
    df['avg_speed_mph'] = df['avg_speed_mph'].replace([float('inf')], 0).fillna(0)

    # Feature 3: Pickup Hour 
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    
    #  NORMALIZATION & EXPORT 
    # Only keep the columns we actually need for the database
    columns_to_keep = [
        'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 
        'trip_distance', 'PULocationID', 'DOLocationID', 'fare_amount', 
        'tip_amount', 'total_amount', 'trip_duration_min', 'avg_speed_mph', 'pickup_hour'
    ]
    df_clean = df[columns_to_keep]
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    # Export the cleaned data for your database
    df_clean.to_csv(output_path, index=False)
    
    #  TRANSPARENCY LOG
    with open(log_path, 'w') as f:
        f.write("--- DATA CLEANING TRANSPARENCY LOG ---\n")
        f.write(f"Execution Date: {datetime.datetime.now()}\n")
        f.write(f"Initial Records Received: {initial_count}\n")
        for entry in log_entries:
            f.write(f"- {entry}\n")
        f.write(f"Final Records Exported: {len(df_clean)}\n")
        f.write(f"Data Reduction: {((initial_count - len(df_clean))/initial_count)*100:.2f}%\n")
    print(f"Success! Cleaned data saved to {output_path}")

if __name__ == '__main__':
    # Get the script directory and construct paths relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    process_nyc_taxi_data(
        csv_path=os.path.join(project_root, 'backend', 'data', 'raw', 'yellow_tripdata_2019-01.csv'),
        lookup_path=os.path.join(project_root, 'backend', 'data', 'raw', 'taxi_zone_lookup.csv'),
        output_path=os.path.join(project_root, 'backend', 'data', 'processed', 'cleaned_trips.csv'),
        log_path=os.path.join(project_root, 'backend', 'data', 'logs', 'transparency_log.txt')
    )