# Architecture Specification

## 1. System Overview

The **Gemini Local LLM Bridge** is a production-grade Model Context Protocol (MCP) server that enables **Google Gemini** (Gemini Web, Personalization, Custom Apps) to consult private, on-premise, or local LLMs (Ollama, LM Studio, vLLM, OpenAI-compatible APIs) on demand.

```mermaid
flowchart TD
    subgraph Client["Google Gemini Ecosystem"]
        G[Gemini Web / Chrome]
    end

    subgraph Ingress["Public / Private Ingress"]
        CT[Cloudflare Tunnel / Reverse Proxy HTTPS]
    end

    subgraph MCP_Layer["MCP Protocol Layer"]
        AUTH[MCPAuthMiddleware]
        SERVER[FastMCP Server]
        TOOL[ask_local_llm Tool Adapter]
    end

    subgraph App_Core["Application Core (Domain & Service)"]
        SVC[LLMService]
        REQ[LLMRequest / LLMResponse]
    end

    subgraph Provider_Layer["Provider Abstraction Layer"]
        FACTORY[ProviderFactory]
        BASE[LLMProvider Interface]
        OPENAI[OpenAICompatibleProvider]
        FAKE[FakeLLMProvider]
    end

    subgraph Backends["LLM Backends (Isolated)"]
        OLLAMA[Ollama]
        LMSTUDIO[LM Studio]
        VLLM[vLLM / LocalAI]
    end

    G -->|JSON-RPC 2.0 over Streamable HTTP| CT
    CT --> AUTH
    AUTH --> SERVER
    SERVER --> TOOL
    TOOL --> SVC
    SVC --> REQ
    SVC --> BASE
    FACTORY --> BASE
    BASE <|-- OPENAI
    BASE <|-- FAKE
    OPENAI -->|HTTP POST /chat/completions| OLLAMA
    OPENAI -->|HTTP POST /chat/completions| LMSTUDIO
    OPENAI -->|HTTP POST /chat/completions| VLLM
```

---

## 2. Layer Responsibilities & Strict Dependency Flow

Dependency rule: **Outer layers depend on inner layers; inner layers NEVER depend on outer layers.**

```
MCP Transport & Middleware (Outer)
         ↓
MCP Tools Adapter
         ↓
Application Service Layer
         ↓
LLMProvider Abstract Interface
         ↓
Provider Implementation (OpenAICompatible, Fake)
         ↓
Infrastructure (HttpClientFactory, Logging)
```

### 1. Domain Layer (`src/app/domain/`)
- Pure Python dataclasses (`LLMRequest`, `LLMResponse`).
- Domain-specific exception hierarchy (`BridgeError`, `ProviderConnectionError`, `ProviderTimeoutError`, `ProviderAuthenticationError`, `ProviderRateLimitError`).
- Zero external framework dependencies.

### 2. Provider Layer (`src/app/providers/`)
- Defines the abstract contract `LLMProvider` (`generate(request) -> LLMResponse`, `check_health() -> bool`).
- Implements `OpenAICompatibleProvider` with exponential backoff retries and connection pooling.
- Implements `FakeLLMProvider` for deterministic unit testing and CI simulation without active model servers.
- `ProviderFactory` builds the appropriate provider based on centralized `Settings`.

### 3. Application Service Layer (`src/app/application/services/`)
- `LLMService` orchestrates execution, validation, latency measurement, and maps domain exceptions into resilient, informative messages for Gemini without crashing the server.

### 4. MCP Layer (`src/app/mcp/`)
- `server.py`: Constructs FastMCP instance with Stateless HTTP support.
- `auth.py`: Starlette middleware enforcing Bearer token verification on protected endpoints.
- `tools/ask_llm.py`: Thin adapter exposing `ask_local_llm` to the MCP tool manifest.

### 5. Configuration & Infrastructure (`src/app/config/`, `src/app/infrastructure/`)
- `settings.py`: Single centralized Pydantic `Settings` class loading and validating environment variables.
- `logging.py`: Structured logger with automated secret/token redaction filter.
- `http_client.py`: Shared connection pooling factory with connection bounds.
