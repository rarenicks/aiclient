# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2025-12-23

### 🚀 New Features

- **Prompt Caching (Anthropic)**: Added `cache_control` to `BaseMessage` to support Anthropic's prompt caching. Added cache metrics to `Usage`.
- **Structured Outputs (Native)**: Added `strict=True` to `ChatModel.generate()` to use OpenAI's native JSON Schema enforcement.
- **Resilience Middleware**: Added `CircuitBreaker` and `RateLimiter` middleware.
- **Observability Middleware**: Added `TracingMiddleware` and `OpenTelemetryMiddleware`.

### ⚡ Improvements

- Added `on_error` hook to `Middleware` protocol for better error handling.
- Enhanced `Usage` model with cache-specific token counts.

### 🐛 Bug Fixes

- Fixed async error handling in `ChatModel` to correctly notify middleware on exceptions.

### 📚 Documentation

- Added comprehensive guides for Prompt Caching, Structured Outputs, Resilience, and Observability.
- Added `examples/` directory with runnable scripts.
