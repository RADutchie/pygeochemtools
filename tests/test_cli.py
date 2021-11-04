#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>

This is the test module for the project's command-line interface (CLI)
module.
"""
# fmt: off
import pytest
import pygeochemtools.cli as cli
from pygeochemtools import __version__
# fmt: on
from click.testing import CliRunner, Result


# To learn more about testing Click applications, visit the link below.
# http://click.pocoo.org/5/testing/


def test_version_displays_library_version():
    """
    Arrange/Act: Run the `version` subcommand.
    Assert: The output matches the library version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["version"])
    assert (
        __version__ in result.output.strip()
    ), "Version number should match library version."


def test_verbose_output():
    """
    Arrange/Act: Run the `version` subcommand with the '-v' flag.
    Assert: The output indicates verbose logging is enabled.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["-v", "version"])
    assert (
        "Verbose" in result.output.strip()
    ), "Verbose logging should be indicated in output."


def test_show_config():
    """
    Arrange/Act: Run the `show_config` command.
    Assert: The output includes the correct headding `COLUMN_NAMES`".
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["show-config"])
    assert result.exit_code == 0
    assert "COLUMN_NAMES" in result.output.strip(), "COLUMN_NAMES should be in output."


def test_get_config_path():
    """
    Arrange/Act: Run the `get_config_path` command.
    Assert: The output includes the correct file name `config.yml`".
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["get-config-path"])
    assert result.exit_code == 0
    assert "config.yml" in result.output.strip(), "config.yml should be in output."


def test_list_columns(mock_csv_path):
    """
    Arrange/Act: Run the `list-columns` command.
    Assert: The output includes 'SAMPLE_NO' in output".
    """
    path = str(mock_csv_path)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli, ["list-columns", "-tsarig", path],
    )
    assert result.exit_code == 0
    assert "SAMPLE_NO" in result.output.strip(), "SAMPLE_NO should be in output."


def test_list_sample_types(mock_csv_path):
    """
    Arrange/Act: Run the `list-sample-types` command.
    Assert: The output includes 'Rock outcrop / float' in output".
    """
    path = str(mock_csv_path)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli, ["list-sample-types", "-tsarig", path],
    )
    assert result.exit_code == 0
    assert (
        "Rock outcrop / float" in result.output.strip()
    ), "Rock outcrop / float should be in output."


def test_list_elements(mock_csv_path):
    """
    Arrange/Act: Run the `list-elements` command.
    Assert: The output includes 'Fe' in output".
    """
    path = str(mock_csv_path)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli, ["list-elements", "-tsarig", path],
    )
    assert result.exit_code == 0
    assert "Fe" in result.output.strip(), "Fe should be in output."


@pytest.mark.parametrize(
    "i1, i2, i3, expected",
    [
        ("-el", "Fe,Au", "--dh-only", "test_wide1",),
        ("-st", "Rock outcrop / float", "--add-units", "test_wide2",),
        ("-dh", "280146,131650", "--add-units", "test_wide3",),
    ],
)
def test_convert_long_to_wide(mock_csv_path, tmp_path, i1, i2, i3, expected, request):
    """
    Arrange/Act: Run the `convert_long_to_wide` command.
    Assert: The output matches an expected output".
    """
    path = str(mock_csv_path)
    temp = str(tmp_path)
    expected = request.getfixturevalue(expected)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli, ["convert-long-to-wide", i1, i2, i3, "-o", temp, path],
    )
    print(result.__dict__)
    print(expected)
    assert result.exit_code == 0
    with open(tmp_path / "sarig_wide_data.csv", "r") as r:
        res = r.read()
    with open(expected, "r") as r:
        expected = r.read()
    assert res == expected


def test_extract_element(mock_csv_path, tmp_path, test_extract_element_expected):
    """
    Arrange/Act: Run the `extract_element` command.
    Assert: The output matches an expected output".
    """
    path = str(mock_csv_path)
    temp = str(tmp_path)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli,
        ["extract-element", "-el", "Fe", "--dh-only", "-t", "sarig", "-o", temp, path],
    )
    print(result.__dict__)
    assert result.exit_code == 0
    with open(tmp_path / "Fe_processed.csv", "r") as r:
        res = r.read()
    with open(test_extract_element_expected, "r") as r:
        expected = r.read()
    assert res == expected
