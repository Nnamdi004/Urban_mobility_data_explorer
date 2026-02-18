"""
Insights Routes - Handle analytics and insights endpoints
"""

from flask import Blueprint, jsonify, request
from services.analytics_service import AnalyticsService
from services.query_service import QueryService

insights_bp = Blueprint('insights', __name__, url_prefix='/api')

# Initialize services
analytics_service = AnalyticsService()
query_service = QueryService()

# ===== Basic Stats =====

@insights_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        stats = query_service.get_basic_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/stats/hourly', methods=['GET'])
def get_hourly_stats():
    """Get trip distribution by hour"""
    try:
        data = query_service.get_hourly_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/stats/borough', methods=['GET'])
def get_borough_stats():
    """Get stats by borough"""
    try:
        data = query_service.get_trips_by_borough()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Analytics (Custom Algorithms) =====

@insights_bp.route('/analytics/top-zones', methods=['GET'])
def analyze_top_zones():
    """Get top zones using custom algorithm"""
    try:
        k = request.args.get('k', default=10, type=int)
        metric = request.args.get('metric', default='pickups', type=str)
        
        results = analytics_service.analyze_top_zones(k, metric)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/analytics/top-routes', methods=['GET'])
def analyze_top_routes():
    """Get top routes using custom algorithm"""
    try:
        k = request.args.get('k', default=10, type=int)
        results = analytics_service.analyze_top_routes(k)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/analytics/anomalies', methods=['GET'])
def detect_anomalies():
    """Detect anomalies using custom detector"""
    try:
        sample_size = request.args.get('sample', default=10000, type=int)
        results = analytics_service.detect_anomalies(sample_size)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/analytics/speed-patterns', methods=['GET'])
def get_speed_patterns():
    """Get speed patterns by hour"""
    try:
        data = analytics_service.analyze_speed_patterns()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/analytics/revenue-hourly', methods=['GET'])
def get_revenue_by_hour():
    """Get revenue analysis by hour"""
    try:
        data = analytics_service.analyze_revenue_by_hour()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/analytics/borough-comparison', methods=['GET'])
def compare_boroughs():
    """Compare all boroughs"""
    try:
        data = analytics_service.compare_boroughs()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insights_bp.route('/analytics/insights', methods=['GET'])
def get_insights():
    """Get key insights using all analytics"""
    try:
        insights = analytics_service.get_insights()
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Routes =====

@insights_bp.route('/routes/popular', methods=['GET'])
def get_popular_routes():
    """Get most popular routes"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        routes = query_service.get_popular_routes(limit)
        return jsonify(routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Search =====

@insights_bp.route('/search/trips', methods=['POST'])
def search_trips():
    """Advanced trip search with filters"""
    try:
        filters = request.json
        results = query_service.search_trips(filters)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== Health Check =====

@insights_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    try:
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
