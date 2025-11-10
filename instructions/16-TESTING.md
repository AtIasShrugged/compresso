# Testing

## Unit Tests

- Usecases: verify prompts, options, formatters.
- Infrastructure: mock LLM/Redis/Transcript.

## Integration Tests

- End-to-end via `httpx.AsyncClient` + test Redis (fakeredis/container).
- HTML snapshots (linear checks of key elements).
