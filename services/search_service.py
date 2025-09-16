import sqlite3
from typing import Dict, List, Any, Optional
from fuzzywuzzy import fuzz
from config.settings import Config
from utils.text_utils import normalize_text

def search_entities(query: str, limit: int = 10, type_filter: Optional[str] = None, 
                   properties: Optional[Dict] = None) -> List[Dict]:
    """Search for entities across all tables with advanced matching"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    results = []
    normalized_query = normalize_text(query)
    
    # Define search configurations for each type
    search_configs = []
    
    if not type_filter or type_filter == 'museum':
        search_configs.append({
            'table': 'museums',
            'fields': ['museum_name', 'legal_name', 'alternate_name', 'museum_type', 'city_admin', 'state_admin'],
            'type': 'museum',
            'type_name': 'Museum/Institution'
        })
    
    if not type_filter or type_filter == 'person':
        search_configs.append({
            'table': 'artists',
            'fields': ['name', 'nationality', 'artist_bio'],
            'type': 'person',
            'type_name': 'Artist/Creator'
        })
    
    if not type_filter or type_filter == 'artifact':
        search_configs.append({
            'table': 'artifacts',
            'fields': ['title', 'artist', 'medium', 'classification', 'department'],
            'type': 'artifact',
            'type_name': 'Cultural Artifact'
        })
    
    # Search each configured table
    for config in search_configs:
        # First try exact matches
        exact_query = f"SELECT * FROM {config['table']} WHERE "
        exact_conditions = []
        for field in config['fields']:
            if field:
                exact_conditions.append(f"LOWER({field}) = ?")
        
        if exact_conditions:
            c.execute(exact_query + " OR ".join(exact_conditions), 
                     [query.lower()] * len(exact_conditions))
            
            for row in c.fetchall():
                result = create_result_from_row(row, config, 100, True)
                if result:
                    results.append(result)
    
    # If we need more results, do fuzzy matching
    if len(results) < limit:
        remaining_limit = limit - len(results)
        fuzzy_results = []
        
        for config in search_configs:
            c.execute(f"SELECT * FROM {config['table']}")
            all_rows = c.fetchall()
            
            for row in all_rows:
                # Skip if already in exact matches
                if any(r['id'] == row['id'] for r in results):
                    continue
                
                # Calculate fuzzy match scores for different fields
                field_scores = []
                
                for field in config['fields']:
                    if row[field]:
                        field_score = fuzz.ratio(normalized_query, normalize_text(row[field]))
                        field_scores.append(field_score)
                
                score = max(field_scores) if field_scores else 0
                
                if score > Config.FUZZY_SEARCH_THRESHOLD:
                    result = create_result_from_row(row, config, score, score > Config.HIGH_MATCH_THRESHOLD)
                    if result:
                        fuzzy_results.append(result)
        
        # Sort by score and add top results
        fuzzy_results.sort(key=lambda x: x['score'], reverse=True)
        results.extend(fuzzy_results[:remaining_limit])
    
    conn.close()
    return results

def create_result_from_row(row, config, score, is_match):
    """Create a result object from a database row"""
    try:
        if config['table'] == 'museums':
            name = row['museum_name'] or row['legal_name'] or 'Unnamed Museum'
            description_parts = []
            if row['city_admin']:
                description_parts.append(row['city_admin'])
            if row['state_admin']:
                description_parts.append(row['state_admin'])
            if row['museum_type']:
                description_parts.append(f"({row['museum_type']})")
            description = ", ".join(description_parts) if description_parts else "Museum"
        
        elif config['table'] == 'artists':
            name = row['name'] or 'Unknown Artist'
            description_parts = []
            if row['nationality']:
                description_parts.append(row['nationality'])
            if row['birth_year'] and row['death_year']:
                description_parts.append(f"({row['birth_year']}–{row['death_year']})")
            elif row['birth_year']:
                description_parts.append(f"(b. {row['birth_year']})")
            if row['artist_bio']:
                bio_parts = row['artist_bio'].split(',')
                if len(bio_parts) > 1:
                    description_parts.append(bio_parts[1].strip())
            description = ", ".join(description_parts) if description_parts else "Artist"
        
        elif config['table'] == 'artifacts':
            name = row['title'] or 'Untitled'
            description_parts = []
            if row['artist']:
                description_parts.append(f"by {row['artist']}")
            if row['date']:
                description_parts.append(row['date'])
            if row['medium']:
                description_parts.append(row['medium'])
            if row['department']:
                description_parts.append(f"({row['department']})")
            description = ", ".join(description_parts) if description_parts else "Artwork"
        
        else:
            return None
        
        return {
            "id": str(row['id']),
            "name": name,
            "type": [{"id": config['type'], "name": config['type_name']}],
            "score": score,
            "match": is_match,
            "description": description
        }
    except Exception as e:
        print(f"Error creating result: {e}")
        return None

def get_entity_by_id(entity_id: str):
    """Get entity by ID from any table"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Try to find entity in all tables
    entity = None
    entity_type = None
    
    # Check museums
    c.execute('SELECT * FROM museums WHERE id = ?', (entity_id,))
    result = c.fetchone()
    if result:
        entity = result
        entity_type = 'museum'
    
    # Check artists
    if not entity:
        c.execute('SELECT * FROM artists WHERE id = ?', (entity_id,))
        result = c.fetchone()
        if result:
            entity = result
            entity_type = 'artist'
    
    # Check artifacts
    if not entity:
        c.execute('SELECT * FROM artifacts WHERE id = ?', (entity_id,))
        result = c.fetchone()
        if result:
            entity = result
            entity_type = 'artifact'
    
    conn.close()
    return entity, entity_type