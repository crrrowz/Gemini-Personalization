# Troubleshooting & FAQ

## 1. Common Issues & Solutions

### Q: "Gemini says 'I cannot help with that' or doesn't recognize the tool"
- **Cause**: Gemini requires tagging the custom app by name with `@` (e.g., `@Gemini Local LLM Bridge`).
- **Fix**: Open a new chat on [https://gemini.google.com](https://gemini.google.com), type `@` to select the app chip, then type your prompt.

### Q: "Connection refused to Ollama / Local LLM from Docker"
- **Cause**: Inside a Docker container, `localhost` refers to the container itself, NOT the host machine.
- **Fix**: In your `.env`, set:
  ```ini
  LLM_BASE_URL=http://host.docker.internal:11434/v1
  ```
  And ensure Ollama is listening on all interfaces (`OLLAMA_HOST=0.0.0.0:11434`).

### Q: "Cloudflare Tunnel shows status: Down in Dashboard"
- **Cause**: You are running a zero-config Quick Tunnel (`trycloudflare.com`) instead of a Named Tunnel with a token.
- **Fix**: This is normal for Quick Tunnels. Use the public URL printed in `docker logs cloudflared-mcp`.

### Q: "Local LLM request timed out"
- **Cause**: The local model is loading into GPU/VRAM or the prompt is too large.
- **Fix**: Increase `LLM_TIMEOUT` in `.env` (e.g., `LLM_TIMEOUT=120`).

---

## 2. Gemini Platform Capability Matrix

| Feature | Gemini Web (`gemini.google.com`) | Gemini in Chrome (Side Panel) | Gemini Live (Audio/Screen Stream) |
|---|---|---|---|
| **Custom MCP Apps via `@`** | **Fully Supported** | **Supported via `@`** | **Limited / Audio-Priority** |
| **Tool Calling (`ask_local_llm`)** | **Verified** | **Verified** | **Requires Explicit Trigger** |
