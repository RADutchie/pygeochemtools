"""Functions to calculate the max chem value down hole

.. currentmodule:: pygeochemtools.aggregation
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union


def max_dh_chem(
    input_data: Union[str, pd.DataFrame], drillhole_id: str
) -> pd.DataFrame:
    """Function to aggregate the processed elemental geochemical data and
    return a dataframe containing max value in each drillhole.

    Requires long format data.

    Args:
        input_data (Union[str, pd.DataFrame]): Path to clean and processed single
            element dataset in csv format or Pandas dataframe of clean and processed
            single element dataset.
        drillhole_id (str): drillhole identifier in dataset.

    Raises:
        ValueError: Error raised if input file is not a valid csv file

    Returns:
        pd.DataFrame: Dataframe containing only the maximum value from each drill hole
    """
    if isinstance(input_data, str):
        path = Path(input_data)
        if path.is_file() and path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            raise ValueError("Ensure file is a valid .csv file")
    else:
        df = input_data

    df_max = df.loc[df.groupby([drillhole_id])["converted_ppm"].idxmax()]

    return df_max


def max_dh_chem_interval(
    input_data: Union[str, pd.DataFrame],
    interval: int,
    drillhole_id: str,
    start_depth_label: str,
    end_depth_label: str,
) -> pd.DataFrame:
    """Function to aggregate the processed singel elemental geochemical data and
    return a dataframe containing max value in each interval down hole for each
    drillhole.

    Requires long format data.

    Args:
        input_data (Union[str, pd.DataFrame]): Input single element geochemical data,
            in long form, as either a path to a csv input file or a pandas dataframe.
        interval (int): The interval, in whole meters, overwhich to aggregate down hole.
        drillhole_id (str): Column headder containing the drill hole identifier.
        start_depth_label (str): Column headder containing the start or from depth data.
        end_depth_label (str): Column headder containing the finish or to depth data.

    Raises:
        ValueError: Error if input file is not a valid csv file

    Returns:
        pd.DataFrame: Dataframe continging the maximum value for each specified
            interval.
    """

    if isinstance(input_data, str):
        path = Path(input_data)
        if path.is_file() and path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            raise ValueError("Ensure file is a valid .csv file")
    else:
        df = input_data

    # calculate median to-from depth
    df["median_depth"] = df[[start_depth_label, end_depth_label]].apply(
        np.nanmedian, axis=1
    )

    # create bins to max depth and then bin median depths
    bins = pd.interval_range(
        start=0, end=df.median_depth.max(), freq=interval, closed="left"
    )
    df["bin"] = pd.cut(df["median_depth"], bins=bins)

    df.dropna(subset=["converted_ppm"], inplace=True)

    # aggregate max values over range
    grp = df.groupby([drillhole_id, "bin"])
    df_max = df.loc[grp.converted_ppm.idxmax().dropna()]

    return df_max
