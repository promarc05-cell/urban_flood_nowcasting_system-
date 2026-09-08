# config.py

"""
Configuration for the real-world Urban Flood Nowcasting study area.
"""

# ============================================================
# STUDY AREA — CENTRAL KOLKATA
# ============================================================

STUDY_AREA = {
    "name": "Central Kolkata Study Area",

    "lat_min": 22.5500,
    "lat_max": 22.5850,

    "lon_min": 88.3400,
    "lon_max": 88.3800
}


# ============================================================
# SPATIAL GRID
# ============================================================

# Model computational grid.
# The actual DEM has much higher resolution (~30 m).
# We aggregate the DEM into this 20 × 20 grid.

GRID_ROWS = 20
GRID_COLS = 20


# ============================================================
# FORECAST
# ============================================================

FORECAST_HOURS = 3


# ============================================================
# ROUTING
# ============================================================

ROUTE_START = None
ROUTE_DESTINATION = None


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = "data"

RAINFALL_DATA_DIR = f"{DATA_DIR}/rainfall"
ROAD_DATA_DIR = f"{DATA_DIR}/roads"


# ============================================================
# DEM FILE
# ============================================================

DEM_FILE = f"{DATA_DIR}/kolkata_dem.tif"