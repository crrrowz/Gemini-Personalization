# Contributing to Gemini Local LLM Bridge

Thank you for your interest in contributing to **Gemini Local LLM Bridge**! We welcome bug fixes, documentation improvements, and architectural enhancements that adhere to our design principles.

---

## 🧭 Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please maintain a professional, respectful, and constructive environment.

---

## 🏗️ Architecture & Philosophy

Before making changes, please read [docs/architecture.md](docs/architecture.md).

Our core architectural mandates:
1. **Strict Dependency Flow**:
   `MCP Transport` $\rightarrow$ `MCP Tool Adapters` $\rightarrow$ `Application Services` $\rightarrow$ `LLMProvider Interface` $\rightarrow$ `Provider Implementation` $\rightarrow$ `Infrastructure`.
2. **Zero Overengineering**: No microservices, messaging queues, or unnecessary frameworks.
3. **Resilience**: The MCP server must never crash due to external LLM downtime or timeouts; errors must map to clean domain responses.
4. **Deterministic Testing**: All new features must include unit tests utilizing `FakeLLMProvider` or mock transports without requiring live external API keys.

---

## 🛠️ Local Development Setup

### 1. Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git
- Docker (optional, for container validation)

### 2. Fork & Clone
```bash
git clone https://github.com/<your-username>/Gemini-Personalization.git
cd Gemini-Personalization
```

### 3. Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Linux / macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```
For local unit testing without an active model server, you can set in `.env`:
```ini
LLM_PROVIDER=fake
```

---

## 🧪 Testing Guidelines

We enforce automated test coverage across unit, integration, and E2E layers.

### Running Tests
```bash
pytest tests/ -v
```

### Test Directory Structure
- `tests/unit/`: Tests for settings, domain dataclasses, exception hierarchies, `FakeLLMProvider`, `OpenAICompatibleProvider`, and `LLMService`.
- `tests/integration/`: Tests for `/health`, `/ready`, root endpoints, and `MCPAuthMiddleware`.
- `tests/e2e/`: End-to-end JSON-RPC protocol tests for tool discovery and invocation.

---

## 🔄 Pull Request Workflow

1. **Branch Naming**: Use descriptive branch names:
   - `feat/feature-name`
   - `fix/bug-fix-name`
   - `docs/documentation-update`
2. **Make Focused Changes**: Avoid mixing unrelated refactoring with feature commits.
3. **Verify Tests**: Ensure `pytest tests/ -v` passes completely with 0 errors or warnings.
4. **Update Documentation**: If configuration options or behaviors change, update `.env.example`, `README.md`, and relevant files in `docs/`.
5. **Submit PR**: Provide a concise summary of the problem, the solution, and verification steps.
