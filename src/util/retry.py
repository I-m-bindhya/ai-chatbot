import asyncio


async def retry_async(
    operation,
    retries=3,
    base_delay=1,
    should_retry=None
):
    for attempt in range(retries):

        try:
            return await operation()

        except Exception as ex:

            if (
                should_retry
                and not should_retry(ex)
            ):
                raise

            if attempt == retries - 1:
                raise

            delay = base_delay * (2 ** attempt)

            await asyncio.sleep(delay)


def is_retryable(error):
    return isinstance(
        error,
        (
            TimeoutError,
            ConnectionError,
        )
    )