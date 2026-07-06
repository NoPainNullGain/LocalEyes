#!/usr/bin/env python3
"""Generate demo.gif for the LocalEyes README."""

from PIL import Image, ImageDraw, ImageFont

W, H = 780, 520
BG = (22, 22, 22)
PROMPT_COLOR = (100, 255, 100)
OUTPUT_COLOR = (220, 220, 220)
DIM_COLOR = (120, 120, 120)
HEADER_BG = (15, 15, 15)
HEADER_TEXT = (160, 160, 160)
ACCENT = (100, 200, 255)
RED = (255, 100, 100)
ORANGE = (255, 180, 80)

FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
FONT_SMALL = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 12)

PAD_X = 24
PAD_Y = 44
LINE_H = 20


def new_frame():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 30], fill=HEADER_BG)
    draw.text((12, 8), "● ● ●   Terminal — LocalEyes Demo", fill=HEADER_TEXT, font=FONT_SMALL)
    return img, draw


def draw_lines(img, draw, lines, start_y=PAD_Y):
    """lines: list of (text, color, x_offset) — x_offset optional."""
    y = start_y
    for item in lines:
        if isinstance(item, tuple):
            text = item[0]
            color = item[1] if len(item) >= 2 else OUTPUT_COLOR
            x = item[2] if len(item) >= 3 else PAD_X
        else:
            text, color, x = item, OUTPUT_COLOR, PAD_X
        draw.text((x, y), text, fill=color, font=FONT)
        y += LINE_H
    return img


frames = []

# Frame 1: command entered
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", PROMPT_COLOR),
]), 1000))

# Frame 2: loading
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("  Grabbing image from clipboard...", DIM_COLOR),
]), 1200))

# Frame 3-4: vision response
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("  Screenshot — VS Code with a TypeScript error.", OUTPUT_COLOR),
    ("", OUTPUT_COLOR),
    ("  Visible text:", OUTPUT_COLOR),
    ('  src/auth/login.ts:42 — TS2345:', RED),
    ('    Argument of type "User" is not assignable to', RED),
    ('    parameter of type "AuthPayload".', RED),
    ('    Property "email" is missing in type "User".', RED),
    ("", OUTPUT_COLOR),
    ("  Layout: File tree on left, editor center, minimap right.", OUTPUT_COLOR),
    ("  Error underlined in red. Status bar: '1 problem'.", OUTPUT_COLOR),
    ("  Dark+ theme, line 42 highlighted.", OUTPUT_COLOR),
]), 5000))

# Frame 5: agentic mode — model looks itself
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", DIM_COLOR),
    ("  ... (output above) ...", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("$ python vision.py screen", PROMPT_COLOR),
]), 1200))

# Frame 6: model captures its own screen
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", DIM_COLOR),
    ("  ... (output above) ...", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("$ python vision.py screen", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("  Capturing display...", DIM_COLOR),
]), 800))

# Frame 7-8: agentic response
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", DIM_COLOR),
    ("  ... (output above) ...", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("$ python vision.py screen", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("  Full display — 2560x1440. Two windows visible:", OUTPUT_COLOR),
    ("", OUTPUT_COLOR),
    ("  Left: VS Code. login.ts open at line 42.", OUTPUT_COLOR),
    ("  Right: Terminal showing build output.", OUTPUT_COLOR),
    ("  Build: 3 TypeScript errors, 0 warnings.", ORANGE),
    ("", OUTPUT_COLOR),
    ("  Errors in: login.ts:42, routes.ts:88, format.ts:15", ORANGE),
    ("  All three: missing 'email' property on User type.", ORANGE),
]), 6000))

# Frame 9: closing tagline
frames.append((lambda: draw_lines(*new_frame(), [
    ("$ python vision.py", DIM_COLOR),
    ("  ... (output above) ...", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("$ python vision.py screen", DIM_COLOR),
    ("  Full display — 2560x1440. Two windows visible:", DIM_COLOR),
    ("", OUTPUT_COLOR),
    ("  ▸ 100% local — nothing leaves your machine", ACCENT),
    ("  ▸ Works with any text-only LLM in Claude Code", ACCENT),
    ("  ▸ Agentic-ready: model sees on its own", ACCENT),
]), 4500))

# Render
print("Rendering demo.gif...")
gif_frames = []
for i, (fn, dur) in enumerate(frames):
    gif_frames.append(fn())
    print(f"  Frame {i+1}/{len(frames)}")

gif_frames[0].save(
    "demo.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=[f[1] for f in frames],
    loop=0,
)
print(f"Done: demo.gif ({len(frames)} frames, ~{sum(f[1] for f in frames)//1000}s loop)")
