import geopandas as gpd

# Load geojson
gdf = gpd.read_file("MUMBAI.geojson")

# Check CRS
print("Original CRS:", gdf.crs)

# Convert to WGS84 if not already
gdf = gdf.to_crs("EPSG:4326")

# Save as shapefile
gdf.to_file("mumbai_boundary.shp", driver="ESRI Shapefile")

print("Conversion complete!")
