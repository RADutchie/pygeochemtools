#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_aggregation
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>

Tests for aggregation module
"""

import pytest
from pandas.testing import assert_frame_equal
from pygeochemtools.geochem import max_dh_chem, max_dh_chem_interval

"""
tests for aggregation function module
"""


@pytest.mark.parametrize(
    "arg", ["mock_single_element_dataframe", "mock_single_element_path"],
)
def test_max_dh_chem(arg, mock_max_dh_expected_dataframe, request):
    """
    Arrange: Load test and expected dataframes.
    Act: Run make_sarig_dataset().
    Assert: return equals expected_df.
    """
    expected_df = mock_max_dh_expected_dataframe
    arg = request.getfixturevalue(arg)
    result = max_dh_chem(arg, drillhole_id="DRILLHOLE_NUMBER")

    assert_frame_equal(result, expected_df)


@pytest.mark.parametrize(
    "arg", ["mock_single_element_dataframe", "mock_single_element_path"],
)
def test_max_dh_chem_interval(arg, mock_max_dh_interval_expected_dataframe, request):
    """
    Arrange: Load test and expected dataframes.
    Act: Run make_sarig_dataset().
    Assert: return equals expected_df.
    """
    expected_df = mock_max_dh_interval_expected_dataframe
    arg = request.getfixturevalue(arg)
    result = max_dh_chem_interval(
        arg,
        interval=20,
        drillhole_id="DRILLHOLE_NUMBER",
        start_depth_label="DH_DEPTH_FROM",
        end_depth_label="DH_DEPTH_TO",
    )

    assert_frame_equal(result, expected_df)
