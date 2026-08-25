from terrain import dem

print("\nTesting terrain...")

# Find the lowest elevation
lowest = min(min(row) for row in dem)

print("Lowest elevation:", lowest, "m")

if lowest == 90:
    print("Terrain test passed!")
else:
    print("Terrain test failed!")