"""Base map creation functions

.. currentmodule:: pygeochemtools.plot.map
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

from typing import List, Union

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import cartopy.mpl as cmpl
except ModuleNotFoundError:
    pass


def SA_base_map(
    title: str,
    inset_title: str,
    projection: int,
    extent: List[int],
    places: List[List[Union[float, float, str]]],
    add_inset=True,
) -> plt.figure:
    """Create default map for plotting.

    Args:
        title (str): [description]
        inset_title (str): [description]
        projection (int, optional): [description].
        add_inset (bool, optional): [description]. Defaults to True.
        extent (list[int], optional): [description].
        places (list[list[float, float, str]], optional): [description].

    Returns:
        tuple containing
        - fig (matplotlib.pyplot.figure): [description]
        - view (matplotlib.axes.Axes): [desc]
        - inset (matplotlib.axes.Axes): [desc]
    """
    proj = ccrs.epsg(projection)
    fig = plt.figure(figsize=(10, 11))
    view = fig.add_subplot(1, 1, 1, projection=proj, aspect="auto")
    view.set_title(title, fontsize=20)
    view.set_extent(extent)
    view.add_feature(cfeature.STATES.with_scale("10m"))
    view.add_feature(cfeature.OCEAN)
    view.add_feature(cfeature.COASTLINE)
    view.add_feature(cfeature.BORDERS, linestyle=":")
    gl = view.gridlines(color="lightgrey", linestyle="-", draw_labels=True)
    gl.top_labels = gl.right_labels = False
    for p in places:
        view.text(
            p[0] + 0.1,
            p[1],
            p[2],
            horizontalalignment="left",
            transform=ccrs.Geodetic(),
        )
        view.plot(
            p[0],
            p[1],
            color="blue",
            marker="o",
            markersize=5,
            transform=ccrs.Geodetic(),
        )
    if add_inset:
        inset = inset_axes(
            view,
            width="30%",
            height="40%",
            loc=3,
            axes_class=cmpl.geoaxes.GeoAxes,
            axes_kwargs=dict(map_projection=proj),
        )
        inset.set_title(inset_title, fontsize=12)
        inset.set_extent(extent)
        inset.add_feature(cfeature.STATES.with_scale("10m"))
        inset.add_feature(cfeature.OCEAN)
        inset.add_feature(cfeature.COASTLINE)
    else:
        inset = None

    return fig, view, inset
