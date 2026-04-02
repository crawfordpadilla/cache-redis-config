import redis
import logging

logger = logging.getLogger(__name__)

def get_redis_client(redis_url):
    """
    Creates a Redis client instance from the provided connection URL.

    Args:
        redis_url (str): The Redis connection URL.

    Returns:
        redis.Redis: The Redis client instance.
    """
    try:
        redis_client = redis.Redis.from_url(redis_url)
        return redis_client
    except redis.errors.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise


def get_configured_redis_client(redis_url, retry_count=3, timeout=5):
    """
    Creates a Redis client instance from the provided connection URL with retry mechanism.

    Args:
        redis_url (str): The Redis connection URL.
        retry_count (int, optional): The number of times to retry connecting to Redis. Defaults to 3.
        timeout (int, optional): The timeout in seconds for each retry attempt. Defaults to 5.

    Returns:
        redis.Redis: The Redis client instance.
    """
    for _ in range(retry_count):
        try:
            redis_client = get_redis_client(redis_url)
            return redis_client
        except redis.errors.ConnectionError:
            if _ < retry_count - 1:
                logger.warning(f"Failed to connect to Redis, retrying in {timeout} seconds...")
                import time
                time.sleep(timeout)
            else:
                logger.error("Failed to connect to Redis after retrying")
                raise