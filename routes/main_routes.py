from flask import Blueprint, request, jsonify
from services.reconciliation_service import get_service_metadata, process_reconciliation_queries
from services.database_service import get_database_stats

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def reconcile():
    """Main reconciliation endpoint following W3C specification"""
    if request.method == 'GET':
        # Return service metadata
        return jsonify(get_service_metadata())
    
    # Handle POST requests for reconciliation
    queries = request.form.get('queries')
    if not queries:
        return jsonify({"error": "No queries provided"}), 400
    
    try:
        results = process_reconciliation_queries(queries)
        return jsonify(results)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@main_bp.route('/stats')
def stats():
    """Statistics endpoint to show loaded data"""
    return jsonify(get_database_stats())