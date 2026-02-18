"""
Data validation - verify data quality after processing
"""

import pandas as pd

class DataValidator:
    """Validate processed data before loading to database"""
    
    def __init__(self):
        self.validation_results = []
        self.is_valid = True
    
    def validate(self, df):
        """Run all validation checks"""
        print("\nValidating processed data...")
        
        self._check_required_columns(df)
        self._check_data_types(df)
        self._check_value_ranges(df)
        self._check_nulls(df)
        self._check_duplicates(df)
        
        if self.is_valid:
            print("\n✓ All validation checks passed")
        else:
            print("\n✗ Validation failed - see issues above")
        
        return self.is_valid
    
    def _check_required_columns(self, df):
        """Check if all required columns exist"""
        required = [
            'tpep_pickup_datetime',
            'tpep_dropoff_datetime',
            'passenger_count',
            'trip_distance',
            'PULocationID',
            'DOLocationID',
            'fare_amount',
            'tip_amount',
            'total_amount',
            'trip_duration_min',
            'avg_speed_mph',
            'pickup_hour'
        ]
        
        missing = [col for col in required if col not in df.columns]
        
        if missing:
            print(f"  ✗ Missing columns: {missing}")
            self.is_valid = False
            self.validation_results.append(f"Missing columns: {missing}")
        else:
            print(f"  ✓ All required columns present")
    
    def _check_data_types(self, df):
        """Check if columns have correct data types"""
        checks = {
            'trip_distance': 'numeric',
            'fare_amount': 'numeric',
            'passenger_count': 'numeric',
            'trip_duration_min': 'numeric',
            'avg_speed_mph': 'numeric',
            'pickup_hour': 'numeric'
        }
        
        issues = []
        for col, expected_type in checks.items():
            if col not in df.columns:
                continue
            
            if expected_type == 'numeric':
                if not pd.api.types.is_numeric_dtype(df[col]):
                    issues.append(f"{col} is not numeric")
        
        if issues:
            print(f"  ✗ Data type issues: {issues}")
            self.is_valid = False
            self.validation_results.extend(issues)
        else:
            print(f"  ✓ All data types correct")
    
    def _check_value_ranges(self, df):
        """Check if values are in expected ranges"""
        checks = [
            ('trip_distance', 0.1, 100, 'miles'),
            ('fare_amount', 0, 500, 'dollars'),
            ('passenger_count', 1, 6, 'passengers'),
            ('trip_duration_min', 1, 1440, 'minutes'),
            ('avg_speed_mph', 0, 80, 'mph'),
            ('pickup_hour', 0, 23, 'hour')
        ]
        
        issues = []
        for col, min_val, max_val, unit in checks:
            if col not in df.columns:
                continue
            
            out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
            if len(out_of_range) > 0:
                issues.append(f"{col}: {len(out_of_range)} values outside [{min_val}, {max_val}] {unit}")
        
        if issues:
            print(f"  ✗ Value range issues:")
            for issue in issues:
                print(f"     - {issue}")
            self.is_valid = False
            self.validation_results.extend(issues)
        else:
            print(f"  ✓ All values in expected ranges")
    
    def _check_nulls(self, df):
        """Check for unexpected null values"""
        critical_cols = [
            'tpep_pickup_datetime',
            'tpep_dropoff_datetime',
            'trip_distance',
            'fare_amount',
            'trip_duration_min'
        ]
        
        issues = []
        for col in critical_cols:
            if col not in df.columns:
                continue
            
            nulls = df[col].isna().sum()
            if nulls > 0:
                issues.append(f"{col}: {nulls} null values")
        
        if issues:
            print(f"  ✗ Null value issues:")
            for issue in issues:
                print(f"     - {issue}")
            self.is_valid = False
            self.validation_results.extend(issues)
        else:
            print(f"  ✓ No unexpected null values")
    
    def _check_duplicates(self, df):
        """Check for duplicates"""
        dupes = df.duplicated(
            subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime',
                   'PULocationID', 'DOLocationID']
        ).sum()
        
        if dupes > 0:
            print(f"  ✗ Found {dupes} potential duplicates")
            self.is_valid = False
            self.validation_results.append(f"{dupes} duplicates found")
        else:
            print(f"  ✓ No duplicates found")
    
    def get_summary(self, df):
        """Get data summary stats"""
        summary = {
            'total_records': len(df),
            'date_range': {
                'start': df['tpep_pickup_datetime'].min(),
                'end': df['tpep_pickup_datetime'].max()
            },
            'avg_fare': df['fare_amount'].mean(),
            'avg_distance': df['trip_distance'].mean(),
            'avg_duration': df['trip_duration_min'].mean(),
            'avg_speed': df['avg_speed_mph'].mean(),
            'total_revenue': df['total_amount'].sum()
        }
        
        print("\nData Summary:")
        print(f"  Total records: {summary['total_records']:,}")
        print(f"  Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"  Avg fare: ${summary['avg_fare']:.2f}")
        print(f"  Avg distance: {summary['avg_distance']:.2f} miles")
        print(f"  Avg duration: {summary['avg_duration']:.1f} minutes")
        print(f"  Avg speed: {summary['avg_speed']:.1f} mph")
        print(f"  Total revenue: ${summary['total_revenue']:,.2f}")
        
        return summary