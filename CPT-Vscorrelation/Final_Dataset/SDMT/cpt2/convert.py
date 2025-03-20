import os
import pandas as pd

input_folder = './'
output_folder = './csv_output_folder'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        txt_file_path = os.path.join(input_folder, filename)

        # Extract the part of the filename before the second underscore
        base_name = filename.split('_')[0] + '_' + filename.split('_')[1]
        csv_file_path = os.path.join(output_folder, base_name + ".csv")

        # Read the content of the .txt file
        df = pd.read_csv(txt_file_path, delimiter=',')  # Adjust delimiter if needed

        # Save the DataFrame to a .csv file
        df.to_csv(csv_file_path, index=False)
