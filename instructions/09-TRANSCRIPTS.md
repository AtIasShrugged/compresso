# TranscriptProvider Interface

```python
class TranscriptProvider(Protocol):
    async def from_url(self, url: str) -> str: ...
    async def from_youtube(self, video_id: str) -> str: ...
```

## URL

**url_reader.py**:

- httpx → HTML → extract main text (DOM "visibility" algorithm, remove navigation/scripts).
- Can integrate readability-lxml (via subprocess) or ready Python analog.

## YouTube

- Try `youtube-transcript-api`.
- Fallback: `yt-dlp -x --audio-format mp3` → whisper (`WHISPER_MODE`):
  - **local**: call whisper (ensure ffmpeg)
  - **openai**: send to OpenAI Transcriptions.
