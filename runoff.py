# runoff.py

"""
Spatial runoff calculation for the Urban Flood Nowcasting System.

Each grid cell has a runoff coefficient.

Runoff = Rainfall × Runoff Coefficient

For the real-world prototype, the model uses a 20 × 20
computational grid.
"""

from config import GRID_ROWS, GRID_COLS


# ============================================================
# RUNOFF COEFFICIENT
# ============================================================

# Prototype assumption:
#
# 0.90 → Highly impervious
# 0.80 → Built-up area
# 0.50 → Mixed/open area
# 0.30 → Green/soil area
#
# For the current real-world prototype, we use 0.80
# as a general urban coefficient across the study area.
#
# Later this can be replaced with a real land-cover dataset.

DEFAULT_RUNOFF_COEFFICIENT = 0.80


# ============================================================
# CREATE 20 × 20 COEFFICIENT GRID
# ============================================================

RUNOFF_COEFFICIENT_GRID = [
    [
        DEFAULT_RUNOFF_COEFFICIENT
        for _ in range(GRID_COLS)
    ]
    for _ in range(GRID_ROWS)
]


# ============================================================
# SINGLE-CELL RUNOFF
# ============================================================

def calculate_runoff(
    rainfall_mm,
    runoff_coefficient
):
    """
    Calculate runoff for one grid cell.

    Formula:
        Runoff = Rainfall × Runoff Coefficient

    Parameters:
        rainfall_mm:
            Rainfall received by the cell in mm.

        runoff_coefficient:
            Fraction of rainfall converted into
            surface runoff.

    Returns:
        Runoff in mm.
    """

    return rainfall_mm * runoff_coefficient


# ============================================================
# SPATIAL RUNOFF
# ============================================================

def calculate_spatial_runoff(rainfall_grid):
    """
    Calculate runoff independently for every
    cell in the spatial rainfall grid.
    """

    rows = len(rainfall_grid)
    cols = len(rainfall_grid[0])

    # --------------------------------------------------------
    # Validate grid size
    # --------------------------------------------------------

    if rows != GRID_ROWS or cols != GRID_COLS:

        raise ValueError(
            f"Rainfall grid must be "
            f"{GRID_ROWS} × {GRID_COLS}."
        )


    # --------------------------------------------------------
    # Calculate runoff
    # --------------------------------------------------------

    runoff_grid = []

    for row in range(rows):

        runoff_row = []

        for col in range(cols):

            rainfall = rainfall_grid[row][col]

            coefficient = (
                RUNOFF_COEFFICIENT_GRID[row][col]
            )

            runoff = calculate_runoff(
                rainfall,
                coefficient
            )

            runoff_row.append(
                round(runoff, 2)
            )

        runoff_grid.append(runoff_row)

    return runoff_grid


# ============================================================
# PRINT RUNOFF GRID
# ============================================================

def print_runoff_grid(runoff_grid):
    """
    Display the spatial runoff grid.
    """

    print("\n--------------------------------------")
    print("SPATIAL RUNOFF GRID")
    print("--------------------------------------")

    for row in runoff_grid:

        print(
            "  ".join(
                f"{value:6.2f}"
                for value in row
            )
        )

    print("\nUnit: mm")


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("       RUNOFF CALCULATION TEST")
    print("======================================")

    # Create a 20 × 20 test rainfall grid
    rainfall_grid = [
        [
            20.0
            for _ in range(GRID_COLS)
        ]
        for _ in range(GRID_ROWS)
    ]

    runoff_grid = calculate_spatial_runoff(
        rainfall_grid
    )

    print_runoff_grid(
        runoff_grid
    )