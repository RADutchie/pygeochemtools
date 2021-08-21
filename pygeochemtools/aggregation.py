"""Functions to calculate the max chem value down hole

.. currentmodule:: pygeochemtools.aggregation
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import pandas as pd
import numpy as np
from pathlib import Path


def max_dh_chem(
    processed_data: pd.DataFrame = None,
    input_data: str = None,
    drillhole_id: str = "DRILLHOLE_NUMBER",
) -> pd.DataFrame:
    """Function to aggregate the processed elemental geochemical data and
    return a dataframe containing max value in each drillhole.

    Args:
        processed_data (pd.DataFrame): Pandas dataframe of clean and processed
            single element dataset. Defaults to None.
        input_data (str): Path to clean and processed single element dataset
            in csv format. Defaults to None.
        drillhole_id (str): drillhole identifier in dataset. Defaults to
            'DRILLHOLE_NUMBER'.

    Raises:
        ValueError: [description]

    Returns:
        pd.DataFrame: Dataframe containing only the maximum value from each drill hole.
    """
    if input_data is not None:
        path = Path(input_data)
        if path.is_file() and path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            raise ValueError("Ensure file is a valid .csv file")
    else:
        df = processed_data

    df_max = df.loc[df.groupby([drillhole_id])["converted_ppm"].idxmax()]

    return df_max


def max_dh_chem_interval(
    processed_data: pd.DataFrame = None,
    input_data: str = None,
    interval: int = 10,
    drillhole_id: str = "DRILLHOLE_NUMBER",
    start_depth_label: str = "DH_DEPTH_TO",
    end_depth_label: str = "DH_DEPTH_FROM",
) -> pd.DataFrame:
    """Function to aggregate the processed elemental geochemical data and
    return a dataframe containing max value in each interval down hole for each
    drillhole.

    Args:
        processed_data (pd.DataFrame, optional): [description]. Defaults to None.
        input_data (str, optional): [description]. Defaults to None.
        interval (int, optional): [description]. Defaults to 10.
        drillhole_id (str, optional): [description]. Defaults to "DRILLHOLE_NUMBER".
        start_depth_label (str, optional): [description]. Defaults to "DH_DEPTH_TO".
        end_depth_label (str, optional): [description]. Defaults to "DH_DEPTH_FROM".

    Raises:
        ValueError: [description]

    Returns:
        pd.DataFrame: [description]
    """

    if input_data is not None:
        path = Path(input_data)
        if path.is_file() and path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            raise ValueError("Ensure file is a valid .csv file")
    else:
        df = processed_data

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
