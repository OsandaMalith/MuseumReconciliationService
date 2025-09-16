from flask import Blueprint, request, jsonify
from services.search_service import search_entities
from services.reconciliation_service import get_available_types, get_available_properties

api_bp = Blueprint('api', __name__)

@api_bp.route('/suggest/entity', methods=['GET'])
def suggest_entity():
    """Entity suggestion endpoint for auto-completion"""
    prefix = request.args.get('prefix', '')
    cursor = request.args.get('cursor', 0)
    
    suggestions = search_entities(prefix, limit=20)
    
    return jsonify({
        "result": suggestions[:10],  # Return max 10 suggestions
        "cursor": cursor + len(suggestions[:10])
    })

@api_bp.route('/suggest/type', methods=['GET'])
def suggest_type():
    """Type suggestion endpoint"""
    prefix = request.args.get('prefix', '').lower()
    
    all_types = get_available_types()
    filtered = [t for t in all_types if prefix in t['name'].lower()]
    
    return jsonify({"result": filtered})

@api_bp.route('/suggest/property', methods=['GET'])
def suggest_property():
    """Property suggestion endpoint"""
    prefix = request.args.get('prefix', '').lower()
    
    all_properties = get_available_properties()['properties']
    filtered = [p for p in all_properties if prefix in p['name'].lower()]
    
    return jsonify({"result": filtered})

@api_bp.route('/extend', methods=['GET'])
def extend():
    """Extend endpoint for getting additional properties"""
    return jsonify(get_available_properties())

@api_bp.route('/flyout', methods=['GET'])
def flyout():
    """Flyout endpoint for entity details (used by some reconciliation clients)"""
    entity_id = request.args.get('id')
    if not entity_id:
        return jsonify({"error": "No ID provided"}), 400
    
    # For now, redirect to preview functionality
    from routes.preview_routes import preview
    return preview(entity_id)