from rainfall import get_rainfall_data


print("Testing rainfall.py...")

# Get rainfall data
data = get_rainfall_data()


# Test 1: Check that data exists
if len(data) > 0:
    print("Rainfall data retrieved: PASS")
else:
    print("Rainfall data retrieved: FAIL")


# Test 2: Check the structure of the first record
if len(data[0]) == 3:
    print("Rainfall record structure: PASS")
else:
    print("Rainfall record structure: FAIL")


# Display the first record
print("First rainfall record:", data[0])