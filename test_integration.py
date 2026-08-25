from terrain import dem, get_flow_direction, calculate_accumulation
from drainage import calculate_excess_water


print("Testing full runoff-terrain-drainage pipeline...")


# -----------------------------------
# Step 1: Create runoff grid
# -----------------------------------

runoff_grid = [
    [10, 10, 10, 10],
    [10, 10, 10, 10],
    [10, 10, 10, 10],
    [10, 10, 10, 10]
]

print("\nRunoff grid:")

for row in runoff_grid:
    print(row)


# -----------------------------------
# Step 2: Calculate terrain accumulation
# -----------------------------------

accumulation = calculate_accumulation(runoff_grid)

print("\nAccumulated runoff:")

for row in accumulation:
    print(row)


# -----------------------------------
# Step 3: Apply drainage
# -----------------------------------

drainage_capacity = 100

excess_water = calculate_excess_water(
    accumulation,
    drainage_capacity
)

print("\nDrainage capacity:", drainage_capacity)

print("\nExcess water:")

for row in excess_water:
    print(row)


# -----------------------------------
# Step 4: Verify pipeline
# -----------------------------------

if accumulation[3][0] == 160:
    print("\nTerrain accumulation: PASS")
else:
    print("\nTerrain accumulation: FAIL")


if excess_water[3][0] == 60:
    print("Drainage calculation: PASS")
else:
    print("Drainage calculation: FAIL")


if accumulation[3][0] == 160 and excess_water[3][0] == 60:
    print("\nFULL PIPELINE TEST: PASS")
else:
    print("\nFULL PIPELINE TEST: FAIL")