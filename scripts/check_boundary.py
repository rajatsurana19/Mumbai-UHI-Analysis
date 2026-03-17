import geopandas as gpd

path = r"D:/UHI-Mumbai/vector/mumbai.geojson"

gdf = gpd.read_file(path)

print(gdf)
print("\nGeometry type:", gdf.geom_type)
print("\nIs empty:", gdf.is_empty)
print("\nBounds:", gdf.total_bounds)