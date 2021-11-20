"""User config helpers

.. currentmodule:: pygeochemtools.utils.config
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import importlib.resources as pkg_resources
import os

import yaml

from .. import data
from ..utils import app_logger

logger = app_logger.get_logger(__name__)


class Config:
    """Load user configuration object"""

    def __init__(self) -> None:
        """Store and load user config"""
        self._config = None
        self.get_config()

    def get_config(self):
        """Read config.

        Loads user config from the user_config.yml located in the
        pygeochemtools.data module
        """

        # read config and store in _config
        with pkg_resources.open_text(data, "user_config.yml") as c:
            self._config = yaml.load(c, Loader=yaml.FullLoader)
            return self._config

    @property
    def column_names(self):
        """Return configured column names"""
        return self._config["COLUMN_NAMES"]

    @property
    def places(self):
        """Return configured place names and coordinates"""
        return self._config["PLACES"]

    @property
    def extent(self):
        """Return configured map extent"""
        return self._config["EXTENT"]

    @property
    def projection(self):
        """Return configured map projection"""
        return self._config["PROJECTION"]

    @property
    def crustal_abund(self):
        """Return configured crustal abundance values"""
        return self._config["CRUSTAL_ABUND"]

    @property
    def path_to_config(self):
        """Return path to configuration file"""
        return os.path.join(data.__path__[0], "user_config.yml")


config = Config()
