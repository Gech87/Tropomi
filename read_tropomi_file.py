import numpy as np
import sys
from netCDF4 import Dataset


def read_tropomi(file_name):
    file_name = file_name.strip()  # strip() removes remove all the leading and trailing spaces from a string
    ds = Dataset(file_name, 'r')  # "Dataset" is a netCDF4 method used to open .nc files
    grp = 'PRODUCT'

    if 'NO2' in file_name:
        sds_name = 'nitrogendioxide_tropospheric_column'
    elif 'AER_AI' in file_name:
        sds_name = 'aerosol_index_354_388'
    elif 'HCHO' in file_name:
        sds_name = 'formaldehyde_tropospheric_vertical_column'
    elif 'CH4' in file_name:
        sds_name = 'methane_mixing_ratio'
    elif 'O3' in file_name:
        sds_name = 'ozone_total_vertical_column'
    elif 'CO' in file_name:
        sds_name = 'carbonmonoxide_total_column'
    elif 'SO2' in file_name:
        sds_name = 'sulfurdioxide_total_vertical_column'
    else:
        sys.exit()

    data = ds.groups[grp].variables[sds_name]  # data will be the array of pollutants concentrations

    # get necessary attributes
    fv = data._FillValue  # _FillValue is an attribute and is needed to represent the data when a value is missed

    # get the data as an array and mask fill/missing values
    dataArray = np.array(data[0][:][:])
    dataArray[dataArray == fv] = np.nan
    data = dataArray
    # data=data.reshape(xdim,ydim)
