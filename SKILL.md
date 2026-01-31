---
name: cerebras
description: Fast LLM inference via Cerebras Cloud. Use as a "junior coder" for well-defined tasks like boilerplate generation, refactoring, test writing, documentation, and format conversions. Triggers when a task is clearly specified and needs fast execution rather than deep reasoning. GLM-4.7 at 1000 tok/s.
---

# Cerebras Skill

Fast inference workhorse for well-defined tasks.

## When to Use

✅ **Good fit:**
- Boilerplate code generation
- Simple refactoring
- Test case writing
- Documentation generation
- Format conversions (JSON↔YAML, etc.)
- Code translation between languages
- Regex/pattern generation
- Simple CRUD operations

❌ **Not ideal for:**
- Complex architectural decisions
- Ambiguous requirements
- Multi-step reasoning chains
- Security-sensitive code review

## Quick Start

```bash
# Simple completion
python3 scripts/cerebras_client.py complete "Write a Python function to reverse a string"

# Code task with context
python3 scripts/cerebras_client.py code "Add error handling" --context "$(cat myfile.py)"

# Chat mode
python3 scripts/cerebras_client.py chat "Explain this code" --context "$(cat myfile.py)"
```

## Python API

```python
from scripts.cerebras_client import CerebrasClient

client = CerebrasClient()

# Simple completion
result = await client.complete("Write pytest tests for a calculator class")

# With system prompt
result = await client.chat(
    messages=[{"role": "user", "content": "Convert this to TypeScript"}],
    system="You are a code translator. Output only code, no explanations."
)

# Streaming
async for chunk in client.stream("Write a long function..."):
    print(chunk, end="")
```

## Models

| Model | Speed | Best For |
|-------|-------|----------|
| `glm-4.7` | 1000 tok/s | Coding tasks, agents |
| `llama-3.3-70b` | 2000 tok/s | General tasks |
| `qwen-3-32b` | 2500 tok/s | Fast general |

Default: `glm-4.7` (best coding performance)

## Configuration

```bash
export CEREBRAS_API_KEY="your-api-key"
```

Or store in `~/.config/cerebras/config`:
```
CEREBRAS_API_KEY=your-api-key
CEREBRAS_MODEL=glm-4.7
```

## Integration with m2

Use Cerebras as junior coder in your workflow:

```python
# Senior (Claude) decides what to do
plan = await claude.think("How should we refactor this module?")

# Junior (Cerebras) executes
for task in plan.tasks:
    result = await cerebras.complete(task.prompt)
    await save_file(task.path, result)
```

## References

- [API Details](references/api.md)
- [Prompt Templates](references/templates.md)
