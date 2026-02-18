"""
Main pipeline runner - orchestrates data loading, cleaning, and processing
"""

import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

from load_data import DataLoader
from clean_data import DataCleaner
from feature_engineering import FeatureEngineer
from validate_data import DataValidator

load_dotenv()

def run_pipeline(sample_size=None):
    """
    Run the complete data pipeline
    
    Args:
        sample_size: if int, process only that many rows (for testing)
    """
    print("="*60)
    print("NYC TAXI DATA PIPELINE")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if sample_size:
        print(f"Running in sample mode: {sample_size:,} records")
    
    print("="*60)
    
    try:
        # step 1: load data
        print("\n[STEP 1/5] Loading data...")
        loader = DataLoader()
        
        # verify files exist first
        if not loader.verify_files_exist():
            print("\n✗ Missing required data files!")
            print("  Please ensure these files are in data/raw/:")
            print("    - yellow_tripdata.parquet")
            print("    - taxi_zone_lookup.csv")
            print("    - taxi_zones.geojson")
            return False
        
        trips_df = loader.load_trip_data(sample=sample_size)
        zones_df = loader.load_zone_lookup()
        geojson = loader.load_zone_geojson()
        
        # step 2: clean data
        print("\n[STEP 2/5] Cleaning data...")
        cleaner = DataCleaner()
        trips_df = cleaner.clean(trips_df)
        
        # step 3: engineer features
        print("\n[STEP 3/5] Engineering features...")
        engineer = FeatureEngineer()
        trips_df = engineer.engineer(trips_df)
        
        # step 4: validate
        print("\n[STEP 4/5] Validating data...")
        validator = DataValidator()
        is_valid = validator.validate(trips_df)
        
        if not is_valid:
            print("\n✗ Validation failed! Check errors above.")
            return False
        
        # get summary
        summary = validator.get_summary(trips_df)
        
        # step 5: save processed data
        print("\n[STEP 5/5] Saving processed data...")
        output_dir = os.getenv('PROCESSED_DATA_DIR', 'data/processed')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'cleaned_trips.parquet')
        trips_df.to_parquet(output_file, engine='pyarrow', index=False)
        print(f"Saved to: {output_file}")
        
        zones_output = os.path.join(output_dir, 'zones.csv')
        zones_df.to_csv(zones_output, index=False)
        print(f"Saved zones to: {zones_output}")
        
        # save cleaning log
        cleaner.save_log()
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETE")
        print("="*60)
        print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Final record count: {len(trips_df):,}")
        print("="*60)
        
        print("\nNext steps:")
        print("  1. Run database seed script: python database/seed.py")
        print("  2. Start backend: python backend/app.py")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Pipeline failed with error:")
        print(f"  {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run NYC taxi data pipeline')
    parser.add_argument('--sample', type=int, help='Process only N records (for testing)')
    
    args = parser.parse_args()
    
    success = run_pipeline(sample_size=args.sample)
    
    if success:
        print("\n✓ Pipeline completed successfully")
    else:
        print("\n✗ Pipeline failed")