from forecast import forecast_rainfall
from runoff import calculate_runoff
from terrain import calculate_accumulation
from drainage import calculate_excess_water
from flood import calculate_flood_risk, calculate_flood_depth


print("Testing complete forecast → flood pipeline...")


# -----------------------------------
# Step 1: Historical rainfall
# -----------------------------------

rainfall_values = [
    40,
    60,
    80,
    90,
    70,
    50,
    30
]


# -----------------------------------
# Step 2: Forecast rainfall
# -----------------------------------

forecast = forecast_rainfall(rainfall_values)

print("\nForecast rainfall:", forecast, "mm")


# -----------------------------------
# Step 3: Forecast runoff
# -----------------------------------

runoff_coefficient = 0.8

forecast_runoff = calculate_runoff(
    forecast,
    runoff_coefficient
)

print("Forecast runoff:", forecast_runoff, "mm")


# -----------------------------------
# Step 4: Create forecast runoff grid
# -----------------------------------

runoff_grid = [
    [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff],
    [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff],
    [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff],
    [forecast_runoff, forecast_runoff, forecast_runoff, forecast_runoff]
]


print("\nForecast runoff grid:")

for row in runoff_grid:
    print(row)


# -----------------------------------
# Step 5: Terrain accumulation
# -----------------------------------

accumulation = calculate_accumulation(runoff_grid)

print("\nForecast accumulated runoff:")

for row in accumulation:
    print(row)


# -----------------------------------
# Step 6: Drainage
# -----------------------------------

drainage_capacity = 100

excess_water = calculate_excess_water(
    accumulation,
    drainage_capacity
)

print("\nFuture excess water:")

for row in excess_water:
    print(row)


# -----------------------------------
# Step 7: Flood risk
# -----------------------------------

risk_grid = calculate_flood_risk(excess_water)

print("\nFuture flood risk:")

for row in risk_grid:
    print(row)


# -----------------------------------
# Step 8: Flood depth
# -----------------------------------

depth_grid = calculate_flood_depth(
    excess_water,
    depth_factor=0.01
)

print("\nFuture estimated flood depth:")

for row in depth_grid:
    print(row)


# -----------------------------------
# Step 9: Final verification
# -----------------------------------

if forecast == 50:
    print("\nForecast: PASS")
else:
    print("\nForecast: FAIL")


if forecast_runoff == 40:
    print("Runoff: PASS")
else:
    print("Runoff: FAIL")


if accumulation[3][0] == 640:
    print("Terrain accumulation: PASS")
else:
    print("Terrain accumulation: FAIL")


if excess_water[3][0] == 540:
    print("Drainage: PASS")
else:
    print("Drainage: FAIL")


if risk_grid[3][0] == "SEVERE":
    print("Flood risk: PASS")
else:
    print("Flood risk: FAIL")


if depth_grid[3][0] == 5.4:
    print("Flood depth: PASS")
else:
    print("Flood depth: FAIL")


if (
    forecast == 50
    and forecast_runoff == 40
    and accumulation[3][0] == 640
    and excess_water[3][0] == 540
    and risk_grid[3][0] == "SEVERE"
    and depth_grid[3][0] == 5.4
):
    print("\n===================================")
    print("FULL FORECAST → FLOOD TEST: PASS")
    print("===================================")
else:
    print("\nFULL FORECAST → FLOOD TEST: FAIL")