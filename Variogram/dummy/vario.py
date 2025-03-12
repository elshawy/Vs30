import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skgstat import Variogram
from skgstat.binning import uniform_count_lags
from skgstat.binning import even_width_lags

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


# Plot the scatter plot


# Additional process: Plotting variograms with different models
print("Plotting variograms with different models...")
V2 = Variogram(coordinates, res, n_lags=12, normalize=False, bin_func=even_width_lags)

fig, _a = plt.subplots(2, 3, figsize=(13, 7), sharex=True, sharey=True)
axes = _a.flatten()
for i, model in enumerate(('spherical', 'exponential', 'gaussian', 'matern', 'stable', 'cubic')):
    V2.model = model
    V2.fit()
    print(f"\nModel: {model}")
    print(f"Model parameters: {V2.parameters}")
    print(f"RMSE: {V2.rmse}")
    V2.plot(axes=axes[i], hist=False, show=False)
    axes[i].set_xlim(0, 30)
    axes[i].set_title('Model: %s; RMSE: %.2f\n' % (model, V2.rmse))

plt.tight_layout()
plt.savefig('variogram_models.png', dpi=600)
plt.show()