import sqlite3

connection = sqlite3.connect("flood.db")
cursor = connection.cursor()

# Create rainfall table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rainfall (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    location TEXT,
    rainfall_mm REAL
)
""")

# Check whether data already exists
cursor.execute("SELECT COUNT(*) FROM rainfall")
count = cursor.fetchone()[0]

# Insert sample data only if table is empty
if count == 0:

    rainfall_data = [
        ("10:00", "Area A", 40),
        ("10:30", "Area A", 60),
        ("11:00", "Area A", 80),
        ("11:30", "Area A", 90),
        ("12:00", "Area A", 70),
        ("12:30", "Area A", 50),
        ("13:00", "Area A", 30)
    ]

    cursor.executemany("""
    INSERT INTO rainfall (time, location, rainfall_mm)
    VALUES (?, ?, ?)
    """, rainfall_data)

    print("Rainfall data inserted successfully!")

else:
    print("Rainfall data already exists. No new data inserted.")

connection.commit()
connection.close()