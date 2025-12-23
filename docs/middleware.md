# Middleware & Observability

Middleware allows you to inject custom logic before a request is sent to the LLM and after a response is received. This is useful for logging, cost tracking, prompt engineering, or PII masking.

## How it Works

A middleware is any class that implements the `Middleware` protocol:

```python
class Middleware(Protocol):
    def before_request(self, model: str, prompt: Union[str, List[BaseMessage]]) -> Union[str, List[BaseMessage]]:
        ...
    def after_response(self, response: ModelResponse) -> ModelResponse:
        ...
```

## Built-in Middleware

### CostTrackingMiddleware

Tracks estimated token usage and USD cost across all requests in a session.

```python
from aiclient import Client
from aiclient.middleware import CostTrackingMiddleware

# 1. Create tracker
tracker = CostTrackingMiddleware()

# 2. Attach to client
client = Client()
client.add_middleware(tracker)

# 3. Use client
client.chat("gpt-4o").generate("Hello")

# 4. Check stats
print(f"Total Cost: ${tracker.total_cost_usd:.4f}")
print(f"Tokens: {tracker.total_input_tokens} In / {tracker.total_output_tokens} Out")
```

## Creating Custom Middleware

### Example: Logging Middleware

```python
class LoggingMiddleware:
    def before_request(self, model, prompt):
        print(f"[LOG] Sending request to {model}")
        return prompt # Must return prompt
        
    def after_response(self, response):
        print(f"[LOG] Received {response.usage.total_tokens} tokens")
        return response # Must return response

client.add_middleware(LoggingMiddleware())
```

### Example: PII Redaction

```python
class PIIFilterMiddleware:
    def before_request(self, model, prompt):
        if isinstance(prompt, str):
            return prompt.replace("EMAIL_ADDRESS", "[REDACTED]")
        return prompt
        
    def after_response(self, response):
        return response
```
```

## Resilience Middleware 🛡️

Protect your application from downstream failures.

### CircuitBreaker
Stops sending requests to a failing provider for a set time prevent cascading failures.

```python
from aiclient import CircuitBreaker

client.add_middleware(CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60.0  # seconds
))
```

### RateLimiter
Limits the number of requests per minute (RPM).

```python
from aiclient import RateLimiter

# Limit to 60 requests per minute
client.add_middleware(RateLimiter(requests_per_minute=60))
```

## Observability Middleware 🔭

### TracingMiddleware
Logs request lifecycles (start, end, error) with a trace ID.

```python
from aiclient import TracingMiddleware
import logging

logging.basicConfig(level=logging.INFO)
client.add_middleware(TracingMiddleware())
```

### OpenTelemetryMiddleware
Integrates with OpenTelemetry for distributed tracing (Datadog, Honeycomb, Jaeger).

```python
from aiclient import OpenTelemetryMiddleware

client.add_middleware(OpenTelemetryMiddleware(service_name="my-ai-service"))
```
