#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_create_dataset
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>

This is a sample test module. #TODO update
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from io import StringIO

from pygeochemtools.geochem import (
    clean_dataset,
    convert_oxides,
    convert_ppm,
    handle_BDL,
)

"""
#TODO update docs
"""


def test_clean_dataset():
    """
    Arrange: Load test and expected dataframes.
    Act: Run clean_dataset().
    Assert: clean_dataset return equals expected_df.
    """
    # fmt: off
    test_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020
    9448	DC	133881.0	NaN	NaN	5314	GEOCHEMISTRY	NaN	Cu	-10	ppm	NaN	134.676298	-32.730410
    9661	DC	6363.0	56.69	57.91	5458	GEOCHEMISTRY	NaN	Cu	<15	ppm	NaN	134.541359	-30.703724
    9662	DC	6363.0	59.13	60.35	5460	GEOCHEMISTRY	NaN	Cu	>15	ppm	NaN	134.541359	-30.703724
    9663	DC	6364.0	47.55	48.77	5462	GEOCHEMISTRY	NaN	Cu	10	ppm	NaN	134.541349	-30.703724"""

    expected_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020	BDL
    9661	DC	6363.0	56.69	57.91	5458	GEOCHEMISTRY	NaN	Cu	15.0	ppm	NaN	134.541359	-30.703724	1
    9662	DC	6363.0	59.13	60.35	5460	GEOCHEMISTRY	NaN	Cu	15.0	ppm	NaN	134.541359	-30.703724	2
    9663	DC	6364.0	47.55	48.77	5462	GEOCHEMISTRY	NaN	Cu	10.0	ppm	NaN	134.541349	-30.703724	0"""
    # fmt: on

    test_df = pd.read_csv(StringIO(test_df), sep="\t")
    expected_df = pd.read_csv(StringIO(expected_df), sep="\t", dtype={"VALUE": float})
    result = clean_dataset(test_df, value="VALUE").reset_index().drop(["index"], axis=1)

    assert_frame_equal(result, expected_df)


def test_convert_oxides():
    # fmt: off
    """
    Arrange: Load test and expected dataframes.
    Act: Run convert_oxides().
    Assert: convert_oxides return equals expected_df.
    """
    
    test_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020
    6482	CT	131649.0	82.5	NaN	3797	GEOCHEMISTRY	NaN	Fe2O3	14.6	%	NaN	133.487917	-31.323508
    7788	CT	131648.0	97.5	100.5	4405	GEOCHEMISTRY	NaN	Fe2O3	7.1	%	NaN	133.547866	-31.525015
    7790	CT	131646.0	87.0	88.5	4408	GEOCHEMISTRY	NaN	Fe2O3	11.5	%	NaN	133.508892	-31.326100"""

    expected_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020
    6482	CT	131649.0	82.5	NaN	3797	GEOCHEMISTRY	NaN	Fe2O3	10.211933	%	NaN	133.487917	-31.323508
    7788	CT	131648.0	97.5	100.5	4405	GEOCHEMISTRY	NaN	Fe2O3	4.966077	%	NaN	133.547866	-31.525015
    7790	CT	131646.0	87.0	88.5	4408	GEOCHEMISTRY	NaN	Fe2O3	8.043646	%	NaN	133.508892	-31.326100"""
    # fmt: on

    test_df = pd.read_csv(StringIO(test_df), sep="\t")
    expected_df = pd.read_csv(StringIO(expected_df), sep="\t", dtype={"VALUE": float})
    result = convert_oxides(test_df, element="Fe2O3", value="VALUE")

    assert_frame_equal(result, expected_df)


def test_convert_ppm():
    # fmt: off
    """
    Arrange: Load test and expected dataframes.
    Act: Run convert_ppm().
    Assert: convert_ppm return equals expected_df.
    """
    
    test_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020	BDL
    9661	DC	6363.0	56.69	57.91	5458	GEOCHEMISTRY	NaN	Fe2O3	15.0	ppb	NaN	134.541359	-30.703724	1
    9662	DC	6363.0	59.13	60.35	5460	GEOCHEMISTRY	NaN	Fe2O3	15.0	%	NaN	134.541359	-30.703724	2
    9663	DC	6364.0	47.55	48.77	5462	GEOCHEMISTRY	NaN	Fe2O3	10.0	ppm	NaN	134.541349	-30.703724	0"""

    expected_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020	BDL\tconverted_ppm
    9661	DC	6363.0	56.69	57.91	5458	GEOCHEMISTRY	NaN	Fe2O3	15.0	ppb	NaN	134.541359	-30.703724	1	0.0015
    9662	DC	6363.0	59.13	60.35	5460	GEOCHEMISTRY	NaN	Fe2O3	15.0	%	NaN	134.541359	-30.703724	2	150000.000
    9663	DC	6364.0	47.55	48.77	5462	GEOCHEMISTRY	NaN	Fe2O3	10.0	ppm	NaN	134.541349	-30.703724	0	10.000"""
    # fmt: on

    test_df = pd.read_csv(StringIO(test_df), sep="\t")
    expected_df = pd.read_csv(StringIO(expected_df), sep="\t")
    result = (
        convert_ppm(test_df, value="VALUE", units="UNIT")
        .reset_index()
        .drop(["index"], axis=1)
    )

    assert_frame_equal(result, expected_df)


def test_handle_BDL():
    # fmt: off
    """
    Arrange: Load test and expected dataframes.
    Act: Run handle_BDL().
    Assert: handle_BDL return equals expected_df.
    """
    test_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020	BDL\tconverted_ppm
    9661	DC	6363.0	56.69	57.91	5458	GEOCHEMISTRY	NaN	Fe2O3	15.0	ppb	NaN	134.541359	-30.703724	1	0.0015
    9662	DC	6363.0	59.13	60.35	5460	GEOCHEMISTRY	NaN	Fe2O3	15.0	%	NaN	134.541359	-30.703724	2	150000.000
    9663	DC	6364.0	47.55	48.77	5462	GEOCHEMISTRY	NaN	Fe2O3	10.0	ppm	NaN	134.541349	-30.703724	0	10.000"""

    expected_df = """
    SAMPLE_NO	SAMPLE_SOURCE_CODE	DRILLHOLE_NUMBER	DH_DEPTH_FROM	DH_DEPTH_TO	SAMPLE_ANALYSIS_NO	ANALYSIS_TYPE_DESC	LABORATORY	CHEM_CODE	VALUE	UNIT	CHEM_METHOD_CODE	LONGITUDE_GDA2020	LATITUDE_GDA2020	BDL\tconverted_ppm
    9661	DC	6363.0	56.69	57.91	5458	GEOCHEMISTRY	NaN	Fe2O3	15.0	ppb	NaN	134.541359	-30.703724	1	0.00001
    9662	DC	6363.0	59.13	60.35	5460	GEOCHEMISTRY	NaN	Fe2O3	15.0	%	NaN	134.541359	-30.703724	2	150000.000
    9663	DC	6364.0	47.55	48.77	5462	GEOCHEMISTRY	NaN	Fe2O3	10.0	ppm	NaN	134.541349	-30.703724	0	10.000"""
    # fmt: on

    test_df = pd.read_csv(StringIO(test_df), sep="\t")
    expected_df = pd.read_csv(StringIO(expected_df), sep="\t")
    result = handle_BDL(test_df, units="UNIT")

    assert_frame_equal(result, expected_df)


# TODO test_add_chem_method

# TODO test_load_sarig_element_dataset
