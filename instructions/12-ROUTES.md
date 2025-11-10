# Routes

## Public

- `GET /login` — login page.
- `POST /login` — verify, set cookie.
- `POST /logout`

## Protected (middleware)

- `GET /` — form with tabs, options, switchers.
- `POST /summarize/text`
- `POST /summarize/url`
- `POST /summarize/youtube`
- `GET /history` — last N
- `GET /api/healthz` — for Render
