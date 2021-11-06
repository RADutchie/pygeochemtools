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


class _Config:
    """Load user configuration object
    """

    def __init__(self) -> None:
        """User config
        """
        self._config = None
        self.get_config()

    def get_config(self):
        """Read config in from config.yml"""
        try:
            # read config and store in _config
            with pkg_resources.open_text(data, "config.yml") as c:
                self._config = yaml.load(c, Loader=yaml.FullLoader)
                return self._config

        except FileNotFoundError:
            logger.info("Using default config")
            with pkg_resources.open_text(data, "default_config.yml") as c:
                self._config = yaml.load(c, Loader=yaml.FullLoader)
                return self._config

    @property
    def column_names(self):
        return self._config["COLUMN_NAMES"]

    @property
    def places(self):
        return self._config["PLACES"]

    @property
    def extent(self):
        return self._config["EXTENT"]

    @property
    def projection(self):
        return self._config["PROJECTION"]

    @property
    def crustal_abund(self):
        return self._config["CRUSTAL_ABUND"]

    @property
    def path_to_config(self):
        return os.path.join(data.__path__[0], "config.yml")


config = _Config()
