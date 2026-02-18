"""
Data loading - reads raw parquet and CSV files
"""

import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DataLoader:
    """Load raw data files"""
    
    def __init__(self):
        self.raw_dir = os.getenv('RAW_DATA_DIR', 'data/raw')
        self.parquet_file = os.getenv('PARQUET_FILE', 'yellow_tripdata.parquet')
        self.zone_lookup_file = os.getenv('ZONE_LOOKUP_FILE', 'taxi_zone_lookup.csv')
        self.zone_geojson_file = os.getenv('ZONE_GEOJSON_FILE', 'taxi_zones.geojson')
    
    def load_trip_data(self, sample=None):
        """
        Load trip data from parquet
        sample: if int, load only that many rows (for testing)
        """
        file_path = os.path.join(self.raw_dir, self.parquet_file)
        
        print(f"Loading trip data from {file_path}...")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Trip data not found: {file_path}")
        
        if sample:
            df = pd.read_parquet(file_path, engine='pyarrow')
            df = df.head(sample)
            print(f"Loaded {len(df)} sample trips")
        else:
            df = pd.read_parquet(file_path, engine='pyarrow')
            print(f"Loaded {len(df)} trips")
        
        return df
    
    def load_zone_lookup(self):
        """Load zone lookup CSV"""
        file_path = os.path.join(self.raw_dir, self.zone_lookup_file)
        
        print(f"Loading zone lookup from {file_path}...")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Zone lookup not found: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} zones")
        
        return df
    
    def load_zone_geojson(self):
        """Load zone GeoJSON file"""
        file_path = os.path.join(self.raw_dir, self.zone_geojson_file)
        
        print(f"Loading GeoJSON from {file_path}...")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GeoJSON not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data.get('features', []))} zone geometries")
        
        return data
    
    def verify_files_exist(self):
        """Check if all required files exist"""
        files = {
            'trip_data': os.path.join(self.raw_dir, self.parquet_file),
            'zone_lookup': os.path.join(self.raw_dir, self.zone_lookup_file),
            'zone_geojson': os.path.join(self.raw_dir, self.zone_geojson_file)
        }
        
        missing = []
        for name, path in files.items():
            if not os.path.exists(path):
                missing.append(f"{name}: {path}")
        
        if missing:
            print("Missing files:")
            for m in missing:
                print(f"  - {m}")
            return False
        
        print("All required files present")
        return True