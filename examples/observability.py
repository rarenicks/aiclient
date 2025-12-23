import logging
import time
from aiclient import Client, TracingMiddleware, OpenTelemetryMiddleware

# Configure basic logging to see traces
logging.basicConfig(level=logging.INFO)

client = Client()

def main():
    print("--- Observability Example ---")
    
    # 1. Add Tracing
    # This logs simple "Trace[...]" lines to stdout/logger
    client.add_middleware(TracingMiddleware())
    
    # 2. Add OpenTelemetry (Optional)
    # Requires opentelemetry-sdk installed and configured
    # client.add_middleware(OpenTelemetryMiddleware())

    print("\nSending request (check logs)...")
    try:
        # Mocking or real call
        # resp = client.chat("gpt-4o").generate("Hello")
        # print(resp.text)
        pass # Skip real call to avoid API key need for demo
    except Exception as e:
        print(e)
        
    print("\nCheck your console logs for 'Trace[...] messages")

if __name__ == "__main__":
    main()
