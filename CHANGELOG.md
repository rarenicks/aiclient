# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-01-02 ("The Feature Complete Release")

### 🚀 New Features

- **Configurable `max_tokens`**: Added `max_tokens` parameter to `generate()` and `generate_async()` methods across all providers.
- **Configurable Timeout**: Added `timeout` parameter to Client (default: 60s) for HTTP request timeouts.
- **Google Gemini Embeddings**: Full embedding support for Google's `text-embedding-004` model.
- **Async Context Manager**: Client now supports `async with Client() as client:` pattern for proper resource cleanup.
- **Token Counting**: New `client.count_tokens(text, model)` method using tiktoken for accurate token estimation.
- **Model Listing**: New `client.list_models(provider)` method to discover available models per provider.
- **LoggingMiddleware**: New built-in middleware for request/response logging with automatic API key redaction.
- **Updated Pricing**: Updated `CostTrackingMiddleware` with latest model pricing (Jan 2026) for OpenAI, Anthropic, Google, and xAI.

### ⚡ Improvements

- **Python 3.12 Support**: Added official Python 3.12 support with classifier.
- **Status Upgrade**: Package status upgraded from Alpha to Beta.
- **Anthropic Default `max_tokens`**: Increased default from 1024 to 4096 tokens.
- **Optional MCP Dependency**: MCP is now an optional dependency (`pip install aiclient-llm[mcp]`).
- **Added `tiktoken`**: Core dependency for token counting.
- **Added `pydantic-settings`**: Core dependency for improved settings management.

### 🐛 Bug Fixes

- Fixed version mismatch between `pyproject.toml` and `__init__.py`.
- Fixed duplicate imports in provider files (openai.py, anthropic.py, google.py).
- Fixed README.md parameter names (`api_key_openai` → `openai_api_key`).
- Fixed Protocol/Class collision in `data_types.py` (removed unused Protocol definitions).
- Fixed hardcoded `max_tokens=1024` in Anthropic provider.

### 📚 Documentation

- Updated README with correct parameter names.
- Added new keywords: `grok`, `ollama`, `lmstudio`.

---

## [0.2.2] - 2025-12-26

### 🐛 Bug Fixes

- Minor import fixes and temperature parameter support.
- Embeddings API support for OpenAI.

---

## [0.2.1] - 2025-12-25

### 🐛 Bug Fixes

- Fixed imports and added temperature parameter.
- Added embeddings support.

---

## [0.2.0] - 2025-12-24 ("The Adoption Layer")

### 🚀 New Features

- **Streaming Support**: Real-time token streaming with `model.stream()` and examples.
- **Memory System**: `ConversationMemory` and `SlidingWindowMemory` for managing chat context.
- **Testing Utilities**: `MockProvider` and `MockTransport` for deterministic testing.
- **Async Batch Processing**: `Client.batch()` and `BatchProcessor` for concurrent requests.
- **Multimodal (Vision)**: Unified `Image` type supporting paths, URLs, and Base64.
- **Model Context Protocol (MCP)**: Support for connecting to external tools via MCP.
- **Semantic Caching**: Embedding-based response caching `SemanticCacheMiddleware`.
- **Resilience**: `RetryMiddleware` (backoff/jitter), `CircuitBreaker`, `RateLimiter`, and `FallbackChain`.
- **Structured Outputs**: Native support for strict JSON Schemas (OpenAI).
- **Observability**: `TracingMiddleware` and `OpenTelemetryMiddleware` hooks.
- **Debug Mode**: Verbose logging enabled via `Client(debug=True)`.
- **Enhanced Error Handling**: Typed exceptions (`AuthenticationError`, `RateLimitError`, `NetworkError`, etc.).

### ⚡ Improvements

- **Type Safety**: Comprehensive type hints across `Client`, `BatchProcessor`, and `Agent`.
- **Performance**: Cached tool lookups in `MCPServerManager`.
- **Usage Tracking**: Enhanced metrics for cache hits and costs.
- **Midleware Hooks**: Added `on_error` support to middleware protocol.

### 📚 Documentation & Examples

- **Production Cookbook**: 5+ real-world examples (Memory, RAG, Agents, Batching).
- **New Guides**: Testing, Memory, Error Handling, and Streaming documentation.
- **Updated README**: Verified badges and comprehensive feature list.

### 🐛 Bug Fixes

- Fixed `httpx` streaming error handling (properly raises `AuthenticationError`).
- Fixed `Memory.load()` serialization.
- Renamed `ConnectionError` to `NetworkError`.
- Fixed `MCPServerManager` initialization.

---
