import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging

# Load the data
print("Loading data...")
data = pd.read_csv('Stacking_result_SCPTSDMT.csv')

# Extract the 'depth_input' and 'RES' columns
print("Extracting coordinates and values...")
depth = data['depth_input'].values
res = data['Combined_Vs_res'].values

# Create a spatial field
print("Creating spatial field...")
coordinates = np.column_stack((depth, np.zeros_like(depth)))  # Use depth as the spatial coordinate

# Set variogram parameters manually
variogram_parameters = {'range': 2.5, 'psill': 0.004, 'nugget': 0.09}

# Perform Ordinary Kriging with specified number of lags
print("Performing Ordinary Kriging...")
OK = OrdinaryKriging(
    coordinates[:, 0], coordinates[:, 1], res,
    variogram_model='gaussian',
    variogram_parameters=variogram_parameters,
    nlags=60,  # Set the number of lags
    verbose=True,
    enable_plotting=True
)

# Extract variogram model parameters
lags = OK.lags
semivariance = OK.semivariance

# Plot the variogram
fig, ax = plt.subplots()
ax.scatter(lags, semivariance, marker='*', color='red', s=30)
#ax.set_xlim(0, 10)  # Set the x-axis limits
#ax.set_ylim(0.08, 0.12)  # Set the y-axis limits
ax.set_xlabel('Lag')
ax.set_ylabel('Semivariance')
ax.set_title('Variogram')
plt.savefig('Variogram.png')
plt.show()