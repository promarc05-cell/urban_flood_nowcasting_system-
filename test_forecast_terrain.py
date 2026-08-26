from forecast import forecast_rainfall
from runoff import calculate_runoff
from terrain import calculate_accumulation


print("Testing forecast → runoff → terrain...")


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
# Step 3: Calculate forecast runoff
# -----------------------------------

runoff_coefficient = 0.8

forecast_runoff = calculate_runoff(
    forecast,
    runoff_coefficient
)

print("Forecast runoff:", forecast_runoff, "mm")


# -----------------------------------
# Step 4: Create runoff grid
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
# Step 5: Calculate terrain accumulation
# -----------------------------------

accumulation = calculate_accumulation(runoff_grid)


print("\nForecast accumulated runoff:")

for row in accumulation:
    print(row)


# -----------------------------------
# Step 6: Verify
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


if (
    forecast == 50
    and forecast_runoff == 40
    and accumulation[3][0] == 640
):
    print("\nFORECAST → RUNOFF → TERRAIN TEST: PASS")
else:
    print("\nFORECAST → RUNOFF → TERRAIN TEST: FAIL")