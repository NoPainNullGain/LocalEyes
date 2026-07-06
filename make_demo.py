#!/usr/bin/env python3
"""Generate demo.gif — before/after: DeepSeek blind → LocalEyes gives sight."""

from PIL import Image, ImageDraw, ImageFont

W, H = 780, 520
BG = (22, 22, 22)
PROMPT = (100, 255, 100)     # green prompt
OUTPUT = (220, 220, 220)     # white text
DIM = (120, 120, 120)        # grey/dim
ERROR = (255, 80, 80)        # red errors
ACCENT = (100, 200, 255)     # blue highlights
HEADER_BG = (15, 15, 15)
HEADER_TEXT = (160, 160, 160)

FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
FONT_SM = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 12)

PX, PY, LH = 24, 44, 20


def frame():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 30], fill=HEADER_BG)
    d.text((12, 8), "● ● ●   Terminal — LocalEyes", fill=HEADER_TEXT, font=FONT_SM)
    return img, d


def render(lines):
    """lines: list of (text, color, x_offset). x_offset optional."""
    img, d = frame()
    y = PY
    for item in lines:
        txt = item[0]
        clr = item[1] if len(item) > 1 else OUTPUT
        x = item[2] if len(item) > 2 else PX
        d.text((x, y), txt, fill=clr, font=FONT)
        y += LH
    return img


# ── SCENE 1: DeepSeek is blind ──────────────────────────────────────────────

s1 = render([
    ("$ deepseek-v4-pro (Claude Code)", PROMPT),
    ("", OUTPUT),
    ("User: Look at this screenshot of my app", (255, 220, 100)),
    ("       C:\\git\\ClaudeLocalEyes\\PligtlyFrontPage.jpg", (255, 220, 100)),
    ("", OUTPUT),
    ("DeepSeek:", PROMPT),
    ("  I cannot view or process images directly.", ERROR),
    ("  I'm a text-only model. I have no way to see", ERROR),
    ("  what's in that screenshot.", ERROR),
    ("", OUTPUT),
    ("  Try describing it to me, or use a cloud vision", DIM),
    ("  API like GPT-4 to get a description first.", DIM),
])

# ── SCENE 2: Install LocalEyes ──────────────────────────────────────────────

s2 = render([
    ("$ pip install Pillow && python install.py", PROMPT),
    ("  COPY  vision.py -> ~/.claude/skills/local-eyes/", DIM),
    ("  COPY  SKILL.md  -> ~/.claude/skills/local-eyes/", DIM),
    ("  COPY  config.json -> ~/.claude/skills/local-eyes/", DIM),
    ("  Done. Skill installed.", DIM),
    ("", OUTPUT),
    ("$ # Now let's try that image again...", DIM),
])

# ── SCENE 3: LocalEyes describes the image (real output, condensed) ────────

s3 = render([
    ("$ python vision.py PligtlyFrontPage.jpg", PROMPT),
    ("", OUTPUT),
    ("  Mobile app — dark blue background. Top center:", (180, 180, 180)),
    ("  shield icon with checkmark, gradient pink-to-red,", (180, 180, 180)),
    ("  gold coins and stars around it.", (180, 180, 180)),
    ("", OUTPUT),
    ('  Title: "Pligtly" — bold, light purple font.', OUTPUT),
    ('  Subtitle: "Gor pligter til leg!"', OUTPUT),
    ("", OUTPUT),
    ("  Two buttons:", OUTPUT),
    ("  1. [pink smiley] Jeg er foraelder", OUTPUT),
    ("     Administrer opgaver og belonninger", DIM),
    ("  2. [star icon]   Jeg er barn", OUTPUT),
    ("     Faerdiggor opgaver og pas dit kaeledyr", DIM),
    ("", OUTPUT),
    ("  Bottom: Privatlivspolitik link.", DIM),
])

# ── SCENE 4: DeepSeek now "sees" the app ────────────────────────────────────

s4 = render([
    ("$ python vision.py PligtlyFrontPage.jpg", DIM),
    ("  ...", DIM),
    ("", OUTPUT),
    ("DeepSeek (now with vision):", PROMPT),
    ("", OUTPUT),
    ("  This is a Danish chore-tracking app for families.", OUTPUT),
    ("  Parents manage tasks and rewards; kids complete", OUTPUT),
    ("  them and care for a virtual pet. Clean two-role", OUTPUT),
    ("  design with clear parent/child onboarding paths.", OUTPUT),
    ("", OUTPUT),
    ("  The shield + coins suggest a gamified reward system.", OUTPUT),
    ("  Privacy link at bottom — GDPR-aware. Mobile-first.", OUTPUT),
    ("", OUTPUT),
    ("  Want me to help with the UI, translations, or build", OUTPUT),
    ("  something similar?", OUTPUT),
])

# ── SCENE 5: Agentic mode — model sees on its own ───────────────────────────

s5 = render([
    ("$ python vision.py screen  # model checks build output", PROMPT),
    ("", OUTPUT),
    ("  Full display — 2560x1440. Terminal + VS Code visible.", OUTPUT),
    ("  Build passed. No errors in output.", (100, 255, 100)),
    ("", OUTPUT),
    ("  ▸ 100% local — nothing leaves your machine", ACCENT),
    ("  ▸ Works with DeepSeek, CodeLlama, Qwen, any text-only LLM", ACCENT),
    ("  ▸ Model takes screenshots on its own during agentic work", ACCENT),
    ("", OUTPUT),
    ("  github.com/NoPainNullGain/LocalEyes", DIM),
])

frames = [(s1, 3500), (s2, 2500), (s3, 6000), (s4, 5500), (s5, 4500)]

print("Rendering demo.gif...")
gif_frames = [f[0] for f in frames]
durations = [f[1] for f in frames]
gif_frames[0].save(
    "demo.gif", save_all=True, append_images=gif_frames[1:],
    duration=durations, loop=0,
)
total = sum(durations) / 1000
print(f"Done: demo.gif ({len(frames)} frames, ~{total:.0f}s loop)")
