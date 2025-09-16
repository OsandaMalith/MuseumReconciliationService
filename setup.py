#!/usr/bin/env python3
"""
Setup script for Museum Cultural Heritage Reconciliation Service
"""

import os
import sys
import subprocess

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'data',
        'static/css',
        'templates',
        'config',
        'services',
        'routes',
        'utils'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def create_init_files():
    """Create __init__.py files for Python packages"""
    packages = ['config', 'services', 'routes', 'utils']
    
    for package in packages:
        init_file = os.path.join(package, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f"# {package.title()} package initialization\n")
            print(f"Created: {init_file}")

def install_requirements():
    """Install Python requirements"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Successfully installed requirements")
    except subprocess.CalledProcessError:
        print("Error installing requirements. Please run 'pip install -r requirements.txt' manually")

def create_sample_data():
    """Create sample CSV files if they don't exist"""
    sample_files = {
        'data/museums.csv': '''Museum ID,Museum Name,Legal Name,Museum Type,City (Administrative Location),State (Administrative Location)
MUS_000001,Sample Art Museum,Sample Art Museum Inc,Art Museum,New York,NY
MUS_000002,History Center,Local History Center,History Museum,Boston,MA''',
        
        'data/artists.csv': '''id,name,nationality,birth_year,death_year,gender
ART_000001,Leonardo da Vinci,Italian,1452,1519,Male
ART_000002,Frida Kahlo,Mexican,1907,1954,Female''',
        
        'data/artworks.csv': '''ObjectID,Title,Artist,Medium,Classification,Department
OBJ_000001,Mona Lisa,Leonardo da Vinci,Oil on canvas,Painting,European Paintings
OBJ_000002,The Two Fridas,Frida Kahlo,Oil on canvas,Painting,Modern Art'''
    }
    
    for filename, content in sample_files.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"Created sample file: {filename}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Museum Cultural Heritage Reconciliation Service Setup")
    print("=" * 60)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Creating package initialization files...")
    create_init_files()
    
    print("\n3. Installing Python requirements...")
    install_requirements()
    
    print("\n4. Creating sample data files...")
    create_sample_data()
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Replace sample CSV files in data/ directory with your actual data")
    print("2. Run the application with: python app.py")
    print("3. Access the service at: http://localhost:5000/")
    print("=" * 60)

if __name__ == '__main__':
    main()