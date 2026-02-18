"""
Zone Routes - Handle zone-related endpoints
"""

from flask import Blueprint, jsonify, request
from models.zone import Zone
from services.query_service import QueryService

zones_bp = Blueprint('zones', __name__, url_prefix='/api/zones')

# Initialize services
zone_model = Zone()
query_service = QueryService()

@zones_bp.route('', methods=['GET'])
def get_zones():
    """Get all zones"""
    try:
        zones = zone_model.get_all()
        return jsonify(zones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zones_bp.route('/<int:zone_id>', methods=['GET'])
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

@zones_bp.route('/top-pickups', methods=['GET'])
def get_top_pickup_zones():
    """Get top pickup zones"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        zones = query_service.get_top_pickup_zones(limit)
        return jsonify(zones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zones_bp.route('/top-dropoffs', methods=['GET'])
def get_top_dropoff_zones():
    """Get top dropoff zones"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        zones = query_service.get_top_dropoff_zones(limit)
        return jsonify(zones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
