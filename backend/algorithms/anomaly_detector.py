"""
Anomaly Detector - Manual Implementation
Detect suspicious trips based on fare, distance, and speed anomalies

No using built-in stats libraries or numpy functions for mean/std
"""

class AnomalyDetector:
    """Detect anomalies in trip data using manual statistical calculations"""
    
    def __init__(self, z_threshold=3.0):
        """
        Args:
            z_threshold: number of standard deviations to consider anomaly
        """
        self.z_threshold = z_threshold
        self.stats_cache = {}
    
    def detect_fare_anomalies(self, trips):
        """
        Find trips with anomalous fare amounts
        
        Args:
            trips: list of dicts with 'fare_amount', 'distance', etc.
        
        Returns:
            list of anomalous trip indices
        
        Algorithm:
        1. Calculate mean and std manually
        2. Find trips beyond z_threshold standard deviations
        3. Also check fare-per-mile ratio
        """
        if not trips:
            return []
        
        fares = [t['fare_amount'] for t in trips]
        distances = [t['trip_distance'] for t in trips]
        
        # calculate statistics manually
        fare_mean = self._calculate_mean(fares)
        fare_std = self._calculate_std(fares, fare_mean)
        
        anomalies = []
        
        for i, trip in enumerate(trips):
            fare = trip['fare_amount']
            distance = trip['trip_distance']
            
            # check z-score
            if fare_std > 0:
                z_score = (fare - fare_mean) / fare_std
                if abs(z_score) > self.z_threshold:
                    anomalies.append({
                        'index': i,
                        'trip_id': trip.get('trip_id'),
                        'reason': 'fare_outlier',
                        'z_score': round(z_score, 2),
                        'fare': fare
                    })
            
            # check fare per mile ratio
            if distance > 0:
                fare_per_mile = fare / distance
                # reasonable range: $2-50 per mile
                if fare_per_mile < 2 or fare_per_mile > 50:
                    anomalies.append({
                        'index': i,
                        'trip_id': trip.get('trip_id'),
                        'reason': 'fare_per_mile_anomaly',
                        'fare_per_mile': round(fare_per_mile, 2),
                        'fare': fare,
                        'distance': distance
                    })
        
        return anomalies
    
    def detect_speed_anomalies(self, trips):
        """
        Find trips with impossible/suspicious speeds
        
        Speed limits in NYC:
        - Average traffic: 10-25 mph
        - Highway: up to 55 mph
        - Unrealistic: > 80 mph or < 1 mph
        """
        anomalies = []
        
        for i, trip in enumerate(trips):
            distance = trip.get('trip_distance', 0)
            duration = trip.get('trip_duration_min', 0)
            
            if duration <= 0 or distance <= 0:
                continue
            
            # calculate speed manually
            speed_mph = (distance / duration) * 60  # convert to mph
            
            # flag suspicious speeds
            if speed_mph > 80:
                anomalies.append({
                    'index': i,
                    'trip_id': trip.get('trip_id'),
                    'reason': 'speed_too_high',
                    'speed_mph': round(speed_mph, 1),
                    'distance': distance,
                    'duration': duration
                })
            elif speed_mph < 1 and distance > 0.5:
                # too slow for significant distance
                anomalies.append({
                    'index': i,
                    'trip_id': trip.get('trip_id'),
                    'reason': 'speed_too_low',
                    'speed_mph': round(speed_mph, 1),
                    'distance': distance,
                    'duration': duration
                })
        
        return anomalies
    
    def detect_distance_time_mismatch(self, trips):
        """
        Detect trips where distance and time don't make sense together
        
        Uses manual calculation of expected time based on distance
        """
        anomalies = []
        
        for i, trip in enumerate(trips):
            distance = trip.get('trip_distance', 0)
            duration = trip.get('trip_duration_min', 0)
            
            if distance <= 0 or duration <= 0:
                continue
            
            # expected time based on distance (manual calculation)
            # assume average NYC speed: 15 mph
            expected_duration = (distance / 15) * 60  # minutes
            
            # allow 50% variance
            min_expected = expected_duration * 0.5
            max_expected = expected_duration * 1.5
            
            if duration < min_expected or duration > max_expected:
                anomalies.append({
                    'index': i,
                    'trip_id': trip.get('trip_id'),
                    'reason': 'distance_time_mismatch',
                    'distance': distance,
                    'duration': duration,
                    'expected_duration': round(expected_duration, 1)
                })
        
        return anomalies
    
    def detect_all_anomalies(self, trips):
        """
        Run all anomaly detection algorithms
        Returns dict with anomalies by type
        """
        results = {
            'fare_anomalies': self.detect_fare_anomalies(trips),
            'speed_anomalies': self.detect_speed_anomalies(trips),
            'mismatch_anomalies': self.detect_distance_time_mismatch(trips)
        }
        
        # count unique anomalous trips
        all_indices = set()
        for anomaly_list in results.values():
            for anomaly in anomaly_list:
                all_indices.add(anomaly['index'])
        
        results['total_anomalous_trips'] = len(all_indices)
        results['anomaly_rate'] = len(all_indices) / len(trips) if trips else 0
        
        return results
    
    # manual statistical functions - no numpy!
    
    def _calculate_mean(self, values):
        """Calculate mean manually"""
        if not values:
            return 0
        total = 0
        for val in values:
            total += val
        return total / len(values)
    
    def _calculate_std(self, values, mean=None):
        """
        Calculate standard deviation manually
        
        Formula: sqrt(sum((x - mean)^2) / n)
        """
        if not values:
            return 0
        
        if mean is None:
            mean = self._calculate_mean(values)
        
        # calculate variance
        squared_diffs = 0
        for val in values:
            diff = val - mean
            squared_diffs += diff * diff
        
        variance = squared_diffs / len(values)
        
        # calculate sqrt manually
        std = self._manual_sqrt(variance)
        return std
    
    def _manual_sqrt(self, n):
        """
        Manual square root using Newton's method
        No using math.sqrt!
        """
        if n < 0:
            return 0
        if n == 0:
            return 0
        
        # initial guess
        x = n / 2.0
        
        # Newton's method iterations
        for _ in range(10):  # 10 iterations is enough for precision
            x = (x + n / x) / 2.0
        
        return x
    
    def get_anomaly_summary(self, trips):
        """
        Get summary statistics about anomalies
        Returns easy-to-read dict
        """
        results = self.detect_all_anomalies(trips)
        
        summary = {
            'total_trips': len(trips),
            'total_anomalies': results['total_anomalous_trips'],
            'anomaly_rate_percent': round(results['anomaly_rate'] * 100, 2),
            'fare_anomalies': len(results['fare_anomalies']),
            'speed_anomalies': len(results['speed_anomalies']),
            'mismatch_anomalies': len(results['mismatch_anomalies'])
        }
        
        return summary


# helper function
def find_anomalies(trips, threshold=3.0):
    """
    Quick function to find anomalies in trip data
    
    Args:
        trips: list of trip dicts
        threshold: z-score threshold
    
    Returns:
        dict with all anomaly results
    """
    detector = AnomalyDetector(z_threshold=threshold)
    return detector.detect_all_anomalies(trips)