from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


my_example_nc_file = 'S5P_RPRO_L2__NO2____20180603T012350_20180603T030718_03301_01_010202_20190207T060023.nc'
fh = Dataset(my_example_nc_file, mode='r')

lons = fh.groups['PRODUCT'].variables['longitude'][0][:][:]
lats = fh.groups['PRODUCT'].variables['latitude'][0][:][:]
no2 = fh.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column'][0][:][:]

print(lons.shape)
print(lats.shape)
print(no2.shape)


# lon_0 = lons.mean()
# lat_0 = lats.mean()

m = Basemap(width=500000, height=350000,
            resolution='l', projection='stere', lat_ts=-40, lat_0=50.8, lon_0=4)

xi, yi = m(lons, lats)

# Plot Data
cs = m.pcolor(xi, yi, np.squeeze(no2), cmap='jet', vmin=0, vmax=0.00038)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")

# cbar.set_label(no2_units)

# Add Title
plt.title('NO2 in atmosphere')

plt.show()
