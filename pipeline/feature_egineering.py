"""
Feature engineering - create derived features
"""

import pandas as pd
import numpy as np

class FeatureEngineer:
    """Add derived features to trip data"""
    
    def engineer(self, df):
        """Add all engineered features"""
        print("\nEngineering features...")
        
        df = self._calculate_duration(df)
        df = self._calculate_speed(df)
        df = self._extract_time_features(df)
        
        print("Feature engineering complete")
        return df
    
    def _calculate_duration(self, df):
        """Calculate trip duration in minutes"""
        print("  - Calculating trip duration...")
        
        df['trip_duration_min'] = (
            df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
        ).dt.total_seconds() / 60
        
        # round to integers
        df['trip_duration_min'] = df['trip_duration_min'].round(0).astype(int)
        
        avg_duration = df['trip_duration_min'].mean()
        print(f"    Average duration: {avg_duration:.1f} minutes")
        
        return df
    
    def _calculate_speed(self, df):
        """Calculate average speed in mph"""
        print("  - Calculating average speed...")
        
        # speed = distance / (time in hours)
        df['avg_speed_mph'] = np.where(
            df['trip_duration_min'] > 0,
            (df['trip_distance'] / (df['trip_duration_min'] / 60)),
            0
        )
        
        df['avg_speed_mph'] = df['avg_speed_mph'].round(2)
        
        # cap unrealistic speeds
        df.loc[df['avg_speed_mph'] > 80, 'avg_speed_mph'] = 80
        df.loc[df['avg_speed_mph'] < 0, 'avg_speed_mph'] = 0
        
        avg_speed = df['avg_speed_mph'].mean()
        print(f"    Average speed: {avg_speed:.1f} mph")
        
        return df
    
    def _extract_time_features(self, df):
        """Extract hour, day of week, etc."""
        print("  - Extracting temporal features...")
        
        # hour of day (0-23)
        df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
        
        # day of week (0=Monday, 6=Sunday)
        df['pickup_day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
        
        # is weekend
        df['is_weekend'] = df['pickup_day_of_week'].isin([5, 6]).astype(int)
        
        # time category
        df['time_category'] = df['pickup_hour'].apply(self._categorize_time)
        
        # date
        df['pickup_date'] = df['tpep_pickup_datetime'].dt.date
        
        weekend_pct = (df['is_weekend'].sum() / len(df)) * 100
        print(f"    Weekend trips: {weekend_pct:.1f}%")
        
        return df
    
    def _categorize_time(self, hour):
        """Categorize hour into time period"""
        if 6 <= hour < 9:
            return 'Morning Rush'
        elif 9 <= hour < 16:
            return 'Midday'
        elif 16 <= hour < 19:
            return 'Evening Rush'
        else:
            return 'Night'
    
    def get_feature_summary(self, df):
        """Get summary of engineered features"""
        summary = {
            'avg_duration_min': df['trip_duration_min'].mean(),
            'avg_speed_mph': df['avg_speed_mph'].mean(),
            'rush_hour_trips': len(df[df['time_category'].isin(['Morning Rush', 'Evening Rush'])]),
            'weekend_trips': df['is_weekend'].sum(),
            'weekday_trips': len(df) - df['is_weekend'].sum()
        }
        
        return summary