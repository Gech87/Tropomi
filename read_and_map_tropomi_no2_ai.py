import numpy as np
from mpl_toolkits.basemap import Basemap
from collections import namedtuple
import matplotlib.pyplot as plt
import sys
from netCDF4 import Dataset


# This finds the user's current path so that all hdf4 files can be found
try:
    fileList = open('fileList.txt', 'r')  # fileList is the name of the txt that contains the names of the .nc files
except:
    print('Did not find a text file containing file names (perhaps name does not match)')
    sys.exit()

# loops through all files listed in the text file
for FILE_NAME in fileList:  # FILE_NAME will be the name of e
    FILE_NAME = FILE_NAME.strip()  # strip() removes remove all the leading and trailing spaces from a string
    file = Dataset(FILE_NAME, 'r')  # Dataset is a netCDF4 method used to open .nc files
    ds = file
    grp = 'PRODUCT'
    lat = ds.groups[grp].variables['latitude'][0][:][:]  # Gets latitude array
    lon = ds.groups[grp].variables['longitude'][0][:][:]  # Gets longitude array
    if 'NO2' in FILE_NAME:
        sds_name = 'nitrogendioxide_tropospheric_column'
    elif 'AER_AI' in FILE_NAME:
        sds_name = 'aerosol_index_354_388'
    elif 'HCHO' in FILE_NAME:
        sds_name = 'formaldehyde_tropospheric_vertical_column'
    elif 'CH4' in FILE_NAME:
        sds_name = 'methane_mixing_ratio'
    elif 'O3' in FILE_NAME:
        sds_name = 'ozone_total_vertical_column'
    elif 'CO' in FILE_NAME:
        sds_name = 'carbonmonoxide_total_column'
    elif 'SO2' in FILE_NAME:
        sds_name = 'sulfurdioxide_total_vertical_column'
    else:
        sys.exit()

    data = ds.groups[grp].variables[sds_name][0]  # data will be the array of pollutants concentrations
        
    # get necessary attributes
    #fv = data._FillValue  # _FillValue is an attribute and is needed to represent the data when a value is missed
        # (empty pixels)
        
    # get lat and lon information
    min_lat = np.min(lat)
    max_lat = np.max(lat)
    min_lon = np.min(lon)
    max_lon = np.max(lon)


    # set map labels
    # map_label = data.units
    #map_title = data.long_name
    #print(data.units)
    
    # get the data as an array and mask fill/missing values
    #dataArray = np.array(data[0][:][:])
    #dataArray[dataArray == fv] = np.nan
    #data = dataArray
    # data=data.reshape(xdim,ydim)

    # get statistics about data
    #average = np.nanmean(dataArray)
    #stdev = np.nanstd(dataArray)
    #median = np.nanmedian(dataArray)
    # map_label='mol/cm2'
        
    # print statistics
    # print('The average of this data is: ',round(average,3),'\nThe standard deviation is: ',round(stdev,3),
    # '\nThe median is: ',round(median,3))
    #print('The average of this data is: ', '{:.2e}'.format(average), '\nThe standard deviation is: ',
          #'{:.2e}'.format(stdev), '\nThe median is: ', '{:.2e}'.format(median))
    #print('The range of latitude in this file is: ', min_lat, ' to ', max_lat, 'degrees \nThe range of longitude in this file is: ', min_lon, ' to ', max_lon, ' degrees')
    #is_map = input('\nWould you like to create a map of this data? Please enter Y or N \n')
        
    # if user would like a map, view it
    #data = np.ma.masked_array(data)
    plt.clf()
    m = Basemap(width=5000000, height=3500000, resolution='l', projection='stere', lat_ts=40, lat_0=50.5039,
                lon_0=4.4699)
    m.drawcoastlines(linewidth=0.5)
    m.drawstates()
    m.drawcountries()
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(-180, 181., 10.), labels=[0, 0, 0, 1], fontsize=10)
    #my_cmap.set_under('w')
    vmin1 = 0.0
    vmax1 = 0.0005
    m.pcolor(lon, lat, data, latlon=True, vmin=vmin1, vmax=vmax1, cmap='jet')
    cb = m.colorbar()
    #cb.set_label(map_label)
    #plt.autoscale()

    # title the plot
    #plt.title('{0}\n {1}'.format(FILE_NAME, map_title))
    fig = plt.gcf()

    # Show the plot window.
    #plt.show()

    # saves as a png if the user would like
    pngfile = '{0}.png'.format(FILE_NAME[:-3])
    fig.savefig(pngfile, dpi=750)
    # close the hdf5 file
    plt.clf()
    plt.cla()
    file.close()
    print('figure')
