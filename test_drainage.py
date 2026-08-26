# test_drainage.py

from drainage import calculate_excess_water


print("Testing drainage...")


# Sample accumulated runoff
accumulation_grid = [
    [20, 50, 80, 120],
    [30, 100, 130, 150],
    [40, 90, 160, 200],
    [10, 70, 110, 180]
]


# Assume drainage can handle 100 mm
drainage_capacity = 100


# Calculate excess water
excess_water = calculate_excess_water(
    accumulation_grid,
    drainage_capacity
)


print("\nAccumulated water:")

for row in accumulation_grid:
    print(row)


print("\nDrainage capacity:", drainage_capacity, "mm")


print("\nExcess water:")

for row in excess_water:
    print(row)


# Expected result
expected = [
    [0, 0, 0, 20],
    [0, 0, 30, 50],
    [0, 0, 60, 100],
    [0, 0, 10, 80]
]


# Verify result
if excess_water == expected:
    print("\nDrainage test: PASS")
else:
    print("\nDrainage test: FAIL")