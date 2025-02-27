import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape

# Path to the input .tif file
input_tif = 'tid.tif'

# Path to the output .shp file
output_shp = 'tid.shp'

# Read the raster file
with rasterio.open(input_tif) as src:
    image = src.read(1)  # Read the first band
    mask = image != src.nodata  # Create a mask for valid data

    # Extract shapes (contours) from the raster
    results = (
        {'properties': {'raster_val': v}, 'geometry': s}
        for i, (s, v) in enumerate(
            shapes(image, mask=mask, transform=src.transform))
    )

    # Convert shapes to GeoDataFrame
    geoms = list(results)
    gdf = gpd.GeoDataFrame.from_features(geoms)

# Save the GeoDataFrame as a shapefile
gdf.to_file(output_shp)