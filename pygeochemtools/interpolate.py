"""Map generation and interpolation module

.. currentmodule:: pygeochemtools.interpolate
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import cartopy.crs as ccrs
import numpy as np
import pandas as pd
from metpy.interpolate import interpolate_to_grid

from .utils import config

LONG = config.column_names["longitude"]
LAT = config.column_names["latitude"]


def interpolate(
    data: pd.DataFrame,
    projection: int,
    interp_type: str = "natural_neighbor",
    hres: int = 10000,
) -> np.array:
    """#TODO docs

    Args:
        data (pd.DataFrame): [description]
        proj ([type]): [description]
        interp_type (str, optional): [description]. Defaults to "natural_neighbor".
        hres (int, optional): [description]. Defaults to 10000.
    """
    x, y, data = (
        data[LONG].values,
        data[LAT].values,
        data["Normalised_crustal_abund (ppm)"].values,
    )
    proj = ccrs.epsg(projection)
    xp, yp, _ = proj.transform_points(ccrs.Geodetic(), x, y).T

    gx, gy, img = interpolate_to_grid(xp, yp, data, interp_type=interp_type, hres=hres)
    img = np.ma.masked_where(np.isnan(img), img)

    return gx, gy, img
