#!C:\Users\andri\OneDrive\Documents\Django Project\restaurant_project\foodonline_main\env1\Scripts\python.exe

import sys

from osgeo.gdal import UseExceptions, deprecation_warn

# import osgeo_utils.gdal_calc as a convenience to use as a script
from osgeo_utils.gdal_calc import *  # noqa
from osgeo_utils.gdal_calc import main

UseExceptions()

deprecation_warn("gdal_calc")
sys.exit(main(sys.argv))
