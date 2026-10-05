# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-05

### Added
- **Production Clean Architecture**: Modular codebase separating Domain, Providers, Application Services, MCP Layer, and Infrastructure.
- **MCP Streamable HTTP Server**: Full JSON-RPC 2.0 implementation over FastMCP and Starlette supporting stateless and stateful HTTP transports.
- **Universal Provider Abstraction**:
  - `OpenAICompatibleProvider` with connection pooling, exponential backoff retries, and timeout management.
  - `FakeLLMProvider` for deterministic, zero-dependency unit and CI testing.
  - `ProviderFactory` for dynamic provider resolution via configuration.
- **Thin-Layer Tool Registration**: `ask_local_llm` adapter receiving `question` and optional `context`.
- **Diagnostics & Probes**: `/health` (liveness), `/ready` (dependency readiness), and root discovery routes.
- **Security Middleware**: `MCPAuthMiddleware` supporting optional Bearer Token verification on protected MCP routes.
- **Secret Sanitization**: Automated log filtering preventing API keys and tokens from appearing in stdout.
- **Production Containerization**: Multi-stage Dockerfile running as non-root `appuser:10001` with built-in healthchecks.
- **Comprehensive Documentation**: Complete guides covering Architecture, Getting Started, Configuration, Visual Gemini Setup, Deployment, and Troubleshooting.
- **Test Suite**: Automated Unit, Integration, and E2E test coverage across all domain and protocol layers.
