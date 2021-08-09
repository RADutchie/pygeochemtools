    """Functions to calculate the max chem value down hole"""

import pandas as pd
import numpy as np
from pathlib import Path


def max_dh_chem(processed_data: pd.DataFrame) -> pd.DataFrame:
    """Function to aggregate the processed elemental geochemical data and
    return a dataframe containing max value in each drillhole

    Args:
        processed_data (pd.DataFrame): [description]
        
    Returns:
        pd.DataFrame: [description]
    """
   #TODO possibly add path to processed file to run on processed dataset, unless just used as helper for interpolate
    df = processed_data

    df_max = df.loc[df.groupby(["DRILLHOLE_NUMBER"])["converted_ppm"].idxmax()]

    return df_max


def max_dh_chem_interval(processed_data: pd.DataFrame, dh_data: str, interval: int)-> pd.DataFrame:
    """Function to aggregate the processed elemental geochemical data and
    return a dataframe containing max value in each interval down hole for each
    drillhole

    Args:
        processed_data (pd.DataFrame): [description]
        dh_data (str): [description]
        interval (int): [description]

    Returns:
        pd.DataFrame: [description]
    """
    dh_data = Path(dh_data)

    df_DH_data = pd.read_csv(dh_data)
    df = processed_data

    # calculate median to-from depth
    df["median_depth"] = df[["DH_DEPTH_TO", "DH_DEPTH_FROM"]].apply(
        np.nanmedian, axis=1
    )

    # create bins to max depth and then bin median depths
    bins = pd.interval_range(
        start=0, end=df.median_depth.max(), freq=interval, closed="left"
    )
    df["bin"] = pd.cut(df["median_depth"], bins=bins)

    df.dropna(subset=["converted_ppm"], inplace=True)

    # aggregate max values over range
    grp = df.groupby(["DRILLHOLE_NUMBER", "bin"])
    df_max = df.loc[grp.converted_ppm.idxmax().dropna()]

    return df_max
