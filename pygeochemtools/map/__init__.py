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
from ..utils import config
from .interpolate import interpolate  # noqa: F401
from .map import SA_base_map  # noqa: F401

try:
    import cartopy.crs as ccrs
except ModuleNotFoundError:
    warnings.warn(
        "Cartopy module required for plotting: https://scitools.org.uk/cartopy/docs/latest/installing.html#requirements",  # noqa: E501
        UserWarning,
    )
    pass


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
    """[summary]#TODO

    Args:
        input_data (str, pd.DataFrame): [description].
        element (str): [description].
        plot_type (str, optional): [description]. Defaults to "point".
        projection (int, optional): [description]. Defaults to PROJECTION.
        log_scale (bool, optional): [description]. Defaults to True.
        out_path (str, optional): [description].
        add_inset (bool, optional): [description]. Defaults to False.

    Raises:
        ValueError: Ensure input_data is a valid CSV file.
    """
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
    """[summary]#TODO

    Args:
        input_data (str, optional): [description]. Defaults to None.
        df (pd.DataFrame, optional): [description]. Defaults to None.
        element (str, optional): [description]. Defaults to None.
        interval (int, optional): [description]. Defaults to 10.
        plot_type:str="point".
        projection (int, optional): [description]. Defaults to PROJECTION.
        log_scale (bool, optional): [description]. Defaults to True.
        out_path (str, optional): [description]. Defaults to None.
        add_inset (bool, optional): [description]. Defaults to False.

    Raises:
        ValueError: [description]
    """
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
                        out_path / f"Interpolated_max_downhole_{element}_{name}m.jpg"
                    )
            else:
                out_path = Path.cwd()
                if plot_type == "point":
                    out_fig = out_path / f"Max_downhole_{element}_{name}m.jpg"
                else:
                    out_fig = (
                        out_path / f"Interpolated_max_downhole_{element}_{name}m.jpg"
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
