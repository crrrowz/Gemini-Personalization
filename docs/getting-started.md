# Getting Started

## 1. Quick Local Setup

### Prerequisites
- Python 3.10+
- An OpenAI-compatible Local LLM server running (e.g., Ollama, LM Studio, vLLM) or use `LLM_PROVIDER=fake` for testing.

### Steps
1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the environment configuration:
   ```bash
   cp .env.example .env
   ```

3. Start the MCP server:
   ```bash
   python -m src.app.main
   ```

4. Verify health locally:
   ```bash
   curl http://localhost:8000/health
   ```
   Or run the diagnostic script:
   ```bash
   python scripts/verify_mcp.py http://localhost:8000
   ```

---

## 2. Quick Docker Setup

1. Start with Docker Compose:
   ```bash
   docker compose up -d
   ```

2. Read the auto-generated Cloudflare tunnel URL:
   ```bash
   docker logs cloudflared-mcp
   ```

3. Verify with the diagnostic script:
   ```bash
   python scripts/verify_mcp.py https://<your-generated-tunnel-domain>.trycloudflare.com
   ```
