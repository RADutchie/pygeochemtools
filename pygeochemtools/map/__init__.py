"""Map generation and interpolation module

.. currentmodule:: pygeochemtools.map
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""
import warnings
from pathlib import Path
from typing import List, Optional, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import BoundaryNorm, LogNorm
from scipy.spatial.qhull import QhullError

from ..geochem import max_dh_chem, max_dh_chem_interval, normalise_crustal_abundace
from ..utils import app_logger, config
from .interpolate import interpolate  # noqa: F401
from .map import SA_base_map  # noqa: F401

cartopy_installed = True
try:
    import cartopy.crs as ccrs
except ModuleNotFoundError:
    warnings.warn(
        "Cartopy module required for plotting: https://scitools.org.uk/cartopy/docs/latest/installing.html#requirements",  # noqa: E501
        UserWarning,
    )
    cartopy_installed = False
    pass

logger = app_logger.get_logger(__name__)

# global var set from config.yml
LONG = config.column_names["longitude"]
LAT = config.column_names["latitude"]
DH_ID = config.column_names["drillhole_id"]
PPM = config.column_names["converted_ppm"]
START_DEPTH = config.column_names["depth_from"]
END_DEPTH = config.column_names["depth_to"]
PROJECTION = config.projection
NORM_DATA = config.column_names["normalised_data"]
PLACES = config.places
EXTENT = config.extent


def plot_max_downhole_chem(
    input_data: Union[str, pd.DataFrame],
    element: str,
    plot_type: str = "point",
    projection: int = PROJECTION,
    extent: List[int] = EXTENT,
    places: List[List[Union[float, float, str]]] = PLACES,
    log_scale: bool = True,
    out_path: Optional[str] = None,
    add_inset: bool = False,
) -> None:
    """Create a map plot of the maximum down hole geochemical values in a dataset.

    .. warning::
        Requires ``Cartopy`` to be installed to use.

    This function takes either a DataFrame or a path to a valid csv file containing
    a single element drillhole dataset. It will isolate the maximum value in each
    drillhole, create a normalised to crustal abundance column and then create either
    a point or interpolated grid map of the maximum values.

    The map can be customised to different locations and projections by editing the
    user configuration file projection, extent and places.

    Args:
        input_data (Union[str, pd.DataFrame]): Path to clean and processed single
            element dataset in csv format or Pandas dataframe of clean and processed
            single element dataset.
        element (str): The element to normalise, to retreive value from config file.
        plot_type (str, optional): Either "point" or "interpolate. Defaults to "point".
        projection (int, optional): Map projection to use inputted as epsg number, i.e.
            3107 for GDA94/SA Lambert. See https://epsg.io for values.
            Defaults to PROJECTION.
        extent (List[int], optional): Map extents in correct values for projection. List
            of values corresponding to [left, right, top, bottom].
            Defaults to EXTENT.
        places (List[List[Union[float, float, str]]], optional): Localities to include
            on map plot with coordinates in appropriate values for he projection. List
            of values corresponding to [latitude, longitude, label]. Defaults to PLACES.
        log_scale (bool, optional): Wether to plot data on a log or linear scale.
            Defaults to True.
        out_path (Optional[str], optional): Optional path to place output file.
            Defaults to None.
        add_inset (bool, optional): Wether to include inset map. Defaults to False.

    Raises:
        ValueError: Error if input file is not a valid csv file

    Output:
        Map file as .jpg file
    """
    if cartopy_installed:
        if isinstance(input_data, str):
            path = Path(input_data)
            if path.is_file() and path.suffix == ".csv":
                df = pd.read_csv(path)
            else:
                raise ValueError("Ensure file is a valid .csv file")
        else:
            df = input_data

        df = max_dh_chem(input_data=df, drillhole_id=DH_ID)

        df = normalise_crustal_abundace(df, element=element, ppm_column_name=PPM)

        # parameters
        max_v, min_v = (
            df["Normalised_crustal_abund_(ppm)"].max().astype(int),
            df["Normalised_crustal_abund_(ppm)"].min().astype(int),
        )
        levels = list(range(min_v, max_v, 1))
        cmap = plt.get_cmap("plasma")
        if log_scale:
            norm = LogNorm()
        else:
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        n_dh = len(df[DH_ID])

        # map paramaters
        mpl.rcParams["agg.path.chunksize"] = 10000
        label = f"{element} values times average crustal abundance"
        inset_title = f"Number of drill holes:\n{n_dh}"
        x, y = df[LONG].values, df[LAT].values
        max_val, min_val, mean_val = (
            df[PPM].max(),
            df[PPM].min(),
            df[PPM].mean(),
        )

        # file output
        if out_path is not None:
            out_path = Path(out_path)
            if plot_type == "point":
                out_fig = out_path / f"Max_downhole_{element}.jpg"
            else:
                out_fig = out_path / f"Interpolated_max_downhole_{element}.jpg"
        else:
            out_path = Path.cwd()
            if plot_type == "point":
                out_fig = out_path / f"Max_downhole_{element}.jpg"
            else:
                out_fig = out_path / f"Interpolated_max_downhole_{element}.jpg"

        # plot

        if plot_type == "point":
            title = f"Maximum down-hole {element} values"
            fig, view, inset = SA_base_map(
                title=title,
                inset_title=inset_title,
                projection=projection,
                places=PLACES,
                extent=EXTENT,
                add_inset=add_inset,
            )
            plot = view.scatter(
                x,
                y,
                c=df["Normalised_crustal_abund_(ppm)"],
                cmap=cmap,
                norm=norm,
                alpha=0.6,
                transform=ccrs.PlateCarree(),
            )
        elif plot_type == "interpolate":
            title = f"Interpolated maximum down-hole {element} values"

            try:
                gx, gy, img = interpolate(
                    data=df, long=LONG, lat=LAT, value=NORM_DATA, projection=projection
                )
            except (QhullError, ZeroDivisionError):
                print("Interpolation error")

            fig, view, inset = SA_base_map(
                title=title,
                inset_title=inset_title,
                projection=projection,
                add_inset=add_inset,
                extent=extent,
                places=places,
            )
            plot = view.pcolormesh(gx, gy, img, cmap=cmap, norm=norm)
        else:
            print("Plot method not implemented")
            pass

        if log_scale:
            fig.colorbar(plot, ax=view, shrink=0.4, pad=0.01, label=label)
        else:
            fig.colorbar(
                plot, ax=view, shrink=0.4, pad=0.01, label=label, boundaries=levels
            )

        if add_inset:
            annot = f"Element concentration:\nmax: {max_val:.2f}ppm\nmean: {mean_val:.2f}ppm\nmin: {min_val:.2f}ppm"  # noqa: E501
            view.annotate(text=annot, xy=(0.33, 0.09), xycoords="axes fraction")
            inset.plot(
                x,
                y,
                color="blue",
                marker="o",
                markersize=2,
                linestyle="None",
                transform=ccrs.Geodetic(),
            )

        plt.savefig(out_fig, dpi=300, bbox_inches="tight")
        plt.close()

    else:
        logger.warning("Function not avaliable. Install Cartopy to use")
        print("Cartopy not installed")


def plot_max_downhole_interval(
    input_data: Union[str, pd.DataFrame],
    element: str,
    interval: int = 10,
    plot_type: str = "point",
    projection: int = PROJECTION,
    extent: List[int] = EXTENT,
    places: List[List[Union[float, float, str]]] = PLACES,
    log_scale: bool = True,
    out_path: Optional[str] = None,
    add_inset: bool = False,
) -> None:
    """Plot of the maximum down hole geochemical values per interval in a dataset.

    .. warning::
        Requires ``Cartopy`` to be installed to use.

    This function takes either a DataFrame or a path to a valid csv file containing
    a single element drillhole dataset. It will isolate the maximum value for each
    interval in each drillhole, create a normalised to crustal abundance column and
    then create either a point or interpolated grid map of the maximum values.

    The map can be customised to different locations and projections by editing the
    user configuration file projection, extent and places.

    Args:
        input_data (Union[str, pd.DataFrame]): Path to clean and processed single
            element dataset in csv format or Pandas dataframe of clean and processed
            single element dataset.
        element (str): The element to normalise, to retreive value from config file.
        interval (int, optional): The interval to aggregate over down hole.
            Defaults to 10.
        plot_type (str, optional): Either "point" or "interpolate. Defaults to "point".
        projection (int, optional): Map projection to use inputted as epsg number, i.e.
            3107 for GDA94/SA Lambert. See https://epsg.io for values.
            Defaults to PROJECTION.
        extent (List[int], optional): Map extents in correct values for projection. List
            of values corresponding to [left, right, top, bottom].
            Defaults to EXTENT.
        places (List[List[Union[float, float, str]]], optional): Localities to include
            on map plot with coordinates in appropriate values for he projection. List
            of values corresponding to [latitude, longitude, label]. Defaults to PLACES.
        log_scale (bool, optional): Wether to plot data on a log or linear scale.
            Defaults to True.
        out_path (Optional[str], optional): Optional path to place output file.
            Defaults to None.
        add_inset (bool, optional): Wether to include inset map. Defaults to False.

    Raises:
        ValueError: Error if input file is not a valid csv file

    Output:
        Map file as .jpg file
    """
    if cartopy_installed:
        if isinstance(input_data, str):
            path = Path(input_data)
            if path.is_file() and path.suffix == ".csv":
                df = pd.read_csv(path)
            else:
                raise ValueError("Ensure file is a valid .csv file")
        else:
            df = input_data

        df = max_dh_chem_interval(
            processed_data=df,
            interval=interval,
            drillhole_id=DH_ID,
            start_depth_label=START_DEPTH,
            end_depth_label=END_DEPTH,
        )

        df = normalise_crustal_abundace(df, element=element, ppm_column_name=PPM)

        # create grouped dataframe for each interval
        depth_grouped = df.groupby("bin")

        # loop over grouping and generate plot
        for name, group in depth_grouped:
            # account for possible empty groups
            if not len(group) < 1:

                # parameters
                max_v, min_v = (
                    group["Normalised_crustal_abund_(ppm)"].max(),
                    group["Normalised_crustal_abund_(ppm)"].min(),
                )

                levels = list(range(int(min_v), int(max_v), 1))
                cmap = plt.get_cmap("plasma")
                if log_scale:
                    norm = LogNorm()
                else:
                    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
                n_dh = len(group[DH_ID])

                # map paramaters
                mpl.rcParams["agg.path.chunksize"] = 10000
                label = f"{element} values times average crustal abundance"
                inset_title = f"Number of drill holes:\n{n_dh}"
                x, y = group[LONG].values, group[LAT].values
                max_val, min_val, mean_val = (
                    group[PPM].max(),
                    group[PPM].min(),
                    group[PPM].mean(),
                )

                # file output
                if out_path is not None:
                    out_path = Path(out_path)
                    if plot_type == "point":
                        out_fig = out_path / f"Max_downhole_{element}_{name}m.jpg"
                    else:
                        out_fig = (
                            out_path
                            / f"Interpolated_max_downhole_{element}_{name}m.jpg"  # noqa
                        )
                else:
                    out_path = Path.cwd()
                    if plot_type == "point":
                        out_fig = out_path / f"Max_downhole_{element}_{name}m.jpg"
                    else:
                        out_fig = (
                            out_path
                            / f"Interpolated_max_downhole_{element}_{name}m.jpg"  # noqa
                        )

                # plot

                if plot_type == "point":
                    title = f"Maximum down-hole {element} values at {name}m interval"
                    fig, view, inset = SA_base_map(
                        title=title,
                        inset_title=inset_title,
                        projection=projection,
                        places=places,
                        extent=extent,
                        add_inset=add_inset,
                    )
                    plot = view.scatter(
                        x,
                        y,
                        c=group["Normalised_crustal_abund_(ppm)"],
                        cmap=cmap,
                        norm=norm,
                        alpha=0.6,
                        transform=ccrs.PlateCarree(),
                    )
                elif plot_type == "interpolate":
                    title = f"Interpolated maximum down-hole {element} values at {name}m interval"  # noqa: E501
                    try:
                        gx, gy, img = interpolate(
                            data=group,
                            long=LONG,
                            lat=LAT,
                            value=NORM_DATA,
                            projection=projection,
                        )
                    except (QhullError, ZeroDivisionError):
                        print("Interpolation error, skipping")
                        continue
                    fig, view, inset = SA_base_map(
                        title=title,
                        inset_title=inset_title,
                        projection=projection,
                        places=places,
                        extent=extent,
                        add_inset=add_inset,
                    )
                    plot = view.pcolormesh(gx, gy, img, cmap=cmap, norm=norm)
                else:
                    print("Plot method not implemented")
                    pass

                if log_scale:
                    fig.colorbar(plot, ax=view, shrink=0.4, pad=0.01, label=label)
                else:
                    fig.colorbar(
                        plot,
                        ax=view,
                        shrink=0.4,
                        pad=0.01,
                        label=label,
                        boundaries=levels,
                    )

                if add_inset:
                    annot = f"Element concentration:\nmax: {max_val:.2f}ppm\nmean: {mean_val:.2f}ppm\nmin: {min_val:.2f}ppm"  # noqa: E501
                    view.annotate(text=annot, xy=(0.33, 0.09), xycoords="axes fraction")
                    inset.plot(
                        x,
                        y,
                        color="blue",
                        marker="o",
                        markersize=2,
                        linestyle="None",
                        transform=ccrs.Geodetic(),
                    )

                plt.savefig(out_fig, dpi=300, bbox_inches="tight")
                plt.close()
            else:
                logger.warning("Function not avaliable. Install Cartopy to use")
                print("Cartopy not installed")
