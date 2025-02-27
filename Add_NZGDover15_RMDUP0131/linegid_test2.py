import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from mpl_toolkits.basemap import Basemap
from pyproj import Proj, transform
import matplotlib.patheffects as PathEffects
from matplotlib.patches import FancyArrow

# Create DataFrames from the given list of tuples
data = [
    (0, '00_water'),
    (1, 'G01'),
    (2, 'G04'),
    (3, 'G05'),
    (4, 'G06'),
    (5, 'G08'),
    (6, 'G09'),
    (7, 'G10'),
    (8, 'G11'),
    (9, 'G12'),
    (10, 'G13'),
    (11, 'G14'),
    (12, 'G15'),
    (13, 'G16'),
    (14, 'G17'),
    (15, 'G18'),
    (255, 'UNDEFINED DATA')
]
df_mapping = pd.DataFrame(data, columns=['gid', 'description'])

data2 = [
    (1 , 'T01'),
    (2 , 'T02'),
    (3 , 'T03'),
    (4 , 'T04'),
    (5 , 'T05'),
    (6 , 'T06'),
    (7 , 'T07'),
    (8 , 'T08'),
    (9 , 'T09'),
    (10 , 'T10'),
    (11 , 'T11'),
    (12 , 'T12'),
    (13 , 'T13'),
    (14 , 'T14'),
    (15 , 'T15'),
    (16 , 'T16'),
    (255, 'UNDEFINED DATA')
]
df_mapping2 = pd.DataFrame(data2, columns=['tid', 'description'])

# Read the CSV file
df = pd.read_csv('Pointsampling1km_gidtid.csv')

# Drop rows with NaN values in 'vs30' and 'tid' columns
df = df.dropna(subset=['gid'])

# Map the 'tid' values in the DataFrame to the corresponding values in the created DataFrame
df['gid'] = df['gid'].map(df_mapping.set_index('gid')['description'])

# Rename columns xcoord and ycoord to longitude and latitude
df = df.rename(columns={'xcoord': 'longitude', 'ycoord': 'latitude'})

# Define the projections
nztm = Proj(init='epsg:2193')  # NZTM
wgs84 = Proj(init='epsg:4326')  # WGS84

# Transform the coordinates
df['longitude'], df['latitude'] = transform(nztm, wgs84, df['longitude'].values, df['latitude'].values)

# Initialize a Basemap instance
plt.figure(figsize=(12, 8))
m = Basemap(projection='merc', llcrnrlat=-47.5, urcrnrlat=-34, llcrnrlon=166, urcrnrlon=179, resolution='i', epsg=4326)
m.arcgisimage(service='World_Shaded_Relief', xpixels=1500, verbose=True)

# Convert coordinates to map projection
x, y = m(df['longitude'].values, df['latitude'].values)

# Assign colors to each group
unique_gids = sorted(df['gid'].unique())
colors = plt.cm.get_cmap('terrain_r', len(unique_gids))

# Plot the scatter points on the map
for i, gid in enumerate(unique_gids):
    subset = df[df['gid'] == gid]
    x, y = m(subset['longitude'].values, subset['latitude'].values)
    m.scatter(x, y, s=1, color=colors(i), label=gid, marker='o', edgecolor='None', alpha=0.9)

# Add ticks
m.drawparallels(np.arange(-47, -34, 4), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(166, 179, 4), labels=[0,0,0,1], fontsize=10)
arx,ary =m(178,-35)
compass = plt.text(arx,ary-0.5,'N',fontsize=18,ha='center',va='center',color='k',weight='bold')
compass.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
arrow = FancyArrow(arx,ary,0,0.5,width=0.18,head_width=0.4, head_length=0.25,fc='k',ec='w')
arrow.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
plt.gca().add_patch(arrow)
# Customize the plot
plt.title('Map with Grouped Color Values by gid', fontsize=12, style='italic')
plt.legend(loc='lower right', scatterpoints=1, markerscale=10)

# Display and save the plot
plt.tight_layout()
plt.savefig('map_grouped_by_gid.png', dpi=300)
plt.show()