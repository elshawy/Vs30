import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pyproj

# Set the pyproj data directory
pyproj.datadir.set_data_dir('/path/to/your/proj/data')

# Read the CSV file
datafile = 'RES_WGS.csv'
df = pd.read_csv(datafile)

# Extract X, Y coordinates and residual values
x_coords = df['xcoord_2']
y_coords = df['ycoord_2']
residuals = df['RES_Vs30']

# Initialize a Basemap instance using an EPSG code and World Shaded Relief map
plt.figure(figsize=(12, 8))
m = Basemap(projection='merc', llcrnrlat=-47, urcrnrlat=-34, llcrnrlon=166, urcrnrlon=179, resolution='i', epsg=4326)
m.arcgisimage(service='World_Shaded_Relief', xpixels=1500, verbose=True)

# Convert coordinates to map projection
x, y = m(x_coords.values, y_coords.values)

# Check if residuals are None and assign a uniform color for those points
residuals = residuals.fillna(-9999)  # Use a placeholder for NaN values

# Ensure residuals are numeric and handle invalid RGBA values
colors = np.where(residuals == -9999, 'gray', residuals)
colors = pd.to_numeric(colors, errors='coerce')

# Sort the data by residual values in reverse order to plot lower residual values later
sorted_indices = np.argsort(colors)[::-1]
x = x[sorted_indices]
y = y[sorted_indices]
colors = colors[sorted_indices]

# Plot the scatter points on the map
sc = m.scatter(x, y, s=50, c=colors, cmap='jet', marker='o', edgecolor='k', alpha=0.7)
sc.set_clim(-1, 1)  # Set color limits on the scatter plot

# Add ticks
m.drawparallels(np.arange(-47, -34, 2), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(166, 179, 2), labels=[0,0,0,1], fontsize=10)

# Customize the plot
cbar = plt.colorbar(sc, label='Residuals')
plt.title('Comparison with Grid 10m-ln(Foster et al.,2019)-ln(Add_NZGD_NSHM_RMDUP)')

# Display and save the plot
plt.tight_layout()
plt.savefig('scatter_map_REsres_STD2.png', dpi=300)
plt.show()
