# Goals

- Full-stack Python (FastAPI + Jinja2), clean architecture, modern minimalist UI.
- Three summarization modes: text, article by URL, YouTube (yt-dlp + Whisper).
- Options: detail level (short/medium/long), model (GPT/Claude/...).
- Password authentication (no registration), 30-day session.
- Cache of last N summaries in Redis (N in config).
- Dev/Prod configurations, deployment on Render.com.
- RU/EN localization, light/dark themes.
- Error logs, pleasant result page (can include emojis 🔹🔸✅).
- API documentation and beautiful README.

## Stages

1. Project initialization
2. Basic architecture (layers, interface skeletons)
3. Infrastructure: configs, logging, i18n, static/themes, sessions, auth
4. Domain and use-cases: summarization (text/URL/video)
5. Integrations: LLM (OpenAI/Claude), yt-dlp, Whisper
6. Redis cache: saving and viewing last N
7. UI: forms, mode switchers, localization, themes
8. API documentation, tests, final polish
9. Prod config and deployment on Render
