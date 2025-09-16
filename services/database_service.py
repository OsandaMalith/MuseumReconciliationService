import sqlite3
import pandas as pd
from config.settings import Config
from utils.text_utils import clean_float_value, clean_numeric_value

def load_csv_data():
    """Load data from CSV files"""
    data = {}
    
    # Load museums CSV
    try:
        museums_df = pd.read_csv(Config.CSV_FILES['museums'])
        data['museums'] = museums_df.fillna('').to_dict('records')
        print(f"Loaded {len(data['museums'])} museums from CSV")
    except FileNotFoundError:
        print(f"Warning: {Config.CSV_FILES['museums']} not found. Using empty dataset.")
        data['museums'] = []
    except Exception as e:
        print(f"Error loading museums CSV: {e}")
        data['museums'] = []
    
    # Load artists CSV
    try:
        artists_df = pd.read_csv(Config.CSV_FILES['artists'])
        data['artists'] = artists_df.fillna('').to_dict('records')
        print(f"Loaded {len(data['artists'])} artists from CSV")
    except FileNotFoundError:
        print(f"Warning: {Config.CSV_FILES['artists']} not found. Using empty dataset.")
        data['artists'] = []
    except Exception as e:
        print(f"Error loading artists CSV: {e}")
        data['artists'] = []
    
    # Load artifacts CSV
    try:
        artifacts_df = pd.read_csv(Config.CSV_FILES['artifacts'])
        data['artifacts'] = artifacts_df.fillna('').to_dict('records')
        print(f"Loaded {len(data['artifacts'])} artifacts from CSV")
    except FileNotFoundError:
        print(f"Warning: {Config.CSV_FILES['artifacts']} not found. Using empty dataset.")
        data['artifacts'] = []
    except Exception as e:
        print(f"Error loading artifacts CSV: {e}")
        data['artifacts'] = []
    
    return data

def init_db():
    """Initialize SQLite database with museum and cultural heritage data from CSV files"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    c = conn.cursor()
    
    # Drop existing tables for clean initialization
    c.execute('DROP TABLE IF EXISTS artifacts')
    c.execute('DROP TABLE IF EXISTS museums')
    c.execute('DROP TABLE IF EXISTS artists')
    c.execute('DROP TABLE IF EXISTS artifact_types')
    
    # Create museums table with fields from CSV
    c.execute('''CREATE TABLE museums
                 (id TEXT PRIMARY KEY, 
                  museum_name TEXT,
                  legal_name TEXT,
                  alternate_name TEXT,
                  museum_type TEXT,
                  street_address_admin TEXT,
                  city_admin TEXT,
                  state_admin TEXT,
                  zip_admin TEXT,
                  phone TEXT,
                  latitude REAL,
                  longitude REAL,
                  county_code TEXT,
                  region_code TEXT,
                  revenue INTEGER,
                  type TEXT DEFAULT 'museum')''')
    
    # Create artists table with fields from CSV
    c.execute('''CREATE TABLE artists
                 (id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  artist_bio TEXT,
                  nationality TEXT,
                  gender TEXT,
                  birth_year INTEGER,
                  death_year INTEGER,
                  wiki_qid TEXT,
                  ulan TEXT,
                  type TEXT DEFAULT 'person')''')
    
    # Create artifacts table with fields from CSV
    c.execute('''CREATE TABLE artifacts
                 (id TEXT PRIMARY KEY,
                  title TEXT NOT NULL,
                  artist TEXT,
                  constituent_id TEXT,
                  artist_bio TEXT,
                  nationality TEXT,
                  begin_date INTEGER,
                  end_date INTEGER,
                  gender TEXT,
                  date TEXT,
                  medium TEXT,
                  dimensions TEXT,
                  credit_line TEXT,
                  accession_number TEXT,
                  classification TEXT,
                  department TEXT,
                  date_acquired TEXT,
                  object_id TEXT,
                  url TEXT,
                  image_url TEXT,
                  on_view TEXT,
                  height_cm REAL,
                  width_cm REAL,
                  length_cm REAL,
                  weight_kg REAL,
                  type TEXT DEFAULT 'artifact')''')
    
    # Create artifact types lookup table
    c.execute('''CREATE TABLE artifact_types
                 (id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  parent_type TEXT)''')
    
    # Load data from CSV files
    csv_data = load_csv_data()
    
    # Insert museums data
    museums_data = []
    for i, museum in enumerate(csv_data['museums']):
        # museum_id = str(museum.get('Museum ID', f'MUS_{i+1:06d}'))
        museum_id = f'MUSEUM_{len(museums_data)+1:06d}'
        museums_data.append((
            museum_id,
            museum.get('Museum Name', ''),
            museum.get('Legal Name', ''),
            museum.get('Alternate Name', ''),
            museum.get('Museum Type', ''),
            museum.get('Street Address (Administrative Location)', ''),
            museum.get('City (Administrative Location)', ''),
            museum.get('State (Administrative Location)', ''),
            museum.get('Zip Code (Administrative Location)', ''),
            museum.get('Phone Number', ''),
            clean_float_value(museum.get('Latitude')),
            clean_float_value(museum.get('Longitude')),
            museum.get('County Code (FIPS)', ''),
            museum.get('Region Code (AAM)', ''),
            clean_numeric_value(museum.get('Revenue')) or 0,
            'museum'
        ))
    
    if museums_data:
        c.executemany('''INSERT INTO museums VALUES 
                         (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', museums_data)
        print(f"Inserted {len(museums_data)} museums into database")
    
    # Insert artists data
    artists_data = []
    for artist in csv_data['artists']:
        # artist_id = str(artist.get('id', f'ART_{len(artists_data)+1:06d}'))
        artist_id = f'ARTIST_{len(artists_data)+1:06d}'
        artists_data.append((
            artist_id,
            artist.get('name', ''),
            artist.get('artist_bio', ''),
            artist.get('nationality', ''),
            artist.get('gender', ''),
            clean_numeric_value(artist.get('birth_year')),
            clean_numeric_value(artist.get('death_year')),
            artist.get('wiki_qid', ''),
            artist.get('ulan', ''),
            'person'
        ))
    
    if artists_data:
        c.executemany('''INSERT INTO artists VALUES 
                         (?,?,?,?,?,?,?,?,?,?)''', artists_data)
        print(f"Inserted {len(artists_data)} artists into database")
    
    # Insert artifacts data
    artifacts_data = []
    for i, artifact in enumerate(csv_data['artifacts']):
        # artifact_id = str(artifact.get('ObjectID', f'OBJ_{i+1:06d}'))
        artifact_id = f'ARTIFACT_{len(artifacts_data)+1:06d}'
        artifacts_data.append((
            artifact_id,
            artifact.get('Title', ''),
            artifact.get('Artist', ''),
            artifact.get('ConstituentID', ''),
            artifact.get('ArtistBio', ''),
            artifact.get('Nationality', ''),
            clean_numeric_value(artifact.get('BeginDate')),
            clean_numeric_value(artifact.get('EndDate')),
            artifact.get('Gender', ''),
            artifact.get('Date', ''),
            artifact.get('Medium', ''),
            artifact.get('Dimensions', ''),
            artifact.get('CreditLine', ''),
            artifact.get('AccessionNumber', ''),
            artifact.get('Classification', ''),
            artifact.get('Department', ''),
            artifact.get('DateAcquired', ''),
            str(artifact.get('ObjectID', '')),
            artifact.get('URL', ''),
            artifact.get('ImageURL', ''),
            artifact.get('OnView', ''),
            clean_float_value(artifact.get('Height (cm)')),
            clean_float_value(artifact.get('Width (cm)')),
            clean_float_value(artifact.get('Length (cm)')),
            clean_float_value(artifact.get('Weight (kg)')),
            'artifact'
        ))
    
    if artifacts_data:
        c.executemany('''INSERT INTO artifacts VALUES 
                         (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', artifacts_data)
        print(f"Inserted {len(artifacts_data)} artifacts into database")
    
    # Insert default artifact types
    artifact_types_data = [
        ("painting", "Painting", "artwork"),
        ("sculpture", "Sculpture", "artwork"),
        ("artifact", "Artifact", None),
        ("textile", "Textile", "artifact"),
        ("pottery", "Pottery", "artifact"),
        ("jewelry", "Jewelry", "artifact"),
        ("manuscript", "Manuscript", "document"),
        ("print", "Print", "artwork"),
        ("photograph", "Photograph", "artwork"),
        ("decorative", "Decorative Arts", "artifact"),
        ("architecture", "Architecture", "artwork"),
        ("drawing", "Drawing", "artwork"),
        ("design", "Design", "artwork")
    ]
    
    c.executemany('INSERT INTO artifact_types VALUES (?,?,?)', artifact_types_data)
    
    # Create indexes for efficient searching
    c.execute('CREATE INDEX IF NOT EXISTS idx_museums_name ON museums(museum_name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_artists_name ON artists(name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_artifacts_title ON artifacts(title)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_artifacts_artist ON artifacts(artist)')
    
    conn.commit()
    conn.close()

def get_database_stats():
    """Get database statistics"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM museums')
    museum_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM artists')
    artist_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM artifacts')
    artifact_count = c.fetchone()[0]
    
    conn.close()
    
    return {
        "museums": museum_count,
        "artists": artist_count,
        "artifacts": artifact_count,
        "total_entities": museum_count + artist_count + artifact_count
    }