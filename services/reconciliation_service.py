import json
from typing import Dict, Any
from services.search_service import search_entities
from config.settings import Config

def process_reconciliation_queries(queries_json: str) -> Dict[str, Any]:
    """Process reconciliation queries following W3C specification"""
    try:
        queries = json.loads(queries_json)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in queries parameter")
    
    results = {}
    
    for query_id, query_data in queries.items():
        query_text = query_data.get('query', '')
        limit = min(query_data.get('limit', Config.DEFAULT_SEARCH_LIMIT), Config.MAX_RESULTS_LIMIT)
        type_filter = None
        properties = query_data.get('properties', {})
        
        # Handle type filtering
        if 'type' in query_data:
            type_filter = query_data['type']
        elif 'types' in query_data and query_data['types']:
            type_filter = query_data['types'][0]
        
        # Search for matches
        matches = search_entities(query_text, limit, type_filter, properties)
        results[query_id] = {"result": matches}
    
    return results

def get_service_metadata() -> Dict[str, Any]:
    """Get service metadata following W3C specification"""
    return Config.SERVICE_METADATA

def get_available_types() -> list:
    """Get available entity types"""
    return [
        {"id": "artifact", "name": "Cultural Artifact"},
        {"id": "museum", "name": "Museum/Institution"},
        {"id": "person", "name": "Artist/Creator"}
    ]

def get_available_properties() -> Dict[str, Any]:
    """Get available properties for extension"""
    return {
        "properties": [
            {"id": "location", "name": "Location"},
            {"id": "date", "name": "Date/Period"},
            {"id": "creator", "name": "Creator/Artist"},
            {"id": "medium", "name": "Medium/Material"},
            {"id": "nationality", "name": "Nationality"},
            {"id": "classification", "name": "Classification"},
            {"id": "department", "name": "Department"},
            {"id": "museum_type", "name": "Museum Type"}
        ]
    }