from flask import Blueprint, request, jsonify
from app.services.demand_service import DemandService
from app.utils.logger import logger

demand_bp = Blueprint('demand', __name__)
demand_service = DemandService()

@demand_bp.route('/api/calculate-demand', methods=['POST'])
def calculate_demand():
    try:
        data = request.get_json()
        
        # Validate required parameters
        required_params = ['entity_id', 'lat', 'lng']
        if not all(param in data for param in required_params):
            return jsonify({'error': 'Required parameters: entity_id, lat, lng'}), 400
            
        # Extract parameters
        entity_id = data['entity_id']
        lat = float(data['lat'])
        lng = float(data['lng'])
        
        # Calculate demand
        results = demand_service.calculate_demand(entity_id, lat, lng)
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error in calculate_demand endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500