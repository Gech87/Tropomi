import numpy as np
import xarray as xr
from collections import namedtuple
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import rcParams
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


Point = namedtuple('Point', 'lon lat')
belgium_coords = Point(4.4699, 50.5039)

extent_size = 4
plot_extent = (belgium_coords.lon-2.5,
               belgium_coords.lon+2.5,
               belgium_coords.lat-1.5,
               belgium_coords.lat+1.5,)

vielsalm_coords = Point(5.9147, 50.2840)
ghent_coords = Point(3.7174, 51.0543)


# S5P_OFFL_L2__NO2____20180903T110440_20180903T124610_04612_01_010100_20180909T131424.nc

# Vielsalm higher than Ghent according to irceline
# S5P_OFFL_L2__NO2____20180925T104944_20180925T123114_04924_01_010100_20181001T123824.nc
# S5P_RPRO_L2__NO2____20180603T113250_20180603T131618_03307_01_010202_20190207T080418.nc
# S5P_OFFL_L2__NO2____20181111T110349_20181111T124519_05591_01_010200_20181117T131345.nc
# S5P_RPRO_L2__NO2____20180622T103549_20180622T121917_03576_01_010202_20190210T082130.nc
# S5P_RPRO_L2__NO2____20180622T121719_20180622T140047_03577_01_010202_20190210T093315.nc
# S5P_RPRO_L2__NO2____20180623T115818_20180623T134145_03591_01_010202_20190210T111240.nc
# S5P_RPRO_L2__NO2____20180708T103539_20180708T121907_03803_01_010202_20190213T020546.nc
# S5P_RPRO_L2__NO2____20180708T121709_20180708T140037_03804_01_010202_20190213T020210.nc

# Ghent higher than Vielsalm according to irceline
# S5P_RPRO_L2__NO2____20181016T105248_20181016T123615_05222_01_010202_20190228T010948.nc
# S5P_RPRO_L2__NO2____20180807T111242_20180807T125544_04229_01_010202_20190217T032726.nc
# S5P_OFFL_L2__NO2____20181212T112106_20181212T130235_06031_01_010202_20181218T141752.nc
# S5P_OFFL_L2__NO2____20181211T114009_20181211T132139_06017_01_010202_20181217T192310.nc
# S5P_RPRO_L2__NO2____20180927T115158_20180927T133525_04953_01_010202_20190224T124227.nc
ds = xr.open_dataset('S5P_RPRO_L2__NO2____20181016T105248_20181016T123615_05222_01_010202_20190228T010948.nc',
                     group='/PRODUCT')  # nitrogendioxide_tropospheric_column

title_text = 'TROPOMI 16-10-2018 (10:52-12:36)'

max_scale = 0.0004

rcParams['font.family'] = 'Arial'


def subset(ds, plot_extent):
    e, w, s, n = plot_extent

    # crop data set around point of interest
    ds = ds.where(
        (ds.longitude > e) &
        (ds.longitude < w) &
        (ds.latitude > s) &
        (ds.latitude < n), drop=True)

    return ds


ds = subset(ds, plot_extent)

# set all negative values to 0
ds.nitrogendioxide_tropospheric_column[0] = ds.nitrogendioxide_tropospheric_column[0].where(ds.nitrogendioxide_tropospheric_column[0] > 0, 0)
cm_values = np.linspace(0, 1, 16536)
# use the Yellow Orange Brown color map as reference
alpha_cm = plt.cm.RdGy_r(cm_values)  # RdGy_r
# change alpha value to follow a square low
alpha_cm[:, -1] = np.sqrt(cm_values)
# build new color map
my_cmap = colors.ListedColormap(alpha_cm)


def plot_ds(ds, title_text, max_scale):
    fig, ax = plt.subplots(figsize=(18, 12))

    ax = plt.axes(projection=ccrs.Mercator())

    # define Natural Earth features
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='white')

    land_10m = cfeature.NaturalEarthFeature(
        category='physical',
        name='land',
        scale='10m',
        edgecolor='face',
        facecolor=cfeature.COLORS['land'])

    # set map background and features
    ax.add_feature(land_10m)
    ax.add_feature(states_provinces, edgecolor='black', linewidth=2)

    # define plot titles, subtitle and caption
    ax.text(0, 1.02, title_text, fontsize=28, fontweight='bold',
            transform=ax.transAxes)

    # set plot frame color
    ax.outline_patch.set_edgecolor('black')

    # define plot extent
    plot_extent_2 = (belgium_coords.lon-2.45,
                     belgium_coords.lon+2.45,
                     belgium_coords.lat-1.45,
                     belgium_coords.lat+1.45,)

    ax.set_extent(plot_extent_2, ccrs.PlateCarree())

    # plot data
    img = ds.nitrogendioxide_tropospheric_column[0].plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(),
                                                                    infer_intervals=True,
                                                                    norm=colors.PowerNorm(gamma=1./2.), cmap=my_cmap,
                                                                    vmin=0,
                                                                    vmax=max_scale, x='longitude', y='latitude',
                                                                    zorder=2)

    # plot mt. Belgium
    ax.plot(ghent_coords.lon, ghent_coords.lat, marker='o', markeredgewidth=3, markeredgecolor='red',
            markerfacecolor='none', markersize=10, transform=ccrs.PlateCarree())
    ax.text(ghent_coords.lon+0.05, ghent_coords.lat, 'Ghent', color='black', fontsize=24, transform=ccrs.PlateCarree())

    ax.plot(vielsalm_coords.lon, vielsalm_coords.lat, marker='o', markeredgewidth=3, markeredgecolor='red',
            markerfacecolor='none', markersize=10, transform=ccrs.PlateCarree())
    ax.text(vielsalm_coords.lon+0.05, vielsalm_coords.lat, 'Vielsalm', color='black', fontsize=24,
            transform=ccrs.PlateCarree())

    img.colorbar.remove()

    # remove default title
    ax.set_title('')
    ax.set_xticks([2.4, 3, 3.6, 4.2, 4.8, 5.4, 6, 6.6], crs=ccrs.PlateCarree())
    ax.set_xticklabels([2.4, 3, 3.6, 4.2, 4.8, 5.4, 6, 6.6], ha='center', fontsize=24)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.xaxis.label.set_visible(False)

    ax.set_yticks([49.2, 49.8, 50.4, 51, 51.6], crs=ccrs.PlateCarree())
    ax.set_yticklabels([49.2, 49.8, 50.4, 51, 51.6], ha='right', fontsize=24)
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.yaxis.label.set_visible(False)

    ax.tick_params(which='major', length=10, width=2, direction='out')

    # set gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=1, color='gray', alpha=0.8,
                      linestyle=':')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # set colorbar properties
    cbar_ax = fig.add_axes([0.77, 0.11, 0.01, 0.755])   # [left, bottom, width, height]
    cbar = plt.colorbar(img, cax=cbar_ax, orientation='vertical',
                        ticks=[0, (1 / 4) * max_scale, (1 / 2) * max_scale, (3 / 4) * max_scale, max_scale],
                        extend='max', format='%.0e', shrink=0.75)
    cbar_ax.tick_params(labelsize=24, length=10, width=2)
    cbar.outline.set_visible(True)
    cbar.set_label('NO$_2$ (mol/m$^2$)', fontsize=24, rotation=270, labelpad=20, fontweight='bold')

    plt.show()


plot_ds(ds, title_text, max_scale)
