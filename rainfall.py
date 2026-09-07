# rainfall.py
"""
Spatial rainfall input for the Urban Flood Nowcasting System.

Current prototype:
    Generates deterministic radar-like rainfall grids for the next 3 hours.

Future:
    The synthetic rainfall generator can be replaced by a real Doppler
    Weather Radar API without changing the downstream flood model.
"""

from typing import Dict, List


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

GRID_ROWS = 4
GRID_COLS = 4
FORECAST_HOURS = 3


# ---------------------------------------------------------
# Prototype spatial rainfall
# ---------------------------------------------------------

def get_spatial_rainfall_forecast() -> Dict[int, List[List[float]]]:
    """
    Return rainfall forecast for the next 3 hours as spatial grids.

    Each grid cell represents a different location in the city.

    Units:
        mm of rainfall during that forecast hour.

    Returns:
        {
            1: [[...], [...], [...], [...]],
            2: [[...], [...], [...], [...]],
            3: [[...], [...], [...], [...]]
        }
    """

    rainfall_forecast = {

        # ---------------------------------------------
        # Hour +1
        # ---------------------------------------------
        1: [
            [20, 25, 32, 28],
            [30, 42, 55, 47],
            [25, 48, 68, 58],
            [15, 28, 40, 35]
        ],

        # ---------------------------------------------
        # Hour +2
        # ---------------------------------------------
        2: [
            [28, 34, 42, 38],
            [38, 52, 65, 56],
            [32, 60, 82, 70],
            [20, 35, 50, 44]
        ],

        # ---------------------------------------------
        # Hour +3
        # ---------------------------------------------
        3: [
            [24, 30, 37, 34],
            [34, 47, 60, 52],
            [28, 55, 76, 65],
            [18, 30, 44, 39]
        ]
    }

    return rainfall_forecast


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_rainfall_forecast(
    rainfall_forecast: Dict[int, List[List[float]]]
) -> bool:
    """
    Validate that the rainfall forecast has:

    - exactly 3 forecast hours
    - correct grid dimensions
    - non-negative rainfall values
    """

    # Check forecast hours
    expected_hours = {1, 2, 3}

    if set(rainfall_forecast.keys()) != expected_hours:
        raise ValueError(
            "Rainfall forecast must contain exactly Hour +1, +2 and +3."
        )

    # Check each grid
    for hour, grid in rainfall_forecast.items():

        if len(grid) != GRID_ROWS:
            raise ValueError(
                f"Hour +{hour}: expected {GRID_ROWS} rows."
            )

        for row in grid:

            if len(row) != GRID_COLS:
                raise ValueError(
                    f"Hour +{hour}: expected {GRID_COLS} columns."
                )

            for rainfall in row:

                if rainfall < 0:
                    raise ValueError(
                        f"Hour +{hour}: rainfall cannot be negative."
                    )

    return True


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def print_rainfall_forecast(
    rainfall_forecast: Dict[int, List[List[float]]]
):
    """
    Print the spatial rainfall forecast in a readable format.
    """

    for hour in range(1, FORECAST_HOURS + 1):

        print("\n--------------------------------------")
        print(f"RAIN-FALL FORECAST: HOUR +{hour}")
        print("--------------------------------------")

        grid = rainfall_forecast[hour]

        for row in grid:
            print("  ".join(f"{value:5.1f}" for value in row))

        print("Unit: mm")


# ---------------------------------------------------------
# Test module
# ---------------------------------------------------------

if __name__ == "__main__":

    forecast = get_spatial_rainfall_forecast()

    validate_rainfall_forecast(forecast)

    print_rainfall_forecast(forecast)

    print("\nSpatial rainfall input: PASS")