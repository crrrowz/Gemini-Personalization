# Security Policy

## 🛡️ Supported Versions

We provide active security fixes for the latest stable release of the `main` branch.

| Version | Supported |
|---|---|
| `main` (Latest) | ✅ Yes |
| `< 1.0.0` | ❌ No (Please upgrade to latest) |

---

## 🔒 Security Architecture & Boundaries

The Gemini Local LLM Bridge is designed with defense-in-depth security principles:
1. **Network Isolation**: The local LLM backend is kept completely isolated on your internal network or localhost; only the MCP endpoint `/mcp` is exposed to Gemini.
2. **Secret Redaction**: Structured logging sanitizes and redacts Bearer tokens, API keys, and sensitive authorization headers from stdout and log streams.
3. **Endpoint Authentication**: Support for optional Bearer Token verification on the `/mcp` endpoint via `AUTH_TOKEN`.
4. **Non-Root Execution**: Docker containers run as unprivileged non-root `appuser` (UID: 10001).

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability within this project, please **DO NOT open a public GitHub issue**.

Please report vulnerabilities privately:
1. Send an email to the project maintainers with the subject line: `[SECURITY VULNERABILITY] Gemini Local LLM Bridge`.
2. Include:
   - A clear description of the vulnerability.
   - Steps to reproduce or proof-of-concept (PoC).
   - Potential impact on users or host infrastructure.
3. You will receive an acknowledgment within **48 hours**, followed by a timeline for investigation, patching, and coordinated disclosure.
