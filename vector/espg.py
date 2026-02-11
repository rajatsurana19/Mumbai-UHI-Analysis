import geopandas as gpd

gdf = gpd.read_file("vector/mumbai_boundary.shp")

print("CRS:", gdf.crs)
print("Number of features:", len(gdf))
print(gdf.head())
