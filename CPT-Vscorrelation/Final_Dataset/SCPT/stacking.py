import os
import pandas as pd

# Define the input and search folders
input_folder = './Result_VsProfiles_over14_Upsampled'
search_folder = './EstimateVs_CPT'
output_file = './Stacking_result.csv'
unmatched_depths_file = './Unmatched_depths.txt'

# List to store the results
results = []

# List to store unmatched depths
unmatched_depths = []

# Iterate through the files in the input folder
for input_filename in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, input_filename)
    input_base_name = os.path.basename(input_file_path)

    # Ignore parts of the filename after the second underscore
    parts = input_base_name.split('_')
    if len(parts) > 2:
        input_base_name = '_'.join(parts[:2]) + '.csv'

    # Flag to check if a match is found
    match_found = False

    # Iterate through the files in the search folder
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            # Ignore parts of the filename after the second underscore
            search_parts = file.split('_')
            if len(search_parts) > 2:
                search_base_name = '_'.join(search_parts[:2]) + '.csv'
            else:
                search_base_name = file

            if search_base_name == input_base_name:
                matching_file_path = os.path.join(root, file)

                # Read both files into DataFrames
                df_input = pd.read_csv(input_file_path)
                df_matching = pd.read_csv(matching_file_path)

                # Set the headers for each DataFrame
                df_input.columns = ['depth_input', 'vs_input']
                df_matching.columns = ['Depth', 'Qc', 'Fc', 'u', 'Hegazy Vs', 'Andrus-H Vs', 'Andrus-P Vs', 'Rob Vs', 'Mc15 Vs', 'Mc18 Vs']

                # Find rows in df_matching where depth_input matches Depth
                for _, row in df_input.iterrows():
                    matching_rows = df_matching[df_matching['Depth'] == row['depth_input']]
                    if not matching_rows.empty:
                        for _, match in matching_rows.iterrows():
                            if pd.notna(match['Mc15 Vs']):
                                results.append({
                                    'File Name': input_filename,
                                    'depth_input': row['depth_input'],
                                    'vs_input': row['vs_input'],
                                    'Depth': match['Depth'],
                                    'Qc': match['Qc'],
                                    'Fc': match['Fc'],
                                    'u': match['u'],
                                    'Hegazy Vs': match['Hegazy Vs'],
                                    'Andrus-H Vs': match['Andrus-H Vs'],
                                    'Andrus-P Vs': match['Andrus-P Vs'],
                                    'Rob Vs': match['Rob Vs'],
                                    'Mc15 Vs': match['Mc15 Vs'],
                                    'Mc18 Vs': match['Mc18 Vs']
                                })
                    else:
                        unmatched_depths.append(f"No matching depth found for depth: {row['depth_input']} in file: {input_filename}")
                match_found = True
                break
        if match_found:
            break

    # If no match is found, print the input file name
    if not match_found:
        print(f"No match found for file: {input_filename}")

# Save the results to a CSV file
df_results = pd.DataFrame(results)
df_results.to_csv(output_file, index=False)

# Save the unmatched depths to a text file
with open(unmatched_depths_file, 'w') as f:
    for item in unmatched_depths:
        f.write("%s\n" % item)

# Load the CSV file into a DataFrame
df = pd.read_csv(output_file)

# Get the number of unique filenames in the 'File Name' column
unique_filenames = df['File Name'].nunique()

print(f'There are {unique_filenames} unique filenames in the "File Name" column.')