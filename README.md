# NYC Taxi Data Explorer 

A full-stack data analytics application for exploring NYC taxi trip patterns, built with Python, Flask, and vanilla JavaScript.

## Team

- Chibueze Onugha
- Michelle Anyika
- Emmanuel Atigbi

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Data Setup](#data-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Custom Algorithms](#custom-algorithms)
- [Troubleshooting](#troubleshooting)

---

## Overview

This application processes and analyzes 7.6 million NYC taxi trip records to reveal urban mobility patterns. It features:
- Custom-built algorithms for Top-K zone analysis and anomaly detection (no built-in libraries)
- Automated ETL pipeline for data cleaning and feature engineering
- RESTful API with 15+ endpoints
- Interactive dashboard with charts and maps

**Assignment Compliance**: This project includes manually implemented algorithms (heap-based Top-K, manual statistical calculations) as required.

---

## Features

### Data Processing
-  Handles 7.6M+ trip records
-  Automated data cleaning (duplicates, outliers, missing values)
-  Feature engineering (speed, duration, time categories)
-  Comprehensive data validation with logging

### Analytics (Custom Algorithms)
-  **Top-K Zones**: Manual min-heap implementation (O(n log k))
-  **Anomaly Detection**: Manual mean/std calculation, no numpy
-  Borough comparison
-  Hourly demand patterns
-  Speed analysis by time of day

### API
-  15+ REST endpoints
-  Pagination and filtering
-  CORS-enabled for frontend
-  JSON responses

### Dashboard
-  Real-time statistics
-  Interactive charts(barChart.js, lineChart.js...)
-  Zone maps (zoneMap.js)
-  Responsive design

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend** | Python | 3.8+ |
| **Framework** | Flask | 2.3.2 |
| **Database** | SQLite | 3.x |
| **Data Processing** | Pandas | 2.0.3 |
| **Frontend** | Vanilla JavaScript | ES6+ |
| **Charts** | barChart.js | 3.x |
| **Maps** | zoneMap.js | 1.9.x |

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning)
- **10GB free disk space** (for data files)
- **Web browser** (Chrome, Firefox, or Edge)

**Check your Python version:**
```bash
python --version
# Should show Python 3.8.0 or higher
```

---

## Installation

### Step 1: Clone or Download the Repository

```bash
# Option A: Clone with Git
git clone https://github.com/Nnamdi004/Urban_mobility_data_explorer.git
cd Urban_mobility_data_explorer

# Option B: Download ZIP and extract
# Then navigate to the folder
cd Urban_mobility_data_explorer
```

### Step 2: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Required packages:**
- pandas (data processing)
- flask (web framework)
- flask-cors (cross-origin requests)
- python-dotenv (environment variables)
- pyarrow (parquet file reading)

**Verify installation:**
```bash
pip list
# Should show pandas, flask, etc.
```

### Step 4: Configure Environment

Create a `.env` file in the project root:

**Windows:**
```cmd
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

The `.env` file should contain:
```env
# Database
DB_PATH=database/nyc_taxi.db
DB_TYPE=sqlite

# Data directories
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed

# Data files
PARQUET_FILE=yellow_tripdata.parquet
ZONE_LOOKUP_FILE=taxi_zone_lookup.csv
ZONE_GEOJSON_FILE=taxi_zones.geojson

# Backend
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
```

---

## Data Setup

### Step 1: Download Required Data Files

You need three files from the NYC Taxi & Limousine Commission:

1. **Trip Data** (yellow_tripdata.parquet)
   - Download from: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
   - Select any month of Yellow Taxi Trip Records
   - File format: Parquet
   - Size: ~500MB - 1GB per month

2. **Zone Lookup** (taxi_zone_lookup.csv)
   - Download from: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
   - Contains zone names and boroughs

3. **Zone Boundaries** (taxi_zones.geojson)
   - Download from: https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc
   - Export as GeoJSON

### Step 2: Place Files in data/raw/

```
data/raw/
├── yellow_tripdata.parquet
├── taxi_zone_lookup.csv
└── taxi_zones.geojson
```

**Verify files exist:**
```bash
# Windows
dir data\raw

# Mac/Linux
ls -lh data/raw/
```

### Step 3: Run Data Pipeline

The pipeline will clean, process, and validate the data:

```bash
# Navigate to pipeline folder
cd pipeline

# Run the complete pipeline
python run_pipeline.py

# OR run with a sample (for testing - processes only 10,000 records)
python run_pipeline.py --sample 10000
```

**Expected output:**
```
========================================================
NYC TAXI DATA PIPELINE
========================================================
Started: 2026-02-18 14:30:00
========================================================

[STEP 1/5] Loading data...
Loading trip data from data/raw/yellow_tripdata.parquet...
Loaded 7,667,792 trips

[STEP 2/5] Cleaning data...
Original records: 7,667,792
...
Retention rate: 94.3%

[STEP 3/5] Engineering features...
  - Calculating trip duration...
  - Calculating average speed...
  - Extracting temporal features...

[STEP 4/5] Validating data...
✓ All validation checks passed

[STEP 5/5] Saving processed data...
Saved to: data/processed/cleaned_trips.parquet

========================================================
PIPELINE COMPLETE
========================================================
Final record count: 7,232,145
```

This creates `data/processed/cleaned_trips.parquet` with cleaned data.

### Step 4: Load Data into Database

```bash
# Navigate to database folder
cd ../database

# Run the seed script
python seed.py
```

**Expected output:**
```
Loading processed data...
Loaded 7,232,145 trips

Creating database...
✓ Database created: database/nyc_taxi.db

Inserting zones...
✓ Inserted 265 zones

Inserting trips (this may take 5-10 minutes)...
Progress: [████████████████████] 100%
✓ Inserted 7,232,145 trips

Creating indexes...
✓ Indexes created

Database setup complete!
Total size: 2.3 GB
```

This creates `database/nyc_taxi.db` (SQLite database file).

---

## Running the Application

### Start the Backend API

```bash
# Navigate to backend folder (from project root)
cd backend

# Start Flask server
python app.py
```

**Expected output:**
```
Starting API server on port 5000...
Debug mode: True
API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Test the API:**

Open browser and visit:
- http://localhost:5000 (Should show "NYC Taxi Data Explorer API")
- http://localhost:5000/api/stats (Should return JSON with statistics)

Or use curl:
```bash
curl http://localhost:5000/api/stats
```

**Keep this terminal open** - the backend must run while using the dashboard.

### Start the Frontend Dashboard

**Option 1: Simple HTTP Server (Recommended)**

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend folder
cd frontend

# Python 3
python -m http.server 8000

# Or Python 2
python -m SimpleHTTPServer 8000
```

Then open: http://localhost:8000

**Option 2: Direct File**

Simply open `frontend/index.html` in your browser by double-clicking it.

**Note**: If opening directly, you might encounter CORS issues. Use Option 1 instead.

### Access the Dashboard

Open your browser and go to:
```
http://localhost:8000
```

You should see:
- Statistics cards (total trips, avg fare, etc.)
- Hourly demand chart
- Borough comparison chart
- Top zones table
- Interactive map

---

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Statistics

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/stats` | GET | Overall statistics | `GET /api/stats` |
| `/stats/hourly` | GET | Trips by hour | `GET /api/stats/hourly` |
| `/stats/borough` | GET | Stats by borough | `GET /api/stats/borough` |

**Example Response:**
```json
{
  "total_trips": 7232145,
  "avg_fare": 16.32,
  "avg_distance": 3.45,
  "avg_duration": 15.7,
  "total_revenue": 118045678.50
}
```

#### Zones

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/zones` | GET | All zones | - |
| `/zones/<id>` | GET | Zone details | `id`: zone ID |
| `/zones/top-pickups` | GET | Top pickup zones | `limit`: number (default 10) |
| `/zones/top-dropoffs` | GET | Top dropoff zones | `limit`: number (default 10) |

#### Trips

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/trips` | GET | Get trips | `page`, `per_page`, `start_date`, `end_date`, `min_fare`, `max_fare` |
| `/trips/<id>` | GET | Single trip | `id`: trip ID |

**Example:**
```
GET /api/trips?page=1&per_page=50&min_fare=10&max_fare=50
```

#### Analytics (Custom Algorithms)

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/analytics/top-zones` | GET | Top K zones (custom algo) | `k`: number (default 10), `metric`: pickups/dropoffs/revenue |
| `/analytics/top-routes` | GET | Popular routes | `k`: number (default 10) |
| `/analytics/anomalies` | GET | Detect anomalies | `sample`: sample size (default 10000) |
| `/analytics/speed-patterns` | GET | Speed by hour | - |
| `/analytics/revenue-hourly` | GET | Revenue by hour | - |
| `/analytics/insights` | GET | Combined insights | - |

**Example:**
```
GET /api/analytics/top-zones?k=5&metric=revenue
```

**Response:**
```json
[
  {
    "location_id": 237,
    "zone": "Upper East Side South",
    "borough": "Manhattan",
    "value": 12456789.50,
    "metric": "revenue"
  },
  ...
]
```

### Error Responses

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `404` - Not found
- `500` - Server error

**Error format:**
```json
{
  "error": "Descriptive error message"
}
```

---

## Project Structure

```
Urban_mobility_data_explorer/
│
├── README.md                    # This file
├── ARCHITECTURE.md             # Technical architecture documentation
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (create from .env.example)
├── .gitignore                  # Git ignore rules
│
├── data/
│   ├── raw/                    # Raw data files (download these)
│   │   ├── yellow_tripdata.parquet
│   │   ├── taxi_zone_lookup.csv
│   │   └── taxi_zones.geojson
│   ├── processed/              # Processed data (created by pipeline)
│   │   └── cleaned_trips.parquet
│   └── logs/                   # Processing logs
│       └── cleaning_log.txt
│
├── pipeline/                   # ETL Data Pipeline
│   ├── __init__.py
│   ├── load_data.py           # Load raw files
│   ├── clean_data.py          # Data cleaning
│   ├── feature_engineering.py # Create derived features
│   ├── validate_data.py       # Data validation
│   └── run_pipeline.py        # Main pipeline runner
│
├── database/
│   ├── schema.sql             # Database schema definition
│   ├── seed.py                # Load data into SQLite
│   └── nyc_taxi.db           # SQLite database (created by seed.py)
│
├── backend/                   # Flask REST API
│   ├── __init__.py
│   ├── app.py                 # Main Flask application
│   │
│   ├── algorithms/            # Custom implementations (assignment requirement!)
│   │   ├── __init__.py
│   │   ├── top_k_zones.py    # Manual Top-K algorithm (no heapq)
│   │   └── anomaly_detector.py # Manual anomaly detection (no numpy)
│   │
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── trip.py           # Trip data model
│   │   └── zone.py           # Zone data model
│   │
│   └── services/              # Business logic
│       ├── __init__.py
│       ├── query_service.py  # Common queries
│       └── analytics_service.py # Analytics using custom algorithms
│
└── frontend/                  # Web Dashboard
    ├── index.html             # Main dashboard page
    ├── css/
    │   └── styles.css
    ├── dashboard/
    ├── auth/
    ├── js/
    │   ├── main.js           # Main application logic
    │   ├── api.js            # API client
    │   └── charts.js         # Chart configurations
    └── assets/
        └── images/
```

---

## Custom Algorithms

This project includes manually implemented algorithms as required by the assignment:

### 1. Top-K Zones Algorithm (`backend/algorithms/top_k_zones.py`)

**What it does:** Finds the K busiest pickup/dropoff zones

**Implementation:**
- Manual min-heap construction
- Manual quicksort for final ordering
- No use of built-in `sort()`, `heapq`, or similar functions

**Time Complexity:** O(n log k) where n = number of zones, k = top K to find

**Usage:**
```python
from backend.algorithms.top_k_zones import TopKZones

finder = TopKZones(k=10)
zone_counts = {1: 1000, 2: 500, 3: 2000, ...}
top_zones = finder.find_top_k_pickups(zone_counts)
# Returns: [(3, 2000), (1, 1000), (2, 500), ...]
```

### 2. Anomaly Detector (`backend/algorithms/anomaly_detector.py`)

**What it does:** Detects suspicious trips based on fare, speed, and distance

**Implementation:**
- Manual mean calculation (no numpy)
- Manual standard deviation calculation
- Manual square root using Newton's method
- Z-score based anomaly detection

**Space Complexity:** O(n) where n = number of trips analyzed

**Usage:**
```python
from backend.algorithms.anomaly_detector import AnomalyDetector

detector = AnomalyDetector(z_threshold=3.0)
trips = [...]  # List of trip dictionaries
anomalies = detector.detect_all_anomalies(trips)
# Returns: {'fare_anomalies': [...], 'speed_anomalies': [...], ...}
```

**See PDF Report for detailed algorithm explanations and pseudocode.**

---

## Troubleshooting

### Problem: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "No such file or directory: database/nyc_taxi.db"

**Solution:**
```bash
# You need to run the database seed script first
cd database
python seed.py
```

### Problem: "Missing data files"

**Solution:**
```bash
# Download the three required files:
# 1. yellow_tripdata.parquet
# 2. taxi_zone_lookup.csv
# 3. taxi_zones.geojson

# Place them in data/raw/ folder

# Verify they exist:
ls data/raw/  # Mac/Linux
dir data\raw  # Windows
```

### Problem: Backend returns "CORS error"

**Solution:**
```bash
# Make sure Flask-CORS is installed
pip install flask-cors

# Verify it's in your requirements.txt
# Restart the backend server
```

### Problem: Frontend shows "Cannot connect to API"

**Solution:**
1. Make sure backend is running (`python backend/app.py`)
2. Check backend is on port 5000: http://localhost:5000
3. Check browser console for errors (F12)
4. Verify API URL in `frontend/js/api.js` is correct

### Problem: "Permission denied" when activating venv

**Windows PowerShell Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use Command Prompt instead of PowerShell
cmd
venv\Scripts\activate.bat
```

### Problem: Pipeline runs out of memory

**Solution:**
```bash
# Process a sample first to test
python run_pipeline.py --sample 100000

# For full dataset, close other applications
# Consider increasing Python memory limit or processing in chunks
```

### Problem: Database file is huge (>5GB)

**Solution:**
```bash
# This is normal for 7M+ records
# To reduce size, you can:

# 1. Process fewer records
python run_pipeline.py --sample 1000000

# 2. Or vacuum the database
sqlite3 database/nyc_taxi.db "VACUUM;"
```

---

## Development Tips

### Running with Sample Data

For faster testing during development:

```bash
# Process only 10,000 records
cd pipeline
python run_pipeline.py --sample 10000

cd ../database
python seed.py
```

### Checking Database Content

```bash
# Open SQLite CLI
sqlite3 database/nyc_taxi.db

# Run queries
SELECT COUNT(*) FROM trips;
SELECT * FROM zones LIMIT 5;
SELECT * FROM trips LIMIT 5;

# Exit
.quit
```

### Testing API Endpoints

Using curl:
```bash
# Get stats
curl http://localhost:5000/api/stats

# Get top zones
curl "http://localhost:5000/api/analytics/top-zones?k=5"

# Get trips with filters
curl "http://localhost:5000/api/trips?page=1&per_page=10&min_fare=10"
```

### Restarting Fresh

```bash
# Delete database
rm database/nyc_taxi.db  # Mac/Linux
del database\nyc_taxi.db  # Windows

# Delete processed data
rm data/processed/*  # Mac/Linux
del data\processed\*  # Windows

# Run pipeline again
cd pipeline
python run_pipeline.py
```

---

## Performance Notes

- **Pipeline**: Processes ~7M records in 5-15 minutes (depends on hardware)
- **Database loading**: 5-10 minutes for 7M records
- **API response time**: < 500ms for most queries
- **Database size**: ~2-3 GB for 7M trips

**Hardware recommendations:**
- 8GB+ RAM
- 10GB+ free disk space
- Modern CPU (i5/Ryzen 5 or better)

---

## Contributing

This is an academic project. If you find issues:

1. Check the troubleshooting section above
2. Review your .env configuration
3. Verify all data files are present
4. Check Python version (3.8+)

---

## License

This project is for educational purposes. Data provided by NYC Taxi & Limousine Commission.

---

## Acknowledgments

- NYC Taxi & Limousine Commission for open data
- Flask framework documentation
- Chart.js and Leaflet.js communities

---

## Video Walkthrough

https://youtu.be/TyAu2EPfhps

## Team Task sheet
https://docs.google.com/spreadsheets/d/1SwW3GJu0nL8595CqCWU290puL2PpBTYC2HN8W2z8CUM/edit?gid=0#gid=0 

## PDF Technical Report

Refer to the docs repo

---
