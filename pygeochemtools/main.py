"""Main high-level functions module

.. currentmodule:: pygeochemtools.main
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

from pathlib import Path

import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import BoundaryNorm, LogNorm

from .aggregation import max_dh_chem
from .create_dataset import (
    add_sarig_chem_method,
    clean_dataset,
    convert_oxides,
    convert_ppm,
    export_dataset,
    load_sarig_element_dataset,
)
from .interpolate import interpolate
from .normalisation import normalise_crustal_abundace
from .plot import SA_base_map
from .utils import config

# global var set from config.yml
LONG = config.column_names["longitude"]
LAT = config.column_names["latitude"]
DH_ID = config.column_names["drillhole_id"]
PPM = config.column_names["converted_ppm"]
PROJECTION = config.projection


def make_sarig_element_dataset(
    path: str, element: str, export: bool = False, out_path: str = None
) -> pd.DataFrame:
    """Create a 'clean' single element dataset derived from the sarig_rs_chem_exp.csv.

    This isolates the selected element from the whole dataset, converts BDL values to
    a low, non zero value, drops rows that contain other symbols such as '>' and '-' and
    converts oxides to elements and all values to ppm. It also adds chem methods to the
    dataset where possible to allow further EDA.

    This data is used to create input data for further processing. This function uses
    dask to handle very large input datasets.

    Important note: the the sarig_rs_chem_exp.csv data is in a long format, with each
    individual analysis as a single row!

    This dataset may need additional EDA and cleaning prior to further processing. In
    that case set export to True to do further processing on the returned dataset.

    Args:
        path (str): Path to main sarig_rs_chem_exp.csv input file.
        element (str): The element to extract and create a sub-dataset of.
        export (bool): Wether to export a csv version of the element dataset.
        Defaults to False.
        out_path (str, optional): Path to place out put file. Defaults to path.

    Returns:
        pd.DataFrame: Dataframe of cleaned geochemical data
    """
    df = load_sarig_element_dataset(path, element=element)

    df = clean_dataset(df)

    df = convert_oxides(df, element=element)

    df = convert_ppm(df, element=element)

    df = add_sarig_chem_method(df)

    if export:
        export_dataset(df, element=element, path=path, out_path=out_path)

    return df


def plot_max_downhole_chem(
    input_data: str = None,
    df: pd.DataFrame = None,
    element: str = None,
    plot_type: str = "point",
    projection: int = PROJECTION,
    log_scale: bool = True,
    out_path: str = None,
    add_inset: bool = False,
) -> None:
    """[summary]

    Args:
        input_data (str, optional): [description]. Defaults to None.
        df (pd.DataFrame, optional): [description]. Defaults to None.
        element (str, optional): [description]. Defaults to None.
        type (str, optional): [description]. Defaults to "point".
        projection (int, optional): [description]. Defaults to PROJECTION.
        log_scale (bool, optional): [description]. Defaults to True.
        out_path (str, optional): [description]. Defaults to None.
        add_inset (bool, optional): [description]. Defaults to False.

    Raises:
        ValueError: [description]
    """
    if input_data is not None:
        path = Path(input_data)
        if path.is_file() and path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            raise ValueError("Ensure file is a valid .csv file")
    else:
        df = df

    df = max_dh_chem(processed_data=df, drillhole_id=DH_ID)

    df = normalise_crustal_abundace(df, element=element, ppm_column_name=PPM)

    # parameters
    max_v, min_v = (
        df["Normalised_crustal_abund (ppm)"].max().astype(int),
        df["Normalised_crustal_abund (ppm)"].min().astype(int),
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
            add_inset=add_inset,
        )
        plot = view.scatter(
            x,
            y,
            c=df["Normalised_crustal_abund (ppm)"],
            cmap=cmap,
            norm=norm,
            alpha=0.6,
            transform=ccrs.PlateCarree(),
        )
    elif plot_type == "interpolate":
        title = f"Interpolated maximum down-hole {element} values"
        gx, gy, img = interpolate(data=df, projection=projection)  # TODO
        fig, view, inset = SA_base_map(
            title=title,
            inset_title=inset_title,
            projection=projection,
            add_inset=add_inset,
        )
        plot = view.pcolormesh(gx, gy, img, cmap=cmap, norm=norm)  # TODO
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
        annot = f"Element concentration:\nmax: {max_val:.2f}ppm\nmean: {mean_val:.2f}ppm\nmin: {min_val:.2f}ppm"
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
