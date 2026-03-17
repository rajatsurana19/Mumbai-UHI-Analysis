import rasterio
import geopandas as gpd
import numpy as np
from rasterio.features import geometry_mask
import matplotlib.pyplot as plt
import re
import os


# For Jan7 2026
b4_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B4.TIF"
b5_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B5.TIF"
b10_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B10.TIF"
mtl_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_MTL.txt"

# For 8 Feb 2026
# b4_path = "D:/UHI-Mumbai/data/Landsat 8/L8O08FEB2026000000001480047PSANSTUC00GTDF/LC81480472026039SGI00_B4.TIF"
# b5_path = "D:/UHI-Mumbai/data/Landsat 8/L8O08FEB2026000000001480047PSANSTUC00GTDF/LC81480472026039SGI00_B5.TIF"
# b10_path = "D:/UHI-Mumbai/data/Landsat 8/L8O08FEB2026000000001480047PSANSTUC00GTDF/LC81480472026039SGI00_B10.TIF"
# mtl_path = "D:/UHI-Mumbai/data/Landsat 8/L8O08FEB2026000000001480047PSANSTUC00GTDF/LC81480472026039SGI00_MTL.txt"

#For 22 Dec 2025
# b4_path = "D:/UHI-Mumbai/data/Landsat 8/L8O22DEC2025000000001480047PSANSTUC00GTDF/LC81480472025356SGI00_B4.TIF"
# b5_path = "D:/UHI-Mumbai/data/Landsat 8/L8O22DEC2025000000001480047PSANSTUC00GTDF/LC81480472025356SGI00_B5.TIF"
# b10_path = "D:/UHI-Mumbai/data/Landsat 8/L8O22DEC2025000000001480047PSANSTUC00GTDF/LC81480472025356SGI00_B10.TIF"
# mtl_path = "D:/UHI-Mumbai/data/Landsat 8/L8O22DEC2025000000001480047PSANSTUC00GTDF/LC81480472025356SGI00_MTL.txt"

#For 23 jan 2026
# b4_path = "D:/UHI-Mumbai/data/Landsat 8/L8O23JAN2026000000001480047PSANSTUC00GTDF/LC81480472026023SGI00_B4.TIF"
# b5_path = "D:/UHI-Mumbai/data/Landsat 8/L8O23JAN2026000000001480047PSANSTUC00GTDF/LC81480472026023SGI00_B5.TIF"
# b10_path = "D:/UHI-Mumbai/data/Landsat 8/L8O23JAN2026000000001480047PSANSTUC00GTDF/LC81480472026023SGI00_B10.TIF"
# mtl_path = "D:/UHI-Mumbai/data/Landsat 8/L8O23JAN2026000000001480047PSANSTUC00GTDF/LC81480472026023SGI00_MTL.txt"

#Landsat 9 Dec 30 2025
# b4_path = "D:/UHI-Mumbai/data/Landsat 9/L9O30DEC2025000000001480047PSANSTUC00GTDF/LC91480472025364SGI00_B4.TIF"
# b5_path = "D:/UHI-Mumbai/data/Landsat 9/L9O30DEC2025000000001480047PSANSTUC00GTDF/LC91480472025364SGI00_B5.TIF"
# b10_path = "D:/UHI-Mumbai/data/Landsat 9/L9O30DEC2025000000001480047PSANSTUC00GTDF/LC91480472025364SGI00_B10.TIF"
# mtl_path = "D:/UHI-Mumbai/data/Landsat 9/L9O30DEC2025000000001480047PSANSTUC00GTDF/LC91480472025364SGI00_MTL.txt"

#landsat 9 15 jan 2026
# b4_path = "D:/UHI-Mumbai/data/Landsat 9/L9O15JAN2026000000001480047PSANSTUC00GTDF/LC91480472026015SGI00_B4.TIF"
# b5_path = "D:/UHI-Mumbai/data/Landsat 9/L9O15JAN2026000000001480047PSANSTUC00GTDF/LC91480472026015SGI00_B5.TIF"
# b10_path = "D:/UHI-Mumbai/data/Landsat 9/L9O15JAN2026000000001480047PSANSTUC00GTDF/LC91480472026015SGI00_B10.TIF"
# mtl_path = "D:/UHI-Mumbai/data/Landsat 9/L9O15JAN2026000000001480047PSANSTUC00GTDF/LC91480472026015SGI00_MTL.txt"

# landsat 9 31 jan 2026
# b4_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_B4.TIF"
# b5_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_B5.TIF"
# b10_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_B10.TIF"
# mtl_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_MTL.txt"

shp_path = r"D:/UHI-Mumbai/vector/mumbai_clean.shp"
scene_name = "L8_2026_Jan7"

# --------------------------------------------------
# OUTPUT FOLDER
# --------------------------------------------------

out_root = r"D:/UHI-Mumbai/uhi_data"
os.makedirs(out_root, exist_ok=True)

# --------------------------------------------------
# LOAD BOUNDARY
# --------------------------------------------------

boundary = gpd.read_file(shp_path)

# --------------------------------------------------
# READ FULL BANDS
# --------------------------------------------------

with rasterio.open(b4_path) as src:
    red = src.read(1).astype(float)
    profile = src.profile
    transform = src.transform
    crs = src.crs

with rasterio.open(b5_path) as src:
    nir = src.read(1).astype(float)

with rasterio.open(b10_path) as src:
    thermal = src.read(1).astype(float)

# Remove no-data
red[red == 0] = np.nan
nir[nir == 0] = np.nan
thermal[thermal == 0] = np.nan

# --------------------------------------------------
# NDVI
# --------------------------------------------------

ndvi = (nir - red) / (nir + red)
mean_ndvi = np.nanmean(ndvi)
print("Mean NDVI:", mean_ndvi)

# --------------------------------------------------
# EMISSIVITY
# --------------------------------------------------

ndvi_min = np.nanmin(ndvi)
ndvi_max = np.nanmax(ndvi)

pv = ((ndvi - ndvi_min) / (ndvi_max - ndvi_min)) ** 2
emissivity = 0.004 * pv + 0.986

# --------------------------------------------------
# READ MTL FILE
# --------------------------------------------------

with open(mtl_path) as f:
    mtl = f.read()

def get_value(name):
    return float(re.search(name + r"\s=\s([0-9.E+-]+)", mtl).group(1))

ML = get_value("RADIANCE_MULT_BAND_10")
AL = get_value("RADIANCE_ADD_BAND_10")
K1 = get_value("K1_CONSTANT_BAND_10")
K2 = get_value("K2_CONSTANT_BAND_10")

# --------------------------------------------------
# LST CALCULATION
# --------------------------------------------------

radiance = ML * thermal + AL
bt = K2 / np.log((K1 / radiance) + 1)

lst = bt / (1 + (10.8e-6 * bt / 1.4388e-2) * np.log(emissivity))
lst_c = lst - 273.15

mean_lst = np.nanmean(lst_c)
print("Mean Scene LST:", mean_lst)

# --------------------------------------------------
# CREATE URBAN MASK (Mumbai)
# --------------------------------------------------

boundary_proj = boundary.to_crs(crs)

urban_mask = geometry_mask(
    boundary_proj.geometry,
    transform=transform,
    invert=True,        # True = inside polygon
    out_shape=lst_c.shape
)

# --------------------------------------------------
# URBAN & RURAL LST
# --------------------------------------------------

urban_lst = np.where(urban_mask, lst_c, np.nan)
rural_lst = np.where(~urban_mask, lst_c, np.nan)

urban_mean = np.nanmean(urban_lst)
rural_mean = np.nanmean(rural_lst)

# --------------------------------------------------
# UHI INTENSITY
# --------------------------------------------------

uhi_intensity = urban_mean - rural_mean

print("\n===== UHI RESULTS =====")
print("Urban Mean LST:", urban_mean)
print("Rural Mean LST:", rural_mean)
print("UHI Intensity (°C):", uhi_intensity)

# --------------------------------------------------
# UHI MAP
# --------------------------------------------------

uhi_map = lst_c - rural_mean

# --------------------------------------------------
# FUNCTION TO SAVE MAPS
# --------------------------------------------------

def save_map(data, cmap, title, filename):
    plt.figure(figsize=(8, 6))
    plt.imshow(data, cmap=cmap)
    plt.colorbar()
    plt.title(title)
    plt.axis("off")
    plt.savefig(os.path.join(out_root, filename), dpi=300)
    plt.close()

# --------------------------------------------------
# SAVE OUTPUT MAPS
# --------------------------------------------------

save_map(ndvi, "RdYlGn", f"NDVI — {scene_name}", f"{scene_name}_NDVI.png")
save_map(lst_c, "hot", f"LST — {scene_name}", f"{scene_name}_LST.png")
save_map(uhi_map, "inferno", f"UHI — {scene_name}", f"{scene_name}_UHI.png")

print("\nAll maps saved successfully!")