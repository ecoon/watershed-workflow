"""Manager for interacting with DayMet datasets.
"""
import os,sys
import logging
import numpy as np
import pyproj
import requests
import requests.exceptions
import shapely.geometry

import workflow.sources.utils as source_utils
import workflow.crs
import workflow.conf
import workflow.warp
import workflow.sources.names


#
class FileManagerDayMet:
    VALID_YEARS = (1980,2018)
    VALID_VARIABLES = ['tmin', 'tmax', 'prcp', 'srad', 'vp', 'swe', 'dayl']
    URL = "http://thredds.daac.ornl.gov/thredds/ncss/grid/ornldaac/1328/{year}/daymet_v3_{variable}_{year}_na.nc4"

    
    def __init__(self):
        self.layer_name = 'NLCD_{1}_{0}_{2}'.format(self.layer, self.year, self.location)
        self.name = 'DayMet 1km'
        self.names = workflow.sources.names.Names(self.name, 'meterology', 'daymet', 'daymet_{year}_{north}x{west}_{south}x{east}.nc')
        #self.native_crs = pyproj.Proj4("")

    def get_meterology(self, varname, year, polygon_or_bounds, crs):
        """Collects file for a single year and single variable."""
        if year > self.VALID_YEARS[1] or year < self.VALID_YEARS[0]:
            raise ValueError("DayMet data is available from {} to {} (does not include {})".format(self.VALID_YEARS[0], self.VALID_YEARS[1], year))
        if varname not in self.VALID_VARIABLES:
            raise ValueError("DayMet data supports variables: {} (not {})".format(', '.join(self.VALID_VARIABLES), varname))

        if type(polygon_or_bounds) is dict:
            # fiona shape object, convert to shapely to get a copy
            polygon_or_bounds = workflow.utils.shape(polygon_or_bounds)

        if type(polygon_or_bounds) is list:
            # bounds
            polygon_or_bounds = workflow.warp.warp_bounds(polygon_or_bounds, crs, workflow.crs.latlon_crs())
        else:
            # polygon
            polygon_or_bounds = workflow.warp.warp_shply(polygon_or_bounds, crs, workflow.crs.latlon_crs()).bounds


    def _download(self, varname, year, bounds):
        url_dict = {'year':str(year),
                    'variable':varname}
            
        request_params = [('var', 'lat'),
                          ('var', 'lon'),
                          ('var', varname),
                          ('west', str(bounds[0])),
                          ('south', str(bounds[1])),
                          ('east', str(bounds[2])),
                          ('north', str(bounds[3])),
                          ('horizStride', '1'),
                          ('time_start', '{}-01-01T12:00:00Z'.format(year)),
                          ('time_end', '{}-12-30T12:00:00Z'.format(year)),
                          ('timeStride', '1'),
                          ('accept', 'netcdf')
                          ]
        r = requests.get(url.format(**url_dict),params=request_params)
        r.raise_for_status()

        with open(self.names.file_name(year=year, north=bounds[3], east=bounds[2], west=bounds[0], south=bounds[1]), 'wb') as fid:
            fid.write(r.content)
        
