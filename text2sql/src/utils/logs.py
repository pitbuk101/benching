from loguru import logger
import sys

class CustomFormatter:
    COLORS = {
        "DEBUG": "\x1b[36;20m",      # torquoise
        "INFO": "\x1b[38;20m",       # grey
        "WARNING": "\x1b[33;20m",    # yellow
        "ERROR": "\x1b[31;20m",      # red
        "CRITICAL": "\x1b[31;1m",    # bold red
    }
    RESET = "\x1b[0m"
    FORMAT = (
        "{time:YYYY-MM-DD HH:mm:ss} - {extra[name]} - {level} - [{thread.name}] {module} - {file.name}:{line} - {function} - {message}\n"
    )

    @staticmethod
    def format(record):
        color = CustomFormatter.COLORS.get(record["level"].name, CustomFormatter.RESET)
        return color + CustomFormatter.FORMAT + CustomFormatter.RESET

# Ensure logger is configured only once
if not getattr(logger, "_custom_configured", False):
    logger.remove()
    logger.add(
        sys.stderr,
        format=CustomFormatter.format,
        colorize=True
    )
    logger._custom_configured = True

def get_custom_logger(name: str):
    """
    Returns a logger with the given name.
    Usage:
        from utils.logs import get_logger
        logger = get_logger("my_module")
        logger.info("message")
    """
    return logger.bind(name=name)