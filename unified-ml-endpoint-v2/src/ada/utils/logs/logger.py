"""Logging module to be used across the codebase."""

import logging
import os

from ada.utils.logs.color_log import ColorizedArgsFormatter


def get_logger(logger_name: str) -> logging.Logger:
    """Creates a logger object that can be imported across the codebase.

    It logs both to files inside a logs directory and to console.
    """

    if not os.path.exists("logs"):
        os.mkdir("logs")

    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():  # Prevent adding multiple handlers
        return logger
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logs/test.log")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = ColorizedArgsFormatter(
        fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
