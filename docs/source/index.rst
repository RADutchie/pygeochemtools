.. pygeochemtools documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pygeochemtools
===============

*A CLI based eclectic set of geochemical data manipulation, QC and plotting tools.*

*Pygeochemtools* is a python library and command line interface tool to enable rapid manipulation, filtering, QC and plotting
of geochemical data. It is primarily designed to allow people with limited or no coding experience to deal with
very large datasets when programs like Excel will struggle. It is designed to natively load and manipulate the geochemical datasets output by the Geological
Survey of South Australia, but will easily handle other datasets with a little bit of configuration in later updates.

Why *pygeochemtools*
----------------------

The SA Geodata database (available via the `SARIG <https://map.sarig.sa.gov.au/>`_ portal data catalogue `here <https://catalog.sarig.sa.gov.au/geonetwork/srv/eng/catalog.search#/metadata/e02583a8-c167-48b4-b6ce-d7acb12418a0>`_)
contains over 10 Gb of geochemical data. That’s a lot of chemistry. Explorers often request extracts of this data set, but then find it a challenge to handle all that data.
Because of the size and amount of data, programs like Excel wont even open the file, and if the extract is small enough to open,
explorers often find the format of the data a challenge. Generally, people like to use wide data for analysis, where each row in a
table represents all the data about a single sample. But database exports are in a long format where each row represents a single data point.

*Pygeochemtools* provides an abstraction and cli to make loading, filtering and restructuring this data easy. It uses python libraries
like dask and pandas under the hood to be able to deal with 'larger than memory' datasets, so you can load and filter those large datasets
and then output something more easy to handle with Excel or other tools.

*Pygeochemtools* is not a geochemical data analysis tool. For that I'd suggest tools like `pyrolite <https://github.com/morganjwilliams/pyrolite>`_ or
checking out the list of other amazing open source geoscience projects compiled by `Software Underground <https://github.com/softwareunderground/awesome-open-geoscience>`_. 

Functionality
---------------

Currently *pygeochemtools* provides the following functionality:
   - Filter large datasets based on a list of elements, sample type or drillhole numbers (or a combination of all three) and convert from long to wide format.
   - Add detailed geochemical methods columns onto the SARIG geochemical dataset.
   - Extract single element datasets from large geochemical datasets.
   - Plot maximum down hole geochemical data maps.
   - Plot maximum down hole chemistry per interval geochemical data maps.

.. note::

   This project is under active development. Suggestions, corrections and contributions are welcome. See the :ref:`development` 
   section on how to contribute.

Future Functionality
---------------------

Future additions to *pygeochemtools* will include:
   - The ability to load and transform generic geochemical data in long format, not specifically the SARIG data structure.
   - A data QA/QC function to generate accuracy and precision metrics on commercial lab data.
   - Other suggestions people may have?

To install *pygeochemtools*, visit the :ref:`getting_started` page and then have a look at the :ref:`usage` page
and the :ref:`examples` page to see how to use pygeochemtools.



.. toctree::
   :maxdepth: 1
   :caption: Contents:

   getting_started
   usage
   examples

.. toctree::
   :maxdepth: 1
   :caption: Development:
   
   development/getting_started
   development/make
   development/docs
   

.. toctree::
   :maxdepth: 1
   :caption: Reference:
   
   api/api
   requirements

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

