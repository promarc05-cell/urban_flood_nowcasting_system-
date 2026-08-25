import sqlite3


def get_rainfall_data():

    connection = sqlite3.connect("flood.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT time, location, rainfall_mm
    FROM rainfall
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def calculate_runoff(rainfall_mm, runoff_coefficient):

    runoff_mm = rainfall_mm * runoff_coefficient

    return runoff_mm


# Get rainfall data from database
rainfall_data = get_rainfall_data()

# Simple prototype coefficient
runoff_coefficient = 0.8


# Calculate runoff for each rainfall record
for time, location, rainfall in rainfall_data:

    runoff = calculate_runoff(rainfall, runoff_coefficient)

    print(
        time,
        location,
        "Rainfall:", rainfall, "mm",
        "Runoff:", runoff, "mm"
    )