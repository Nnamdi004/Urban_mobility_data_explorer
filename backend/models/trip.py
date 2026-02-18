"""
Trip model - handles trip data from database
"""

import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Trip:
    """Model for trip records"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DB_PATH', 'database/nyc_taxi.db')
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # return rows as dicts
        return conn
    
    def get_by_id(self, trip_id):
        """Get single trip by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.*, 
                   pu_zone.zone as pickup_zone,
                   pu_zone.borough as pickup_borough,
                   do_zone.zone as dropoff_zone,
                   do_zone.borough as dropoff_borough
            FROM trips t
            LEFT JOIN zones pu_zone ON t.pickup_location_id = pu_zone.location_id
            LEFT JOIN zones do_zone ON t.dropoff_location_id = do_zone.location_id
            WHERE t.trip_id = ?
        """, (trip_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_all(self, limit=100, offset=0):
        """Get all trips with pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM trips
            ORDER BY pickup_datetime DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def filter_trips(self, filters=None, limit=100):
        """
        Filter trips based on criteria
        
        filters can include:
        - start_date, end_date
        - min_fare, max_fare
        - min_distance, max_distance
        - pickup_location_id, dropoff_location_id
        """
        if filters is None:
            filters = {}
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # build query dynamically
        query = "SELECT * FROM trips WHERE 1=1"
        params = []
        
        if 'start_date' in filters:
            query += " AND pickup_datetime >= ?"
            params.append(filters['start_date'])
        
        if 'end_date' in filters:
            query += " AND pickup_datetime <= ?"
            params.append(filters['end_date'])
        
        if 'min_fare' in filters:
            query += " AND fare_amount >= ?"
            params.append(filters['min_fare'])
        
        if 'max_fare' in filters:
            query += " AND fare_amount <= ?"
            params.append(filters['max_fare'])
        
        if 'min_distance' in filters:
            query += " AND trip_distance >= ?"
            params.append(filters['min_distance'])
        
        if 'max_distance' in filters:
            query += " AND trip_distance <= ?"
            params.append(filters['max_distance'])
        
        if 'pickup_location_id' in filters:
            query += " AND pickup_location_id = ?"
            params.append(filters['pickup_location_id'])
        
        if 'dropoff_location_id' in filters:
            query += " AND dropoff_location_id = ?"
            params.append(filters['dropoff_location_id'])
        
        query += " ORDER BY pickup_datetime DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_by_hour(self, hour):
        """Get trips by hour of day"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM trips
            WHERE pickup_hour = ?
            LIMIT 1000
        """, (hour,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_by_zone(self, zone_id, location_type='pickup'):
        """
        Get trips by zone
        location_type: 'pickup' or 'dropoff'
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if location_type == 'pickup':
            query = "SELECT * FROM trips WHERE pickup_location_id = ? LIMIT 1000"
        else:
            query = "SELECT * FROM trips WHERE dropoff_location_id = ? LIMIT 1000"
        
        cursor.execute(query, (zone_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def count(self, filters=None):
        """Count trips with optional filters"""
        if filters is None:
            filters = {}
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) as count FROM trips WHERE 1=1"
        params = []
        
        if 'start_date' in filters:
            query += " AND pickup_datetime >= ?"
            params.append(filters['start_date'])
        
        if 'end_date' in filters:
            query += " AND pickup_datetime <= ?"
            params.append(filters['end_date'])
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        
        return result['count'] if result else 0
    
    def get_date_range(self):
        """Get min and max dates in dataset"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                MIN(pickup_datetime) as min_date,
                MAX(pickup_datetime) as max_date
            FROM trips
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'min_date': result['min_date'],
                'max_date': result['max_date']
            }
        return None