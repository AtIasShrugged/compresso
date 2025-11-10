# LLMClient Interface

```python
class LLMClient(Protocol):
    async def summarize(self, text: str, options: SummaryOptions) -> str: ...
```

## Implementations

- **OpenAIClient**: reads `OPENAI_API_KEY`, maps model.
- **AnthropicClient**: reads `ANTHROPIC_API_KEY`.
- **(Optional) OllamaClient**: local.

## Client Selection

- By prefix: `options.model.split(":")[0]`.
