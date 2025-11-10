# Deploy on Render

## Procfile (if needed)

```bash
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Setup

- Create Web Service → Python → connect repository.
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: from Procfile or directly (see above).
- Disks not needed (except local Whisper: then ffmpeg + build packs).
- Set ENV: keys, Redis URL, `APP_ENV=prod`.
- Connect domain, enable HTTPS.
