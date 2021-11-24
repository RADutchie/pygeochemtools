
.. toctree::
    :glob:

.. _getting_started:

***************
Getting started
***************

Installing the Library
======================

``pygeochemtools`` requires Python version 3.8 or greater.

You can use pip to install ``pygeochemtools`` into a new virtual environment. 

.. code-block:: bash

    pip install pygeochemtools

.. note::
    pygeochemtools is not packaged for Anaconda, so ``conda install pygeochemtools`` wont work.

Optional dependencies
----------------------

``pygeochemtools`` requires `Cartopy <https://scitools.org.uk/cartopy/docs/latest/index.html>`_ in order to plot maps.
``Cartopy`` requires some additional dependencies to be able to run and so is not automatically installed with the above command.

To install ``pygeochemtools`` with map plotting functionality, first install the ``Cartopy`` dependencies GEOS, Shapely and PROJ.
See the ``Cartopy`` `installation guide <https://scitools.org.uk/cartopy/docs/latest/installing.html>`_ for details on how to do this.

You can then install ``pygeochemtools``, including ``Cartopy`` with pip.

.. code-block:: bash

    pip install pygeochemtools[cartopy]

Alternatively, if you use `Anaconda <https://www.anaconda.com/>`_, you can install Cartopy using conda. This may be the easiest option if you are on a windows system.

.. code-block:: bash

    conda install -c conda-forge cartopy

.. note::

    If you don't have ``Cartopy`` installed, you will see a warning message when using the CLI and will not be able to use the plotting functions

Building from source
---------------------

If you want to build ``pygeochemtools`` from source you can clone the source files from `github <https://github.com/RADutchie/pygeochemtools>`_
and build a local installation into a new virtual environment.

.. code-block:: bash

    git clone https://github.com/RADutchie/pygeochemtools.git
    cd pygeochemtools
    python -m pip install .

.. seealso:: :ref:`Development <development>` to install a local development version

