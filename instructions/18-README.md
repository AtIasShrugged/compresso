# Compresso

Compresso — minimal fast LLM summarizer (Text • Article • YouTube)

## Screenshots

(to be added)

## Features

- ✨ Three summarization modes
- 🎛 Detail and model options
- 🌓 Dark/light themes
- 🌍 RU/EN localization
- ⚡️ FastAPI + Jinja2, clean architecture
- 🧰 Caching last N in Redis
- 🔐 Password authentication (no DB)
- ☁️ Ready for Render deployment

## Quick Start (Dev)

```bash
cp .env.example .env        # fill in keys
docker run -p 6379:6379 redis:7
uvicorn app.main:app --reload
```

## Configuration

See `docs/03-CONFIG.md`

## Deployment

See `docs/17-DEPLOY-RENDER.md`

## License

MIT
