import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=250, mean=0, std_dev=45):
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
random_fields = generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=2.5)
print(random_fields)

# Load the 'Depth' and 'Andrus-P Vs' columns from the CSV file
data = pd.read_csv('SCPT_195188.csv', usecols=['Depth', 'Andrus-P Vs'])

# Match depths and add values of the second column to 'Andrus-P Vs'
matched_vs = np.interp(data['Depth'], depths, random_fields[1, :])  # Use the second realization (index 1)
data['Andrus-P Vs'] += matched_vs

print(data)