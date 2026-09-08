# rainfall.py

"""
Spatial rainfall input for the Urban Flood Nowcasting System.

Current prototype:
    Generates deterministic radar-like rainfall grids
    for the next 3 hours.

The original prototype rainfall pattern was 4 × 4.
It is expanded to the 20 × 20 model grid so that it
matches the real DEM.

Future:
    The synthetic rainfall generator can be replaced by
    a real spatial rainfall / weather API without changing
    the downstream flood model.
"""

from typing import Dict, List

from config import (
    GRID_ROWS,
    GRID_COLS,
    FORECAST_HOURS
)


# ============================================================
# BASE PROTOTYPE RAINFALL
# ============================================================

# Original 4 × 4 rainfall pattern.
#
# These values represent rainfall in mm during each
# forecast hour.

BASE_RAINFALL = {

    # --------------------------------------------------------
    # Hour +1
    # --------------------------------------------------------

    1: [
        [20, 25, 32, 28],
        [30, 42, 55, 47],
        [25, 48, 68, 58],
        [15, 28, 40, 35]
    ],

    # --------------------------------------------------------
    # Hour +2
    # --------------------------------------------------------

    2: [
        [28, 34, 42, 38],
        [38, 52, 65, 56],
        [32, 60, 82, 70],
        [20, 35, 50, 44]
    ],

    # --------------------------------------------------------
    # Hour +3
    # --------------------------------------------------------

    3: [
        [24, 30, 37, 34],
        [34, 47, 60, 52],
        [28, 55, 76, 65],
        [18, 30, 44, 39]
    ]
}


# ============================================================
# EXPAND 4 × 4 → 20 × 20
# ============================================================

def expand_rainfall_grid(base_grid):
    """
    Expand the original 4 × 4 rainfall grid
    into the model's 20 × 20 grid.

    Each original rainfall cell becomes a 5 × 5
    block in the model grid.

    This is only a prototype spatial expansion.
    Later, real spatial rainfall data will directly
    populate the 20 × 20 grid.
    """

    base_rows = len(base_grid)
    base_cols = len(base_grid[0])

    if GRID_ROWS % base_rows != 0:
        raise ValueError(
            "Model rows must be divisible by "
            "the base rainfall rows."
        )

    if GRID_COLS % base_cols != 0:
        raise ValueError(
            "Model columns must be divisible by "
            "the base rainfall columns."
        )

    row_scale = GRID_ROWS // base_rows
    col_scale = GRID_COLS // base_cols

    expanded_grid = []

    for row in base_grid:

        for _ in range(row_scale):

            expanded_row = []

            for value in row:

                for _ in range(col_scale):

                    expanded_row.append(
                        float(value)
                    )

            expanded_grid.append(
                expanded_row
            )

    return expanded_grid


# ============================================================
# SPATIAL RAINFALL FORECAST
# ============================================================

def get_spatial_rainfall_forecast() -> Dict[int, List[List[float]]]:
    """
    Return rainfall forecast for the next 3 hours.

    Returns:

        {
            1: 20 × 20 rainfall grid,
            2: 20 × 20 rainfall grid,
            3: 20 × 20 rainfall grid
        }

    Units:
        mm during the forecast hour.
    """

    rainfall_forecast = {}

    for hour in range(
        1,
        FORECAST_HOURS + 1
    ):

        if hour not in BASE_RAINFALL:

            raise ValueError(
                f"No rainfall data available "
                f"for forecast hour +{hour}."
            )

        rainfall_forecast[hour] = (
            expand_rainfall_grid(
                BASE_RAINFALL[hour]
            )
        )

    return rainfall_forecast


# ============================================================
# VALIDATION
# ============================================================

def validate_rainfall_forecast(
    rainfall_forecast:
    Dict[int, List[List[float]]]
) -> bool:
    """
    Validate rainfall forecast.

    Checks:

    - exactly 3 forecast hours
    - 20 × 20 grid
    - non-negative rainfall
    """

    expected_hours = set(
        range(
            1,
            FORECAST_HOURS + 1
        )
    )

    # --------------------------------------------------------
    # Check forecast hours
    # --------------------------------------------------------

    if set(rainfall_forecast.keys()) != expected_hours:

        raise ValueError(
            "Rainfall forecast must contain "
            "Hour +1, +2 and +3."
        )


    # --------------------------------------------------------
    # Check every rainfall grid
    # --------------------------------------------------------

    for hour, grid in rainfall_forecast.items():

        if len(grid) != GRID_ROWS:

            raise ValueError(
                f"Hour +{hour}: expected "
                f"{GRID_ROWS} rows."
            )

        for row in grid:

            if len(row) != GRID_COLS:

                raise ValueError(
                    f"Hour +{hour}: expected "
                    f"{GRID_COLS} columns."
                )

            for rainfall in row:

                if rainfall < 0:

                    raise ValueError(
                        f"Hour +{hour}: rainfall "
                        f"cannot be negative."
                    )

    return True


# ============================================================
# PRINT RAINFALL FORECAST
# ============================================================

def print_rainfall_forecast(
    rainfall_forecast:
    Dict[int, List[List[float]]]
):
    """
    Print the spatial rainfall forecast.
    """

    for hour in range(
        1,
        FORECAST_HOURS + 1
    ):

        print("\n--------------------------------------")
        print(
            f"RAIN-FALL FORECAST: HOUR +{hour}"
        )
        print("--------------------------------------")

        grid = rainfall_forecast[hour]

        for row in grid:

            print(
                "  ".join(
                    f"{value:5.1f}"
                    for value in row
                )
            )

        print("Unit: mm")


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    forecast = (
        get_spatial_rainfall_forecast()
    )

    validate_rainfall_forecast(
        forecast
    )

    print_rainfall_forecast(
        forecast
    )

    print("\nSpatial rainfall input: PASS")