import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gstools as gs
import warnings
from scipy.spatial.distance import pdist, squareform

warnings.filterwarnings('ignore')

# Load the data
data = pd.read_csv('Stacking_results_ANDMC1518_RES.csv')

# Extract the 'depth_input' and 'RES' columns
depth = data['depth_input'].values
ze = np.zeros_like(depth)  # Set y coordinates to 0 for 2D coordinates
coords = np.column_stack((depth, ze)).T  # gstools requires coordinates in (2, n) shape
values = data['RES'].values

# Set the semivariogram model to use (e.g., Spherical)
model_name = 'Spherical'

# Calculate distances between data pairs
distances = pdist(coords.T)

# Custom binning function to calculate bin centers and edges
def equal_count_binning(distances, n_bins):
    sorted_distances = np.sort(distances)
    n_pairs = len(sorted_distances)
    pairs_per_bin = n_pairs // n_bins

    bin_edges = [sorted_distances[i * pairs_per_bin] for i in range(n_bins)]
    bin_edges.append(sorted_distances[-1])

    bin_centers = 0.5 * (np.array(bin_edges[:-1]) + np.array(bin_edges[1:]))
    return bin_centers, bin_edges

try:
    # Calculate distances
    distances = pdist(coords.T)
    # Calculate bin centers and edges using custom binning function
    n_bins = 60
    bin_center, bin_edges = equal_count_binning(distances, n_bins)

    # Calculate the experimental semivariogram
    gamma = gs.vario_estimate(
        pos=coords,  # Coordinates in (2, n) shape
        field=values,  # Data values
        bin_edges=bin_edges,  # Custom bin edges
        estimator='matheron'  # Method for calculating the experimental semivariogram
    )

    # Create the semivariogram model (using gstools models)
    model = gs.Spherical(dim=1)  # 1D data

    # Fit the model
    model.fit_variogram(bin_center, gamma)

    # Calculate the theoretical semivariogram
    theoretical = model.variogram(bin_center)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(bin_center, gamma, 'o', label=f'{model_name} - Experimental')
    plt.plot(bin_center, theoretical, '-', label=f'{model_name} - Theoretical')
    plt.axvline(x=model.len_scale, color='r', linestyle='--', label=f'Correlation Depth (Range) = {model.len_scale:.2f}')
    plt.title(f'Semivariogram - {model_name} (Equal Count Bins)')
    plt.xlabel('Lag Distance (Depth)')
    plt.ylabel('Semivariance')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Model {model_name} fitted successfully.")
    print(f"Nugget: {model.nugget}")
    print(f"Sill: {model.sill}")
    print(f"Correlation Depth (Range): {model.len_scale}")

    # Check the number of pairs in each bin
    hist, _ = np.histogram(distances, bins=bin_edges)
    print("\nNumber of pairs in each bin:")
    for i, count in enumerate(hist):
        print(f"Bin {i+1}: {count} pairs")
except Exception as e:
    print(f"Error with model {model_name}: {e}")