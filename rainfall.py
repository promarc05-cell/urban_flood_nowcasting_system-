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


# Test
if __name__ == "__main__":

    rainfall_data = get_rainfall_data()

    for row in rainfall_data:
        print(row)