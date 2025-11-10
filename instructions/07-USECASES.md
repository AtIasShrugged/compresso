# Models

## SummaryOptions

- **mode**: `text|url|youtube`
- **detail**: `short|medium|long`
- **model**: str (e.g., `"openai:gpt-4o-mini"` or `"anthropic:claude-3-sonnet"`)
- **with_timestamps**: bool (for video — `detail=long` enables it)

## SummaryResult

- **id**, **created_at**, **mode**, **options**, **input_fingerprint**
- **content_md** (or content_html), **meta** (duration, timestamps, etc.)

## Algorithms

### Text

Normalize input → LLM prompt → format response.

### URL

Get article text (readability, boilerplate removal), fallback to simple `httpx.get().text` + extractor.

### YouTube

1. Try `youtube-transcript-api`
2. If not available — `yt-dlp` audio → Whisper (local|openai)
3. Detect chapters/timestamps (based on subtitle start times), if `detail=long`
4. LLM prompt with instruction to add timestamps.

## Prompting

- Prompt template depends on detail + mode + UI locale.
- Example for video (EN, long):  
  _"Create a detailed summary with bullet points, include timestamps in mm:ss format before each point, use emojis for accents."_
