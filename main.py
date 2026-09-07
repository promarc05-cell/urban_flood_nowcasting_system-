# main.py

from rainfall import (
    get_spatial_rainfall_forecast,
    validate_rainfall_forecast
)

from runoff import calculate_spatial_runoff

from terrain import (
    DEM,
    calculate_flow_direction,
    calculate_accumulation,
    print_dem,
    print_flow_direction,
    print_accumulation_grid
)

from drainage import (
    DRAINAGE_CAPACITY_GRID,
    calculate_excess_water,
    print_drainage_capacity,
    print_excess_water
)

from flood import (
    calculate_flood_risk,
    calculate_flood_depth,
    calculate_risk_score,
    print_risk_grid,
    print_depth_grid,
    print_risk_score_grid
)

from routing import (
    find_safest_route,
    calculate_route_summary,
    print_route
)


# ============================================================
# CONFIGURATION
# ============================================================

# Prototype conversion factor.
# This is NOT a calibrated hydraulic relationship.
DEPTH_FACTOR = 0.01


# Example routing locations.
# Format: (row, column)

ROUTE_START = (3, 0)
ROUTE_DESTINATION = (0, 3)


# ============================================================
# MAIN SYSTEM
# ============================================================

def main():

    print("======================================")
    print("   URBAN FLOOD NOWCASTING SYSTEM")
    print("======================================")

    # --------------------------------------------------------
    # STEP 1: LOAD SPATIAL RAINFALL
    # --------------------------------------------------------

    rainfall_forecast = get_spatial_rainfall_forecast()

    if not validate_rainfall_forecast(
        rainfall_forecast
    ):
        print("ERROR: Invalid rainfall forecast.")
        return

    print(
        "\nSpatial rainfall forecast "
        "loaded successfully."
    )

    # --------------------------------------------------------
    # STEP 3: TERRAIN
    # --------------------------------------------------------

    print_dem(DEM)

    flow_map = calculate_flow_direction(DEM)

    print_flow_direction(
        flow_map,
        DEM
    )

    # --------------------------------------------------------
    # STEP 4: DRAINAGE
    # --------------------------------------------------------

    print_drainage_capacity(
        DRAINAGE_CAPACITY_GRID
    )

    # --------------------------------------------------------
    # ROUTING LOCATIONS
    # --------------------------------------------------------

    print("\nRouting Configuration:")

    print(
        f"Start        : {ROUTE_START}"
    )

    print(
        f"Destination  : {ROUTE_DESTINATION}"
    )

    # --------------------------------------------------------
    # PROCESS EACH FORECAST HOUR
    # --------------------------------------------------------

    for hour in range(1, 4):

        print("\n")
        print("======================================")
        print(
            f"          FORECAST HOUR +{hour}"
        )
        print("======================================")

        # ----------------------------------------------------
        # STEP 1: SPATIAL RAINFALL
        # ----------------------------------------------------

        rainfall_grid = rainfall_forecast[hour]

        print("\nRainfall Grid (mm):")

        for row in rainfall_grid:

            print(
                "  ".join(
                    f"{value:6.1f}"
                    for value in row
                )
            )

        # ----------------------------------------------------
        # STEP 2: SPATIAL RUNOFF
        # ----------------------------------------------------

        runoff_grid = calculate_spatial_runoff(
            rainfall_grid
        )

        print("\nSpatial Runoff Grid:")

        for row in runoff_grid:

            print(
                "  ".join(
                    f"{value:8.2f}"
                    for value in row
                )
            )

        # ----------------------------------------------------
        # STEP 3: TERRAIN / ACCUMULATION
        # ----------------------------------------------------

        accumulation_grid = calculate_accumulation(
            runoff_grid,
            DEM
        )

        print_accumulation_grid(
            accumulation_grid
        )

        # ----------------------------------------------------
        # STEP 4: DRAINAGE
        # ----------------------------------------------------

        excess_water_grid = calculate_excess_water(
            accumulation_grid,
            DRAINAGE_CAPACITY_GRID
        )

        print_excess_water(
            excess_water_grid
        )

        # ----------------------------------------------------
        # STEP 5: FLOOD RISK
        # ----------------------------------------------------

        risk_grid = calculate_flood_risk(
            excess_water_grid
        )

        print_risk_grid(
            risk_grid
        )

        # ----------------------------------------------------
        # RISK SCORE
        # ----------------------------------------------------

        risk_score_grid = calculate_risk_score(
            excess_water_grid
        )

        print_risk_score_grid(
            risk_score_grid
        )

        # ----------------------------------------------------
        # FLOOD DEPTH
        # ----------------------------------------------------

        depth_grid = calculate_flood_depth(
            excess_water_grid,
            DEPTH_FACTOR
        )

        print_depth_grid(
            depth_grid
        )

        # ----------------------------------------------------
        # STEP 7: SAFE ROUTING
        # ----------------------------------------------------

        route, route_cost = find_safest_route(
            risk_grid,
            ROUTE_START,
            ROUTE_DESTINATION
        )

        print_route(
            route,
            route_cost
        )

        # ----------------------------------------------------
        # ROUTE SUMMARY
        # ----------------------------------------------------

        if route:

            summary = calculate_route_summary(
                route,
                risk_grid
            )

            print("\nRoute Summary:")

            print(
                f"Route Length : "
                f"{summary['route_length']} cells"
            )

            print(
                f"LOW Cells    : "
                f"{summary['low_cells']}"
            )

            print(
                f"MEDIUM Cells : "
                f"{summary['medium_cells']}"
            )

            print(
                f"HIGH Cells   : "
                f"{summary['high_cells']}"
            )

            print(
                f"SEVERE Cells : "
                f"{summary['severe_cells']}"
            )

        else:

            print(
                "\nWARNING: No safe route "
                "is available."
            )

    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print("\n======================================")
    print("       FLOOD ANALYSIS COMPLETE")
    print("======================================")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()

