#!C:\Users\andri\OneDrive\Documents\Django Project\restaurant_project\foodonline_main\env1\Scripts\python.exe

import sys

from osgeo.gdal import UseExceptions, deprecation_warn

# import osgeo_utils.gdal_proximity as a convenience to use as a script
from osgeo_utils.gdal_proximity import *  # noqa
from osgeo_utils.gdal_proximity import main

UseExceptions()

deprecation_warn("gdal_proximity")
sys.exit(main(sys.argv))
