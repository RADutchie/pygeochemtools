"""User config helpers

.. currentmodule:: pygeochemtools.utils.config
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import importlib.resources as pkg_resources
import yaml
import os
from .. import data


class Config:
    """Load user configuration object
    """

    def __init__(self) -> None:
        """User config
        """
        # print("Loading config")
        with pkg_resources.open_text(data, "config.yml") as c:
            self.config = yaml.load(c, Loader=yaml.FullLoader)
        self.column_names = self.config["COLUMN_NAMES"]
        self.places = self.config["PLACES"]
        self.extent = self.config["EXTENT"]
        self.projection = self.config["PROJECTION"]
        self.crustal_abund = self.config["CRUSTAL_ABUND"]
        self.path = os.path.join(data.__path__[0], "config.yml")


config = Config()
