# Gemini Local LLM Bridge

[![Tests](https://img.shields.io/badge/tests-20%20passed-success)](tests/)
[![Architecture](https://img.shields.io/badge/architecture-Clean%20%26%20Modular-blue)](docs/architecture.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Docker Ready](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)](Dockerfile)

A production-ready **Model Context Protocol (MCP)** server enabling **Google Gemini** (Gemini Web, Personalization, and Custom Apps) to securely consult private, on-premise, or local LLMs (Ollama, LM Studio, vLLM, OpenAI-compatible APIs) on demand.

---

## 🚀 Key Features

- **Clean Architecture**: Strict separation of concerns (Domain $\rightarrow$ Providers $\rightarrow$ Application Service $\rightarrow$ MCP Layer).
- **Universal Provider Support**: Connects to any OpenAI-compatible API (Ollama, LM Studio, vLLM, LocalAI) and includes a deterministic `FakeLLMProvider` for testing.
- **Production-Ready Docker**: Multi-stage build, minimal footprint, non-root user execution (`appuser:10001`), native container healthchecks.
- **Resilient Error Handling**: Connection pooling, configurable timeouts, retries with backoff, and graceful fallback messages for Gemini.
- **Enterprise Security**: Bearer Token authentication on MCP endpoints, log secret sanitization, and network isolation.

---

## 🛠️ User Journey & Architecture

```
User in Gemini
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ Google Gemini Web / Custom Apps                             │
│ Tag: @Gemini Local LLM Bridge                               │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON-RPC 2.0 (Streamable HTTP / SSE)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Ingress (Cloudflare Tunnel / HTTPS Reverse Proxy)           │
│ https://<public-domain>/mcp                                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ MCP Server (FastMCP + Starlette + Auth Middleware)          │
│ Tool: ask_local_llm(question, context)                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Application Core (LLMService)                               │
│ Request validation, timing, resilience                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Local LLM Backend (Isolated on Localhost / Private Network) │
│ Ollama / LM Studio / vLLM (POST /v1/chat/completions)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Compatibility Matrix

| Environment | Status | Verification Notes |
|---|---|---|
| **Windows 10 / 11 (Native)** | **Supported** | Tested with Python 3.12 & native PowerShell |
| **Linux (Ubuntu / Debian)** | **Supported** | Tested with Docker Debian slim |
| **Docker & Docker Compose** | **Supported** | Multi-stage, non-root `appuser`, healthy status |
| **Gemini Web (`gemini.google.com`)** | **Verified** | Full tool execution via `@` mention |
| **Gemini in Chrome (Side Panel)** | **Verified** | Supported via `@` mention |
| **Gemini Live (Audio/Screen Stream)** | **Limited** | Audio-priority; requires explicit prompt triggering |

---

## ⚡ Quick Start (Docker - Recommended)

### 1. Configure Environment
```bash
cp .env.example .env
```
*(If your Local LLM runs directly on your host machine, set `LLM_BASE_URL=http://host.docker.internal:11434/v1` in `.env`)*

### 2. Start Services
```bash
docker compose up -d
```

### 3. Retrieve Public Tunnel URL
```bash
docker logs cloudflared-mcp
```
Look for: `Your quick Tunnel has been created! Visit it at: https://<subdomain>.trycloudflare.com`

### 4. Run Diagnostics
```bash
python scripts/verify_mcp.py https://<subdomain>.trycloudflare.com
```

---

## 💻 Native Local Run (Without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure `.env`:**
   ```ini
   MCP_HOST=0.0.0.0
   MCP_PORT=8000
   LLM_BASE_URL=http://127.0.0.1:11434/v1
   LLM_MODEL=llama3.2
   ```
3. **Start the server:**
   ```bash
   python -m src.app.main
   ```
4. **Health check:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## 🔗 Connecting to Google Gemini

See the **[Visual Setup Guide (Step-by-Step with Screenshots)](docs/gemini-setup-guide.md)** or follow these steps:

1. Open [Google Gemini](https://gemini.google.com).
2. Go to **Settings $\rightarrow$ Personalization $\rightarrow$ Custom Apps** (or **Connected Apps**).
3. Click **Add Custom App / MCP Server**.
4. Enter the public endpoint:
   ```
   https://<your-public-url>/mcp
   ```
5. *(Optional)* If you set `AUTH_TOKEN` in `.env`, provide the Bearer token under Authentication.
6. In any chat, type:
   > `@Gemini Local LLM Bridge What is the difference between a process and a thread?`
7. Click **Allow** on Gemini's permission card.

---

## 🧪 Testing in Gemini

### ✅ Invocation Syntax (Mandatory `@` Mention)

You must address the custom app using `@` at the beginning of your prompt:

> **`@Gemini Local LLM Bridge Consult the local LLM on how to optimize heavy database query performance.`**

Or for coding tasks:

> **`@Gemini Local LLM Bridge Review this Python function and suggest performance optimizations.`**

---

## 🧪 Automated Tests

Run the full automated test suite (Unit, Integration, and E2E):
```bash
pytest tests/ -v
```

---

## 📖 Documentation Index

- **[Documentation Overview](docs/README.md)**
- **[Visual Setup Guide (Screenshots & Walkthrough)](docs/gemini-setup-guide.md)**
- **[Architecture Specification & Diagrams](docs/architecture.md)**
- **[Getting Started Guide](docs/getting-started.md)**
- **[Configuration Reference](docs/configuration.md)**
- **[Production Deployment (VPS, Reverse Proxy, Named Tunnels)](docs/deployment.md)**
- **[Troubleshooting & FAQ](docs/troubleshooting.md)**
- **[Contributing Guide](CONTRIBUTING.md)**
- **[Security Policy](SECURITY.md)**
- **[Code of Conduct](CODE_OF_CONDUCT.md)**
- **[Changelog](CHANGELOG.md)**
- **[Support](SUPPORT.md)**

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
