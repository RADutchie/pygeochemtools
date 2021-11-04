"""Functions to perform conversions on geochem data

.. currentmodule:: pygeochemtools.conversions
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import pandas as pd


def convert_oxides(df: pd.DataFrame, element: str, value: str) -> pd.DataFrame:
    """Convert selected oxides to elements

    Args:
        df (pd.DataFrame): Input dataframe
        element (str): Oxide to convert. Can be any of:
            'Fe2O3', 'FeO', 'U3O8', 'CoO', 'NiO'
        value (str): Name of column containing geochemical data values.

    Returns:
        pd.DataFrame: Dataframe with oxides converted in place
    """
    df = df

    if element == "Fe2O3":
        df[value] = df[value] / 1.4297
    elif element == "FeO":
        df[value] = df[value] / 1.2865
    elif element == "U3O8":
        df[value] = df[value] / 1.1792
    elif element == "CoO":
        df[value] = df[value] / 1.2715
    elif element == "NiO":
        df[value] = df[value] / 1.2725
    else:
        pass

    return df


def convert_ppm(
    df: pd.DataFrame, value: str, units: str, convert_wtperc: bool = True,
) -> pd.DataFrame:
    """Create new column called 'converted_ppm' and converts values to ppm.

    Args:
        df (pd.DataFrame): Input dataframe
        value (str): Name of column containing geochemical data values.
        units (str): Name of column containing geochemical data units.
        convert_wtperc (bool): Wether to convert wt% to ppm. Defaults to True

    Returns:
        pd.DataFrame: Dataframe with new 'converted_ppm' column
    """
    df = df

    df["converted_ppm"] = df[value]

    if convert_wtperc:
        df.loc[(df[units] == "%"), "converted_ppm"] = (
            df.loc[(df[units] == "%"), value] * 10000
        )

    df.loc[(df[units] == "ppb"), "converted_ppm"] = (
        df.loc[(df[units] == "ppb"), value] / 10000
    )

    return df
