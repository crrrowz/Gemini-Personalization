# Configuration Reference

This document provides a comprehensive reference for all configurable options in **Gemini Local LLM Bridge**.

All options can be set via environment variables or specified in a `.env` file at the root of the project.

---

## Configuration Variables

| Variable | Description | Type | Default | Allowed Values | Security / Usage Note |
|---|---|---|---|---|---|
| `MCP_HOST` | Host IP address to bind the MCP server. | `string` | `0.0.0.0` | Any valid IP (`0.0.0.0`, `127.0.0.1`) | `0.0.0.0` binds to all network interfaces. |
| `MCP_PORT` | Port number for the MCP server. | `integer` | `8000` | `1024-65535` | Used by Docker and local uvicorn runner. |
| `MCP_PATH` | Path prefix for MCP JSON-RPC endpoint. | `string` | `/mcp` | Any valid URL path | Must match the URL configured in Gemini Custom App. |
| `MCP_SERVER_NAME` | Display name advertised in MCP server info. | `string` | `Gemini-Local-LLM-Bridge` | Alphanumeric string | Shown in MCP tool manifests. |
| `AUTH_TOKEN` | Bearer token required for Gemini requests. | `string` | `""` (Disabled) | Secret string | If set, requests must include `Authorization: Bearer <AUTH_TOKEN>`. |
| `LLM_PROVIDER` | Active LLM backend provider implementation. | `string` | `openai_compatible` | `openai_compatible`, `fake` | Use `fake` for testing without an active model server. |
| `LLM_BASE_URL` | Base URL of the OpenAI-compatible LLM endpoint. | `string` | `http://127.0.0.1:11434/v1` | Valid HTTP/HTTPS URL | Set to `http://host.docker.internal:11434/v1` if running in Docker. |
| `LLM_API_KEY` | API Key for authenticating with LLM backend. | `string` | `""` | Secret string | Optional for local Ollama/LM Studio; required for remote APIs. |
| `LLM_MODEL` | Model identifier to pass in completion requests. | `string` | `llama3.2` | Any model name (e.g. `llama3.2`, `mistral`) | Must be installed/pulled on the LLM backend. |
| `LLM_TIMEOUT` | Maximum wall-clock time (in seconds) per request. | `float` | `60.0` | `1.0 - 600.0` | Increase for large models or complex reasoning prompts. |
| `LLM_MAX_RETRIES` | Number of retry attempts on network/server errors. | `integer` | `2` | `0 - 5` | Uses exponential backoff (e.g., 2s, 4s). |
| `LLM_SYSTEM_PROMPT` | Default system prompt sent to the LLM backend. | `string` | Default assistant prompt | Text prompt | Guides the tone and behavior of the local model. |
| `LOG_LEVEL` | Verbosity of application and diagnostic logs. | `string` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | Structured logs sanitize secrets automatically. |

---

## Example Configurations

### 1. Local Ollama on Host (with Dockerized MCP)
```ini
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_PATH=/mcp
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.2
LLM_TIMEOUT=60
LOG_LEVEL=INFO
```

### 2. Local LM Studio
```ini
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://host.docker.internal:1234/v1
LLM_MODEL=local-model
LLM_TIMEOUT=90
```

### 3. Authenticated Remote API
```ini
AUTH_TOKEN=super-secret-mcp-key
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
```

### 4. CI / Deterministic Test Mode
```ini
LLM_PROVIDER=fake
LLM_MODEL=fake-model-v1
LOG_LEVEL=DEBUG
```
