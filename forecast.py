def forecast_rainfall(rainfall_values):
    """
    Forecast rainfall using the average of the
    most recent 3 rainfall observations.
    """

    if len(rainfall_values) == 0:
        return 0

    recent_values = rainfall_values[-3:]

    forecast = sum(recent_values) / len(recent_values)

    return forecast


def forecast_next_3_hours(rainfall_values):
    """
    Generate a simple trend-aware rainfall forecast
    for the next 3 hours.

    The recent average is used as the baseline.
    A fraction of the recent rainfall trend is then
    applied to each future hour.
    """

    if len(rainfall_values) == 0:
        return [0, 0, 0]

    baseline = forecast_rainfall(rainfall_values)

    if len(rainfall_values) >= 2:

        latest = rainfall_values[-1]
        previous = rainfall_values[-2]

        trend = latest - previous

    else:

        trend = 0

    forecasts = []

    for hour in range(1, 4):

        # Apply only 25% of the recent trend per hour.
        forecast = baseline + (trend * 0.25 * hour)

        # Rainfall cannot be negative.
        forecast = max(forecast, 0)

        forecasts.append(forecast)

    return forecasts


# Test
if __name__ == "__main__":

    rainfall_values = [40, 60, 80, 90, 70, 50, 30]

    forecasts = forecast_next_3_hours(rainfall_values)

    print("Next 3 hour rainfall forecast:")

    for hour, value in enumerate(forecasts, start=1):

        print(
            "Hour",
            hour,
            ":",
            round(value, 2),
            "mm"
        )