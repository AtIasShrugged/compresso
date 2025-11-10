# Main Page (/)

- Top bar: logo/name, RU/EN switchers, ☼︎/🌙 (theme), logout.
- Three modes (tabs):
  1. **Text** — large `<textarea>`
  2. **Article URL** — `<input type=url>`
  3. **YouTube** — `<input type=url>`
- Options:
  - **Detail level**: radio (short / medium / long)
  - **Model**: select (openai/claude/ollama — read from settings)
- **Summarize** button.
- After submission — result page.

## Result Page

- Header + badge (model, mode, length).
- Content — bullet list with emojis and/or timestamps ⏱️ for video.
- Buttons: copy, save to cache, back.
- "Recent summaries" block (link in sidebar or separate page /history).

## History Page (/history)

- Last N entries, no pagination needed.
- Cards: date, mode, parameters, "Open/Copy/Delete".
- Trim on add (remove old ones beyond N).
