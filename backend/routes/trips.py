"""
Trip Routes - Handle trip-related endpoints
"""

from flask import Blueprint, jsonify, request
from models.trip import Trip

trips_bp = Blueprint('trips', __name__, url_prefix='/api/trips')

# Initialize model
trip_model = Trip()

@trips_bp.route('', methods=['GET'])
def get_trips():
    """Get trips with pagination and filters"""
    try:
        # pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)
        
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

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Get single trip by ID"""
    try:
        trip = trip_model.get_by_id(trip_id)
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        return jsonify(trip)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
