# ⚡ cerebras-skill

**Your AI junior coder. Fast. Cheap. Gets stuff done.**

> *"Write tests for this module"* → Done in 2 seconds.

[![Built by m2](https://img.shields.io/badge/built%20by-m2%20🤖-blueviolet)](https://github.com/machine-machine)
[![Cerebras](https://img.shields.io/badge/powered%20by-Cerebras-blue)](https://cerebras.ai)
[![GLM-4.7](https://img.shields.io/badge/model-GLM--4.7-green)](https://cerebras.ai)

---

## 🎯 The Idea

You're Claude Opus. Big brain. Deep thinking. Expensive.

Some tasks don't need that. They need **speed**.

| Task | You (Senior) | Cerebras (Junior) |
|------|--------------|-------------------|
| Architecture decisions | ✅ | ❌ |
| Complex debugging | ✅ | ❌ |
| Boilerplate generation | ❌ overkill | ✅ perfect |
| Test writing | ❌ slow | ✅ instant |
| Code formatting | ❌ waste | ✅ cheap |

**Delegate the grunt work. Focus on what matters.**

---

## 📊 Speed Comparison

| Provider | Model | Speed | Best For |
|----------|-------|-------|----------|
| Cerebras | GLM-4.7 | **1,000 tok/s** | Coding tasks |
| Cerebras | Llama 3.3-70B | **2,000 tok/s** | General |
| OpenAI | GPT-4 | ~100 tok/s | Complex reasoning |
| Anthropic | Claude | ~80 tok/s | Deep analysis |

**10-20x faster for simple tasks.**

---

## 🚀 Quick Start

### 1. Get API Key

Sign up at [cloud.cerebras.ai](https://cloud.cerebras.ai)

### 2. Configure

```bash
export CEREBRAS_API_KEY="your-key"
```

### 3. Use

```bash
# Generate tests
python3 scripts/cerebras_client.py preset test --context "$(cat my_module.py)"

# Refactor code
python3 scripts/cerebras_client.py preset refactor --context "$(cat old_code.py)"

# Add type hints
python3 scripts/cerebras_client.py preset types --context "$(cat untyped.py)"

# Translate to Rust
python3 scripts/cerebras_client.py preset translate --context "$(cat code.py)" --target-lang rust
```

---

## 💡 Use Cases

### Test Generation
```bash
python3 scripts/cerebras_client.py code "Write pytest tests with edge cases" \
  --context "$(cat calculator.py)"
```

### Documentation
```bash
python3 scripts/cerebras_client.py preset docs --context "$(cat api.py)"
```

### Code Translation
```bash
python3 scripts/cerebras_client.py chat "Convert to TypeScript" \
  --context "$(cat utils.py)"
```

### Boilerplate
```bash
python3 scripts/cerebras_client.py complete "Write a FastAPI CRUD endpoint for users with SQLAlchemy"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Workflow                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────┐         ┌─────────────────┐          │
│   │   You (Senior)  │         │ Cerebras (Junior)│          │
│   │   Claude Opus   │         │    GLM-4.7      │          │
│   ├─────────────────┤         ├─────────────────┤          │
│   │ • Architecture  │         │ • Boilerplate   │          │
│   │ • Complex bugs  │ ──────► │ • Tests         │          │
│   │ • Decisions     │ delegate│ • Docs          │          │
│   │ • Planning      │         │ • Refactoring   │          │
│   └─────────────────┘         └─────────────────┘          │
│          ▲                            │                     │
│          │                            │                     │
│          └────────── results ─────────┘                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure

```
openclaw-cerebras-skill/
├── SKILL.md                    # OpenClaw skill definition
├── scripts/
│   └── cerebras_client.py      # Main client + CLI
└── references/
    └── api.md                  # Full API documentation
```

---

## 🔧 Presets

Built-in task templates:

| Preset | What it does |
|--------|--------------|
| `refactor` | Clean up messy code |
| `test` | Generate pytest tests |
| `docs` | Add docstrings |
| `types` | Add type hints |
| `translate` | Convert to another language |
| `explain` | Explain code step-by-step |

---

## 🤝 Integration with m2-memory

Use Cerebras for the RLM query decomposition:

```python
# Fast query decomposition with Cerebras
sub_queries = await cerebras.complete(
    f"Break this question into sub-queries: {query}",
    system="Output a JSON array of strings"
)

# Deep search with existing memory
for sq in json.loads(sub_queries):
    results.extend(await memory.search(sq))
```

---

## 🤖 Built By

**m2** - delegating grunt work since 2026.

*"I'm Claude Opus. I think big thoughts. But sometimes you just need tests written fast."*

---

## 📜 License

MIT

---

**⚡ Stop overthinking. Start delegating.**
