import time
import threading
from typing import Dict, Union, List, Optional
from .types import ModelResponse, BaseMessage
from .middleware import Middleware

class CircuitBreaker(Middleware):
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        self._failures = 0
        self._state = "CLOSED" # CLOSED, OPEN, HALF_OPEN
        self._last_failure_time = 0.0
        self._lock = threading.Lock()

    def before_request(self, model: str, prompt: Union[str, List[BaseMessage]]) -> Union[str, List[BaseMessage]]:
        with self._lock:
            current_time = time.time()
            
            if self._state == "OPEN":
                if current_time - self._last_failure_time > self.recovery_timeout:
                    self._state = "HALF_OPEN"
                    # Allow this request to proceed as probe
                else:
                    raise Exception(f"CircuitBreaker is OPEN for {model}. Too many failures.")
        
        return prompt

    def after_response(self, response: ModelResponse) -> ModelResponse:
        # If we successfully got a response, reset
        with self._lock:
            if self._state == "HALF_OPEN":
                self._state = "CLOSED"
                self._failures = 0
            elif self._state == "CLOSED":
                self._failures = 0 
        return response

    def on_error(self, error: Exception, model: str) -> None:
        with self._lock:
            self._failures += 1
            self._last_failure_time = time.time()
            if self._failures >= self.failure_threshold:
                self._state = "OPEN"

class RateLimiter(Middleware):
    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
        self.window = 60.0
        self._timestamps = []
        self._lock = threading.Lock()
        
    def before_request(self, model: str, prompt: Union[str, List[BaseMessage]]) -> Union[str, List[BaseMessage]]:
        with self._lock:
            now = time.time()
            # Remove old timestamps
            self._timestamps = [t for t in self._timestamps if now - t < self.window]
            
            if len(self._timestamps) >= self.rpm:
                 wait_time = self.window - (now - self._timestamps[0])
                 # Blocking sleep or raise? Usually sleep for rate limiter, or raise.
                 # Let's sleep to "shape" traffic.
                 if wait_time > 0:
                     time.sleep(wait_time)
                     # Re-check time? or just proceed.
                     # If we sleep, we are now at 'now + wait_time'.
                     self._timestamps.append(time.time()) # Approx
            else:
                self._timestamps.append(now)
                
        return prompt

    def after_response(self, response: ModelResponse) -> ModelResponse:
        return response

    def on_error(self, error: Exception, model: str) -> None:
        pass
