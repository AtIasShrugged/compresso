# Logging

- Use loguru or structlog.
- Levels: INFO, WARNING, ERROR.
- Required entries: login, LLM/HTTP/yt-dlp/whisper errors, cache operations.
- In prod enable JSON format.
