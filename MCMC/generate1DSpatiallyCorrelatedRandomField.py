import numpy as np
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from vs_calc import VsProfile, vs30_correlations
def generate_spatially_correlated_field(depths, num_realizations, correlation_length, mean=0, std_dev=45):
    """
    Generates spatially correlated 1D random fields using Cholesky decomposition.

    Parameters:
        depths (numpy array): Depth values in meters.
        num_realizations (int): Number of realizations to generate.
        correlation_length (float): Correlation length (controls spatial continuity).
        mean (float): Mean of the random field.
        std_dev (float): Standard deviation of the random field.

    Returns:
        numpy array: A (num_realizations x len(depths)) array of random field realizations.
    """
    num_points = len(depths)

    # Compute the correlation matrix using an exponential model
    correlation_matrix = np.exp(-np.abs(np.subtract.outer(depths, depths)) / correlation_length)

    # Perform Cholesky decomposition
    L = np.linalg.cholesky(correlation_matrix)

    # Generate independent standard normal random variables
    uncorrelated_random_fields = np.random.randn(num_realizations, num_points)

    # Apply correlation via Cholesky decomposition
    correlated_fields = mean + std_dev * (uncorrelated_random_fields @ L.T)

    return correlated_fields

# Define depth range
depths = np.linspace(0, 30, 3001)  # Depths from 0 to 30m with 0.01m increments
print(depths)

# Generate 100 realizations
random_fields = generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=250)
print(random_fields)

# Load the 'Depth' and 'Andrus-P Vs' columns from the CSV file
filename = 'SCPT_195188.csv'
data = pd.read_csv(filename, usecols=['Depth', 'Andrus-P Vs'])

# Interpolate the random fields to match the depths in the CSV file
matched_random_fields = np.array([np.interp(data['Depth'], depths, random_fields[i, :]) for i in range(random_fields.shape[0])]).T

# Create a new DataFrame with the matched depths and interpolated random fields
matched_data = pd.DataFrame(matched_random_fields, columns=[f'Random_Field_{i}' for i in range(random_fields.shape[0])])
matched_data['Depth'] = data['Depth']

# Merge the matched data with the original data
merged_data = pd.merge(data, matched_data, on='Depth')

# Add the values of the second column to 'Andrus-P Vs' for other columns excepting depths column
for i in range(1, random_fields.shape[0]):
    merged_data[f'Andrus-P Vs_{i}'] = merged_data['Andrus-P Vs'] + merged_data[f'Random_Field_{i}']
merged_data = merged_data.drop(columns=merged_data.filter(like='Random_Field_').columns)
print(merged_data)

# Calculate the minimum and maximum values for all columns except 'Depth'
min_values = merged_data.drop(columns=['Depth']).min(axis=1)
max_values = merged_data.drop(columns=['Depth']).max(axis=1)

# Create new arrays for minimum and maximum values
min_array = np.column_stack((merged_data['Depth'], min_values))
max_array = np.column_stack((merged_data['Depth'], max_values))
data_origin = pd.read_csv('SCPT_195188.csv', usecols=['Depth', 'Andrus-P Vs'])

plt.figure(figsize=(6, 10))
plt.plot(min_array[:, 1], min_array[:, 0], color='grey', linestyle='--', label='Minimum Values')
plt.plot(max_array[:, 1], max_array[:, 0], color='grey',linestyle='--', label='Maximum Values')

# Plot the minimum and maximum values
plt.plot(data_origin['Andrus-P Vs'], data_origin['Depth'], color='red', label='Original Data')
plt.xlabel('Andrus-P Vs')
plt.ylabel('Depth (m)')
plt.title('Minimum and Maximum Values Plot')
plt.gca().invert_yaxis()  # Invert y-axis to match depth convention
plt.legend()
plt.savefig('min_max_values_plot.png')
plt.show()
plt.close()
# Directory to save CSV files
save_path = f'vs_profiles for {filename}'
os.makedirs(save_path, exist_ok=True)

# Loop to save Depth and Vs pairs into separate CSV files
for col in merged_data.columns:
    if col != 'Depth':
        output_df = merged_data[['Depth', col]]
        output_df.columns = ['d', 'vs']
        output_df.to_csv(os.path.join(save_path, f'depth_vs_{col}.csv'), index=False)
        print(f'Saved {os.path.join(save_path, f"depth_vs_{col}.csv")}')


examples_dir = Path(save_path)
import os

# Remove the existing file if it exists
result_file_path = examples_dir / 'vsz_estimation.csv'
#result_file_path = examples_dir / 'vs30_estimation.csv'
if os.path.exists(result_file_path):
    os.remove(result_file_path)

for file_path in examples_dir.glob('*.csv'):
    file_name = file_path.stem
    try:
        # Create VsProfile objects from the CPT file
        vs_profile = VsProfile.from_file2(file_path, file_name)
        vsz = vs_profile.calc_vsz()
        #vs30 = vs30_correlations.boore_2004(vs_profile)[0]

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        continue

    with open(result_file_path, 'a') as output_file:
        output_file.write(f"{file_name},{vsz}\n")
        #output_file.write(f"{file_name},{vs30}\n")

# Load the Vs30 values from the CSV file
vsz_data = pd.read_csv(f'vs_profiles for {filename}/vsz_estimation.csv', header=None, names=['File', 'Vsz'])
plt.hist(vsz_data['Vsz'], bins=30)
std = np.log(vsz_data['Vsz']).std()
plt.text(0.5, 0.5, f"Standard Deviation of Vsz values: {std}", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
print(f"Standard Deviation of Vsz values: {std}")

plt.xlabel('Vsz (m/s)')
plt.ylabel('Counts')
plt.title('Vsz Histogram')
plt.savefig('vsz_histogram.png')

#vs30_data = pd.read_csv(f'vs_profiles for {filename}/vs30_estimation.csv', header=None, names=['File', 'Vs30'])
#std = np.log(vs30_data['Vs30']).std()
#print(f"Standard Deviation of Vs30 values: {std}")
