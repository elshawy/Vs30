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
models = ['spherical', 'exponential', 'gaussian', 'matern', 'stable', 'cubic']

# Plotting variograms with different models
print("Plotting variograms with different models...")

for model in models:
    V = Variogram(coordinates, res, n_lags=100, model=model, normalize=False, bin_func=uniform_count_lags)
    V.fit()

    plt.figure(figsize=(8, 6))
    V.plot(hist=True, show=False)
    #plt.ylim(0.0, max(V.experimental))
    plt.title(f'Model: {model}\nRMSE: {V.rmse:.2f}')
    print(f"Model: {model}", f"Model parameters: {V.parameters}", f"RMSE: {V.rmse}")
    plt.savefig(f'variogram_uniformcounts_{model}.png', dpi=600)
    plt.show()