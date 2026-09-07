# terrain.py

# Simple 4x4 Digital Elevation Model (DEM)
# Higher value = higher elevation
DEM = [
    [100, 102, 105, 107],
    [98,  100, 103, 105],
    [95,  97,  99, 101],
    [90,  92,  94,  97]
]


def get_neighbors(row, col, rows, cols):
    """
    Return all valid 8-directional neighboring cells.
    Includes:
    - Up
    - Down
    - Left
    - Right
    - 4 diagonals
    """

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    neighbors = []

    for dr, dc in directions:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))

    return neighbors


def calculate_flow_direction(dem=None):
    """
    Determine lower neighboring cells for every grid cell.

    Water is allowed to flow only from a higher cell
    toward a lower elevation cell.

    Returns:
        flow_map[row][col] = list of lower neighboring cells
    """

    if dem is None:
        dem = DEM

    rows = len(dem)
    cols = len(dem[0])

    flow_map = [[[] for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):

            current_elevation = dem[row][col]

            neighbors = get_neighbors(
                row,
                col,
                rows,
                cols
            )

            lower_neighbors = []

            for nr, nc in neighbors:

                if dem[nr][nc] < current_elevation:
                    lower_neighbors.append((nr, nc))

            flow_map[row][col] = lower_neighbors

    return flow_map


def calculate_accumulation(runoff_grid, dem=None):
    """
    Calculate spatial water accumulation.

    Water starts as runoff in each cell.

    Each cell sends its available water equally
    to all lower neighboring cells.

    Cells with no lower neighbor retain the water,
    representing local low points / sinks.

    Returns:
        accumulation_grid
    """

    if dem is None:
        dem = DEM

    rows = len(dem)
    cols = len(dem[0])

    # Start with runoff as the initial amount of water
    accumulation = [
        [float(runoff_grid[r][c]) for c in range(cols)]
        for r in range(rows)
    ]

    flow_map = calculate_flow_direction(dem)

    # Process cells from highest elevation to lowest elevation.
    # This allows upstream water to reach downstream cells.
    cells = []

    for row in range(rows):
        for col in range(cols):
            cells.append((dem[row][col], row, col))

    cells.sort(reverse=True)

    for elevation, row, col in cells:

        downstream_cells = flow_map[row][col]

        # No lower neighboring cell:
        # water remains in this location.
        if not downstream_cells:
            continue

        current_water = accumulation[row][col]

        # Split water equally among all lower neighbors.
        flow_amount = current_water / len(downstream_cells)

        for nr, nc in downstream_cells:
            accumulation[nr][nc] += flow_amount

    return accumulation


def print_dem(dem=None):
    """
    Print the Digital Elevation Model.
    """

    if dem is None:
        dem = DEM

    print("\nTerrain Elevation (DEM):")

    for row in dem:
        print("  ".join(f"{value:6.1f}" for value in row))


def print_flow_direction(flow_map, dem=None):
    """
    Print simplified flow information.
    """

    if dem is None:
        dem = DEM

    print("\nTerrain Flow Direction:")

    rows = len(dem)
    cols = len(dem[0])

    for row in range(rows):
        for col in range(cols):

            current = (row, col)
            destinations = flow_map[row][col]

            if destinations:
                destination_text = ", ".join(
                    f"({r},{c})" for r, c in destinations
                )

                print(
                    f"Cell ({row},{col}) "
                    f"elev={dem[row][col]} "
                    f"-> {destination_text}"
                )
            else:
                print(
                    f"Cell ({row},{col}) "
                    f"elev={dem[row][col]} "
                    f"-> LOW POINT / SINK"
                )


def print_accumulation_grid(accumulation_grid):
    """
    Print the final accumulated water grid.
    """

    print("\nWater Accumulation:")

    for row in accumulation_grid:
        print("  ".join(f"{value:8.2f}" for value in row))

