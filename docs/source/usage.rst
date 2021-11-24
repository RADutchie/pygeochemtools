
.. toctree::
    :glob:

.. _usage:

*********************************
How to use pygeochemtools
*********************************

Introduction
=============

*pygeochemtools* is designed to be used in a number of ways. If you're familiar with Python, the ``pygeochemtools`` package
can be used just like any other Python library. However, for those who are not used to using Python scripts, or just want to
quickly convert a data file or make a map, ``pygeochemtools`` is also designed to be used as a simple command line tool (CLI).

*pygeochemtools* Python api
===========================

The ``pygeochemtools`` package provides a relatively simple API to perform either the main automated functions, similar to
the output of the CLI, or access to the various functions and methods available.

To get started using the ``pygeochemtools`` api, you first need to:

.. code-block:: python

    import pygeochemtools as pygt

All the ``pygeochemtools`` functions and methods return a ``pandas`` DataFrame object, so you can incorporate any of the ``pygeochemtools``
functionality into your data workflows.

For the complete api, see the :ref:`api`.

Using the CLI
==============
Using the CLI is a simple method to quickly perform the main high-level functions and transformations in the ``pygeochemtools`` kit and
output new, filtered and transformed csv files.

Getting started with the CLI
-----------------------------
Once you have ``pygeochemtools`` properly installed in a virtual environment, and the virtual environment active, the CLI should just
work. In your shell of choice (e.g. bash, sh, cmd, powershell, Anaconda Prompt) type:

.. code-block:: bash
    
    pygt --help

This will bring up the main help/entry info for the CLI:

.. code-block:: bash

    Usage: pygt [OPTIONS] COMMAND [ARGS]...

    Run pygeochemtools.

    An eclectic set of geochemical data manipulation, QC and plotting tools.

    Options:
    -v, --verbose  Enable verbose output; 1 = less, 4 = more.  [x>=0]
    --help         Show this message and exit.

    Commands:
    show-config                  Display the user configuration.
    get-config-path              Display path to user editable config.yml...
    edit-config                  Launch default editor to edit user...
    version                      Get the library version.
    list-columns                 Display the column headers in the loaded...
    list-sample-types            Display the sample types listed in the...
    list-elements                Display the list of element labels in dataset
    convert-long-to-wide         Convert sarig long form data to wide form.
    extract-element              Extract single element dataset(s)
    plot-max-downhole            Plot maximum downhole geochemical values map
    plot-max-downhole-intervals  Plot maximum downhole geochemical values...

The CLI is built around four main functions:
    * setting user configuration
    * displaying dataset metadata
    * transforming data
    * plotting geochemical maps

To find out extra information, or how to use any of the listed commands, simply type the command and the ``--help`` option:

.. code-block:: bash

    ~$ pygt extract-element --help
    Usage: pygt extract-element [OPTIONS] PATH

      Extract single element dataset(s)

      Requires path to file and element to extract. You can extract multiple
      elements at once by providing multiple element options.

      Will output a file called 'element'_processed.csv to either the current
      working directory or a directory specified with the -o option.

      By selecting --dh_only, will filter dataset to only include samples with a
      drillhole_id.

      Example:

      extract three element datasets from drillholes only from input datafile

      `$ pygt extract-element /test_input.csv -el Au -el Cu -el Fe --dh-only -t
      sarig`

    Options:
      -el, --element TEXT     Select one or more elements
      --dh-only               Filter to only drillholes
      -t, --type [sarig|gen]  Select input file structure
      -o, --out-path TEXT     Optional path to place output file, defaults to PATH
      --help                  Show this message and exit.

User configuration
-------------------

In order to allow for some generalities and greater user control on the command line, ``pygeochemtools`` has a user configuration file
to pre-set a number of variables. This includes:

    - Setting column header names (This one is important for using different datasets, in the format 'variable_name': 'equivalent name in dataset')
    - Map place names and locations to annotate map output (latitude, longitude, label in decimal degrees) 
    - Map extents (west, east, south, north in decimal degrees)
    - Map projection (EPSG number for your projection from `<https://epsg.io>`_)
    - Average crustal abundance values for data normalisations

At runtime, ``pygeochemtools`` looks for the ``user_config.yml`` file, reads the config and applies the values.

**Commands:**

.. code-block:: bash

    show-config                  Display the user configuration.
    get-config-path              Display path to user editable user_config.yml file.
    edit-config                  Launch default editor to edit user_config.yml file.

.. warning::
    If you want to edit the config, it is recommended to duplicate the existing file and renaming it to ensure you have a backup of the
    original user_config file.

Dataset metadata
-----------------

These commands are useful to interrogate the labels in the dataset. This is important when trying to filter data, as the labels need to
exactly match those in the data.

**Commands**

.. code-block:: bash

    list-columns                 Display the column headers in the loaded dataset
    list-sample-types            Display the sample types listed in the loaded dataset
    list-elements                Display the list of element labels in dataset

**Example usage**

.. code-block:: bash

    ~$ pygt list-columns --help

    Usage: pygt list-columns [OPTIONS] PATH

    Display the column headers in the loaded dataset

    Options:
    -t, --type [sarig|general]  Select input file structure
    --help                      Show this message and exit.

.. code-block:: bash

    ~$ pygt list-columns -t sarig ~/geochem_data/test_input.csv
    Dataset structure set to sarig
    Data loaded
    Index(['SAMPLE_NO', 'SAMPLE_SOURCE_CODE', 'SAMPLE_SOURCE',
        'ROCK_GROUP_CODE', 'ROCK_GROUP', 'LITHO_CODE', 'LITHO_CONF',
        'LITHOLOGY_NAME', 'LITHO_MODIFIER', 'MAP_SYMBOL', 'STRAT_CONF',
        'STRAT_NAME', 'COLLECTED_BY', 'COLLECTORS_NUMBER', 'COLLECTED_DATE',
        'DRILLHOLE_NUMBER', 'DH_NAME', 'DH_DEPTH_FROM', 'DH_DEPTH_TO',
        'SITE_NO', 'EASTING_GDA2020', 'NORTHING_GDA2020', 'ZONE_GDA2020',
        'LONGITUDE_GDA2020', 'LATITUDE_GDA2020', 'LONGITUDE_GDA94',
        'LATITUDE_GDA94', 'SAMPLE_ANALYSIS_NO', 'OTHER_ANALYSIS_ID',
        'ANALYSIS_TYPE_DESC', 'LABORATORY', 'CHEM_CODE', 'VALUE', 'UNIT',
        'CHEM_METHOD_CODE', 'CHEM_METHOD_DESC'],
        dtype='object')
        (

Transforming data
-----------------

There are two tools available for data filtering and transformations:

**Convert SARIG dataset from long to wide**

.. code-block:: bash

    ~$ pygt convert-long-to-wide --help
    Usage: pygt convert-long-to-wide [OPTIONS] PATH

    Convert sarig long form data to wide form.

    Requires path to sarig_rs_chem_exp file. You can filter this dataset down to
    a manageable size either by providing a list of elements, sample types or
    drillhole numbers, or a combination of the three.

    Options:
    -el, --elements TEXT     Enter a list of elements to filter to, or nothing
    -st, --sample-type TEXT  Enter a list of sample types to filter to, or
                            nothing
    -dh, --drillholes TEXT   Enter a list of drillhole numbers to filter to, or
                            Nothing
    --dh-only                Filter to only drillholes
    --add-units              Include chem units
    --add-methods            Export method metadata for the filtered samples
    -o, --out-path TEXT      Optional path to place output file, defaults to
                            PATH
    --help                   Show this message and exit.

**Extract single element datasets**

.. code-block:: bash

    ~$ pygt extract-element --help
    Usage: pygt extract-element [OPTIONS] PATH

    Extract single element dataset(s)

    Requires path to file and element to extract. You can extract multiple
    elements at once by providing multiple element options.

    Options:
    -el, --element TEXT     Select one or more elements
    --dh-only               Filter to only drillholes
    -t, --type [sarig|gen]  Select input file structure
    -o, --out-path TEXT     Optional path to place output file, defaults to PATH
    --help                  Show this message and exit.

Both of these commands will output a new data file to either the current working directory (default) or a specified directory location.

Plotting geochemical maps
--------------------------

Once you have a single element dataset(s) available, ``pygeochemtools`` will allow you to generate either a point plot or interpolated
gridded map displaying either the maximum down hole chemical values, or the maximum values over a selected interval. 

.. code-block::

    ~$ pygt plot-max-downhole --help
    Usage: pygt plot-max-downhole [OPTIONS] PATH ELEMENT

    Plot maximum downhole geochemical values map

    Requires path to extracted single element data file and element to plot.

    Options:
    -t, --plot-type [point|interpolate]
                                    Select map type
    -s, --scale TEXT                Select either log-scale (default) or set to
                                    False for linear scale
    -o, --out-path TEXT             Optional path to place output file, defaults
                                    to current working directory
    --add-inset                     Optional flag to add inset map with
                                    drillhole locations
    --help                          Show this message and exit.

.. code-block:: bash

    ~$ pygt plot-max-downhole-intervals --help
    Usage: pygt plot-max-downhole-intervals [OPTIONS] PATH ELEMENT INTERVAL

    Plot maximum downhole geochemical values map for each interval

    Requires path to extracted single element data file, element and interval.
    The interval should be in whole meters as an integer.

    Options:
    -t, --plot-type [point|interpolate]
                                    Select map type
    -s, --scale TEXT                Select either log-scale (default) or set to
                                    False for linear scale
    -o, --out-path TEXT             Optional path to place output file, defaults
                                    to current working directory
    --add-inset                     Optional flag to add inset map with
                                    drillhole locations
    --help                          Show this message and exit.

Both of these map creation commands will output maps, as jpg files, to either the current working directory, or another specified
directory location.

.. note::

    For more detailed instructions and examples, run ``pygt [COMMAND] --help`` on the CLI and visit the :ref:`examples` page.