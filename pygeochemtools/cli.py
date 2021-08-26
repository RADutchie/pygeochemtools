#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: pygeochemtools.cli
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""
import logging
from pathlib import Path
from pygeochemtools.main import plot_max_downhole_interval

import click

from .__init__ import (
    __version__,
    make_sarig_element_dataset,
    plot_max_downhole_chem,
)
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


@click.group()
@click.option(
    "--verbose", "-v", count=True, help="Enable verbose output; 1 = less, 4 = more.",
)
@pass_info
def cli(info: Info, verbose: int):
    """Run pygeochemtools.

    An eclectic set of geochemical data manipulation and plotting tools.
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
    click.secho("COLUMN_NAMES", fg="blue", bold=True)
    click.secho(config.column_names, fg="red")
    click.secho("PLACES", fg="blue", bold=True)
    click.secho(config.places, fg="red")
    click.secho("EXTENT", fg="blue", bold=True)
    click.secho(config.extent, fg="red")
    click.secho("PROJECTION", fg="blue", bold=True)
    click.secho(config.projection, fg="red")
    click.secho("CRUSTAL_ABUND", fg="blue", bold=True)
    click.secho(config.crustal_abund, fg="red")


@cli.command()
@pass_info
def get_config_path(_: Info):
    """Display path to user editable config.yml file."""
    path = config.path
    click.echo(path)


@cli.command()
@pass_info
def edit_config(_: Info):
    """Launch default editor to edit user configuration"""
    path = config.path
    click.edit(filename=path)


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@pass_info
@click.argument("path", type=click.Path(exists=True))
@click.argument("element", type=str)
@click.option(
    "-t",
    "--type",
    type=click.Choice(["sarig", "gen"]),
    help="Select input file structure",
)
@click.option(
    "-e", "--export", default=True, help="Optional flag to turn-off file export"
)
@click.option(
    "-o", "--out-path", help="Optional path to place output file, defaults to PATH",
)
def extract_element(_: Info, path, element, type, export, out_path):
    """Extract single element dataset

    Requires path to file and element to extract.
    """
    click.secho(f"Dataset structure set to {type}", fg="blue")
    if type == "sarig":
        make_sarig_element_dataset(
            path=path, element=element, export=export, out_path=out_path
        )

    else:
        click.secho(f"{type} not implemented yet", fg="red")

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
    "-i",
    "--add-inset",
    default=False,
    help="Optional flag to add inset map with drillhole locations",
)
def plot_max_downhole(_: Info, path, element, plot_type, scale, out_path, add_inset):
    """Plot maximum downhole geochemical values map

    Requires path to data file and element.
    """
    click.secho(f"Map output set to {plot_type}", fg="blue")
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
    "-i",
    "--add-inset",
    default=False,
    help="Optional flag to add inset map with drillhole locations",
)
def plot_max_downhole_intervals(
    _: Info, path, element, interval, plot_type, scale, out_path, add_inset
):
    """Plot maximum downhole geochemical values map for each interval

    Requires path to data file, element and interval. The interval should be in
    whole meters as an integer.
    """
    click.secho(f"Map output set to {plot_type}", fg="blue")
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
