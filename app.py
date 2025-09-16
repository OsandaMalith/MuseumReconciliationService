from flask import Flask
from flask_cors import CORS
from config.settings import Config
from services.database_service import init_db
from routes.main_routes import main_bp
from routes.api_routes import api_bp
from routes.preview_routes import preview_bp
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for OpenRefine
    
    # Load configuration
    app.config.from_object(Config)
    
    # Ensure `data` directory exists
    os.makedirs("data", exist_ok=True)

    # Initialize database only if it does not exist
    db_path = os.path.join("data", "museum_reconciliation.db")
    if not os.path.exists(db_path):
        print(f"Database not found. Creating new DB at {db_path}...")
        init_db()
    else:
        print(f"Using existing database at {db_path}")
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(preview_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 80)
    print("Museum Cultural Heritage Reconciliation Service (CSV-Powered)")
    print("=" * 80)
    print("Loading data from CSV files:")
    print(f"- Museums: {Config.CSV_FILES['museums']}")
    print(f"- Artists: {Config.CSV_FILES['artists']}")  
    print(f"- Artifacts: {Config.CSV_FILES['artifacts']}")
    print("-" * 80)
    print("Service URL: http://localhost:5000/")
    print("Statistics: http://localhost:5000/stats")
    print("\nTo use with OpenRefine:")
    print("1. Start OpenRefine and load your cultural heritage data")
    print("2. Select column > Reconcile > Start reconciling...")
    print("3. Add Standard Service: http://localhost:5000/")
    print("4. Select appropriate entity type:")
    print("   - Cultural Artifact (paintings, sculptures, etc.)")
    print("   - Museum/Institution")
    print("   - Artist/Creator")
    print("\nFeatures:")
    print("- Fuzzy string matching for flexible name matching")
    print("- Enhanced preview pages with images and detailed information")
    print("- Support for empty CSV fields")
    print("- Auto-suggestion for entity completion")
    print("- External links to Wikidata and Getty ULAN (when available)")
    print("=" * 80)
    
    app.run(debug=Config.DEBUG, port=Config.PORT)