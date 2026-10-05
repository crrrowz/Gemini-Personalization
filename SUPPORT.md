# Support Guide

Thank you for using **Gemini Local LLM Bridge**!

To ensure you get help as quickly and effectively as possible, please route your inquiry to the appropriate channel:

---

## 🔍 Where to Get Help

### 1. Questions & Usage Help
If you have questions about:
- Connecting Gemini to your custom model
- Configuring Ollama, LM Studio, or vLLM
- Setting up Cloudflare Tunnels or Nginx Reverse Proxies

👉 **Check our documentation first:**
- [Visual Setup Guide](docs/gemini-setup-guide.md)
- [Troubleshooting & FAQ](docs/troubleshooting.md)
- [Deployment Guide](docs/deployment.md)

If your question is not covered, open a discussion or question in the **GitHub Discussions** tab.

---

### 2. Bug Reports
If you encounter a bug or unexpected behavior:
1. Ensure you have tested with the latest version of the repository.
2. Run the diagnostic script:
   ```bash
   python scripts/verify_mcp.py http://localhost:8000
   ```
3. Open a **GitHub Issue** and include:
   - Your OS and Python / Docker version
   - Configuration used (without secrets or API keys)
   - Steps to reproduce the issue
   - Relevant log output from `docker logs gemini-mcp-server`

---

### 3. Feature Requests
If you have an idea for a new feature or provider implementation:
- Open an issue titled `[Feature Request]: <short description>` detailing your use case, expected behavior, and architectural impact.

---

### 4. Security Vulnerabilities
- For security issues, please follow the confidential reporting instructions outlined in [SECURITY.md](SECURITY.md).
