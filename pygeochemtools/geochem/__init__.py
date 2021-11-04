"""
Geochemical data manipulation module

.. currentmodule:: pygeochemtools.geochem
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

from typing import List, Optional, Union

import pandas as pd

from ..utils import config, export_dataset
from .aggregation import max_dh_chem, max_dh_chem_interval  # noqa: F401
from .conversions import convert_oxides, convert_ppm  # noqa: F401
from .create_dataset import LoadAndFilter  # noqa: F401
from .create_dataset import add_sarig_chem_method, clean_dataset, handle_BDL
from .normalisation import normalise_crustal_abundace  # noqa: F401
from .transform import long_to_wide, sarig_methods_wide  # noqa: F401

# Global variables from user config file
VALUE = config.column_names["value"]
UNITS = config.column_names["units"]
SAMPLE_TYPE = config.column_names["sample_type"]
ELEMENT = config.column_names["element"]
DH_ID = config.column_names["drillhole_id"]
SAMPLE_ID = config.column_names["sample_no"]


def make_sarig_element_dataset(
    path: str,
    element: str,
    dh_only: bool = True,
    export: bool = False,
    out_path: Optional[str] = None,
) -> pd.DataFrame:
    """Create a 'clean' single element drillhole dataset derived from the
    sarig_rs_chem_exp.csv.

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
    dataset = LoadAndFilter()
    dataset.load_sarig_data(path)
    df = dataset.sarig_filter_drillhole_element(element, dh_only=dh_only)

    df = clean_dataset(df, value=VALUE, dash_BDL_indicator=False)

    df = convert_oxides(df, element=element, value=VALUE)

    df = convert_ppm(df, value=VALUE, units=UNITS)

    df = handle_BDL(df, units=UNITS)

    df = add_sarig_chem_method(df)

    if export:
        export_dataset(df, label=(element + "_processed"), path=path, out_path=out_path)

    return df


def sarig_long_to_wide(
    path: str,
    elements: Optional[List[str]] = None,
    sample_type: Optional[List[str]] = None,
    drillholes: Optional[Union[List[int], bool]] = None,
    include_units: bool = False,
    export_methods: bool = False,
    export: bool = False,
    out_path: Optional[str] = None,
) -> pd.DataFrame:
    """Convert sarig long form data to wide form.

    Args:
        path (str): [description]
        elements (Optional[List[str]]): [description]
        sample_type (Optional[List[str]]): [description]
        drillholes (Optional[Union[List[int], bool]]): [description]
        include_units (bool): [description]
        export_methods (bool): [description]
        export (bool): [description]
        out_path (Optional[str]): [description]

    Returns:
        pd.DataFrame: [description]
    """
    # TODO add conversion long to wide with el and sample selection and output
    dataset = LoadAndFilter()
    dataset.load_sarig_data(path)

    filtered_data = dataset.sarig_filter(
        elements=elements, sample_type=sample_type, drillholes=drillholes
    )
    filtered_metadata = filtered_data.drop_duplicates(subset=[SAMPLE_ID]).drop(
        columns=[
            "SAMPLE_ANALYSIS_NO",
            "OTHER_ANALYSIS_ID",
            "ANALYSIS_TYPE_DESC",
            "LABORATORY",
            "CHEM_CODE",
            "VALUE",
            "UNIT",
            "CHEM_METHOD_CODE",
            "CHEM_METHOD_DESC",
        ]
    )

    wide_vals = long_to_wide(
        filtered_data,
        sample_id=SAMPLE_ID,
        element_id=ELEMENT,
        value=VALUE,
        units=UNITS,
        include_units=include_units,
    )

    wide_data_out = filtered_metadata.merge(wide_vals, how="inner", on=SAMPLE_ID)

    if export_methods:
        filtered_data = add_sarig_chem_method(filtered_data)
        wide_methods = sarig_methods_wide(
            filtered_data, sample_id=SAMPLE_ID, element_id=ELEMENT
        )
        wide_methods_out = filtered_metadata.merge(
            wide_methods, how="inner", on=SAMPLE_ID
        )
        export_dataset(
            wide_methods_out, label="sarig_wide_methods", path=path, out_path=out_path
        )

    if export:
        export_dataset(
            wide_data_out, label="sarig_wide_data", path=path, out_path=out_path
        )

    return wide_data_out
