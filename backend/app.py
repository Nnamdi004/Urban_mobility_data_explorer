"""
Flask Backend API for NYC Taxi Data Explorer
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# add parent dir to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_config
from routes.trips import trips_bp
from routes.zones import zones_bp
from routes.insights import insights_bp

load_dotenv()

# Initialize Flask app with config
config = get_config()
app = Flask(__name__)
app.config.from_object(config)
CORS(app, origins=app.config['CORS_ORIGINS'])

# Register blueprints
app.register_blueprint(trips_bp)
app.register_blueprint(zones_bp)
app.register_blueprint(insights_bp)

@app.route('/')
def home():
    return jsonify({
        'message': 'NYC Taxi Data Explorer API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            'trips': '/api/trips',
            'zones': '/api/zones',
            'stats': '/api/stats',
            'analytics': '/api/analytics',
            'health': '/api/health'
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(f"Starting API server on port {app.config['API_PORT']}...")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Database: {app.config['DB_PATH']}")
    print(f"API will be available at http://localhost:{app.config['API_PORT']}")
    
    app.run(
        host=app.config['API_HOST'], 
        port=app.config['API_PORT'], 
        debug=app.config['DEBUG']
    )