# test_flood.py

from flood import calculate_flood_risk


print("Testing flood risk...")


# Sample excess-water grid
excess_water = [
    [0, 20, 50, 60],
    [0, 30, 75, 100],
    [10, 50, 101, 150],
    [0, 1, 40, 200]
]


# Calculate flood risk
risk_grid = calculate_flood_risk(excess_water)


print("\nExcess water:")

for row in excess_water:
    print(row)


print("\nFlood risk:")

for row in risk_grid:
    print(row)


# Expected result
expected = [
    ["LOW", "MEDIUM", "MEDIUM", "HIGH"],
    ["LOW", "MEDIUM", "HIGH", "HIGH"],
    ["MEDIUM", "MEDIUM", "SEVERE", "SEVERE"],
    ["LOW", "MEDIUM", "MEDIUM", "SEVERE"]
]


# Test result
if risk_grid == expected:
    print("\nFlood risk test: PASS")
else:
    print("\nFlood risk test: FAIL")