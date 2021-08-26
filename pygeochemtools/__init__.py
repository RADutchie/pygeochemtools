#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A cli to create and plot maximum down hole geochemical element maps.

.. currentmodule:: pygeochemtools
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

from .version import __version__, __release__  # noqa
from .main import (
    make_sarig_element_dataset,
    plot_max_downhole_chem,
    plot_max_downhole_interval,
)  # noqa
