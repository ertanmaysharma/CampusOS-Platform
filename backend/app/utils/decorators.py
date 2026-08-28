import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def timing_decorator(fn):
    """Log execution time of a function."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        duration = (time.time() - start) * 1000
        logger.info(f"{fn.__name__} executed in {duration:.2f}ms")
        return result
    return wrapper
