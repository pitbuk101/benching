import logging
import os
from omegaconf import DictConfig

def setup_logging(config: DictConfig) -> logging.Logger:
    """
    Sets up logging for the application based on the provided configuration.
    """
    log_config = config.logging
    log_level_str = log_config.get("level", "INFO").upper() # Default to INFO if not set
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    date_format = log_config.get("date_format", "%Y-%m-%d %H:%M:%S")
    
    # Create a logger instance. Using client_name makes logs distinguishable.
    logger_name = config.get("client_name", "ProcurementSuiteApp")
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level) # Set level on the logger itself

    # Clear existing handlers to avoid duplicate logs if called multiple times (e.g. in tests)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level) # Set level on handler too
    formatter = logging.Formatter(log_format, datefmt=date_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler (optional)
    if log_config.get("log_file_enabled", True): # Default to True if not set
        log_dir = config.paths.get("log_dir", "./logs/") # Default if not set
        os.makedirs(log_dir, exist_ok=True)
        
        # Sanitize client name for filename to avoid issues with special characters
        client_name_for_log = "".join(c if c.isalnum() else "_" for c in config.get("client_name", "app"))
        log_filename = os.path.join(log_dir, f"{client_name_for_log}_workflow.log")
        
        fh = logging.FileHandler(log_filename, mode='a') # Append mode
        fh.setLevel(log_level) # Set level on handler
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info(f"Logging to file: {log_filename}")

    # Prevent log propagation to root logger if it has handlers that might duplicate
    logger.propagate = False 

    logger.info(f"Logging setup complete for {logger_name}. Level: {log_level_str}")
    return logger