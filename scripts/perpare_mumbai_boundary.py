import geopandas as gpd

input_path = r"D:/UHI-Mumbai/vector/mumbai.geojson"
output_path = r"D:/UHI-Mumbai/vector/mumbai_clean.shp"

gdf = gpd.read_file(input_path)

# -----------------------------------
# 1. Remove EMPTY geometries
# -----------------------------------
gdf = gdf[~gdf.geometry.is_empty]
gdf = gdf[gdf.geometry.notnull()]

# -----------------------------------
# 2. FIX INVALID GEOMETRY
# -----------------------------------
gdf["geometry"] = gdf.buffer(0)

# -----------------------------------
# 3. Merge into single Mumbai polygon
# -----------------------------------
mumbai = gdf.unary_union

# Convert back to GeoDataFrame
mumbai_gdf = gpd.GeoDataFrame(geometry=[mumbai], crs=gdf.crs)

# -----------------------------------
# 4. Save cleaned boundary
# -----------------------------------
mumbai_gdf.to_file(output_path)

print("Clean Mumbai boundary created successfully!")