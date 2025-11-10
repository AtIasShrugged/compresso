# Compresso

**Compresso** — Fast LLM Summarizer for Text, Articles, and YouTube videos

A minimal, full-stack Python application built with FastAPI and clean architecture principles.

## ✨ Features

- **Three Summarization Modes**
  - 📝 Text - Direct text input
  - 📰 Article URL - Automatic article extraction
  - 🎥 YouTube - Video transcript with timestamps

- **Flexible Options**
  - Detail levels: Short, Medium, Long
  - Multiple LLM models: GPT-4o, Claude 3.5, and more
  - Timestamp support for video summaries

- **Modern UI/UX**
  - 🌓 Dark/Light theme with system preference detection
  - 🌍 RU/EN localization
  - 📱 Responsive design

- **Built for Production**
  - ⚡️ FastAPI + Jinja2 SSR
  - 🔐 Session-based authentication (no database required)
  - 🧰 Redis caching for recent summaries
  - 📊 Structured logging
  - 🏗️ Clean architecture (domain, infrastructure, presentation layers)

## 🚀 Quick Start (Development)

### Prerequisites

- Python 3.11+
- Redis (local or Docker)
- OpenAI and/or Anthropic API keys

### Installation

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd compresso
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

   Required environment variables:
   ```ini
   APP_SECRET=your-secret-key-here
   APP_LOGIN_PASSWORD=your-password
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   REDIS_URL=redis://localhost:6379/0
   ```

4. **Start Redis**
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:7
   
   # Or use local Redis
   redis-server
   ```

5. **Run application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open browser**
   ```
   http://localhost:8000
   ```

   Default credentials:
   - Username: `admin`
   - Password: (as set in `.env`)

## 📁 Project Structure

```
compresso/
├── app/
│   ├── core/              # Domain layer
│   │   ├── entities/      # Business entities
│   │   ├── ports/         # Port interfaces
│   │   └── usecases/      # Business logic
│   ├── infra/             # Infrastructure layer
│   │   ├── llm/           # LLM clients (OpenAI, Anthropic)
│   │   ├── transcript/    # URL & YouTube providers
│   │   ├── cache/         # Redis cache
│   │   ├── i18n/          # Localization
│   │   └── auth/          # Authentication
│   ├── web/               # Presentation layer
│   │   ├── routes/        # FastAPI routes
│   │   ├── templates/     # Jinja2 templates
│   │   └── static/        # CSS, JS
│   ├── config/            # Configuration
│   └── main.py            # FastAPI app
├── locales/               # Translation files
├── prompts/               # LLM prompt templates
├── instructions/          # Project documentation
└── requirements.txt
```

## 🔧 Configuration

See `.env.example` for all configuration options.

### Key Settings

- `APP_ENV`: `dev` or `prod`
- `APP_SECRET`: Secret key for session signing
- `CACHE_MAX_ITEMS`: Maximum cached summaries (default: 50)
- `WHISPER_MODE`: `local` or `openai` for video transcription
- `LLM_DEFAULT`: Default model (e.g., `openai:gpt-4o-mini`)

## 🌐 Localization

Translations are stored in `locales/{lang}.json`. Supported languages:
- English (`en`)
- Russian (`ru`)

To add a new language:
1. Create `locales/{lang}.json`
2. Add to `APP_ALLOWED_LOCALES` in `.env`

## 🎨 Theming

The application supports light/dark themes with:
- System preference detection
- Manual toggle
- LocalStorage persistence
- CSS variables for easy customization

Edit `app/web/static/css/main.css` to customize colors.

## 📝 Prompt Templates

Prompt templates are in `prompts/{lang}/{mode}_{detail}.txt`:
- `text_short.txt`, `text_medium.txt`, `text_long.txt`
- `url_short.txt`, `url_medium.txt`, `url_long.txt`
- `youtube_short.txt`, `youtube_medium.txt`, `youtube_long.txt`

## 🚀 Deployment on Render

1. **Create Web Service** on [Render.com](https://render.com)

2. **Configuration**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   Set all required variables from `.env.example`
   - Set `APP_ENV=prod`
   - Use Render's managed Redis add-on or external Redis URL

4. **(Optional) Custom Domain**: Configure in Render dashboard

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Type checking
mypy app

# Linting
ruff check app
```

## 📄 API Documentation

When running in development mode, API docs are available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🏗️ Architecture

**Clean Architecture** with three layers:

1. **Domain (Core)**
   - Entities: `SummaryOptions`, `SummaryResult`
   - Ports: Interfaces for LLM, Transcript, Cache
   - Use Cases: Business logic

2. **Infrastructure**
   - Adapters implementing ports
   - External services (OpenAI, Anthropic, Redis)
   - I18n, Authentication

3. **Presentation (Web)**
   - FastAPI routes
   - Jinja2 templates
   - Static assets

## 🔒 Security

- Session-based authentication with signed cookies
- HttpOnly, Secure, SameSite cookies in production
- Input size limits (100k characters)
- No sensitive data in logs
- Secrets via environment variables

## 📚 Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Templates**: Jinja2
- **Styling**: CSS with variables
- **LLM**: OpenAI, Anthropic
- **Transcription**: youtube-transcript-api, yt-dlp, Whisper
- **Cache**: Redis
- **Extraction**: BeautifulSoup4, readability-lxml
- **Logging**: Loguru
- **Config**: Pydantic Settings

## 📖 License

MIT

## 🤝 Contributing

Contributions are welcome! Please follow the clean architecture principles and existing code style.

## 📧 Contact

For issues and questions, please open a GitHub issue.
