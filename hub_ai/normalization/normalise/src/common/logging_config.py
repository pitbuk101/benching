import logging
import normalise.env as env

def setup_logging() -> logging.Logger:
    """
    Sets up logging for the application based on the provided configuration.
    """
    log_level_str = env.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_format = env.LOG_FORMAT
    date_format = env.LOG_DATE_FORMAT
    logger_name = env.CLIENT_NAME
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if logger.hasHandlers():
        logger.handlers.clear()
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter(log_format, datefmt=date_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False
    logger.info(f"Logging setup complete for {logger_name}. Level: {log_level_str}")
    return logger