import os
import pandas as pd
from geopy.distance import geodesic

folder_path = './'
reference_file = 'Geonet Metadata Summary_v1.4.csv'
distance_threshold = 5

def is_within_distance(coord1, coord2, threshold):
    return geodesic(coord1, coord2).meters <= threshold

results = []

# Load the reference file
reference_df = pd.read_csv(os.path.join(folder_path, reference_file), delimiter=',')
reference_coordinates = reference_df[['Latitude', 'Longitude', 'Vs30']].values

# Collect all coordinates and Vs30 values from all other CSV files
all_coordinates = []

for file_name in os.listdir(folder_path):
    if file_name.endswith('*.csv') and file_name != reference_file:
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, delimiter=',')
        if 'Latitude' in df.columns and 'Longitude' in df.columns and 'Vs30' in df.columns:
            coordinates = df[['Latitude', 'Longitude', 'Vs30']].values
            for coord in coordinates:
                all_coordinates.append((file_name, coord))
        else:
            print(f"File {file_name} does not contain 'Latitude', 'Longitude', and 'Vs30' columns")

# Compare reference coordinates with all other coordinates
for i, ref_coord in enumerate(reference_coordinates):
    for file_name, coord in all_coordinates:
        if is_within_distance(ref_coord[:2], coord[:2], distance_threshold):
            results.append((reference_file, ref_coord, file_name, coord))
    # Check progress
    if (i + 1) % 10 == 0 or (i + 1) == len(reference_coordinates):
        print(f"Processed {i + 1} out of {len(reference_coordinates)} reference coordinates")

# Write results to an output CSV file
output_file = 'results_noFoster.csv'
with open(output_file, 'w') as f:
    f.write('File1,Latitude1,Longitude1,Vs30_1,File2,Latitude2,Longitude2,Vs30_2\n')
    for result in results:
        file1, coord1, file2, coord2 = result
        if coord1[2] == coord2[2]:  # Check if Vs30_1 and Vs30_2 are different
            f.write(f"{file1},{coord1[0]},{coord1[1]},{coord1[2]},{file2},{coord2[0]},{coord2[1]},{coord2[2]}\n")