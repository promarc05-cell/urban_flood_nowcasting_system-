from rainfall import get_rainfall_data
from forecast import forecast_next_3_hours
from runoff import calculate_runoff
from terrain import calculate_accumulation
from drainage import calculate_excess_water
from flood import calculate_flood_risk, calculate_flood_depth


print("======================================")
print("   URBAN FLOOD NOWCASTING SYSTEM")
print("======================================")


# -----------------------------------
# Step 1: Get rainfall data
# -----------------------------------

rainfall_data = get_rainfall_data()

print("\nRainfall data:")

for record in rainfall_data:
    print(record)


# -----------------------------------
# Step 2: Extract rainfall values
# -----------------------------------

rainfall_values = []

for record in rainfall_data:
    rainfall_values.append(record[2])


# -----------------------------------
# Step 3: Forecast next 3 hours
# -----------------------------------

forecasts = forecast_next_3_hours(rainfall_values)


# -----------------------------------
# Process each forecast hour
# -----------------------------------

for hour, forecast in enumerate(forecasts, start=1):

    print("\n======================================")
    print("          HOUR", hour, "FORECAST")
    print("======================================")

    # Forecast rainfall
    print("\nForecast rainfall:", forecast, "mm")


    # -----------------------------------
    # Step 4: Calculate forecast runoff
    # -----------------------------------

    runoff_coefficient = 0.8

    forecast_runoff = calculate_runoff(
        forecast,
        runoff_coefficient
    )

    print("Forecast runoff:", forecast_runoff, "mm")


    # -----------------------------------
    # Step 5: Create runoff grid
    # -----------------------------------

    runoff_grid = [
        [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff],
        [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff],
        [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff],
        [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff]
    ]


    # -----------------------------------
    # Step 6: Terrain accumulation
    # -----------------------------------

    accumulation = calculate_accumulation(runoff_grid)

    print("\nAccumulated runoff:")

    for row in accumulation:
        print(row)


    # -----------------------------------
    # Step 7: Drainage
    # -----------------------------------

    drainage_capacity = 100

    excess_water = calculate_excess_water(
        accumulation,
        drainage_capacity
    )

    print("\nExcess water:")

    for row in excess_water:
        print(row)


    # -----------------------------------
    # Step 8: Flood risk
    # -----------------------------------

    risk_grid = calculate_flood_risk(excess_water)

    print("\nFlood risk:")

    for row in risk_grid:
        print(row)


    # -----------------------------------
    # Step 9: Flood depth
    # -----------------------------------

    depth_grid = calculate_flood_depth(
        excess_water,
        depth_factor=0.01
    )

    print("\nEstimated flood depth:")

    for row in depth_grid:
        print(row)


print("\n======================================")
print("       3-HOUR FORECAST COMPLETE")
print("======================================")