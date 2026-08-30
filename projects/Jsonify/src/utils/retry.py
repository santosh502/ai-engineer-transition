from src.config import config
from src.utils.exceptions import RetryableError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


def retry_extraction(func):
    return retry(
        stop=stop_after_attempt(config.max_retries),
        wait=wait_exponential(
            multiplier=1, min=config.retry_min_wait, max=config.retry_max_wait
        ),
        retry=retry_if_exception_type(RetryableError),
        reraise=True,
    )(func)
