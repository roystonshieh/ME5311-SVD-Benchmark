import os
import xarray as xr

# dimensions of data
n_samples = 16071
n_latitudes = 101 
n_longitudes = 161
shape = (n_samples, n_latitudes, n_longitudes)

# load data
ds = xr.open_dataset('slp.nc') # change to 't2m.nc' for temperature data

# visualize dataset content
print(ds)

# get data values
da = ds['msl'] # 'msl' is the variable name for slp, change to 't2m' for temperature data
x = da.values
print(x)
print(x.shape)

# get time snapshots
da = ds['time']
t = da.values
print(t)

# get longitude values
da = ds['longitude']
lon = da.values
print(lon)

# get latitude values 
da = ds['latitude']
lat = da.values
print(lat)

# # ONLY if not enough memory
# low_res_ds = ds[{'longitude': slice(None, None, 2), 'latitude': slice(None, None, 2)}] 
# low_res_ds.to_netcdf(path='slp_low_res.nc') # change to 't2m_low_res.nc' for temperature data