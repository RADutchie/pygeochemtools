"""Logging utility

.. currentmodule:: pygeochemtools.utils.app_logger
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

import logging  # noqa: F401
import io  # noqa: F401


_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def get_file_handler():
    """Log file handler.

    Returns:
        FileHandler: Log FileHandler object.
    """
    file_handler = logging.FileHandler("x.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    """Log stream handler.

    Returns:
        TextIO: Log StreamHandler object
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name: str):
    """Get logger call.

    Args:
        name (str): Module name

    Returns:
        Logger: Return Logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
