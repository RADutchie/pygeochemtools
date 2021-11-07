
.. toctree::
    :glob:

.. _development:

***************
Contributing
***************

``Pygeochemtools`` is under active development. If you find any problems, have feature requests or wish to contribute
to the source code or documentation, consider opening a new github `issue <https://github.com/RADutchie/pygeochemtools/issues>`_
or `pull request <https://github.com/RADutchie/pygeochemtools/pulls>`_.

Installing local development version
====================================

This section provides instructions for setting up your development environment.  If you follow the
steps from top to bottom you should be ready to roll by the end.


Get the Source
---------------

The source code for the `pygeochemtools` project lives at `github <https://github.com/RADutchie/pygeochemtools>`_.  
You can use ``git clone`` to get it.

.. code-block:: bash

   git clone https://github.com/RADutchie/pygeochemtools.git

Create the Virtual Environment
------------------------------

You can create a virtual environment and install the project's dependencies using :ref:`make <make>`.

.. code-block:: bash

    make venv
    make install
    source venv/bin/activate

If you are using Anaconda environments

.. code-block:: bash

    conda create --name <env_name> python=3.8
    conda activate <env_name>
    make install

You will need to ensure the additional dependencies required for ``Cartopy`` are also installed. See :ref:`getting started <getting_started>` section. 

Try It Out
-----------

One way to test out the environment is to run the tests.  You can do this with the ``make test``
target.

.. code-block:: bash

    make test

If the tests run and pass, you're ready to roll.

Running the CLI
---------------

To install an editable verion of the project locally to enable use of the CLI while changing the
source code you can use the ``make build`` target.

.. code-block:: bash

    make build 

Getting Answers
---------------

Once the environment is set up, you can perform a quick build of this project
documentation using the ``make answers`` target.

.. code-block:: bash

    make answers
