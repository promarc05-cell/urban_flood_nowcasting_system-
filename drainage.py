# drainage.py

def calculate_excess_water(accumulation_grid, drainage_capacity):
    """
    Calculate the amount of water remaining
    after drainage.
    """

    excess_water = []

    for row in accumulation_grid:

        excess_row = []

        for water in row:

            # Water above drainage capacity becomes excess
            excess = max(water - drainage_capacity, 0)

            excess_row.append(excess)

        excess_water.append(excess_row)

    return excess_water