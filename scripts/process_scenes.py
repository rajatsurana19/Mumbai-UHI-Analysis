import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
import matplotlib.pyplot as plt
import re
import os

# -------------------------------
# INPUT FILES (CHANGE PER SCENE)
# -------------------------------

# For Jan7 2026
# b4_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B4.TIF"
# b5_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B5.TIF"
# b10_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B10.TIF"
# mtl_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_MTL.txt"

#For 8 Feb 2026
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
b4_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_B4.TIF"
b5_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_B5.TIF"
b10_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_B10.TIF"
mtl_path = "D:/UHI-Mumbai/data/Landsat 9/L9O31JAN2026000000001480047PSANSTUC00GTDF/LC91480472026031SGI00_MTL.txt"

shp_path = r"D:/UHI-Mumbai/vector/mumbai_clean.shp"

# Scene name (for saving outputs)
scene_name = "L9_2026_Jan15"


# -------------------------------
# OUTPUT FOLDERS
# -------------------------------

out_ndvi = r"D:/UHI-Mumbai/outputs/NDVI_maps"
out_lst = r"D:/UHI-Mumbai/outputs/LST_maps"

os.makedirs(out_ndvi, exist_ok=True)
os.makedirs(out_lst, exist_ok=True)


# -------------------------------
# LOAD BOUNDARY
# -------------------------------

boundary = gpd.read_file(shp_path)


def clip_raster(raster_path):
    with rasterio.open(raster_path) as src:
        boundary_proj = boundary.to_crs(src.crs)
        clipped, _ = mask(src, boundary_proj.geometry, crop=True)
    return clipped[0]


# Clip bands
red = clip_raster(b4_path).astype(float)
nir = clip_raster(b5_path).astype(float)
thermal = clip_raster(b10_path).astype(float)

red[red == 0] = np.nan
nir[nir == 0] = np.nan


# -------------------------------
# NDVI
# -------------------------------

ndvi = (nir - red) / (nir + red)

mean_ndvi = np.nanmean(ndvi)
print("Mean NDVI:", mean_ndvi)


# -------------------------------
# EMISSIVITY
# -------------------------------

ndvi_min = np.nanmin(ndvi)
ndvi_max = np.nanmax(ndvi)

pv = ((ndvi - ndvi_min) / (ndvi_max - ndvi_min)) ** 2
emissivity = 0.004 * pv + 0.986


# -------------------------------
# READ MTL
# -------------------------------

with open(mtl_path) as f:
    mtl = f.read()

def get_value(name):
    return float(re.search(name + r"\s=\s([0-9.E+-]+)", mtl).group(1))

ML = get_value("RADIANCE_MULT_BAND_10")
AL = get_value("RADIANCE_ADD_BAND_10")
K1 = get_value("K1_CONSTANT_BAND_10")
K2 = get_value("K2_CONSTANT_BAND_10")


# -------------------------------
# LST
# -------------------------------

radiance = ML * thermal + AL
bt = K2 / np.log((K1 / radiance) + 1)

lst = bt / (1 + (10.8e-6 * bt / 1.4388e-2) * np.log(emissivity))
lst_c = lst - 273.15

mean_lst = np.nanmean(lst_c)
print("Mean LST (°C):", mean_lst)


# -------------------------------
# SAVE NDVI MAP
# -------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap="RdYlGn")
plt.colorbar(label="NDVI")
plt.title(f"NDVI — {scene_name}")
plt.axis("off")

ndvi_file = os.path.join(out_ndvi, f"{scene_name}_NDVI.png")
plt.savefig(ndvi_file, dpi=300)
plt.close()


# -------------------------------
# SAVE LST MAP
# -------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(lst_c, cmap="hot")
plt.colorbar(label="Temperature (°C)")
plt.title(f"LST — {scene_name}")
plt.axis("off")

lst_file = os.path.join(out_lst, f"{scene_name}_LST.png")
plt.savefig(lst_file, dpi=300)
plt.close()


print("Maps saved successfully!")