# flood.py

def calculate_flood_risk(excess_water_grid):
    """
    Convert excess water into flood-risk categories.
    """

    risk_grid = []

    for row in excess_water_grid:

        risk_row = []

        for water in row:

            if water == 0:
                risk = "LOW"

            elif water <= 50:
                risk = "MEDIUM"

            elif water <= 100:
                risk = "HIGH"

            else:
                risk = "SEVERE"

            risk_row.append(risk)

        risk_grid.append(risk_row)

    return risk_grid

def calculate_flood_depth(excess_water_grid, depth_factor=0.01):
    """
    Estimate flood depth from excess water.

    depth_factor is a simplified prototype conversion factor.
    """

    depth_grid = []

    for row in excess_water_grid:

        depth_row = []

        for water in row:

            depth = water * depth_factor

            depth_row.append(round(depth, 2))

        depth_grid.append(depth_row)

    return depth_grid