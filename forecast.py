def forecast_rainfall(rainfall_values):
    """
    Forecast rainfall using the average
    of the most recent 3 rainfall values.
    """

    recent_values = rainfall_values[-3:]

    forecast = sum(recent_values) / len(recent_values)

    return forecast


def forecast_next_3_hours(rainfall_values):
    """
    Generate rainfall forecasts for the next 3 hours.
    """

    forecast = forecast_rainfall(rainfall_values)

    forecasts = [
        forecast,
        forecast,
        forecast
    ]

    return forecasts


# Test
if __name__ == "__main__":

    rainfall_values = [40, 60, 80, 90, 70, 50, 30]

    forecasts = forecast_next_3_hours(rainfall_values)

    print("Next 3 hour rainfall forecast:")

    for hour, value in enumerate(forecasts, start=1):
        print("Hour", hour, ":", value, "mm")