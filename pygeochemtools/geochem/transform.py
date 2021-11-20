"""Data transformation

.. currentmodule:: pygeochemtools.transform
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""
import numpy as np
import pandas as pd


def long_to_wide(
    df: pd.DataFrame,
    sample_id: str,
    element_id: str,
    value: str,
    units: str,
    include_units: bool = False,
) -> pd.DataFrame:
    """Convert geochemical data tables from long to wide form.

    This function takes a dataframe of long form geochemical data, i.e. data with one
    row per element, and converts it to a standard wide form data with one row per
    sample and each element in a separate column.

    Args:
        df (pd.DataFrame): Dataframe containing long form data.
        sample_id (str): Name of column containing sample ID's.
        element_id (str): Name of column containing geochemical element names.
        value (str): Name of column containing geochemical data values.
        units (str): Name of column containing geochemical data units.
        include_units (bool, optional): Wether to include units in the output. Defaults
            to False.

    Returns:
        pd.DataFrame: Dataframe converted to wide table format with one sample per row
        and columns for each element.
    """
    df = df
    df = df.drop_duplicates(subset=[sample_id, element_id])

    if include_units:
        data = df.pivot(
            index=[sample_id], columns=element_id, values=[value]
        ).droplevel(0, axis=1)

        unit = (
            df.pivot(index=[sample_id], columns=element_id, values=[units])
            .add_suffix("_UNIT")
            .droplevel(0, axis=1)
        )

        assert (
            data.columns.size == unit.columns.size
        ), "pivoted column lengths aren't equal"

        c = np.empty((data.columns.size + unit.columns.size,), dtype=object,)
        c[0::2], c[1::2] = (
            data.columns,
            unit.columns,
        )

        df_wide = pd.concat([data, unit], axis=1)[c]

        return df_wide

    else:
        data = df.pivot(
            index=[sample_id], columns=element_id, values=[value]
        ).droplevel(0, axis=1)

        return data


def sarig_methods_wide(
    df: pd.DataFrame, sample_id: str, element_id: str,
) -> pd.DataFrame:
    """Create a corresponding methods table to match the pivoted wide form data.

    .. note::
        This requires the input dataframe to already have had methods mapping applied
        by running ``pygeochemtools.geochem.create_dataset.add_sarig_chem_method``
        function.

    Args:
        df (pd.DataFrame): Dataframe containing long form data.
        sample_id (str): Name of column containing sample ID's.
        element_id (str): Name of column containing geochemical element names.

    Returns:
        pd.DataFrame: Dataframe with mapped geochemical methods converted to wide form
            with one method per sample.
    """
    ...
    df = df
    df = df.drop_duplicates(subset=[sample_id, element_id])

    method_code = (
        df.pivot(index=[sample_id], columns=element_id, values=["CHEM_METHOD_CODE"],)
        .add_suffix("_METHOD_CODE")
        .droplevel(0, axis=1)
    )
    determination = (
        df.pivot(index=[sample_id], columns=element_id, values=["DETERMINATION"],)
        .add_suffix("_DETERMINATION")
        .droplevel(0, axis=1)
    )
    digestion = (
        df.pivot(index=[sample_id], columns=element_id, values=["DIGESTION"],)
        .add_suffix("_DIGESTION")
        .droplevel(0, axis=1)
    )
    fusion = (
        df.pivot(index=[sample_id], columns=element_id, values=["FUSION"],)
        .add_suffix("_FUSION")
        .droplevel(0, axis=1)
    )
    assert (
        method_code.columns.size
        == determination.columns.size  # noqa: W503
        == digestion.columns.size  # noqa: W503
        == fusion.columns.size  # noqa: W503
    ), "pivoted column lengths aren't equal"

    c = np.empty(
        (
            method_code.columns.size
            + determination.columns.size  # noqa: W503
            + digestion.columns.size  # noqa: W503
            + fusion.columns.size,  # noqa: W503
        ),
        dtype=object,
    )
    c[0::4], c[1::4], c[2::4], c[3::4] = (
        method_code.columns,
        determination.columns,
        digestion.columns,
        fusion.columns,
    )

    df_wide = pd.concat([method_code, determination, digestion, fusion], axis=1)[c]

    return df_wide
