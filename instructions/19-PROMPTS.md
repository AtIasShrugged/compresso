# Prompt Library (i18n)

- `prompts/ru/...`, `prompts/en/...`
- Placeholders: `{detail}`, `{mode}`, `{timestamps}`

## Example EN (video, long)

```text
Create a detailed, structured video summary.
• At the beginning of each point, indicate the timestamp in [mm:ss] format.
• Format as a bulleted list with emojis.
• Avoid word-for-word retelling, highlight semantic blocks and conclusions.
Transcript text:
{content}
```

## Mini-checklist Before Start

- Repository with basic structure
- Configured `settings.py` and `.env`
- Connected static, Jinja2, locales
- Auth middleware and `/login` page
- Routes `/`, `/history`, handlers for three modes
- Port implementations: LLM, URL, YouTube, Redis
- Error logging
- Use-case tests
- README and OpenAPI metadata
- Dev/Prod configs and Render deployment
