from terrain import dem, get_flow_direction

print("\nTesting terrain...")

# Test 1: Find the lowest elevation
lowest = min(min(row) for row in dem)

print("Lowest elevation:", lowest, "m")

if lowest == 90:
    print("Lowest elevation test: PASS")
else:
    print("Lowest elevation test: FAIL")


# Test 2: Test flow direction
# Cell (1,1) has elevation 100 m
flow = get_flow_direction(1, 1)

print("Cell (1,1) elevation:", dem[1][1])
print("Water flows toward:", flow)

# The lowest neighboring cell is (2,0), with elevation 95 m
if flow == (2, 0):
    print("Flow direction test: PASS")
else:
    print("Flow direction test: FAIL")