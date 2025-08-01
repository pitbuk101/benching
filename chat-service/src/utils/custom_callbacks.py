import time
from src.utils.logs import get_custom_logger
logger = get_custom_logger(__name__)

def timed_node_sync(name):
    def decorator(fn):
        def wrapper(state):
            start = time.time()
            logger.info(f"[{name}] START")
            result = fn(state)
            duration = time.time() - start
            logger.info(f"[{name}] END - Duration: {duration:.4f}s")
            return result
        return wrapper
    return decorator
