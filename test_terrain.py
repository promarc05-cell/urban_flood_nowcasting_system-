from terrain import (
    dem,
    get_flow_direction,
    calculate_accumulation,
    calculate_runoff_accumulation
)


print("\nTesting terrain...")


# Test 1: Find the lowest elevation

lowest = min(min(row) for row in dem)

print("Lowest elevation:", lowest, "m")

if lowest == 90:
    print("Lowest elevation test: PASS")
else:
    print("Lowest elevation test: FAIL")


# Test 2: Test flow direction

flow = get_flow_direction(1, 1)

print("Cell (1,1) elevation:", dem[1][1])
print("Water flows toward:", flow)

if flow == (2, 0):
    print("Flow direction test: PASS")
else:
    print("Flow direction test: FAIL")


# Test 3: Test basic water accumulation

runoff_grid = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]

accumulation = calculate_accumulation(runoff_grid)

print("\nWater accumulation:")

for row in accumulation:
    print(row)

if accumulation[3][0] == 16:
    print("Water accumulation test: PASS")
else:
    print("Water accumulation test: FAIL")


# Test 4: Test runoff-based accumulation

print("\nTesting runoff accumulation...")

runoff_grid = [
    [10, 10, 10, 10],
    [10, 10, 10, 10],
    [10, 10, 10, 10],
    [10, 10, 10, 10]
]


# Create flow-direction grid

flow_directions = []

for r in range(len(dem)):

    row = []

    for c in range(len(dem[0])):

        row.append(get_flow_direction(r, c))

    flow_directions.append(row)


# Calculate runoff accumulation

accumulation = calculate_runoff_accumulation(
    runoff_grid,
    flow_directions
)


print("\nRunoff accumulation:")

for row in accumulation:
    print(row)


# Check that runoff accumulation was calculated

# The lowest cell should receive runoff from all 16 cells.
expected_accumulation = 16 * 10

if accumulation[3][0] == expected_accumulation:
    print("Runoff accumulation test: PASS")
else:
    print("Runoff accumulation test: FAIL")