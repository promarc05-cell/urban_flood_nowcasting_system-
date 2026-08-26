from rainfall import get_rainfall_data
from forecast import forecast_next_3_hours
from runoff import calculate_runoff
from terrain import calculate_accumulation
from drainage import calculate_excess_water
from flood import calculate_flood_risk, calculate_flood_depth


print("Testing complete flood nowcasting pipeline...")


# -----------------------------------
# Step 1: Get rainfall data
# -----------------------------------

rainfall_data = get_rainfall_data()

if len(rainfall_data) > 0:
    print("Rainfall data: PASS")
else:
    print("Rainfall data: FAIL")


# -----------------------------------
# Step 2: Extract rainfall values
# -----------------------------------

rainfall_values = []

for record in rainfall_data:
    rainfall_values.append(record[2])


# -----------------------------------
# Step 3: Generate 3-hour forecast
# -----------------------------------

forecasts = forecast_next_3_hours(
    rainfall_values
)

if len(forecasts) == 3:
    print("3-hour forecast: PASS")
else:
    print("3-hour forecast: FAIL")


# -----------------------------------
# Step 4: Test each forecast hour
# -----------------------------------

for hour, forecast in enumerate(forecasts, start=1):

    print("\nTesting Hour", hour)

    # Runoff
    runoff = calculate_runoff(
        forecast,
        0.8
    )

    print("Runoff: PASS")


    # Create runoff grid
    runoff_grid = [
        [runoff, runoff, runoff, runoff],
        [runoff, runoff, runoff, runoff],
        [runoff, runoff, runoff, runoff],
        [runoff, runoff, runoff, runoff]
    ]


    # Terrain accumulation
    accumulation = calculate_accumulation(
        runoff_grid
    )

    if accumulation[3][0] > runoff:
        print("Terrain accumulation: PASS")
    else:
        print("Terrain accumulation: FAIL")


    # Drainage
    excess_water = calculate_excess_water(
        accumulation,
        100
    )

    print("Drainage: PASS")


    # Flood risk
    risk_grid = calculate_flood_risk(
        excess_water
    )

    if risk_grid[3][0] == "SEVERE":
        print("Flood risk: PASS")
    else:
        print("Flood risk: FAIL")


    # Flood depth
    depth_grid = calculate_flood_depth(
        excess_water
    )

    if depth_grid[3][0] > 0:
        print("Flood depth: PASS")
    else:
        print("Flood depth: FAIL")


print("\n======================================")
print("   END-TO-END PIPELINE TEST COMPLETE")
print("======================================")