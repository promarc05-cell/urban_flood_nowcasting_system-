# geo.py

"""
Geographic utilities for the Urban Flood Nowcasting System.

This module converts a latitude/longitude study area into
a simple spatial grid that can be used by the existing
rainfall, runoff, terrain and flood modules.
"""

from config import STUDY_AREA, GRID_ROWS, GRID_COLS


# ============================================================
# STUDY AREA
# ============================================================

def get_study_area():
    """
    Return the configured geographic study area.
    """

    return STUDY_AREA.copy()


# ============================================================
# VALIDATION
# ============================================================

def validate_study_area(study_area=None):
    """
    Validate latitude/longitude boundaries.
    """

    if study_area is None:
        study_area = STUDY_AREA

    required_keys = [
        "lat_min",
        "lat_max",
        "lon_min",
        "lon_max"
    ]

    for key in required_keys:
        if key not in study_area:
            raise ValueError(f"Missing study area parameter: {key}")

    if study_area["lat_min"] >= study_area["lat_max"]:
        raise ValueError("lat_min must be smaller than lat_max")

    if study_area["lon_min"] >= study_area["lon_max"]:
        raise ValueError("lon_min must be smaller than lon_max")

    if not (-90 <= study_area["lat_min"] <= 90):
        raise ValueError("Invalid latitude")

    if not (-90 <= study_area["lat_max"] <= 90):
        raise ValueError("Invalid latitude")

    if not (-180 <= study_area["lon_min"] <= 180):
        raise ValueError("Invalid longitude")

    if not (-180 <= study_area["lon_max"] <= 180):
        raise ValueError("Invalid longitude")

    return True


# ============================================================
# GRID GENERATION
# ============================================================

def create_geo_grid(
    rows=GRID_ROWS,
    cols=GRID_COLS,
    study_area=None
):
    """
    Create a geographic grid.

    Each cell contains:

        row
        col
        lat_min
        lat_max
        lon_min
        lon_max
        latitude
        longitude

    latitude/longitude represent the cell center.
    """

    if study_area is None:
        study_area = STUDY_AREA

    validate_study_area(study_area)

    if rows <= 0 or cols <= 0:
        raise ValueError("Grid rows and columns must be positive")

    lat_min = study_area["lat_min"]
    lat_max = study_area["lat_max"]

    lon_min = study_area["lon_min"]
    lon_max = study_area["lon_max"]

    lat_step = (lat_max - lat_min) / rows
    lon_step = (lon_max - lon_min) / cols

    grid = []

    for row in range(rows):

        grid_row = []

        cell_lat_min = lat_min + row * lat_step
        cell_lat_max = lat_min + (row + 1) * lat_step

        for col in range(cols):

            cell_lon_min = lon_min + col * lon_step
            cell_lon_max = lon_min + (col + 1) * lon_step

            center_lat = (
                cell_lat_min + cell_lat_max
            ) / 2

            center_lon = (
                cell_lon_min + cell_lon_max
            ) / 2

            cell = {
                "row": row,
                "col": col,

                "lat_min": cell_lat_min,
                "lat_max": cell_lat_max,

                "lon_min": cell_lon_min,
                "lon_max": cell_lon_max,

                "latitude": center_lat,
                "longitude": center_lon
            }

            grid_row.append(cell)

        grid.append(grid_row)

    return grid


# ============================================================
# PRINT GRID
# ============================================================

def print_geo_grid(grid):
    """
    Print grid cell coordinates.
    """

    print("\n======================================")
    print("       GEOGRAPHIC GRID")
    print("======================================")

    for row in grid:

        for cell in row:

            print(
                f"Cell ({cell['row']},{cell['col']}) "
                f"→ "
                f"{cell['latitude']:.6f}, "
                f"{cell['longitude']:.6f}"
            )

        print()


# ============================================================
# CELL LOOKUP
# ============================================================

def get_cell_center(grid, row, col):
    """
    Return the latitude/longitude of a grid cell.
    """

    if row < 0 or row >= len(grid):
        raise IndexError("Invalid grid row")

    if col < 0 or col >= len(grid[0]):
        raise IndexError("Invalid grid column")

    cell = grid[row][col]

    return (
        cell["latitude"],
        cell["longitude"]
    )


# ============================================================
# FIND CELL FROM COORDINATES
# ============================================================

def get_cell_from_coordinates(
    latitude,
    longitude,
    study_area=None,
    rows=GRID_ROWS,
    cols=GRID_COLS
):
    """
    Convert latitude/longitude into a grid cell.

    Returns:

        (row, col)

    or None if the coordinate lies outside
    the study area.
    """

    if study_area is None:
        study_area = STUDY_AREA

    validate_study_area(study_area)

    if not (
        study_area["lat_min"]
        <= latitude
        <= study_area["lat_max"]
    ):
        return None

    if not (
        study_area["lon_min"]
        <= longitude
        <= study_area["lon_max"]
    ):
        return None

    lat_step = (
        study_area["lat_max"]
        - study_area["lat_min"]
    ) / rows

    lon_step = (
        study_area["lon_max"]
        - study_area["lon_min"]
    ) / cols

    row = int(
        (latitude - study_area["lat_min"])
        / lat_step
    )

    col = int(
        (longitude - study_area["lon_min"])
        / lon_step
    )

    # Boundary protection
    row = min(row, rows - 1)
    col = min(col, cols - 1)

    return row, col


# ============================================================
# SUMMARY
# ============================================================

def print_study_area():

    print("\n======================================")
    print("      KOLKATA STUDY AREA")
    print("======================================")

    print(
        f"Latitude : "
        f"{STUDY_AREA['lat_min']} → "
        f"{STUDY_AREA['lat_max']}"
    )

    print(
        f"Longitude: "
        f"{STUDY_AREA['lon_min']} → "
        f"{STUDY_AREA['lon_max']}"
    )

    print(
        f"Grid     : "
        f"{GRID_ROWS} × {GRID_COLS}"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print_study_area()

    grid = create_geo_grid()

    print_geo_grid(grid)

    test_lat = 22.565
    test_lon = 88.360

    cell = get_cell_from_coordinates(
        test_lat,
        test_lon
    )

    print("\nTest coordinate:")
    print(test_lat, test_lon)

    print("Grid cell:", cell)