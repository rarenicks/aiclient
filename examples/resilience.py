import time
from aiclient import Client, CircuitBreaker, RateLimiter

client = Client()

def main():
    print("--- Resilience Example ---")
    
    # 1. Setup Middleware
    # CircuitBreaker: Opens after 3 failures, waits 10s
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
    # RateLimiter: 60 requests/min = 1 req/sec
    rl = RateLimiter(requests_per_minute=60)
    
    client.add_middleware(cb)
    client.add_middleware(rl)
    
    print("Middleware configured.")
    
    # 2. Simulate Requests (Mock)
    # In real usage, these would hit API.
    # RateLimiter will automatically sleep if we go too fast.
    
    start = time.time()
    for i in range(5):
        print(f"Request {i+1}...")
        # Simulating call (won't actually work without keys/mock)
        # client.chat("gpt-4o").generate("hi")
        pass
    
    print("Done. RateLimiter ensured pacing if calls were made.")

if __name__ == "__main__":
    main()
