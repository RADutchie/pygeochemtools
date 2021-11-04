#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_main
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>

Tests for main high level functions in geochem.__init__
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from io import StringIO

from pygeochemtools.geochem import make_sarig_element_dataset, sarig_long_to_wide


def test_make_sarig_element_dataset(mock_csv_path):
    """
    Arrange: Load test and expected dataframes.
    Act: Run make_sarig_dataset().
    Assert: return equals expected_df.
    """
    # fmt: off
    expected_df = """SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020	BDL	converted_ppm	DETERMINATION	DIGESTION	FUSION
    9022	DC	123456	10	20	5112	GEOCHEMISTRY		Fe	8.25	%	IC1	134.2249681	-30.3564693	0	82500	ICP-OES	PERC	unknown
    10906	CT	654321	183.6	195.3	10385	GEOCHEMISTRY		Fe	740	ppm		135.1358039	-33.2075473	0	740	unknown	unknown	unknown"""
    # fmt: on
    expected_df = pd.read_csv(
        StringIO(expected_df),
        sep="\t",
        dtype={
            "VALUE": float,
            "DRILLHOLE_NUMBER": float,
            "LABORATORY": object,
            "converted_ppm": float,
        },
    )
    result = (
        make_sarig_element_dataset(mock_csv_path, "Fe")
        .reset_index()
        .drop(["index"], axis=1)
    )

    assert_frame_equal(result, expected_df)


@pytest.mark.parametrize(
    "i1, i2, expected",
    [
        ({"elements": ["Fe", "Au"]}, {"drillholes": True}, "test_wide1",),
        (
            {"sample_type": ["Rock outcrop / float"]},
            {"include_units": True},
            "test_wide2",
        ),
        ({"drillholes": [280146, 131650]}, {"include_units": True}, "test_wide3",),
    ],
)
def test_sarig_long_to_wide(mock_csv_path, i1, i2, expected, request, tmp_path):
    """
    Arrange: Load test and expected dataframes.
    Act: Run sarig_long_to_wide().
    Assert: return equals expected_df.
    """
    path = str(mock_csv_path)
    temp = str(tmp_path)
    expected = request.getfixturevalue(expected)

    result = sarig_long_to_wide(path, **i1, **i2, export=True, out_path=temp)

    print(result.__dict__)
    assert type(result) == pd.DataFrame

    with open(tmp_path / "sarig_wide_data.csv", "r") as r:
        res = r.read()
    with open(expected, "r") as r:
        expected = r.read()
    assert res == expected


def test_sarig_long_to_wide_methods(
    mock_csv_path, mock_wide_methods_expected, request, tmp_path
):
    """
    Arrange: Load test and expected dataframes.
    Act: Run sarig_long_to_wide().
    Assert: return equals expected_df.
    """
    path = str(mock_csv_path)
    temp = str(tmp_path)
    expected = request.getfixturevalue(mock_wide_methods_expected)

    result = sarig_long_to_wide(path, export_methods=True, export=True, out_path=temp)

    print(result.__dict__)

    with open(tmp_path / "sarig_wide_methods.csv", "r") as r:
        res = r.read()
    with open(expected, "r") as r:
        expected = r.read()
    assert res == expected
