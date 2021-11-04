"""Normalisation functions

.. currentmodule:: pygeochemtools.normalisation
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import pandas as pd

from ..utils import config


def normalise_crustal_abundace(
    df: pd.DataFrame, element: str, ppm_column_name: str
) -> pd.DataFrame:
    """Create a column with ppm values normalised against average crusta abundance.

    Uses the average crustal abundance values of Rudnick and Gao, 2004.

    Args:
        df (pd.DataFrame): [description]#TODO
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
            f"Element {element} does not have a crustal abundance value in the config.yml file"  # noqa: E501
        )
    df["Normalised_crustal_abund_(ppm)"] = df[ppm_column_name].apply(
        lambda x: x / norm_val
    )

    return df
