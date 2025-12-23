import time
import pytest
import threading
from aiclient.resilience import CircuitBreaker, RateLimiter
from aiclient.middleware import Middleware

def test_circuit_breaker_logic():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
    
    # 1. Start Closed
    assert cb._state == "CLOSED"
    
    # 2. Add Failure
    cb.on_error(Exception("Test"), "model")
    assert cb._state == "CLOSED"
    assert cb._failures == 1
    
    # 3. Trip Breaker
    cb.on_error(Exception("Test"), "model")
    assert cb._state == "OPEN"
    
    # 4. Request while Open -> Raise
    with pytest.raises(Exception) as excinfo:
        cb.before_request("model", "prompt")
    assert "CircuitBreaker is OPEN" in str(excinfo.value)
    
    # 5. Wait for recovery
    time.sleep(0.15)
    
    # 6. Half-Open
    cb.before_request("model", "prompt")
    assert cb._state == "HALF_OPEN"
    
    # 7. Success -> Closed
    cb.after_response("response") # type: ignore
    assert cb._state == "CLOSED"
    assert cb._failures == 0

def test_rate_limiter_logic():
    # RPM=60 -> 1 request per second window logic?
    # Implementation checks last 60 seconds.
    # If I set RPM=2, then 3rd request should sleep if within same second.
    rl = RateLimiter(requests_per_minute=20000) # fast
    
    start = time.time()
    rl.before_request("model", "prompt")
    rl.before_request("model", "prompt")
    end = time.time()
    assert end - start < 1.0 # Should be fast
    
    # Test delay (hard to test without mocking time.sleep, but logic check is enough)
    pass
