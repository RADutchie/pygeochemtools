# pygeochemtools

*A CLI based eclectic set of geochemical data manipulation, QC and plotting tools.*

*Pygeochemtools* is a python library and command line interface tool to enable rapid manipulation, filtering, QC and plotting
of geochemical data. It is primarily designed to allow people with limited or no coding experience to deal with
very large datasets when programs like Excel will struggle. It is designed to natively load and manipulate the geochemical datasets output by the Geological Survey of South Australia, but will easily handle other datasets with a little bit of configuration in later updates.

For more information checkout the [pygeochemtools](http://pygeochemtools.readthedocs.io/) documentation.

## Project Features

Currently *pygeochemtools* provides the following functionality:
   * Filter large datasets based on a list of elements, sample type or drillhole numbers (or a combination of all three) and convert from long to wide format.
   * Add detailed geochemical methods columns onto the SARIG geochemical dataset.
   * Extract single element datasets from large geochemical datasets.
   * Plot maximum down hole geochemical data maps.
   * Plot maximum down hole chemistry per interval geochemical data maps.

## Getting Started

The project's documentation contains a section to help you
[get started](https://pygeochemtools.readthedocs.io/en/latest/getting_started.html) as a user or
developer of the library.

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

* [Project Documentation](http://pygeochemtools.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **Rian Dutch** - *Initial work* - [github](https://github.com/RADutchie)

See also the list of [contributors](https://github.com/RADutchie/pygeochemtools/contributors) who participated in this project.

## LicenseMIT License

Copyright (c) Rian Dutch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.