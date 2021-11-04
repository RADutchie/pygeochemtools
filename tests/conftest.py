#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: conftest
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>

Test fixtures
"""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def script_loc(request):
    return Path(request.fspath).parent


@pytest.fixture
def mock_csv_path(script_loc):
    return script_loc.joinpath("test_data/make_sarig_element_dataset_testdata.csv")


@pytest.fixture
def test_wide1(script_loc):
    return script_loc.joinpath("test_data/sarig_wide_test1.csv")


@pytest.fixture
def test_wide2(script_loc):
    return script_loc.joinpath("test_data/sarig_wide_test2.csv")


@pytest.fixture
def test_wide3(script_loc):
    return script_loc.joinpath("test_data/sarig_wide_test3.csv")


@pytest.fixture
def test_extract_element_expected(script_loc):
    return script_loc.joinpath("test_data/extract_element.csv")


@pytest.fixture
def mock_single_element_path(script_loc):
    return str(script_loc.joinpath("test_data/FeO_processed.csv"))


@pytest.fixture
def mock_single_element_dataframe(script_loc):
    path = script_loc.joinpath("test_data/FeO_processed.csv")
    return pd.read_csv(path)


@pytest.fixture
def mock_max_dh_expected_dataframe(script_loc):
    path = script_loc.joinpath("test_data/max_dh_expected.zip")
    return pd.read_pickle(path)


@pytest.fixture
def mock_max_dh_interval_expected_dataframe(script_loc):
    path = script_loc.joinpath("test_data/max_dh_interval_expected.zip")
    return pd.read_pickle(path)


@pytest.fixture
def mock_wide_methods_expected(script_loc):
    return script_loc.joinpath("test_data/wide_methods_expected.csv")
