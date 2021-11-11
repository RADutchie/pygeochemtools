"""Data interpolation module

.. currentmodule:: pygeochemtools.interpolate
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import numpy as np
import pandas as pd
from metpy.interpolate import interpolate_to_grid

try:
    import cartopy.crs as ccrs
except ModuleNotFoundError:
    pass


def interpolate(
    data: pd.DataFrame,
    long: str,
    lat: str,
    value: str,
    projection: int,
    interp_type: str = "natural_neighbor",
    hres: float = 10000,
    **kwargs: dict,
) -> np.array:
    """Wrapper for the metpy interpolate_to_grid function. # noqa: D401, E501

    See https://unidata.github.io/MetPy/latest/api/generated/metpy.interpolate.interpolate_to_grid.htm
    for details and options.

    Args:
        data (pd.DataFrame): Dataframe continaing Latitude, Longitute and Values cols.
        long (str): Column name containing longitude values.
        lat (str): Column name containing latitude values.
        value (str): Column name containing data values for interpolation.
        proj (int): EPSG projection code from https://spatialreference.org/
        interp_type (str, optional): What type of interpolation to use.
            Available options include: 1) “linear”, “nearest”, “cubic”, or “rbf” from
            scipy.interpolate. 2) “natural_neighbor”, “barnes”, or “cressman” from
            metpy.interpolate. Defaults to "natural_neighbor".
        hres (float, optional):  The horizontal resolution of the generated grid,
            given in the same units as the x and y parameters . Defaults to 10000.
        **kwargs (dict, optional): additional keyword arguments to pass to the metpy
            interpolate_to_grid function.

    Returns:
        gx ((N,2) ndarray): Meshgrid for the resulting interpolation in the x dimension
        gy ((N,2) ndarray): Meshgrid for the resulting interpolation in the y dimension
        gx ((M,N) ndarray): 2-dimensional array representing the interpolated values for each grid.
    """
    x, y, data = (
        data[long].values,
        data[lat].values,
        data[value].values,
    )
    proj = ccrs.epsg(projection)
    xp, yp, _ = proj.transform_points(ccrs.Geodetic(), x, y).T

    gx, gy, img = interpolate_to_grid(
        xp, yp, data, interp_type=interp_type, hres=hres, **kwargs
    )
    img = np.ma.masked_where(np.isnan(img), img)

    return gx, gy, img
