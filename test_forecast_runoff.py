from forecast import forecast_rainfall
from runoff import calculate_runoff


print("Testing forecast to runoff...")


# Historical rainfall
rainfall_values = [
    40,
    60,
    80,
    90,
    70,
    50,
    30
]


# Step 1: Forecast rainfall
forecast = forecast_rainfall(rainfall_values)

print("\nForecast rainfall:", forecast, "mm")


# Step 2: Convert forecast rainfall into runoff
runoff = calculate_runoff(forecast, 0.8)

print("Forecast runoff:", runoff, "mm")


# Expected values
expected_forecast = 50
expected_runoff = 40


# Verify forecast
if forecast == expected_forecast:
    print("\nForecast calculation: PASS")
else:
    print("\nForecast calculation: FAIL")


# Verify runoff
if runoff == expected_runoff:
    print("Runoff calculation: PASS")
else:
    print("Runoff calculation: FAIL")


# Verify complete connection
if forecast == expected_forecast and runoff == expected_runoff:
    print("\nFORECAST → RUNOFF TEST: PASS")
else:
    print("\nFORECAST → RUNOFF TEST: FAIL")