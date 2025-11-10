# Requirements

- First page — login.
- No registration, 1–N passwords from config.
- Session (signed cookie) for 30 days.
- CSRF not needed (forms — POST with cookie; optionally add token).

## Implementation

- Middleware on Starlette to check cookie session.
- Login logic: verify user/password against config, issue Set-Cookie (HttpOnly, Secure in prod).
- Logout — clear cookie.
