"""Functions to load and filter input geochem data

.. currentmodule:: pygeochemtools.geochem.create_dataset
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import importlib.resources as pkg_resources
from pathlib import Path
from typing import List, Optional, Union

import dask.dataframe as dd
import pandas as pd

from ..utils import config


def clean_dataset(
    df: pd.DataFrame, value: str, dash_BDL_indicator: bool = False
) -> pd.DataFrame:
    """Remove non-numeric characters.

    Clean non-numeric characters from dataframe and flag below detection
    limit rows (1), and greater than measurable rows (2) in new BDL column.

    Args:
        df (pd.DataFrame): Input dataframe to clean.
        value (str): Name of column containing geochemical data values.
        dash_BDL_indicator (bool): Indicator if the '-' sign indicates below
            detection limits or not. Defaults to False.

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    # create BDL/ODL flag and remove strings from values
    df["BDL"] = 0
    if not dash_BDL_indicator:
        # drop rows that contain a '-' sign, removes both '-12' and '5-10' range values
        df.drop(
            df[df[value].str.contains(r"-", na=False, regex=False)].index, inplace=True
        )
    else:
        df.loc[df[value].str.contains("-", na=False, regex=False), "BDL"] = 1

    df.loc[df[value].str.contains("<", na=False, regex=False), "BDL"] = 1
    df.loc[df[value].str.contains(">", na=False, regex=False), "BDL"] = 2
    df[value] = (
        df[value].astype(str).str.replace(r"[<>-]", "", regex=True).astype(float)
    )

    return df


def handle_BDL(df: pd.DataFrame, units: str) -> pd.DataFrame:
    """Convert below detection limit values to low, non-zero values.

    Converts below detection limit values, like "<10", to low numeric ppm values.
    All BDL units are converted to a value of 0.001ppm except ppb values which are
    converted to 0.00001ppm.

    .. note::
        Requires clean_dataset() function to be run to create the "BDL" flag column
        first.

    Args:
        df (pd.DataFrame): Input dataframe to clean.
        units (str): Name of the units column headder in df.

    Returns:
        pd.DataFrame: DataFrame with BDL values converted to low ppm values in the
            "converted_ppm" column.
    """
    # convert the BDL values to low but non-zero values
    df = df
    df.loc[df["BDL"] == 1, "converted_ppm"] = 0.001
    # convert bdl values to 0.01ppb for ppb values
    df.loc[(df["BDL"] == 1) & (df[units] == "ppb"), "converted_ppm"] = 0.00001

    return df


def add_sarig_chem_method(df: pd.DataFrame) -> pd.DataFrame:
    """Add normalised chem method columns to dataset.

    Function to map normalised chem method types onto the SARIG CHEM_METHOD_CODE column.
    The chem methods provided in the SARIG dataset relate to individual lab codes. This
    function maps those codes, where known, to a generic analysis method, digestion and
    fusion type.

    This is useful for further EDA and cleaning of data, as some methods are no longer
    applicable, or contain too much noise.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Dataframe with 'CHEM_METHODE_CODE mapped to three new columns:
        'DETERMINATION', 'DIGESTION' and 'FUSION'
    """
    from .. import data  # relative-import the *package* containing the templates

    stream = pkg_resources.open_text(data, "sarig_method_code_map.csv")
    chem_methods = pd.read_csv(stream, encoding="utf-8")

    determination_map = chem_methods.set_index("CHEM_METHOD")[
        "DETERMINATION_CODE_RD"
    ].to_dict()
    digestion_map = chem_methods.set_index("CHEM_METHOD")["DIGESTION_CODE_RD"].to_dict()
    fusion_map = chem_methods.set_index("CHEM_METHOD")["FUSION_TYPE"].to_dict()

    df["DETERMINATION"] = df.CHEM_METHOD_CODE.map(determination_map).fillna("unknown")
    df["DIGESTION"] = df.CHEM_METHOD_CODE.map(digestion_map).fillna("unknown")
    df["FUSION"] = df.CHEM_METHOD_CODE.map(fusion_map).fillna("unknown")

    return df


class LoadAndFilter:
    """Class to load and filter geochem datasets from csv input."""

    def __init__(self) -> None:
        """Dask dataframe object"""
        self.ddf = None
        self.loaded = False
        self.partial_filter_ddf = None

    def load_sarig_data(self, path: str) -> None:
        """Load data from the sarig_rs_chem_exp.csv dataset.

        This function uses dask to handle very large input datasets.

        .. warning::
            The the sarig_rs_chem_exp.csv data is in a long format, with
            each individual analysis as a single row!

        Args:
            path (str): Path to main sarig_rs_chem_exp.csv input file.
        """
        path = Path(path)
        if path.is_file() and path.suffix == ".csv":
            self.ddf = dd.read_csv(
                path,
                dtype={
                    "ROCK_GROUP_CODE": "object",
                    "ROCK_GROUP": "object",
                    "LITHO_CODE": "object",
                    "LITHO_CONF": "object",
                    "LITHOLOGY_NAME": "object",
                    "LITHO_MODIFIER": "object",
                    "MAP_SYMBOL": "object",
                    "STRAT_CONF": "object",
                    "STRAT_NAME": "object",
                    "COLLECTORS_NUMBER": "object",
                    "COLLECTED_DATE": "object",
                    "DH_NAME": "object",
                    "OTHER_ANALYSIS_ID": "object",
                    "LABORATORY": "object",
                    "VALUE": "object",
                    "CHEM_METHOD_CODE": "object",
                    "CHEM_METHOD_DESC": "object",
                },
            )
            print("Data loaded")
        else:
            print("Unable to load from file. Make sure file is a correct .csv")
        self.loaded = True

    def load_chem_data(self, path: str) -> None:
        """Not implemented yet. Func to load generic datasets.

        Args:
            path (str): Path to input csv file.
        """
        print("function not implemented yet")

    def list_columns(self):
        """Return the column headers from the dataset"""
        return self.ddf.columns

    def list_sample_types(self):
        """Return a list of sample types in the dataset"""
        SAMPLE_TYPE = config.column_names["sample_type"]
        return self.ddf[SAMPLE_TYPE].unique().compute()

    def list_elements(self):
        """Return a list of elements in the dataset"""
        ELEMENT = config.column_names["element"]
        return list(self.ddf[ELEMENT].unique().compute())

    def sarig_filter_drillhole_element(
        self, element: str, dh_only: bool
    ) -> pd.DataFrame:
        """Create a 'clean' single element dataset derived from the sarig_rs_chem_exp.csv.

            This isolates samples from drillholes (ones that have a drill hole id) and
            the selected element from the whole dataset and is used to create
            input data for further processing.

        Args:
            element (str): The element to extract and create a sub-dataset of.
            dh_only (bool): Wether to filter to drillholes only or return all sample
                types.

        Returns:
            pd.DataFrame: Dataframe filtered to the desired element.
        """
        ddf_ = self.ddf
        if dh_only:
            ddf_ = ddf_.dropna(subset=["DRILLHOLE_NUMBER"])
        ddf_ = ddf_[
            [
                "SAMPLE_NO",
                "SAMPLE_SOURCE_CODE",
                "DRILLHOLE_NUMBER",
                "DH_DEPTH_FROM",
                "DH_DEPTH_TO",
                "SAMPLE_ANALYSIS_NO",
                "ANALYSIS_TYPE_DESC",
                "LABORATORY",
                "CHEM_CODE",
                "VALUE",
                "UNIT",
                "CHEM_METHOD_CODE",
                "LONGITUDE_GDA2020",
                "LATITUDE_GDA2020",
            ]
        ]
        ddf_ = ddf_[ddf_.UNIT != "cps"]
        return ddf_[ddf_.CHEM_CODE == element].compute()

    def sarig_filter(
        self,
        sample_type: Optional[List[str]] = None,
        elements: Optional[List[str]] = None,
        drillholes: Optional[Union[List[int], bool]] = None,
    ) -> pd.DataFrame:
        """Filter sarig dataset.

        Reduce the size of the sarig_rs_chem_exp.csv dataset by filtering samples based
        on a list of elements, sample types and/or drillhole numbers, or a combination
        of all three.


        Args:
            sample_type (Optional[List[str]], optional): List of sample types to
                include. Defaults to None.
            elements (Optional[List[str]], optional): List of elements to include.
                Defaults to None.
            drillholes (Optional[Union[List[int], bool]], optional): Either a list of
                drillhole numbers to filter to, or True to filter dataset to just
                those samples from drillholes. Defaults to None.

        Raises:
        MemoryError: If filtered dataset is still too large to fit in avaliable memory.

        Returns:
            pd.DataFrame: Dataframe containing only those samples belonging to the
                listed sample types
        """
        ddf_ = self.ddf
        if isinstance(drillholes, bool):
            if drillholes:
                ddf_ = ddf_.dropna(subset=["DRILLHOLE_NUMBER"])
            else:
                pass
        if isinstance(drillholes, list):
            ddf_ = ddf_[ddf_["DRILLHOLE_NUMBER"].isin(drillholes)]
        if sample_type is not None:
            ddf_ = ddf_[ddf_["SAMPLE_SOURCE"].isin(sample_type)]
        if elements is not None:
            ddf_ = ddf_[ddf_["CHEM_CODE"].isin(elements)]

        try:
            return ddf_.compute()
        except MemoryError:
            print(
                "Ran into a MemoryError, your dataset is probably still too big to \
                fit in your avaliable memory"
            )
