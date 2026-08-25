import sqlite3
import os


# Check whether database file exists
if os.path.exists("flood.db"):
    print("Database file exists: PASS")
else:
    print("Database file exists: FAIL")


# Connect to database
connection = sqlite3.connect("flood.db")
cursor = connection.cursor()


# Check whether rainfall table exists
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table' AND name='rainfall'
""")

table = cursor.fetchone()


if table:
    print("Rainfall table exists: PASS")
else:
    print("Rainfall table exists: FAIL")


# Check whether rainfall data exists
cursor.execute("SELECT COUNT(*) FROM rainfall")

count = cursor.fetchone()[0]


if count > 0:
    print("Rainfall data exists: PASS")
    print("Number of rainfall records:", count)
else:
    print("Rainfall data exists: FAIL")


connection.close()