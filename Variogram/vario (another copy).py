import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skgstat import Variogram
from skgstat.binning import even_width_lags
from skgstat.binning import uniform_count_lags

# Load the data
print("Loading data...")
data = pd.read_csv('Stacking_results_ANDMC1518_RES.csv')

# Extract the 'depth_input' and 'RES' columns
print("Extracting coordinates and values...")
depth = data['depth_input'].values
res = data['RES'].values

# Create a spatial field
print("Creating spatial field...")
coordinates = np.column_stack((depth, np.zeros_like(depth)))  # Use depth as the spatial coordinate
print(coordinates)

# List of models to iterate over
models = [10, 20, 30, 40, 50, 60,70, 80, 90, 100]

# Plotting variograms with different models
print("Plotting variograms with different models...")

for model in models:
    V = Variogram(coordinates, res, n_lags=model, model='exponential', normalize=False, bin_func=uniform_count_lags)

    plt.figure(figsize=(8, 6))
    lags = V.bins
    experimental = V.experimental
    plt.plot(lags, experimental, 'o', label='Experimental Variogram')
    #plt.hist(lags, bins=model, alpha=0.3, label='Histogram')
    plt.grid(True)
    plt.title(f'Model : Exponential N: {model}\nRMSE: {V.rmse:.2f}')
    print(f"Model: {model}", f"Model parameters: {V.parameters}", f"RMSE: {V.rmse}")
    plt.savefig(f'variogram_uniformcount_{model}.png', dpi=600)
    plt.show()