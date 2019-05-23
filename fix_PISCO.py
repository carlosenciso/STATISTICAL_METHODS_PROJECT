#!/media/carlos/DATA/anaconda3/envs/py37/bin/python
# @Author: carlos
# @Date:   2019-05-23T12:30:58-05:00
# @Email:  carlos.enciso.o@gmail.com
# @Last modified by:   carlos
# @Last modified time: 2019-05-23T13:19:03-05:00
# @License: Peruvian Geophysical Institute
# @Copyright: MIT
#-------------------
# Import modules
#-------------------
import xarray as xr
import os

diri_nc = './DATASET/'
fili_nc = [os.path.join(diri_nc,x) for x in os.listdir(diri_nc) if x.endswith('.nc')]

def fix_calendar(ds, timevar='T'):
    if ds[timevar].attrs['calendar'] == '360':
        ds[timevar].attrs['calendar'] = '360_day'
    elif ds[timevar].attrs['calendar'] == 'standard':
        ds[timevar].attrs['calendar'] = '360_day'
    else:
        ds[timevar].attrs['calendar'] = '360_day'
    return ds

def time_nonstandard(ds,timevar='T'):
    datetimeindex = ds.indexes[timevar].to_datetimeindex()
    ds[timevar] = datetimeindex
    return ds

#------------------------------
# Fixing PISCO
#------------------------------
ds = xr.open_dataset(fili_nc[0], decode_cf=False)
ds = fix_calendar(ds, timevar='z')
ds = xr.decode_cf(ds)
ds = time_nonstandard(ds, timevar='z')
#------------------------------
# Saving new PISCO
#------------------------------
ds = ds.rename({'latitude':'lat', 'longitude':'lon',
                'z':'time', 'variable':'P'})
ds.attrs['title'] = 'Pisco_new'
ds.attrs['author'] = 'Carlos Enciso v.0.1'
ds['P'].attrs['units'] = 'mm'
dw = ds.sortby(ds['lat'])
dw.to_netcdf(path=diri_nc+'new_PISCO.nc')
