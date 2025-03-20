import pandas as pd

# Define the list of allowed depth_input values
allowed_depths = [
    0, 0.1, 0.5, 0.51, 1, 1.01, 1.5, 1.51, 2, 2.01, 2.5, 2.51, 3, 3.01, 3.5, 3.51, 4, 4.01, 4.5, 4.51, 5, 5.01, 5.5, 5.51, 6, 6.01, 6.5, 6.51, 7, 7.01, 7.5, 7.51, 8, 8.01, 8.5, 8.51, 9, 9.01, 9.5, 9.51, 10, 10.01, 10.5, 10.51, 11, 11.01, 11.5, 11.51, 12, 12.01, 12.5, 12.51, 13, 13.01, 13.5, 13.51, 14, 14.01, 14.5, 14.51, 15, 15.01, 15.5, 15.51, 16, 16.01, 16.5, 16.51, 17, 17.01, 17.5, 17.51, 18, 18.01, 18.5, 18.51, 19, 19.01, 19.5, 19.51, 20, 20.01, 20.5, 20.51, 21, 21.01, 21.5, 21.51, 22, 22.01, 22.5, 22.51, 23, 23.01, 23.5, 23.51, 24, 24.01, 24.5, 24.51, 25, 25.01, 25.5, 25.51, 26, 26.01, 26.5, 26.51, 27, 27.01, 27.5, 27.51, 28, 28.01, 28.5, 28.51, 29, 29.01, 29.5, 29.51, 30, 30.01
]

# Read the Stacking_results.csv file into a DataFrame
df = pd.read_csv('Stacking_result_SDMT.csv')

# Filter the DataFrame to keep only the rows where depth_input is in the list of allowed values
df_filtered = df[df['depth_input'].isin(allowed_depths)]

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv('Stacking_result_SDMT_downsampled.csv', index=False)