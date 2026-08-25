from rainfall import get_rainfall_data
from runoff import calculate_runoff


print("Testing runoff.py...")


# Get rainfall data from database
rainfall_data = get_rainfall_data()


# Use the same coefficient as our prototype
runoff_coefficient = 0.8


# Test the calculation itself
test_runoff = calculate_runoff(80, runoff_coefficient)

if test_runoff == 64:
    print("Runoff calculation test: PASS")
else:
    print("Runoff calculation test: FAIL")


# Test runoff using database rainfall data
time, location, rainfall = rainfall_data[0]

runoff = calculate_runoff(rainfall, runoff_coefficient)

print("\nFirst rainfall record:")
print("Time:", time)
print("Location:", location)
print("Rainfall:", rainfall, "mm")
print("Runoff:", runoff, "mm")


# Check that runoff was calculated
if runoff == rainfall * runoff_coefficient:
    print("Database rainfall → runoff: PASS")
else:
    print("Database rainfall → runoff: FAIL")