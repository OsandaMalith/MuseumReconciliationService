from flask import Blueprint, render_template
from services.search_service import get_entity_by_id

preview_bp = Blueprint('preview', __name__, template_folder='../templates')

@preview_bp.route('/preview/<entity_id>')
def preview(entity_id):
    """Preview endpoint for entity details with enhanced information"""
    entity, entity_type = get_entity_by_id(entity_id)
    print(entity_type)
    
    if not entity:
        return "Entity not found", 404
    
    # Generate appropriate template based on entity type
    if entity_type == 'museum':
        return render_template('museum_preview.html', entity=entity)
    elif entity_type == 'artist':
        return render_template('artist_preview.html', entity=entity)
    else:  # artifact
        return render_template('artifact_preview.html', entity=entity)

@preview_bp.route('/view/<entity_id>')
def view(entity_id):
    """View endpoint - returns the same as preview"""
    return preview(entity_id)