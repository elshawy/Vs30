import numpy as np
import matplotlib.pyplot as plt

def generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=2.5, mean=0, std_dev=1):
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
depths = np.linspace(0, 30, 61)  # Depths from 0 to 30m with 1m increments
print(depths)
# Generate 100 realizations
random_fields = generate_spatially_correlated_field(depths, num_realizations=100, correlation_length=2.5)

# Plot some realizations
plt.figure(figsize=(4, 6))
for i in range(1):  # Plot 2 sample realizations
    plt.plot(random_fields[i, :], depths, label=f'Realization {i+1}')
plt.xlabel("Random Field Value")
plt.ylabel("Depth (m)")
plt.title("Sample Realizations of 1D Spatially Correlated Random Field")
plt.grid(which="both")
plt.xlim(-3,3)
plt.ylim(0,30)
plt.legend()
plt.gca().invert_yaxis()  # Invert y-axis to match depth convention
plt.show()
#plt.savefig("1D_field.png",dpi=200)
