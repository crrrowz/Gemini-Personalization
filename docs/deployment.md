# Deployment Guide

## 1. Development Mode (Cloudflare Quick Tunnel)
Included out of the box in `compose.yml`. Runs a quick, account-less tunnel that gives you a public HTTPS URL (`*.trycloudflare.com`).
```bash
docker compose up -d
docker logs cloudflared-mcp
```

---

## 2. Production Self-Hosted (VPS with Reverse Proxy)

When deploying to a public Linux VPS (Ubuntu/Debian) with Nginx/Caddy and Let's Encrypt SSL:

### Nginx Reverse Proxy Configuration
```nginx
server {
    server_name mcp.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Essential for MCP SSE & Event Streams
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding off;
        proxy_read_timeout 300s;
    }
}
```

---

## 3. Production with Named Cloudflare Tunnel

In the Cloudflare Zero Trust Dashboard:
1. Create a Named Tunnel.
2. Assign a Public Hostname (e.g. `mcp.yourdomain.com`).
3. Set Service URL to `http://gemini-mcp:8000` (within Docker network) or `http://localhost:8000`.
4. Run cloudflared with your persistent token:
   ```bash
   cloudflared tunnel run --token <YOUR_TOKEN>
   ```
