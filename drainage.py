# drainage.py

# ============================================================
# SPATIAL DRAINAGE CAPACITY
# ============================================================
#
# Higher value  -> better drainage
# Lower value   -> poorer drainage
#
# This is a prototype assumption.
# In a real system, these values would come from drainage/
# stormwater infrastructure data.
# ============================================================

DRAINAGE_CAPACITY_GRID = [
    [120, 110, 100, 90],
    [110, 100, 90, 70],
    [90,  80,  60, 50],
    [70,  60,  40, 30]
]


def _resize_capacity_grid(capacity_grid, rows, cols):
    """Resize the prototype capacity grid with nearest-neighbor sampling."""

    source_rows = len(capacity_grid)
    source_cols = len(capacity_grid[0])

    return [
        [
            capacity_grid[
                min(int(r * source_rows / rows), source_rows - 1)
            ][
                min(int(c * source_cols / cols), source_cols - 1)
            ]
            for c in range(cols)
        ]
        for r in range(rows)
    ]


def calculate_excess_water(
    water_grid,
    drainage_capacity_grid=None
):
    """
    Calculate excess water for every grid cell.

    Formula:

        Excess Water =
            max(Accumulated Water - Drainage Capacity, 0)

    Parameters:
        water_grid:
            2D grid containing accumulated water.

        drainage_capacity_grid:
            2D grid containing drainage capacity.

    Returns:
        2D grid containing excess water.
    """

    if drainage_capacity_grid is None:
        drainage_capacity_grid = DRAINAGE_CAPACITY_GRID

    rows = len(water_grid)
    cols = len(water_grid[0])

    if isinstance(drainage_capacity_grid, (int, float)):
        drainage_capacity_grid = [
            [drainage_capacity_grid for _ in range(cols)]
            for _ in range(rows)
        ]
    elif drainage_capacity_grid is DRAINAGE_CAPACITY_GRID and (
        len(drainage_capacity_grid) != rows
        or len(drainage_capacity_grid[0]) != cols
    ):
        drainage_capacity_grid = _resize_capacity_grid(
            drainage_capacity_grid,
            rows,
            cols
        )

    # Validate dimensions
    if len(drainage_capacity_grid) != rows:
        raise ValueError(
            "Water grid and drainage grid must have "
            "the same number of rows."
        )

    for row in drainage_capacity_grid:
        if len(row) != cols:
            raise ValueError(
                "Water grid and drainage grid must have "
                "the same number of columns."
            )

    excess_water = []

    for r in range(rows):

        excess_row = []

        for c in range(cols):

            water = water_grid[r][c]
            capacity = drainage_capacity_grid[r][c]

            excess = max(water - capacity, 0)

            excess_row.append(excess)

        excess_water.append(excess_row)

    return excess_water


def print_drainage_capacity(
    drainage_capacity_grid=None
):
    """
    Print the spatial drainage capacity grid.
    """

    if drainage_capacity_grid is None:
        drainage_capacity_grid = DRAINAGE_CAPACITY_GRID

    print("\nDrainage Capacity:")

    for row in drainage_capacity_grid:
        print(
            "  ".join(
                f"{value:8.2f}" for value in row
            )
        )


def print_excess_water(excess_water_grid):
    """
    Print the excess water grid.
    """

    print("\nExcess Water After Drainage:")

    for row in excess_water_grid:
        print(
            "  ".join(
                f"{value:8.2f}" for value in row
            )
        )

