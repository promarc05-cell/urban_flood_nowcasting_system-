# main.py

from rainfall import (
    get_spatial_rainfall_forecast,
    validate_rainfall_forecast
)

from runoff import calculate_spatial_runoff
from terrain import calculate_accumulation
from drainage import calculate_excess_water
from flood import (
    calculate_flood_risk,
    calculate_flood_depth
)

from dem import load_dem


def get_max_value(grid):
    """Return the maximum value from a 2D grid."""

    return max(
        max(row)
        for row in grid
    )


print("======================================")
print("   URBAN FLOOD NOWCASTING SYSTEM")
print("======================================\n")


# ============================================================
# STEP 1 — RAINFALL FORECAST
# ============================================================

print("Loading spatial rainfall forecast...")

rainfall_forecast = (
    get_spatial_rainfall_forecast()
)

validate_rainfall_forecast(
    rainfall_forecast
)

print(
    "\nSpatial rainfall forecast loaded."
)

print(
    "Forecast grid: 20 × 20"
)


# ============================================================
# STEP 2 — REAL DEM
# ============================================================

print(
    "\nLoading real Central Kolkata DEM..."
)

elevation_grid = load_dem()

print(
    "\nReal DEM loaded successfully."
)


# ============================================================
# STEP 3 — PROCESS EACH FORECAST HOUR
# ============================================================

for hour in range(
    1,
    len(rainfall_forecast) + 1
):

    print("\n")
    print("======================================")
    print(
        f"        FORECAST HOUR {hour}"
    )
    print("======================================")


    # ========================================================
    # RAINFALL
    # ========================================================

    rainfall_grid = (
        rainfall_forecast[hour]
    )

    print(
        "\nRainfall grid loaded."
    )


    # ========================================================
    # RUNOFF
    # ========================================================

    runoff_grid = (
        calculate_spatial_runoff(
            rainfall_grid
        )
    )

    print(
        "Runoff calculated successfully."
    )


    # ========================================================
    # TERRAIN
    # ========================================================

    accumulation_grid = (
        calculate_accumulation(
            runoff_grid,
            elevation_grid
        )
    )

    print(
        "Water accumulation calculated "
        "using real DEM."
    )


    # ========================================================
    # DRAINAGE
    # ========================================================

    excess_water_grid = (
        calculate_excess_water(
            accumulation_grid
        )
    )

    print(
        "Drainage/excess water calculated."
    )


    # ========================================================
    # FLOOD RISK
    # ========================================================

    risk_grid = (
        calculate_flood_risk(
            excess_water_grid
        )
    )

    print(
        "Flood risk calculated."
    )


    # ========================================================
    # FLOOD DEPTH
    # ========================================================

    depth_grid = (
        calculate_flood_depth(
            excess_water_grid
        )
    )

    print(
        "Flood depth calculated."
    )


    # ========================================================
    # RESULT SUMMARY
    # ========================================================

    print("\n--------------------------------------")
    print(
        f"RESULT SUMMARY — HOUR +{hour}"
    )
    print("--------------------------------------")

    print(
        f"Maximum rainfall: "
        f"{get_max_value(rainfall_grid):.2f} mm"
    )

    print(
        f"Maximum runoff: "
        f"{get_max_value(runoff_grid):.2f} mm"
    )

    print(
        f"Maximum accumulation: "
        f"{get_max_value(accumulation_grid):.2f} mm"
    )

    print(
        f"Maximum excess water: "
        f"{get_max_value(excess_water_grid):.2f} mm"
    )

    print(
        f"Maximum flood depth: "
        f"{get_max_value(depth_grid):.2f}"
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("======================================")
print("       NOWCASTING COMPLETED")
print("======================================")