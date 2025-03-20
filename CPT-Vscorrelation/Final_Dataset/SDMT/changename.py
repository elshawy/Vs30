import os
import pandas as pd
import shutil

# Define the input and output folders
input_folder = './ESTIMATED_VS_CPT'
output_folder = './ESTIMATED_VS_CPT_processed'
reference_csv_path = './out_test_sdmt_trans.csv'

# Read the reference CSV file into a DataFrame
reference_df = pd.read_csv(reference_csv_path)

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the files in the input folder
for input_filename in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, input_filename)

    # Ignore parts of the filename after the second underscore
    parts = input_filename.split('_')
    if len(parts) > 2:
        input_filename = '_'.join(parts[:2]) + '.csv'

    # Check if the filename matches any entry in the reference DataFrame
    for _, row in reference_df.iterrows():
        if row.iloc[1] == input_filename.replace('.csv', ''):
            # Replace the filename with the value in the second column and remove .csv extension
            new_filename = row.iloc[0]
            output_file_path = os.path.join(output_folder, new_filename + '.csv')
            shutil.copy(input_file_path, output_file_path)
            print(f"Previous name: {input_filename}, New name: {new_filename}.csv")
            break
    else:
        # If no match is found, print a message
        print(f"No match found for file: {input_filename}")