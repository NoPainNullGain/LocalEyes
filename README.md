# 👁️ LocalEyes

**Give Claude Code working eyes using your local GPU.** No cloud APIs, no uploads, no cost. A local Ollama vision model converts screenshots into text descriptions Claude can read. Private, fast, free.

### The problem
Claude Code (and most LLMs) can't see images. Other solutions upload screenshots to cloud vision APIs. This one stays on your machine — the vision model runs locally via Ollama.

### How it looks in practice

```
You:    Win+Shift+S  (take a screenshot of an error dialog)
You:    "what's wrong with this?"
Claude: <grabs clipboard, sees error via vision model>
Claude: "That's a TypeScript error in login.ts line 42 — the type
         'User' is missing the 'email' property. Here's the fix..."

Claude: <running build autonomously, it fails>
Claude: <takes its own screenshot: python vision.py screen>
Claude: "I can see 3 build errors in the terminal — fixing them now..."
```

---

## Setup (2 minutes)

### Prerequisites
```bash
ollama pull qwen2.5vl:7b   # one-time, ~4 GB
pip install Pillow
```

### Install
```bash
git clone https://github.com/NoPainNullGain/LocalEyes
cd LocalEyes
python install.py
```

### Verify
```bash
# Press Win+Shift+S to screenshot something, then:
python ~/.claude/skills/local-eyes/vision.py
```

---

## Two modes

| Mode | Trigger | Command |
|------|---------|---------|
| **User shows Claude** | You screenshot something and ask about it | `python vision.py` |
| **Claude looks itself** | Claude decides it needs visual context during agentic work | `python vision.py screen` |

### User mode
```bash
python vision.py                           # describe the clipboard screenshot
python vision.py "What error is shown?"    # focused question
```

### Agentic mode (Claude's own eyes)
```bash
python vision.py screen                              # capture full display
python vision.py screen "Transcribe the terminal"    # focused
python vision.py screenshot.png                      # read a saved file
```

Claude will use `screen` mode **on its own** during workflows — after builds, during debugging, when implementing UI from mockups. No prompt needed.

---

## Configuration

Edit `~/.claude/skills/local-eyes/config.json`:

```json
{
  "ollama_host": "http://localhost:11434",
  "vision_model": "qwen2.5vl:7b",
  "timeout_seconds": 120,
  "temperature": 0.1
}
```

| Setting | Purpose |
|---------|---------|
| `ollama_host` | Where Ollama runs (change for remote GPU servers) |
| `vision_model` | Model to use — try `qwen3-vl`, `llama3.2-vision`, `minicpm-v` |
| `timeout_seconds` | Max wait (increase for large images or slow GPUs) |
| `temperature` | 0.0 = strictly factual, 1.0 = creative descriptions |

Override any setting per-session:
```bash
export OLLAMA_VISION_MODEL="qwen3-vl:latest"
```

---

## How it works

```
┌──────────────────────────┐       ┌─────────────────────────┐
│   Claude Code            │       │  Your machine (Ollama)   │
│                          │       │                         │
│  Main model (text)       │──→──→│  qwen2.5vl:7b (vision)   │
│  DeepSeek / Claude       │←──←──│                         │
│                          │ text  │  "The screenshot shows  │
│  "I can see that..."     │       │   a terminal with..."   │
└──────────────────────────┘       └─────────────────────────┘
```

1. Claude runs `python vision.py` (clipboard, screen, or file)
2. Script captures the image, base64-encodes it
3. Sent to Ollama's local API at `localhost:11434`
4. Qwen2.5-VL returns a detailed text description
5. Claude reads the description and reasons about it

**Nothing leaves your machine.**

---

## Platform support

| OS | Screen capture | Clipboard | Status |
|----|---------------|-----------|--------|
| Windows 10/11 | ✓ | ✓ | Fully tested |
| macOS | ✓ | ✓ | Should work (untested) |
| Linux (X11) | ✓ | ✓ | Should work (untested) |
| Linux (Wayland) | requires `scrot` | ✓ | YMMV |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **"Cannot reach Ollama"** | Run `ollama serve` in a terminal |
| **"No image on clipboard"** | Press Win+Shift+S to take a screenshot first |
| **"Model not found"** | `ollama pull qwen2.5vl:7b` (~4 GB one-time) |
| **"Pillow is required"** | `pip install Pillow` |
| **Timeout** | Increase `timeout_seconds` in config.json |
| **First request slow** | Model loads into VRAM on first call (30-60s). Subsequent calls are fast. |

---

## Files

```
LocalEyes/
├── vision.py       # Engine: screen capture, clipboard, Ollama API
├── SKILL.md        # Instructions Claude reads to use its eyes
├── config.json     # User settings — edit, don't touch code
├── install.py      # One-command installer
├── LICENSE         # MIT
└── README.md
```

## License

MIT © [NoPainNullGain](https://github.com/NoPainNullGain)
