"""
Flask Backend API for NYC Taxi Data Explorer
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# add parent dir to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.trip import Trip
from models.zone import Zone
from services.query_service import QueryService
from services.analytics_service import AnalyticsService

load_dotenv()

app = Flask(__name__)
CORS(app)  # allow frontend to call our API

# initialize services
trip_model = Trip()
zone_model = Zone()
query_service = QueryService()
analytics_service = AnalyticsService()

@app.route('/')
def home():
    return jsonify({
        'message': 'NYC Taxi Data Explorer API',
        'version': '1.0',
        'status': 'running'
    })

# ===== Basic Stats Endpoints =====

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        stats = query_service.get_basic_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/hourly', methods=['GET'])
def get_hourly_stats():
    """Get trip distribution by hour"""
    try:
        data = query_service.get_hourly_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/borough', methods=['GET'])
def get_borough_stats():
    """Get stats by borough"""
    try:
        data = query_service.get_trips_by_borough()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Zone Endpoints =====

@app.route('/api/zones', methods=['GET'])
def get_zones():
    """Get all zones"""
    try:
        zones = zone_model.get_all()
        return jsonify(zones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/zones/<int:zone_id>', methods=['GET'])
def get_zone(zone_id):
    """Get specific zone with stats"""
    try:
        zone = zone_model.get_by_id(zone_id)
        if not zone:
            return jsonify({'error': 'Zone not found'}), 404
        
        stats = zone_model.get_zone_stats(zone_id)
        return jsonify({**zone, **stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/zones/top-pickups', methods=['GET'])
def get_top_pickup_zones():
    """Get top pickup zones"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        zones = query_service.get_top_pickup_zones(limit)
        return jsonify(zones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/zones/top-dropoffs', methods=['GET'])
def get_top_dropoff_zones():
    """Get top dropoff zones"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        zones = query_service.get_top_dropoff_zones(limit)
        return jsonify(zones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Trip Endpoints =====

@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Get trips with pagination and filters"""
    try:
        # pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)
        offset = (page - 1) * per_page
        
        # filters
        filters = {}
        if request.args.get('start_date'):
            filters['start_date'] = request.args.get('start_date')
        if request.args.get('end_date'):
            filters['end_date'] = request.args.get('end_date')
        if request.args.get('min_fare'):
            filters['min_fare'] = float(request.args.get('min_fare'))
        if request.args.get('max_fare'):
            filters['max_fare'] = float(request.args.get('max_fare'))
        if request.args.get('pickup_zone'):
            filters['pickup_location_id'] = int(request.args.get('pickup_zone'))
        
        trips = trip_model.filter_trips(filters, limit=per_page)
        total = trip_model.count(filters)
        
        return jsonify({
            'trips': trips,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Get single trip by ID"""
    try:
        trip = trip_model.get_by_id(trip_id)
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        return jsonify(trip)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Analytics Endpoints (using custom algorithms) =====

@app.route('/api/analytics/top-zones', methods=['GET'])
def analyze_top_zones():
    """Get top zones using custom algorithm"""
    try:
        k = request.args.get('k', default=10, type=int)
        metric = request.args.get('metric', default='pickups', type=str)
        
        results = analytics_service.analyze_top_zones(k, metric)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/top-routes', methods=['GET'])
def analyze_top_routes():
    """Get top routes using custom algorithm"""
    try:
        k = request.args.get('k', default=10, type=int)
        results = analytics_service.analyze_top_routes(k)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/anomalies', methods=['GET'])
def detect_anomalies():
    """Detect anomalies using custom detector"""
    try:
        sample_size = request.args.get('sample', default=10000, type=int)
        results = analytics_service.detect_anomalies(sample_size)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/speed-patterns', methods=['GET'])
def get_speed_patterns():
    """Get speed patterns by hour"""
    try:
        data = analytics_service.analyze_speed_patterns()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/revenue-hourly', methods=['GET'])
def get_revenue_by_hour():
    """Get revenue analysis by hour"""
    try:
        data = analytics_service.analyze_revenue_by_hour()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/borough-comparison', methods=['GET'])
def compare_boroughs():
    """Compare all boroughs"""
    try:
        data = analytics_service.compare_boroughs()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/insights', methods=['GET'])
def get_insights():
    """Get key insights using all analytics"""
    try:
        insights = analytics_service.get_insights()
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Popular Routes =====

@app.route('/api/routes/popular', methods=['GET'])
def get_popular_routes():
    """Get most popular routes"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        routes = query_service.get_popular_routes(limit)
        return jsonify(routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Search =====

@app.route('/api/search/trips', methods=['POST'])
def search_trips():
    """Advanced trip search with filters"""
    try:
        filters = request.json
        results = query_service.search_trips(filters)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Health Check =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    try:
        # test db connection
        stats = query_service.get_basic_stats()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'total_trips': stats['total_trips']
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"Starting API server on port {port}...")
    print(f"Debug mode: {debug}")
    print(f"API will be available at http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)