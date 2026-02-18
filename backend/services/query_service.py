"""
Query Service - handles common database queries
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class QueryService:
    """Service for executing common database queries"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DB_PATH', 'database/nyc_taxi.db')
    
    def get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_basic_stats(self):
        """Get overall statistics"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                COUNT(*) as total_trips,
                AVG(fare_amount) as avg_fare,
                AVG(trip_distance) as avg_distance,
                AVG(trip_duration_min) as avg_duration,
                SUM(fare_amount) as total_revenue
            FROM trips
        """)
        
        result = dict(cur.fetchone())
        conn.close()
        
        return {
            'total_trips': result['total_trips'],
            'avg_fare': round(result['avg_fare'], 2) if result['avg_fare'] else 0,
            'avg_distance': round(result['avg_distance'], 2) if result['avg_distance'] else 0,
            'avg_duration': round(result['avg_duration'], 1) if result['avg_duration'] else 0,
            'total_revenue': round(result['total_revenue'], 2) if result['total_revenue'] else 0
        }
    
    def get_hourly_distribution(self):
        """Get trip count by hour"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                pickup_hour,
                COUNT(*) as trip_count,
                AVG(fare_amount) as avg_fare,
                AVG(trip_distance) as avg_distance
            FROM trips
            GROUP BY pickup_hour
            ORDER BY pickup_hour
        """)
        
        rows = cur.fetchall()
        conn.close()
        
        return [{
            'hour': row['pickup_hour'],
            'trip_count': row['trip_count'],
            'avg_fare': round(row['avg_fare'], 2),
            'avg_distance': round(row['avg_distance'], 2)
        } for row in rows]
    
    def get_trips_by_borough(self):
        """Get trip stats by borough"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                z.borough,
                COUNT(t.trip_id) as trip_count,
                AVG(t.fare_amount) as avg_fare,
                AVG(t.trip_distance) as avg_distance,
                SUM(t.fare_amount) as total_revenue
            FROM trips t
            JOIN zones z ON t.pickup_location_id = z.location_id
            GROUP BY z.borough
            ORDER BY trip_count DESC
        """)
        
        rows = cur.fetchall()
        conn.close()
        
        return [{
            'borough': row['borough'],
            'trip_count': row['trip_count'],
            'avg_fare': round(row['avg_fare'], 2),
            'avg_distance': round(row['avg_distance'], 2),
            'total_revenue': round(row['total_revenue'], 2)
        } for row in rows]
    
    def get_top_pickup_zones(self, limit=10):
        """Get zones with most pickups"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                z.location_id,
                z.zone,
                z.borough,
                COUNT(t.trip_id) as pickup_count,
                AVG(t.fare_amount) as avg_fare
            FROM zones z
            LEFT JOIN trips t ON z.location_id = t.pickup_location_id
            GROUP BY z.location_id
            ORDER BY pickup_count DESC
            LIMIT ?
        """, (limit,))
        
        rows = cur.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_top_dropoff_zones(self, limit=10):
        """Get zones with most dropoffs"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                z.location_id,
                z.zone,
                z.borough,
                COUNT(t.trip_id) as dropoff_count
            FROM zones z
            LEFT JOIN trips t ON z.location_id = t.dropoff_location_id
            GROUP BY z.location_id
            ORDER BY dropoff_count DESC
            LIMIT ?
        """, (limit,))
        
        rows = cur.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_popular_routes(self, limit=10):
        """Get most common pickup->dropoff routes"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                t.pickup_location_id,
                t.dropoff_location_id,
                pu_zone.zone as pickup_zone,
                pu_zone.borough as pickup_borough,
                do_zone.zone as dropoff_zone,
                do_zone.borough as dropoff_borough,
                COUNT(*) as trip_count,
                AVG(t.fare_amount) as avg_fare,
                AVG(t.trip_distance) as avg_distance
            FROM trips t
            JOIN zones pu_zone ON t.pickup_location_id = pu_zone.location_id
            JOIN zones do_zone ON t.dropoff_location_id = do_zone.location_id
            GROUP BY t.pickup_location_id, t.dropoff_location_id
            ORDER BY trip_count DESC
            LIMIT ?
        """, (limit,))
        
        rows = cur.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_fare_distribution(self, bins=10):
        """Get fare amount distribution"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        # get min/max fare
        cur.execute("SELECT MIN(fare_amount) as min_fare, MAX(fare_amount) as max_fare FROM trips")
        range_data = dict(cur.fetchone())
        
        min_fare = range_data['min_fare']
        max_fare = range_data['max_fare']
        
        # calculate bin size
        bin_size = (max_fare - min_fare) / bins
        
        # manually create bins and count
        distribution = []
        for i in range(bins):
            bin_start = min_fare + (i * bin_size)
            bin_end = bin_start + bin_size
            
            cur.execute("""
                SELECT COUNT(*) as count
                FROM trips
                WHERE fare_amount >= ? AND fare_amount < ?
            """, (bin_start, bin_end))
            
            count = cur.fetchone()['count']
            distribution.append({
                'bin_start': round(bin_start, 2),
                'bin_end': round(bin_end, 2),
                'count': count
            })
        
        conn.close()
        return distribution
    
    def search_trips(self, filters):
        """
        Flexible search with multiple filters
        filters = {
            'start_date': '2024-01-01',
            'end_date': '2024-01-31',
            'min_fare': 10,
            'max_fare': 50,
            'pickup_zone': 123,
            'dropoff_zone': 456,
            'limit': 100
        }
        """
        conn = self.get_conn()
        cur = conn.cursor()
        
        query = """
            SELECT t.*,
                   pu_zone.zone as pickup_zone,
                   do_zone.zone as dropoff_zone
            FROM trips t
            JOIN zones pu_zone ON t.pickup_location_id = pu_zone.location_id
            JOIN zones do_zone ON t.dropoff_location_id = do_zone.location_id
            WHERE 1=1
        """
        params = []
        
        if 'start_date' in filters:
            query += " AND t.pickup_datetime >= ?"
            params.append(filters['start_date'])
        
        if 'end_date' in filters:
            query += " AND t.pickup_datetime <= ?"
            params.append(filters['end_date'])
        
        if 'min_fare' in filters:
            query += " AND t.fare_amount >= ?"
            params.append(filters['min_fare'])
        
        if 'max_fare' in filters:
            query += " AND t.fare_amount <= ?"
            params.append(filters['max_fare'])
        
        if 'pickup_zone' in filters:
            query += " AND t.pickup_location_id = ?"
            params.append(filters['pickup_zone'])
        
        if 'dropoff_zone' in filters:
            query += " AND t.dropoff_location_id = ?"
            params.append(filters['dropoff_zone'])
        
        limit = filters.get('limit', 100)
        query += " ORDER BY t.pickup_datetime DESC LIMIT ?"
        params.append(limit)
        
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]