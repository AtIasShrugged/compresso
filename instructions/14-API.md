# API

## Auto-documentation

- FastAPI provides `/docs` and `/redoc` automatically.
- Add OpenAPI metadata (title/version/description, contact, license).

## REST Endpoints

- `POST /api/summarize` — JSON `{ mode, input, detail, model }`
- `GET /api/history?limit=N`

## Response Examples

- SummaryResult in JSON and Markdown (`content_md`, `meta`).
