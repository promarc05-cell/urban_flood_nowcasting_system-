# terrain.py

dem = [
    [100, 102, 105, 107],
    [98,  100, 103, 105],
    [95,  97,  99, 101],
    [90,  92,  94,  97]
]


def get_flow_direction(row, col):
    """
    Find the lowest neighboring cell for a given DEM cell.
    """

    rows = len(dem)
    cols = len(dem[0])

    current_elevation = dem[row][col]

    lowest_elevation = current_elevation
    flow_cell = None

    # Check all 8 neighboring cells
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:

            # Skip the current cell
            if dr == 0 and dc == 0:
                continue

            new_row = row + dr
            new_col = col + dc

            # Make sure the neighbor is inside the DEM
            if 0 <= new_row < rows and 0 <= new_col < cols:

                neighbor_elevation = dem[new_row][new_col]

                # Find a lower neighboring cell
                if neighbor_elevation < lowest_elevation:
                    lowest_elevation = neighbor_elevation
                    flow_cell = (new_row, new_col)

    return flow_cell


print("Terrain elevation:")

for row in dem:
    print(row)

def calculate_accumulation(runoff_grid):
    """
    Calculate how runoff accumulates as it flows downhill.

    runoff_grid must have the same dimensions as the DEM.
    """

    rows = len(dem)
    cols = len(dem[0])

    # Start with the local runoff at every cell
    accumulation = [
        row[:] for row in runoff_grid
    ]

    # Process higher cells before lower cells
    cells = []

    for row in range(rows):
        for col in range(cols):
            cells.append((dem[row][col], row, col))

    cells.sort(reverse=True)

    # Send accumulated water to the next lower cell
    for elevation, row, col in cells:

        flow_cell = get_flow_direction(row, col)

        if flow_cell is not None:
            next_row, next_col = flow_cell

            accumulation[next_row][next_col] += accumulation[row][col]

    return accumulation