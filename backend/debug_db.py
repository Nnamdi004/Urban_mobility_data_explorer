import os
import sys
import sqlite3
from dotenv import load_dotenv

print("="*50)
print("DATABASE CONNECTION DEBUG")
print("="*50)

# Load environment
load_dotenv()

print(f"\n1. Current working directory: {os.getcwd()}")
print(f"2. Script location: {os.path.dirname(os.path.abspath(__file__))}")

# Check .env file
env_path = os.path.join(os.getcwd(), '.env')
print(f"\n3. Looking for .env at: {env_path}")
print(f"   .env exists: {os.path.exists(env_path)}")

# Get DB_PATH from environment
db_path = os.getenv('DB_PATH', 'database/nyc_taxi.db')
print(f"\n4. DB_PATH from .env: {db_path}")

# Check if database file exists
print(f"\n5. Checking database file:")
print(f"   Path: {db_path}")
print(f"   Exists: {os.path.exists(db_path)}")
print(f"   Absolute path: {os.path.abspath(db_path)}")

# Try different paths
possible_paths = [
    db_path,
    '../database/nyc_taxi.db',
    'c:/Users/USER/IdeaProjects/NewYorktax/Urban_mobility_data_explorer/database/nyc_taxi.db',
    os.path.join(os.path.dirname(os.getcwd()), 'database', 'nyc_taxi.db')
]

print(f"\n6. Testing possible paths:")
for path in possible_paths:
    exists = os.path.exists(path)
    symbol = 'OK' if exists else 'NO'
    print(f"   [{symbol}] {path}")
    if exists:
        print(f"        Size: {os.path.getsize(path) / (1024**3):.2f} GB")

# Try to connect
print(f"\n7. Attempting connection with: {db_path}")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM trips")
    count = cursor.fetchone()[0]
    print(f"   [SUCCESS] Found {count:,} trips")
    conn.close()
except Exception as e:
    print(f"   [FAILED] {e}")

print("\n" + "="*50)
