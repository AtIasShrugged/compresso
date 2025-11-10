# Package Structure (Clean Architecture)

```
app/
  core/               # domain models, interfaces (port/adapter)
    entities/
      summary.py
      options.py
    ports/
      llm.py          # LLM client interface
      transcript.py   # transcription/text getting interface
      cache.py
    usecases/
      summarize_text.py
      summarize_url.py
      summarize_youtube.py
  infra/              # ports realization
    llm/
      openai_client.py
      claude_client.py
    transcript/
      url_reader.py       # article extraction
      ytdlp_whisper.py    # youtube -> audio -> whisper
    cache/
      redis_cache.py
    i18n/
      locale.py
    auth/
      session.py
  web/
    routes/
      pages.py        # SSR (Jinja2)
      api.py          # REST
    templates/
      base.html
      index.html
      result.html
      login.html
      _components/
        header.html
        footer.html
        form_controls.html
    static/
      css/
        main.css      # CSS variables (light/dark), responsive grid
      js/
        theme.js      # theme switch, save in localStorage
        i18n.js       # locale switch (cookie)
  config/
    settings.py       # pydantic BaseSettings with DEV/PROD
  main.py             # FastAPI init, middlewares, mounts
```

## Data Flow

- Presentation (web/routes) calls usecases, passes Options and input data.
- Usecases work only with ports (LLMClient, TranscriptProvider, CacheProvider).
- Infra implements ports (OpenAI/Claude, yt-dlp+whisper, Redis).
- i18n/locale provides string translations for Jinja2.
