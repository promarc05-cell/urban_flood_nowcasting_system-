import sqlite3
import requests
from datetime import datetime

def update_rainfall_from_api(db_path="flood.db"):
    """
    Fetches the last 6 hours of real precipitation data from Open-Meteo API
    and updates the SQLite database.
    """
    # Change these three variables to test different cities!
    city_name = "Mumbai"
    lat = 19.07
    lon = 72.87
    
    # Open-Meteo URL
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&past_hours=6&hourly=precipitation&timezone=auto"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        times = data['hourly']['time'][:7]
        precip = data['hourly']['precipitation'][:7]
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM rainfall")
        
        for t, p in zip(times, precip):
            dt = datetime.fromisoformat(t).strftime('%Y-%m-%d %H:%M')
            cursor.execute(
                "INSERT INTO rainfall (time, location, rainfall_mm) VALUES (?, ?, ?)",
                (dt, city_name, p)  # <-- Now it uses the dynamic city name
            )
            
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"⚠️ Error fetching API data (falling back to existing DB data): {e}")


def get_rainfall_data(db_path="flood.db"):
    """
    Updates the database with live data, then retrieves records in chronological order.
    Returns the exact tuple format expected by main.py: (time, location, rainfall_mm)
    """
    # 1. Fetch fresh data and update DB
    update_rainfall_from_api(db_path)
    
    # 2. Read from DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # We must select all 3 columns to keep main.py happy!
    cursor.execute("SELECT time, location, rainfall_mm FROM rainfall ORDER BY time ASC")
    rows = cursor.fetchall()
    conn.close()
    
    return rows

# Test the API independently
if __name__ == "__main__":
    print("Fetching live data from Open-Meteo...")
    live_data = get_rainfall_data()
    print("Live data format:")
    for row in live_data:
        print(row)