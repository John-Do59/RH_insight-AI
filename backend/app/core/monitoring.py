import time
import logging
from functools import wraps
from typing import Any, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("RHInsight-Profiling")

def profile_async(name: str):
    """
    Decorator to measure execution time of an async function.
    """
    def decorator(func: Callable):
        import inspect
        
        if inspect.isasyncgenfunction(func):
            @wraps(func)
            async def async_gen_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    async for item in func(*args, **kwargs):
                        yield item
                finally:
                    end_time = time.perf_counter()
                    elapsed = end_time - start_time
                    logger.info(f"PROFILING | {name} | Duration: {elapsed:.4f}s")
            return async_gen_wrapper
        else:
            @wraps(func)
            async def async_func_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.perf_counter()
                    elapsed = end_time - start_time
                    logger.info(f"PROFILING | {name} | Duration: {elapsed:.4f}s")
            return async_func_wrapper
    return decorator

class MetricsCollector:
    def __init__(self):
        self.metrics = {}

    def record(self, name: str, duration: float):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(duration)
        logger.info(f"METRIC | {name} | {duration:.4f}s")

metrics = MetricsCollector()
