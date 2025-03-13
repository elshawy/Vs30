import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=250, mean=0, std_dev=np.log1p(45)):
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
depths = np.linspace(0, 30, 3001)  # Depths from 0 to 30m with 1m increments
print(depths)

# Generate 100 realizations
random_fields = generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=250)
print(random_fields)

# Load the 'Depth' and 'Andrus-P Vs' columns from the CSV file
data = pd.read_csv('SCPT_195188.csv', usecols=['Depth', 'Andrus-P Vs'])
data['Andrus-P Vs'] = np.log(data['Andrus-P Vs'])

# Interpolate the random fields to match the depths in the CSV file
matched_random_fields = np.array([np.interp(data['Depth'], depths, random_fields[i, :]) for i in range(random_fields.shape[0])]).T


# Create a new DataFrame with the matched depths and interpolated random fields
matched_data = pd.DataFrame(matched_random_fields, columns=[f'Random_Field_{i}' for i in range(random_fields.shape[0])])
matched_data['Depth'] = data['Depth']

# Merge the matched data with the original data
merged_data = pd.merge(data, matched_data, on='Depth')

# Add the values of the second column to 'Andrus-P Vs' for other columns excepting depths column
for i in range(1, random_fields.shape[0]):
    merged_data[f'Andrus-P Vs_{i}'] = merged_data['Andrus-P Vs'] + (merged_data['Andrus-P Vs'] * merged_data[f'Random_Field_{i}'])

merged_data = merged_data.drop(columns=merged_data.filter(like='Random_Field_').columns)
print(merged_data)

# Calculate the standard deviation at each depth for the original data within merged_data
std_values = merged_data.drop(columns=['Depth']).std(axis=1)

print("Standard deviation at each depth:")
print(std_values)


# Calculate the minimum and maximum values for all columns except 'Depth'
min_values = np.exp(merged_data.drop(columns=['Depth']).min(axis=1))
max_values = np.exp(merged_data.drop(columns=['Depth']).max(axis=1))

# Create new arrays for minimum and maximum values
min_array = np.column_stack((merged_data['Depth'], min_values))
max_array = np.column_stack((merged_data['Depth'], max_values))

print("Minimum values array:")
print(min_array)
print("Maximum values array:")
print(max_array)
data_origin = pd.read_csv('SCPT_195188.csv', usecols=['Depth', 'Andrus-P Vs'])

# Plot the minimum and maximum values
plt.figure(figsize=(6, 10))
plt.plot(min_array[:, 1], min_array[:, 0], color='grey', linestyle='--', label='Minimum Values')
plt.plot(max_array[:, 1], max_array[:, 0], color='grey',linestyle='--', label='Maximum Values')
plt.plot(data_origin['Andrus-P Vs'], data_origin['Depth'], color='red', label='Original Data')
plt.xlabel('Andrus-P Vs')
plt.ylabel('Depth (m)')
plt.title('Minimum and Maximum Values Plot')
plt.gca().invert_yaxis()  # Invert y-axis to match depth convention
plt.legend()
plt.show()