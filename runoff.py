# runoff.py

"""
Spatial runoff calculation for the Urban Flood Nowcasting System.

Each grid cell has its own runoff coefficient based on
land-cover / imperviousness.

Runoff = Rainfall × Runoff Coefficient
"""

# 4 × 4 land-cover grid
#
# Values:
# 0.90 → Highly impervious (roads/concrete)
# 0.80 → Built-up area
# 0.50 → Mixed/open area
# 0.30 → Green/soil area

RUNOFF_COEFFICIENT_GRID = [
    [0.90, 0.80, 0.50, 0.80],
    [0.90, 0.90, 0.80, 0.50],
    [0.30, 0.50, 0.90, 0.80],
    [0.30, 0.50, 0.50, 0.30]
]


def calculate_runoff(rainfall_mm, runoff_coefficient):
    """
    Calculate runoff for one grid cell.

    Formula:
        Runoff = Rainfall × Runoff Coefficient

    Parameters:
        rainfall_mm: rainfall received by the cell in mm
        runoff_coefficient: fraction converted to surface runoff

    Returns:
        runoff in mm
    """

    return rainfall_mm * runoff_coefficient


def calculate_spatial_runoff(rainfall_grid):
    """
    Calculate runoff independently for every grid cell.
    """

    rows = len(rainfall_grid)
    cols = len(rainfall_grid[0])

    if rows != len(RUNOFF_COEFFICIENT_GRID):
        raise ValueError("Rainfall grid size does not match land-cover grid.")

    runoff_grid = []

    for row in range(rows):

        runoff_row = []

        for col in range(cols):

            rainfall = rainfall_grid[row][col]
            coefficient = RUNOFF_COEFFICIENT_GRID[row][col]

            runoff = calculate_runoff(
                rainfall,
                coefficient
            )

            runoff_row.append(round(runoff, 2))

        runoff_grid.append(runoff_row)

    return runoff_grid


def print_runoff_grid(runoff_grid):
    """
    Display runoff grid.
    """

    print("\n--------------------------------------")
    print("SPATIAL RUNOFF GRID")
    print("--------------------------------------")

    for row in runoff_grid:
        print("  ".join(f"{value:6.2f}" for value in row))

    print("Unit: mm")


if __name__ == "__main__":

    # Example rainfall grid
    rainfall_grid = [
        [20, 25, 32, 28],
        [30, 42, 55, 47],
        [25, 48, 68, 58],
        [15, 28, 40, 35]
    ]

    runoff_grid = calculate_spatial_runoff(rainfall_grid)

    print_runoff_grid(runoff_grid)