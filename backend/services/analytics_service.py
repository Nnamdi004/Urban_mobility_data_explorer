"""
Analytics Service - advanced analytics using custom algorithms
"""

import sqlite3
import os
import sys
from dotenv import load_dotenv

# add parent dir to path to import algorithms
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.top_k_zones import TopKZones
from algorithms.anomaly_detector import AnomalyDetector

load_dotenv()

class AnalyticsService:
    """Service for advanced analytics"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DB_PATH', 'database/nyc_taxi.db')
        self.top_k_finder = TopKZones(k=10)
        self.anomaly_detector = AnomalyDetector(z_threshold=3.0)
    
    def get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def analyze_top_zones(self, k=10, metric='pickups'):
        """
        Find top K zones using our custom algorithm
        
        metric: 'pickups', 'dropoffs', or 'revenue'
        """
        conn = self.get_conn()
        cur = conn.cursor()
        
        if metric == 'pickups':
            # get pickup counts
            cur.execute("""
                SELECT pickup_location_id, COUNT(*) as count
                FROM trips
                GROUP BY pickup_location_id
            """)
        elif metric == 'dropoffs':
            # get dropoff counts
            cur.execute("""
                SELECT dropoff_location_id, COUNT(*) as count
                FROM trips
                GROUP BY dropoff_location_id
            """)
        else:  # revenue
            # get revenue by pickup zone
            cur.execute("""
                SELECT pickup_location_id, SUM(fare_amount) as total_revenue
                FROM trips
                GROUP BY pickup_location_id
            """)
        
        rows = cur.fetchall()
        
        # convert to dict for our algorithm
        if metric == 'revenue':
            zone_data = {row[0]: row[1] for row in rows}  # zone_id: revenue
        else:
            zone_data = {row[0]: row[1] for row in rows}  # zone_id: count
        
        # use our custom top K algorithm
        self.top_k_finder.k = k
        if metric == 'revenue':
            top_zones = self.top_k_finder.find_top_k_by_revenue(zone_data)
        else:
            top_zones = self.top_k_finder.find_top_k_pickups(zone_data)
        
        # get zone names
        results = []
        for zone_id, value in top_zones:
            cur.execute("SELECT * FROM zones WHERE location_id = ?", (zone_id,))
            zone_info = dict(cur.fetchone())
            results.append({
                'location_id': zone_id,
                'zone': zone_info['zone'],
                'borough': zone_info['borough'],
                'value': round(value, 2) if metric == 'revenue' else value,
                'metric': metric
            })
        
        conn.close()
        return results
    
    def analyze_top_routes(self, k=10):
        """Find top K routes using custom algorithm"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        # get all route counts
        cur.execute("""
            SELECT pickup_location_id, dropoff_location_id, COUNT(*) as count
            FROM trips
            GROUP BY pickup_location_id, dropoff_location_id
        """)
        
        rows = cur.fetchall()
        
        # convert to dict
        route_counts = {(row[0], row[1]): row[2] for row in rows}
        
        # use custom algorithm
        top_routes = self.top_k_finder.find_top_routes(route_counts, k)
        
        # get zone info
        results = []
        for (pickup_id, dropoff_id), count in top_routes:
            cur.execute("SELECT zone, borough FROM zones WHERE location_id = ?", (pickup_id,))
            pickup_info = dict(cur.fetchone())
            
            cur.execute("SELECT zone, borough FROM zones WHERE location_id = ?", (dropoff_id,))
            dropoff_info = dict(cur.fetchone())
            
            results.append({
                'pickup_location_id': pickup_id,
                'pickup_zone': pickup_info['zone'],
                'pickup_borough': pickup_info['borough'],
                'dropoff_location_id': dropoff_id,
                'dropoff_zone': dropoff_info['zone'],
                'dropoff_borough': dropoff_info['borough'],
                'trip_count': count
            })
        
        conn.close()
        return results
    
    def detect_anomalies(self, sample_size=10000):
        """
        Run anomaly detection on sample of trips
        Uses our custom anomaly detector
        """
        conn = self.get_conn()
        cur = conn.cursor()
        
        # get random sample
        cur.execute("""
            SELECT 
                trip_id,
                fare_amount,
                trip_distance,
                trip_duration_min
            FROM trips
            ORDER BY RANDOM()
            LIMIT ?
        """, (sample_size,))
        
        rows = cur.fetchall()
        trips = [dict(row) for row in rows]
        
        # run anomaly detection
        anomalies = self.anomaly_detector.detect_all_anomalies(trips)
        summary = self.anomaly_detector.get_anomaly_summary(trips)
        
        conn.close()
        
        return {
            'summary': summary,
            'anomalies': anomalies
        }
    
    def analyze_speed_patterns(self):
        """Analyze average speeds by hour"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                pickup_hour,
                AVG(avg_speed_mph) as avg_speed,
                COUNT(*) as trip_count
            FROM trips
            WHERE avg_speed_mph > 0 AND avg_speed_mph < 80
            GROUP BY pickup_hour
            ORDER BY pickup_hour
        """)
        
        rows = cur.fetchall()
        conn.close()
        
        return [{
            'hour': row['pickup_hour'],
            'avg_speed': round(row['avg_speed'], 2),
            'trip_count': row['trip_count']
        } for row in rows]
    
    def analyze_revenue_by_hour(self):
        """Revenue analysis by hour"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                pickup_hour,
                COUNT(*) as trip_count,
                SUM(fare_amount) as total_revenue,
                AVG(fare_amount) as avg_fare
            FROM trips
            GROUP BY pickup_hour
            ORDER BY pickup_hour
        """)
        
        rows = cur.fetchall()
        conn.close()
        
        return [{
            'hour': row['pickup_hour'],
            'trip_count': row['trip_count'],
            'total_revenue': round(row['total_revenue'], 2),
            'avg_fare': round(row['avg_fare'], 2)
        } for row in rows]
    
    def compare_boroughs(self):
        """Compare boroughs across multiple metrics"""
        conn = self.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                z.borough,
                COUNT(t.trip_id) as trip_count,
                AVG(t.fare_amount) as avg_fare,
                AVG(t.trip_distance) as avg_distance,
                AVG(t.trip_duration_min) as avg_duration,
                AVG(t.avg_speed_mph) as avg_speed,
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
            'avg_duration': round(row['avg_duration'], 1),
            'avg_speed': round(row['avg_speed'], 1),
            'total_revenue': round(row['total_revenue'], 2)
        } for row in rows]
    
    def get_insights(self):
        """
        Get key insights - combines multiple analyses
        Returns top findings
        """
        # top zones
        top_pickup_zones = self.analyze_top_zones(k=3, metric='pickups')
        top_revenue_zones = self.analyze_top_zones(k=3, metric='revenue')
        
        # top routes
        top_routes = self.analyze_top_routes(k=3)
        
        # borough comparison
        borough_stats = self.compare_boroughs()
        
        # speed patterns
        speed_by_hour = self.analyze_speed_patterns()
        
        # find rush hours (lowest speed)
        slowest_hours = sorted(speed_by_hour, key=lambda x: x['avg_speed'])[:3]
        
        return {
            'top_pickup_zones': top_pickup_zones,
            'top_revenue_zones': top_revenue_zones,
            'top_routes': top_routes,
            'borough_comparison': borough_stats,
            'slowest_hours': slowest_hours
        }