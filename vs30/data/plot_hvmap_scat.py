import os
import pandas as pd
from pyproj import Transformer

# Set the PROJ_LIB environment variable
os.environ['PROJ_LIB'] = '/home/jki140/miniforge3/envs/Vs30/share/proj'

# Load the data
data = pd.read_csv('McGann_cptVs30data_v25.csv')

# Define the transformers
transformer_to_wgs84 = Transformer.from_crs("EPSG:2193", "EPSG:4326", always_xy=True)
transformer_to_nzmg = Transformer.from_crs("EPSG:2193", "EPSG:27200", always_xy=True)

# Transform the coordinates
data[['WGS84_Lat', 'WGS84_Lon']] = data.apply(
    lambda row: pd.Series(transformer_to_wgs84.transform(row['NZTM_X'], row['NZTM_Y'])), axis=1)
data[['NZMG_Easting', 'NZMG_Northing']] = data.apply(
    lambda row: pd.Series(transformer_to_nzmg.transform(row['NZTM_X'], row['NZTM_Y'])), axis=1)

# Save the transformed data to a new CSV file
data.to_csv('transformed_coordinates.csv', index=False)