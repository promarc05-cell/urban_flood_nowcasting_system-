from forecast import forecast_rainfall


rainfall = [40, 60, 80, 90, 70, 50, 30]

forecast = forecast_rainfall(rainfall)

print("Forecast rainfall:", forecast)

if forecast == 50:
    print("Forecast test: PASS")
else:
    print("Forecast test: FAIL")