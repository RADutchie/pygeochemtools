"""Normalisation fuctions

.. currentmodule:: pygeochemtools.noralisation
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import pandas as pd

from .utils import config

PPM_COLUMN_NAME = config.column_names["converted_ppm"]


def normalise_crustal_abundace(
    df: pd.DataFrame, element: str, ppm_column_name: str = PPM_COLUMN_NAME
) -> pd.DataFrame:
    """Create a column with ppm values normalised against average crusta abundance.

    Uses the average crustal abundance values of Rudnick and Gao, 2004.

    Args:
        df (pd.DataFrame): [description]
        element (str): [description]
        ppm_column_name (str): [Desc]

    Returns:
        pd.DataFrame: [description]
    """
    df = df
    try:
        norm_val = config.crustal_abund[element]
    except KeyError:
        print(
            f"Element {element} does not have a crustal abundance value in the config.yml file"
        )
    df["Normalised_crustal_abund (ppm)"] = df[ppm_column_name].apply(
        lambda x: x / norm_val
    )

    return df
