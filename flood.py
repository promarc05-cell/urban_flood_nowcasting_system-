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