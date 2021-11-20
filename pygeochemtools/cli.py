#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

.. currentmodule:: pygeochemtools.cli
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""
import logging
import os
from pathlib import Path

import click
from rich.pretty import pprint as rprint

from .__init__ import __version__
from .geochem import LoadAndFilter, make_sarig_element_dataset, sarig_long_to_wide
from .map import plot_max_downhole_chem, plot_max_downhole_interval
from .utils import config

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


class NaturalOrderGroup(click.Group):
    """Command group to list commands in the order given"""

    def list_commands(self, ctx):
        """List commands in the order given"""
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
@click.option(
    "--verbose", "-v", count=True, help="Enable verbose output; 1 = less, 4 = more.",
)
@pass_info
def cli(info: Info, verbose: int):
    """Run pygeochemtools.

    An eclectic set of geochemical data manipulation, QC and plotting tools.
    """
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


@cli.command()
@pass_info
def show_config(_: Info):
    """Display the user configuration."""
    # configuration = config.config.__str__()
    click.secho("COLUMN_NAMES", fg="red", bold=True)
    rprint(config.column_names, indent_guides=False)
    click.secho("PLACES", fg="red", bold=True)
    rprint(config.places, indent_guides=False)
    click.secho("EXTENT", fg="red", bold=True)
    rprint(config.extent, indent_guides=False)
    click.secho("PROJECTION", fg="red", bold=True)
    rprint(config.projection, indent_guides=False)
    click.secho("CRUSTAL_ABUND", fg="red", bold=True)
    rprint(config.crustal_abund, indent_guides=False)


@cli.command()
@pass_info
def get_config_path(_: Info):
    """Display path to user editable config.yml file."""
    path = config.path_to_config
    click.echo(path)


@cli.command()
@pass_info
def edit_config(_: Info):
    """Launch default editor to edit user configuration"""
    path = config.path_to_config
    click.edit(filename=path)


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@pass_info
@click.option(
    "-t",
    "--type",
    "type_",
    type=click.Choice(["sarig", "general"]),
    help="Select input file structure",
)
@click.argument("path", type=click.Path(exists=True))
def list_columns(_: Info, type_, path):
    """Display the column headers in the loaded dataset"""
    dataset = LoadAndFilter()
    click.secho(f"Dataset structure set to {type_}", fg="red")
    if type_ == "sarig":
        dataset.load_sarig_data(path)
        rprint(dataset.list_columns(), indent_guides=False)
    else:
        click.secho(f"{type_} not implemented yet", fg="red")


@cli.command()
@pass_info
@click.option(
    "-t",
    "--type",
    "type_",
    type=click.Choice(["sarig", "gen"]),
    help="Select input file structure",
)
@click.argument("path", type=click.Path(exists=True))
def list_sample_types(_: Info, type_, path):
    """Display the sample types listed in the sample type column"""
    dataset = LoadAndFilter()
    click.secho(f"Dataset structure set to {type_}", fg="red")
    if type_ == "sarig":
        dataset.load_sarig_data(path)
        rprint(dataset.list_sample_types(), indent_guides=False)
    else:
        click.secho(f"{type_} not implemented yet", fg="red")


@cli.command()
@pass_info
@click.option(
    "-t",
    "--type",
    "type_",
    type=click.Choice(["sarig", "gen"]),
    help="Select input file structure",
)
@click.argument("path", type=click.Path(exists=True))
def list_elements(_: Info, type_, path):
    """Display the list of element labels in dataset"""
    dataset = LoadAndFilter()
    click.secho(f"Dataset structure set to {type_}", fg="red")
    if type_ == "sarig":
        dataset.load_sarig_data(path)
        click.secho(dataset.list_elements(), fg="green")
    else:
        click.secho(f"{type_} not implemented yet", fg="red")


@cli.command()
@pass_info
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-el",
    "--elements",
    type=str,
    help="Enter a list of elements to filter to, or nothing",
)
@click.option(
    "-st",
    "--sample-type",
    type=str,
    help="Enter a list of sample types to filter to, or nothing",
)
@click.option(
    "-dh",
    "--drillholes",
    type=str,
    help="Enter a list of drillhole numbers to filter to, or Nothing",
)
@click.option(
    "--dh-only", is_flag=True, help="Filter to only drillholes",
)
@click.option(
    "--add-units", "include_units", is_flag=True, help="Include chem units",
)
@click.option(
    "--add-methods",
    "export_methods",
    is_flag=True,
    help="Export method metadata for the filtered samples",
)
@click.option(
    "-o", "--out-path", help="Optional path to place output file, defaults to PATH",
)
def convert_long_to_wide(
    _: Info,
    path,
    elements,
    sample_type,
    drillholes,
    dh_only,
    include_units,
    export_methods,
    out_path,
):
    """Convert sarig long form data to wide form.

    Requires path to sarig_rs_chem_exp file. You can filter this dataset down
    to a managable size either by providing a list of elements, sample types
    or drillhole numbers, or a combination of the three.

    Will output a file called sarig_wide_data.csv to either the current working directory or
    a directory specified with the -o option.

    Optional flags:
    --dh_only, will filter dataset to only include samples with a
    drillhole_id.

    --add-units, will include measurement units in the output file.

    --add-methods, will export an additional file called sarig_wide_methods.csv
    which will include the determination methods for each sample and analyte.

    Note:

    Elements, sample types and drillholes must be entered with a single ',' between
    them and no spaces, e.g. Au,Cu,Pb.
    Sample types which contain spaces must be enclosed in '' and typed exactly as
    presented in the file, e.g. 'Drill core,Rock outcrop / float'

    Example usage:

    Filter data to just Cu and Au, only from drillholes and include the units:

    `$ pygt convert-long-to-wide -el Cu,Au --inc-units --dh-only data/sarig_rs_chem_exp.csv`

    Filter data to just Cu, Fe and Pb analytes, only from Drill core and Soil samples, and include both units and
    export the methods as well:

    `$ pygt convert-long-to-wide -el Cu,Fe,Pb -st 'Drill core,Soil' --inc-units --inc-methods data/sarig_rs_chem_exp.csv`
    """  # noqa: E501
    # Convert click str input into list of str
    if isinstance(elements, str):
        elements = list(elements.split(","))

    if isinstance(sample_type, str):
        sample_type = list(sample_type.split(","))

    if dh_only:
        sarig_long_to_wide(
            path=path,
            elements=elements,
            sample_type=sample_type,
            drillholes=dh_only,
            include_units=include_units,
            export_methods=export_methods,
            export=True,
            out_path=out_path,
        )
    else:
        if isinstance(drillholes, str):
            # Convert click str input into list of int
            drillholes = [int(i) for i in (list(drillholes.split(",")))]

        sarig_long_to_wide(
            path=path,
            elements=elements,
            sample_type=sample_type,
            drillholes=drillholes,
            include_units=include_units,
            export_methods=export_methods,
            export=True,
            out_path=out_path,
        )

    if out_path:
        click.echo(f"File written to {out_path}")
    else:
        click.echo(f"File written to {os.getcwd()}")


@cli.command()
@pass_info
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-el", "--element", type=str, multiple=True, help="Select one or more elements"
)
@click.option(
    "--dh-only", is_flag=True, help="Filter to only drillholes",
)
@click.option(
    "-t",
    "--type",
    "type_",
    type=click.Choice(["sarig", "gen"]),
    help="Select input file structure",
)
@click.option(
    "-o", "--out-path", help="Optional path to place output file, defaults to PATH",
)
def extract_element(_: Info, path, element, dh_only, type_, out_path):
    """Extract single element dataset(s)

    Requires path to file and element to extract. You can extract multiple elements at
    once by providing multiple element options.

    Will output a file called 'element'_processed.csv to either the current working directory or
    a directory specified with the -o option.

    By selecting --dh_only, will filter dataset to only include samples with a
    drillhole_id.

    Example:

    extract three element datasets from drillholes only from input datafile

    `$ pygt extract-element /test_input.csv -el Au -el Cu -el Fe --dh-only -t sarig`
    """  # noqa: E501
    click.secho(f"Dataset structure set to {type_}", fg="red")
    if type_ == "sarig":
        with click.progressbar(element) as bar:
            for e in bar:
                make_sarig_element_dataset(
                    path=path,
                    element=e,
                    dh_only=dh_only,
                    export=True,
                    out_path=out_path,
                )

    else:
        click.secho(f"{type_} not implemented yet", fg="red")

    if out_path:
        click.echo(f"File written to {out_path}")
    else:
        click.echo(f"File written to {path}")


@cli.command()
@pass_info
@click.argument("path", type=click.Path(exists=True))
@click.argument("element", type=str)
@click.option(
    "-t",
    "--plot-type",
    type=click.Choice(["point", "interpolate"]),
    help="Select map type",
)
@click.option(
    "-s",
    "--scale",
    default=True,
    help="Select either log-scale (default) or set to False for linear scale",
)
@click.option(
    "-o",
    "--out-path",
    help="Optional path to place output file, defaults to current working directory",
)
@click.option(
    "--add-inset",
    is_flag=True,
    help="Optional flag to add inset map with drillhole locations",
)
def plot_max_downhole(_: Info, path, element, plot_type, scale, out_path, add_inset):
    """Plot maximum downhole geochemical values map

    Requires path to extracted single element data file and element to plot.

    NOTE: The element needs to be the element name, not an oxide, i.e. Fe for Fe2O3

    NOTE: Must have Cartopy library installed to use.

    Example:

    Create an interpolated plot for maximum Cu values down hole with inset map:

    `$ pygt plot-max-downhole -t interpolate --add-inset path/to/Cu_processed.csv Cu`
    """
    click.secho(f"Map output set to {plot_type}", fg="red")
    if plot_type == "point":
        plot_max_downhole_chem(
            input_data=path,
            element=element,
            plot_type="point",
            log_scale=scale,
            out_path=out_path,
            add_inset=add_inset,
        )

    elif plot_type == "interpolate":
        plot_max_downhole_chem(
            input_data=path,
            element=element,
            plot_type="interpolate",
            log_scale=scale,
            out_path=out_path,
            add_inset=add_inset,
        )
    else:
        click.secho(f"{plot_type} not implemented", fg="red")

    if out_path:
        click.echo(f"File written to {out_path}")
    else:
        click.echo(f"File written to {Path.cwd()}")


@cli.command()
@pass_info
@click.argument("path", type=click.Path(exists=True))
@click.argument("element", type=str)
@click.argument("interval", type=int)
@click.option(
    "-t",
    "--plot-type",
    type=click.Choice(["point", "interpolate"]),
    help="Select map type",
)
@click.option(
    "-s",
    "--scale",
    default=True,
    help="Select either log-scale (default) or set to False for linear scale",
)
@click.option(
    "-o",
    "--out-path",
    help="Optional path to place output file, defaults to current working directory",
)
@click.option(
    "--add-inset",
    is_flag=True,
    help="Optional flag to add inset map with drillhole locations",
)
def plot_max_downhole_intervals(
    _: Info, path, element, interval, plot_type, scale, out_path, add_inset
):
    """Plot maximum downhole geochemical values map for each interval

    Requires path to extracted single element data file, element and interval. The
    interval should be in whole meters as an integer.

    NOTE: The element needs to be the element name, not an oxide, i.e. Fe for Fe2O3

    NOTE: Must have Cartopy library installed to use.

    Example:

    Create a point plot for maximum Fe values every 20m down hole with inset map, from
    Fe2O3 data with linear scale:

    `$ pygt plot-max-downhole-intervals -t point --add-inset -s False
    path/to/Fe2O3_processed.csv Fe 20`
    """
    click.secho(f"Map output set to {plot_type}", fg="red")
    if plot_type == "point":
        plot_max_downhole_interval(
            input_data=path,
            element=element,
            interval=interval,
            plot_type="point",
            log_scale=scale,
            out_path=out_path,
            add_inset=add_inset,
        )

    elif plot_type == "interpolate":
        plot_max_downhole_interval(
            input_data=path,
            element=element,
            interval=interval,
            plot_type="interpolate",
            log_scale=scale,
            out_path=out_path,
            add_inset=add_inset,
        )
    else:
        click.secho(f"{plot_type} not implemented", fg="red")

    if out_path:
        click.echo(f"File written to {out_path}")
    else:
        click.echo(f"File written to {Path.cwd()}")
