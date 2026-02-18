"""
Zone model - handles zone/location data
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class Zone:
    """Model for taxi zones"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DB_PATH', 'database/nyc_taxi.db')
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_all(self):
        """Get all zones"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM zones ORDER BY borough, zone")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_by_id(self, location_id):
        """Get zone by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM zones WHERE location_id = ?", (location_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_by_borough(self, borough):
        """Get all zones in a borough"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM zones 
            WHERE borough = ?
            ORDER BY zone
        """, (borough,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_boroughs(self):
        """Get list of unique boroughs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT borough FROM zones ORDER BY borough")
        rows = cursor.fetchall()
        conn.close()
        
        return [row['borough'] for row in rows]
    
    def search(self, query):
        """Search zones by name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM zones 
            WHERE zone LIKE ? OR borough LIKE ?
            ORDER BY zone
        """, (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_zone_stats(self, location_id):
        """
        Get statistics for a specific zone
        Returns pickup/dropoff counts, avg fare, etc.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # pickup stats
        cursor.execute("""
            SELECT 
                COUNT(*) as pickup_count,
                AVG(fare_amount) as avg_fare,
                AVG(trip_distance) as avg_distance,
                AVG(trip_duration_min) as avg_duration
            FROM trips
            WHERE pickup_location_id = ?
        """, (location_id,))
        
        pickup_stats = dict(cursor.fetchone())
        
        # dropoff stats
        cursor.execute("""
            SELECT 
                COUNT(*) as dropoff_count
            FROM trips
            WHERE dropoff_location_id = ?
        """, (location_id,))
        
        dropoff_stats = dict(cursor.fetchone())
        
        conn.close()
        
        return {
            'location_id': location_id,
            'pickup_count': pickup_stats['pickup_count'],
            'dropoff_count': dropoff_stats['dropoff_count'],
            'avg_fare': round(pickup_stats['avg_fare'], 2) if pickup_stats['avg_fare'] else 0,
            'avg_distance': round(pickup_stats['avg_distance'], 2) if pickup_stats['avg_distance'] else 0,
            'avg_duration': round(pickup_stats['avg_duration'], 1) if pickup_stats['avg_duration'] else 0
        }
    
    def get_popular_zones(self, limit=10, by='pickup'):
        """
        Get most popular zones by pickup or dropoff count
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if by == 'pickup':
            query = """
                SELECT 
                    z.*,
                    COUNT(t.trip_id) as trip_count
                FROM zones z
                LEFT JOIN trips t ON z.location_id = t.pickup_location_id
                GROUP BY z.location_id
                ORDER BY trip_count DESC
                LIMIT ?
            """
        else:
            query = """
                SELECT 
                    z.*,
                    COUNT(t.trip_id) as trip_count
                FROM zones z
                LEFT JOIN trips t ON z.location_id = t.dropoff_location_id
                GROUP BY z.location_id
                ORDER BY trip_count DESC
                LIMIT ?
            """
        
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]