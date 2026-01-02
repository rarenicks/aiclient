import asyncio
import random
import time
from typing import Any, List, Union

import httpx

from ..data_types import BaseMessage, ModelResponse


class RetryMiddleware:
    """
    Middleware that retries requests on transient failures (429, 5xx).
    Implements exponential backoff with jitter.
    """

    def __init__(
        self, max_retries: int = 3, backoff_factor: float = 1.0, max_delay: float = 60.0
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay

    def before_request(
        self, model: str, prompt: Union[str, List[BaseMessage]]
    ) -> Union[str, List[BaseMessage]]:
        # No Modification
        return prompt

    def after_response(self, response: ModelResponse) -> ModelResponse:
        return response

    def on_error(self, error: Exception, model: str, **kwargs: Any) -> None:
        """
        Calculates backoff and sleeps if retryable.
        If not retryable, raises error to abort the model's loop.
        """
        attempt = kwargs.get("attempt", 0)

        if not self.should_retry(error):
            # Not a retryable error (e.g. 400 Bad Request)
            # Raise it to break the ChatModel loop (which catches Exception)
            # Note: This raised exception will be caught by ChatModel's except block?
            # Wait, ChatModel: try...except Exception as e...
            # If mw.on_error raises E2, it bubbles out of the except block (chained).
            # So yes, raising here aborts the loop.
            raise error

        # If we are here, it IS retryable.
        # Check if we exceeded our own max_retries?
        # Only if we want to valid independent of ChatModel.
        if attempt >= self.max_retries:
            raise error

        # Sleep
        delay = self.calculate_delay(attempt)
        time.sleep(delay)

    async def on_error_async(self, error: Exception, model: str, **kwargs: Any) -> None:
        """Async version of on_error."""
        attempt = kwargs.get("attempt", 0)

        if not self.should_retry(error):
            raise error

        if attempt >= self.max_retries:
            raise error

        # Async Sleep
        delay = self.calculate_delay(attempt)
        await asyncio.sleep(delay)

    def should_retry(self, exception: Exception) -> bool:
        """Helper to determine if an exception is retryable."""
        if isinstance(exception, httpx.HTTPStatusError):
            code = exception.response.status_code
            return code == 429 or 500 <= code < 600
        return False

    def calculate_delay(self, attempt: int) -> float:
        delay = self.backoff_factor * (2**attempt)
        jitter = random.uniform(0, 0.1 * delay)
        return min(delay + jitter, self.max_delay)
