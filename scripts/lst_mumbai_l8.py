import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
import matplotlib.pyplot as plt
import re

# -------------------------------
# FILE PATHS (EDIT IF NEEDED)
# -------------------------------

b4_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B4.TIF"
b5_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B5.TIF"
b10_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_B10.TIF"
mtl_path = r"D:/UHI-Mumbai/data/Landsat 8/L8O07JAN2026000000001480047PSANSTUC00GTDF/LC81480472026007SGI00_MTL.txt"


b4_path = "D:\UHI-Mumbai\data\Landsat 8\L8O08FEB2026000000001480047PSANSTUC00GTDF\LC81480472026039SGI00_B4.TIF"
b5_path = "D:\UHI-Mumbai\data\Landsat 8\L8O08FEB2026000000001480047PSANSTUC00GTDF\LC81480472026039SGI00_B5.TIF"
b10_path = "D:\UHI-Mumbai\data\Landsat 8\L8O08FEB2026000000001480047PSANSTUC00GTDF\LC81480472026039SGI00_B10.TIF"
mtl_path = "D:\UHI-Mumbai\data\Landsat 8\L8O08FEB2026000000001480047PSANSTUC00GTDF\LC81480472026039SGI00_MTL.txt"


shp_path = r"D:/UHI-Mumbai/vector/mumbai_clean.shp"


# -------------------------------
# LOAD MUMBAI BOUNDARY
# -------------------------------

boundary = gpd.read_file(shp_path)

# -------------------------------
# FUNCTION TO CLIP RASTER
# -------------------------------

def clip_raster(raster_path):
    with rasterio.open(raster_path) as src:
        boundary_proj = boundary.to_crs(src.crs)
        clipped, transform = mask(src, boundary_proj.geometry, crop=True)
    return clipped[0]


# Clip bands
red = clip_raster(b4_path).astype(float)
nir = clip_raster(b5_path).astype(float)
thermal = clip_raster(b10_path).astype(float)

# Avoid divide-by-zero
red[red == 0] = np.nan
nir[nir == 0] = np.nan


# -------------------------------
# NDVI
# -------------------------------

ndvi = (nir - red) / (nir + red)

print("NDVI range:", np.nanmin(ndvi), np.nanmax(ndvi))


# -------------------------------
# EMISSIVITY FROM NDVI
# -------------------------------

ndvi_min = np.nanmin(ndvi)
ndvi_max = np.nanmax(ndvi)

pv = ((ndvi - ndvi_min) / (ndvi_max - ndvi_min)) ** 2
emissivity = 0.004 * pv + 0.986


# -------------------------------
# READ MTL CONSTANTS
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
# DN → RADIANCE
# -------------------------------

radiance = ML * thermal + AL


# -------------------------------
# BRIGHTNESS TEMPERATURE
# -------------------------------

bt = K2 / np.log((K1 / radiance) + 1)


# -------------------------------
# LAND SURFACE TEMPERATURE (°C)
# -------------------------------

lst = bt / (1 + (10.8e-6 * bt / 1.4388e-2) * np.log(emissivity))
lst_c = lst - 273.15

print("LST range (°C):", np.nanmin(lst_c), np.nanmax(lst_c))


# -------------------------------
# PLOT RESULT
# -------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(lst_c, cmap="hot")
plt.colorbar(label="Temperature (°C)")
plt.title("Mumbai Land Surface Temperature — Jan 7, 2026")
plt.axis("off")
plt.show()

mean_ndvi = np.nanmean(ndvi)
mean_lst = np.nanmean(lst_c)

print("Mean NDVI:", mean_ndvi)
print("Mean LST (°C):", mean_lst)