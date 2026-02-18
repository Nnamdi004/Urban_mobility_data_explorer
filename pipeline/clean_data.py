"""
Data cleaning - remove outliers, handle missing values
"""

import pandas as pd
import numpy as np

class DataCleaner:
    """Clean and validate trip data"""
    
    def __init__(self):
        self.cleaning_log = []
        self.stats = {
            'original_count': 0,
            'final_count': 0,
            'removed_count': 0
        }
    
    def clean(self, df):
        """Main cleaning pipeline"""
        print("\nStarting data cleaning...")
        self.stats['original_count'] = len(df)
        print(f"Original records: {self.stats['original_count']:,}")
        
        df = self._handle_missing_values(df)
        df = self._remove_duplicates(df)
        df = self._filter_outliers(df)
        df = self._validate_timestamps(df)
        df = self._validate_locations(df)
        
        self.stats['final_count'] = len(df)
        self.stats['removed_count'] = self.stats['original_count'] - self.stats['final_count']
        
        print(f"\nCleaning complete:")
        print(f"  Kept: {self.stats['final_count']:,}")
        print(f"  Removed: {self.stats['removed_count']:,}")
        print(f"  Retention: {self.stats['final_count']/self.stats['original_count']*100:.1f}%")
        
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values"""
        print("\n1. Handling missing values...")
        
        # critical fields can't be null
        critical = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 
                   'trip_distance', 'fare_amount']
        
        before = len(df)
        for col in critical:
            if col in df.columns:
                missing = df[col].isna().sum()
                if missing > 0:
                    df = df.dropna(subset=[col])
                    self._log(f"Removed {missing} records with missing {col}")
        
        removed = before - len(df)
        if removed > 0:
            print(f"   Removed {removed} records with missing critical fields")
        
        # fill passenger count with 1 if missing
        if 'passenger_count' in df.columns:
            missing = df['passenger_count'].isna().sum()
            if missing > 0:
                df['passenger_count'].fillna(1, inplace=True)
                print(f"   Filled {missing} missing passenger counts with 1")
        
        return df
    
    def _remove_duplicates(self, df):
        """Remove duplicate records"""
        print("\n2. Removing duplicates...")
        
        before = len(df)
        df = df.drop_duplicates(
            subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime',
                   'PULocationID', 'DOLocationID', 'trip_distance'],
            keep='first'
        )
        removed = before - len(df)
        
        if removed > 0:
            print(f"   Removed {removed} duplicates")
            self._log(f"Removed {removed} duplicate records")
        else:
            print(f"   No duplicates found")
        
        return df
    
    def _filter_outliers(self, df):
        """Remove outlier values"""
        print("\n3. Filtering outliers...")
        
        before = len(df)
        
        # distance outliers
        df = df[(df['trip_distance'] >= 0.1) & (df['trip_distance'] <= 100)]
        distance_removed = before - len(df)
        if distance_removed > 0:
            print(f"   Removed {distance_removed} trips with bad distances")
            self._log(f"Removed {distance_removed} distance outliers")
        
        before = len(df)
        
        # passenger outliers
        if 'passenger_count' in df.columns:
            df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 6)]
            passenger_removed = before - len(df)
            if passenger_removed > 0:
                print(f"   Removed {passenger_removed} trips with bad passenger counts")
                self._log(f"Removed {passenger_removed} passenger outliers")
        
        before = len(df)
        
        # fare outliers
        df = df[(df['fare_amount'] >= 0) & (df['fare_amount'] <= 500)]
        fare_removed = before - len(df)
        if fare_removed > 0:
            print(f"   Removed {fare_removed} trips with bad fares")
            self._log(f"Removed {fare_removed} fare outliers")
        
        return df
    
    def _validate_timestamps(self, df):
        """Validate trip timestamps"""
        print("\n4. Validating timestamps...")
        
        before = len(df)
        
        # dropoff must be after pickup
        df = df[df['tpep_dropoff_datetime'] > df['tpep_pickup_datetime']]
        time_removed = before - len(df)
        if time_removed > 0:
            print(f"   Removed {time_removed} trips with invalid timestamps")
            self._log(f"Removed {time_removed} invalid timestamps")
        
        before = len(df)
        
        # remove trips longer than 24 hours
        duration = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
        df = df[duration <= 1440]  # 24 hours in minutes
        long_removed = before - len(df)
        if long_removed > 0:
            print(f"   Removed {long_removed} trips longer than 24 hours")
            self._log(f"Removed {long_removed} trips over 24 hours")
        
        return df
    
    def _validate_locations(self, df):
        """Validate location IDs"""
        print("\n5. Validating location IDs...")
        
        before = len(df)
        
        # valid location IDs: 1-263
        df = df[(df['PULocationID'] >= 1) & (df['PULocationID'] <= 263)]
        df = df[(df['DOLocationID'] >= 1) & (df['DOLocationID'] <= 263)]
        
        removed = before - len(df)
        if removed > 0:
            print(f"   Removed {removed} trips with invalid location IDs")
            self._log(f"Removed {removed} invalid location IDs")
        
        return df
    
    def _log(self, message):
        """Add entry to cleaning log"""
        self.cleaning_log.append(message)
    
    def save_log(self, output_path='data/logs/cleaning_log.txt'):
        """Save cleaning log to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("Data Cleaning Log\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Original records: {self.stats['original_count']:,}\n")
            f.write(f"Final records: {self.stats['final_count']:,}\n")
            f.write(f"Removed: {self.stats['removed_count']:,}\n")
            f.write(f"Retention rate: {self.stats['final_count']/self.stats['original_count']*100:.2f}%\n\n")
            f.write("Cleaning steps:\n")
            for entry in self.cleaning_log:
                f.write(f"  - {entry}\n")
        
        print(f"\nCleaning log saved to {output_path}")