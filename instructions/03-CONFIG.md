# Environment Variables

```ini
APP_ENV=dev|prod
APP_SECRET=<random-hex>
APP_LOCALE_DEFAULT=en
APP_ALLOWED_LOCALES=en,ru

# Auth
APP_LOGIN_USER=sasha
APP_LOGIN_PASSWORD=<strong_password>
APP_SESSION_DAYS=30

# Redis
REDIS_URL=redis://localhost:6379/0
CACHE_MAX_ITEMS=50

# LLMs
LLM_DEFAULT=openai:gpt-4o-mini
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...

# Whisper
WHISPER_MODE=local|openai
WHISPER_MODEL=small
```

## Pydantic Settings Example

- `config/settings.py` with BaseSettings
- Separate DevSettings and ProdSettings, selected by APP_ENV.
