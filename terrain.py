import numpy as np

from dem import load_dem


# ============================================================
# LOAD REAL DEM
# ============================================================

def get_real_elevation():
    """
    Load the real Central Kolkata DEM.

    Returns
    -------
    numpy.ndarray
        20 × 20 elevation grid.
    """

    elevation_grid = load_dem()

    return elevation_grid


# ============================================================
# GLOBAL DEM
# ============================================================

# Load the real DEM when this module is imported.
# This allows dashboard.py and other modules to use:
#
#     from terrain import DEM
#
# The DEM is loaded from:
#
#     data/kolkata_dem.tif
#
DEM = get_real_elevation()


# ============================================================
# WATER ACCUMULATION
# ============================================================

def calculate_accumulation(
    rainfall_grid,
    elevation_grid
):
    """
    Calculate water accumulation using the real DEM.

    Water flows from higher elevation cells toward
    lower neighboring cells.

    8-directional movement is used:

        ↖   ↑   ↗
        ←   •   →
        ↙   ↓   ↘

    Parameters
    ----------
    rainfall_grid : 2D list / numpy array
        Rainfall or runoff input for each grid cell.

    elevation_grid : 2D list / numpy array
        Real elevation values from the DEM.

    Returns
    -------
    numpy.ndarray
        Water accumulation grid.
    """

    rainfall_grid = np.array(
        rainfall_grid,
        dtype=float
    )

    elevation_grid = np.array(
        elevation_grid,
        dtype=float
    )

    rows, cols = rainfall_grid.shape

    # ========================================================
    # VALIDATION
    # ========================================================

    if elevation_grid.shape != rainfall_grid.shape:

        raise ValueError(
            "Rainfall grid and elevation grid "
            "must have the same dimensions."
        )

    if np.isnan(elevation_grid).any():

        raise ValueError(
            "Elevation grid contains invalid "
            "NaN values."
        )

    # ========================================================
    # INITIAL WATER
    # ========================================================

    # Every cell initially contains the supplied
    # rainfall/runoff amount.

    accumulation = rainfall_grid.copy()

    # ========================================================
    # 8-DIRECTIONAL NEIGHBORS
    # ========================================================

    directions = [

        (-1, -1),   # Northwest
        (-1,  0),   # North
        (-1,  1),   # Northeast

        ( 0, -1),   # West
        ( 0,  1),   # East

        ( 1, -1),   # Southwest
        ( 1,  0),   # South
        ( 1,  1)    # Southeast

    ]

    # ========================================================
    # PROCESS CELLS FROM HIGHER TO LOWER ELEVATION
    # ========================================================

    cells = []

    for r in range(rows):

        for c in range(cols):

            cells.append(
                (
                    elevation_grid[r, c],
                    r,
                    c
                )
            )

    # Highest elevation first
    cells.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # ========================================================
    # WATER FLOW
    # ========================================================

    for elevation, r, c in cells:

        lower_neighbors = []

        # ----------------------------------------------------
        # Find lower neighboring cells
        # ----------------------------------------------------

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            # Check row boundary
            if nr < 0 or nr >= rows:
                continue

            # Check column boundary
            if nc < 0 or nc >= cols:
                continue

            # Water flows only downhill
            if (
                elevation_grid[nr, nc]
                < elevation_grid[r, c]
            ):

                lower_neighbors.append(
                    (nr, nc)
                )

        # ----------------------------------------------------
        # No lower neighbor
        # ----------------------------------------------------

        if len(lower_neighbors) == 0:

            # Local low point.
            # Water remains in this cell.

            continue

        # ----------------------------------------------------
        # Split water between lower neighbors
        # ----------------------------------------------------

        water = accumulation[r, c]

        share = (
            water /
            len(lower_neighbors)
        )

        for nr, nc in lower_neighbors:

            accumulation[nr, nc] += share

    return accumulation


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       REAL TERRAIN PROCESSING")
    print("======================================")

    # --------------------------------------------------------
    # Load real DEM
    # --------------------------------------------------------

    elevation_grid = get_real_elevation()

    print()
    print(
        "Real elevation successfully loaded."
    )

    print(
        f"Grid size: "
        f"{elevation_grid.shape[0]} × "
        f"{elevation_grid.shape[1]}"
    )

    print(
        f"Minimum elevation: "
        f"{np.min(elevation_grid):.2f}"
    )

    print(
        f"Maximum elevation: "
        f"{np.max(elevation_grid):.2f}"
    )

    # --------------------------------------------------------
    # Create test rainfall/runoff
    # --------------------------------------------------------
    #
    # This is ONLY for testing terrain.py.
    # main.py will provide the actual runoff grid.
    #

    rainfall_grid = np.ones(
        elevation_grid.shape,
        dtype=float
    )

    # --------------------------------------------------------
    # Calculate accumulation
    # --------------------------------------------------------

    accumulation = calculate_accumulation(
        rainfall_grid,
        elevation_grid
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print()
    print(
        "Water accumulation grid:"
    )

    print(
        np.round(
            accumulation,
            2
        )
    )

    print()
    print(
        "Terrain processing completed successfully."
    )