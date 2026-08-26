from forecast import forecast_rainfall
from runoff import calculate_runoff
from terrain import calculate_accumulation
from drainage import calculate_excess_water


print("Testing forecast → runoff → terrain → drainage...")


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
# Step 4: Create future runoff grid
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
# Step 6: Apply drainage
# -----------------------------------

drainage_capacity = 100

excess_water = calculate_excess_water(
    accumulation,
    drainage_capacity
)

print("\nDrainage capacity:", drainage_capacity, "mm")

print("\nFuture excess water:")

for row in excess_water:
    print(row)


# -----------------------------------
# Step 7: Verify
# -----------------------------------

if forecast == 50:
    print("\nForecast calculation: PASS")
else:
    print("\nForecast calculation: FAIL")


if forecast_runoff == 40:
    print("Forecast runoff calculation: PASS")
else:
    print("Forecast runoff calculation: FAIL")


if accumulation[3][0] == 640:
    print("Terrain accumulation: PASS")
else:
    print("Terrain accumulation: FAIL")


if excess_water[3][0] == 540:
    print("Drainage calculation: PASS")
else:
    print("Drainage calculation: FAIL")


if (
    forecast == 50
    and forecast_runoff == 40
    and accumulation[3][0] == 640
    and excess_water[3][0] == 540
):
    print("\nFORECAST → RUNOFF → TERRAIN → DRAINAGE TEST: PASS")
else:
    print("\nFORECAST → RUNOFF → TERRAIN → DRAINAGE TEST: FAIL")