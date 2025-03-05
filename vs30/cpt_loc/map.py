import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pyproj import Transformer

# Load the data
cpt = pd.read_csv('converted_cptvs30_2.csv',
    sep=",",
    usecols=[3, 4, 2],
    names=["vs30","xcoord", "ycoord"],
    skiprows=1,
    engine="c",
    dtype=np.float32,
)

# Filter out rows with NaN values in the vs30 column
cpt = cpt[~np.isnan(cpt.vs30)].reset_index()

# Create a scatter plot
plt.figure(figsize=(10, 8))

# Create Basemap instance
m = Basemap(projection='merc',
            llcrnrlat=cpt['ycoord'].min() - 1.5,
            urcrnrlat=cpt['ycoord'].max() + 1.5,
            llcrnrlon=cpt['xcoord'].min() - 1.5,
            urcrnrlon=cpt['xcoord'].max() + 1.5,
            resolution='i')

# Draw map details
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='lightgray', lake_color='aqua')

# Convert coordinates
x, y = m(cpt['xcoord'], cpt['ycoord'])

# Create scatter plot
sc = m.scatter(x, y, c=cpt['vs30'], cmap='viridis_r', s=50, edgecolor='k', vmin=100, vmax=800)

# Add colorbar
plt.colorbar(sc, label='Vs30')

# Add wider ticks with interval of 2
m.drawparallels(np.arange(-90., 91., 2), labels=[1,0,0,0], fontsize=10, linewidth=2)
m.drawmeridians(np.arange(-180., 181., 2), labels=[0,0,0,1], fontsize=10, linewidth=2)

# Adjust tick labels to avoid overlapping
plt.gca().tick_params(axis='both', which='major', pad=15)

# Add simple compass
plt.annotate('N', xy=(0.95, 0.95), xycoords='axes fraction', fontsize=15,
             ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
plt.arrow(0.95, 0.90, 0, 0.05, transform=plt.gca().transAxes, color='black', head_width=0.02)

# Add scalebar
m.drawmapscale(cpt['xcoord'].min(), cpt['ycoord'].min(), cpt['xcoord'].mean(), cpt['ycoord'].mean(), 10,
               barstyle='fancy', labelstyle='simple', units='km', fontsize=10, yoffset=0.02)

# Add labels and title
plt.xlabel('Longitude', labelpad=20)
plt.ylabel('Latitude', labelpad=20)
plt.title('Scatter Plot of Vs30 with Basemap')
plt.grid(True)
plt.savefig('Vs30_map.png', dpi=300)
plt.show()