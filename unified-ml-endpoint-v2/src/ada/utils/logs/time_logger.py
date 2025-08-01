"""A module for logging the execution time of functions."""
import logging
import os
import time

# Configure logger
time_logger = logging.getLogger("time_logger")
time_logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add file handler to logger
time_logger.addHandler(file_handler)


# Decorator function to log time taken by a function
def log_time(func):
    """A decorator for tracing the execution time of functions.

    This decorator wraps a function and logs the elapsed time it takes to execute
    the wrapped function. The logged information includes the function name, file name,
    and elapsed time in milliseconds.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    def time_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        file_name = os.path.basename(func.__code__.co_filename)
        time_logger.info("%s in %s took %.2f s", func.__qualname__, file_name, elapsed_time)
        return result

    return time_wrapper
