# Tools

- Python 3.11+
- FastAPI, Uvicorn
- Jinja2 (via Jinja2Templates)
- httpx (async HTTP)
- youtube-transcript-api, yt-dlp
- Whisper: either binary (openai-whisper) or OpenAI Whisper API
- Redis (in prod — managed Redis; in dev — local Docker)
- pydantic-settings
- loguru/structlog (your choice)
- Babel/simple JSON dictionaries for i18n

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn jinja2 httpx python-multipart
pip install pydantic-settings loguru redis
pip install youtube-transcript-api yt-dlp
# for local whisper:
pip install openai-whisper # or torchaudio + ffmpeg installed in system
# for OpenAI/Claude:
pip install openai anthropic
```
