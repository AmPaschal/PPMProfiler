import json

# Read the original JSON file
with open('/usr/local/google/home/pamusuo/Research/PPMProfiler/permission_files/permission_file_default.json') as file:
    original_data = json.load(file)

counts = [1, 3, 5, 10, 15, 20, 30, 40]

for count in counts:

    # Create a new dictionary for modified data
    modified_data = {}

    # Duplicate each key-value pair 100 times and modify the keys
    for key, value in original_data.items():
        modified_data[key] = value
        for i in range(count - 1):
            modified_key = f"{key}_{i}"  # Add an integer to make the key unique
            modified_data[modified_key] = value

    # Write the modified data to a new JSON file
    with open(f'/usr/local/google/home/pamusuo/Research/PPMProfiler/permission_files/permission_file_{count}.json', 'w') as file:
        json.dump(modified_data, file, indent=4)

    print(f"{count} JSON file created successfully.")
