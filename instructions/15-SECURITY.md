# Security

- Store secrets only in ENV/Render Secrets.
- Cookies: HttpOnly, Secure (prod), SameSite=Lax.
- Limit input text size (e.g., 100k characters).
- Limit processing duration (timeouts).
- Logs without sensitive data.
- CORS closed (not needed for SSR).
- Rate-limit (optional).
