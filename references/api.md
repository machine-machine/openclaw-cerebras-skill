# Cerebras API Reference

## CerebrasClient

### Constructor

```python
CerebrasClient(api_key: str = None, model: str = None)
```

- `api_key`: Cerebras API key (falls back to env/config)
- `model`: Model to use (default: glm-4.7)

### Methods

#### complete()

```python
await client.complete(
    prompt: str,
    system: str = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str
```

Simple prompt → completion.

#### chat()

```python
await client.chat(
    messages: list[dict],  # [{"role": "user", "content": "..."}]
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str
```

Multi-turn chat completion.

#### stream()

```python
async for chunk in client.stream(
    prompt: str,
    system: str = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
):
    print(chunk, end="")
```

Streaming completion.

#### code()

```python
await client.code(
    task: str,
    context: str = None,
    language: str = "python",
) -> str
```

Code generation with coding-optimized prompts.

## CLI Usage

```bash
# Simple completion
python3 cerebras_client.py complete "Explain recursion"

# With streaming
python3 cerebras_client.py complete "Write a long story" --stream

# Code generation
python3 cerebras_client.py code "Add logging" --context "$(cat app.py)"

# Chat with context
python3 cerebras_client.py chat "What's wrong here?" --context "$(cat error.log)"

# Presets
python3 cerebras_client.py preset refactor --context "$(cat old_code.py)"
python3 cerebras_client.py preset test --context "$(cat module.py)"
python3 cerebras_client.py preset translate --context "$(cat code.py)" --target-lang rust
```

## Available Presets

| Preset | Description |
|--------|-------------|
| `refactor` | Clean up and improve code |
| `test` | Generate pytest tests |
| `docs` | Add docstrings and comments |
| `types` | Add Python type hints |
| `translate` | Translate to another language |
| `explain` | Explain code step by step |

## Configuration

### Environment Variable

```bash
export CEREBRAS_API_KEY="your-key"
export CEREBRAS_MODEL="glm-4.7"  # optional
```

### Config File

`~/.config/cerebras/config`:
```
CEREBRAS_API_KEY=your-key
CEREBRAS_MODEL=glm-4.7
```

## Error Handling

```python
try:
    result = await client.complete(prompt)
except Exception as e:
    if "401" in str(e):
        print("Invalid API key")
    elif "429" in str(e):
        print("Rate limited")
    else:
        print(f"Error: {e}")
```
