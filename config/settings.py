import os

class Config:
    """Application configuration"""
    
    # Flask settings
    DEBUG = True
    PORT = 5000
    
    # Database settings
    DATABASE_PATH = 'data/museum_reconciliation.db'
    
    # CSV file paths
    CSV_FILES = {
        'museums': 'data/museums.csv',
        'artists': 'data/artists.csv',
        'artifacts': 'data/artworks.csv'
    }
    
    # Service metadata following W3C Reconciliation API specification
    SERVICE_METADATA = {
        "versions": ["0.2"],
        "name": "Museum Cultural Heritage Reconciliation Service",
        "identifierSpace": "http://museum-reconciliation.example.org/identifier",
        "schemaSpace": "http://museum-reconciliation.example.org/schema",
        "view": {
            "url": "http://localhost:5000/view/{{id}}"
        },
        "preview": {
            "url": "http://localhost:5000/preview/{{id}}",
            "width": 600,
            "height": 400
        },
        "defaultTypes": [
            {
                "id": "artifact",
                "name": "Cultural Artifact"
            },
            {
                "id": "museum",
                "name": "Museum/Institution"
            },
            {
                "id": "person",
                "name": "Artist/Creator"
            }
        ],
        "suggest": {
            "entity": {
                "service_url": "http://localhost:5000",
                "service_path": "/suggest/entity"
            },
            "type": {
                "service_url": "http://localhost:5000",
                "service_path": "/suggest/type"
            },
            "property": {
                "service_url": "http://localhost:5000",
                "service_path": "/suggest/property"
            }
        }
    }
    
    # Search configuration
    FUZZY_SEARCH_THRESHOLD = 40
    HIGH_MATCH_THRESHOLD = 80
    MAX_RESULTS_LIMIT = 100
    DEFAULT_SEARCH_LIMIT = 10
    
    # Preview templates
    TEMPLATE_FOLDER = 'templates'