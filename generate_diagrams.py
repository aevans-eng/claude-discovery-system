"""
Generate architecture diagrams for the Claude Discovery System README.
Uses Pillow — no external assets needed.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Colors — dark theme matching GitHub dark mode
BG = (13, 17, 23)          # GitHub dark bg
CARD_BG = (22, 27, 34)     # Card background
BORDER = (48, 54, 61)      # Subtle border
TEXT = (201, 209, 217)      # Primary text
TEXT_DIM = (110, 118, 129)  # Secondary text
BLUE = (88, 166, 255)       # Links / Tier 1
GREEN = (126, 231, 135)     # Success / Tier 2
PURPLE = (210, 168, 255)    # Hub / Tier 0
ORANGE = (240, 136, 62)     # Claude / Action
RED = (248, 81, 73)         # Warning
WHITE = (240, 246, 252)     # Bright text

# Fonts
try:
    FONT_SM = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    FONT_MD = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    FONT_LG = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)
    FONT_XL = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
    FONT_MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
    FONT_MONO_SM = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
except:
    FONT_SM = ImageFont.load_default()
    FONT_MD = FONT_SM
    FONT_LG = FONT_SM
    FONT_XL = FONT_SM
    FONT_MONO = FONT_SM
    FONT_MONO_SM = FONT_SM


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow(draw, start, end, color, width=2, head_size=10):
    """Draw an arrow from start to end."""
    draw.line([start, end], fill=color, width=width)
    # Arrowhead
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    x, y = end
    for da in [2.5, -2.5]:  # ~145 degree spread
        ax = x - head_size * math.cos(angle + da)
        ay = y - head_size * math.sin(angle + da)
        draw.line([(x, y), (int(ax), int(ay))], fill=color, width=width)


def text_center(draw, xy, text, font, fill):
    """Draw centered text at (cx, cy)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((xy[0] - tw // 2, xy[1] - th // 2), text, fill=fill, font=font)


def generate_architecture():
    """Generate the hub-and-spoke architecture diagram."""
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    text_center(draw, (W // 2, 35), "Discovery System Architecture", FONT_XL, WHITE)
    text_center(draw, (W // 2, 70), "Hub-and-spoke with auto-loaded registry", FONT_SM, TEXT_DIM)

    # === TIER 0: Auto-loaded files (top row) ===
    tier0_y = 120

    # CLAUDE.md card
    rounded_rect(draw, (60, tier0_y, 280, tier0_y + 80), 10, fill=CARD_BG, outline=PURPLE, width=2)
    text_center(draw, (170, tier0_y + 25), "CLAUDE.md", FONT_MD, PURPLE)
    text_center(draw, (170, tier0_y + 52), "Rules & behavior", FONT_SM, TEXT_DIM)

    # MEMORY.md card
    rounded_rect(draw, (320, tier0_y, 540, tier0_y + 80), 10, fill=CARD_BG, outline=PURPLE, width=2)
    text_center(draw, (430, tier0_y + 25), "MEMORY.md", FONT_MD, PURPLE)
    text_center(draw, (430, tier0_y + 52), "Who the user is", FONT_SM, TEXT_DIM)

    # Tier 0 label
    rounded_rect(draw, (15, tier0_y + 15, 55, tier0_y + 50), 6, fill=(45, 30, 60), outline=PURPLE, width=1)
    text_center(draw, (35, tier0_y + 32), "T0", FONT_SM, PURPLE)

    # === TIER 1: Registry (center, prominent) ===
    hub_x, hub_y = W // 2, 320
    hub_w, hub_h = 480, 120

    # Glow effect
    for i in range(3, 0, -1):
        glow_color = (BLUE[0] // (4 - i), BLUE[1] // (4 - i), BLUE[2] // (4 - i))
        rounded_rect(draw, (hub_x - hub_w // 2 - i * 3, hub_y - hub_h // 2 - i * 3,
                           hub_x + hub_w // 2 + i * 3, hub_y + hub_h // 2 + i * 3),
                    14, fill=None, outline=glow_color, width=1)

    rounded_rect(draw, (hub_x - hub_w // 2, hub_y - hub_h // 2,
                        hub_x + hub_w // 2, hub_y + hub_h // 2),
                12, fill=CARD_BG, outline=BLUE, width=2)

    text_center(draw, (hub_x, hub_y - 30), "discovery-protocol.md", FONT_LG, BLUE)
    text_center(draw, (hub_x, hub_y + 5), ".claude/rules/  •  auto-loaded  •  survives compaction", FONT_MONO_SM, TEXT_DIM)
    text_center(draw, (hub_x, hub_y + 30), "Project registry + orient/update protocol", FONT_SM, TEXT)

    # Tier 1 label
    rounded_rect(draw, (hub_x - hub_w // 2 - 45, hub_y - 18, hub_x - hub_w // 2 - 5, hub_y + 17), 6,
                fill=(15, 30, 50), outline=BLUE, width=1)
    text_center(draw, (hub_x - hub_w // 2 - 25, hub_y), "T1", FONT_SM, BLUE)

    # Auto-load badge
    badge_x = hub_x + hub_w // 2 + 15
    rounded_rect(draw, (badge_x, hub_y - 15, badge_x + 100, hub_y + 15), 12,
                fill=(15, 40, 20), outline=GREEN, width=1)
    text_center(draw, (badge_x + 50, hub_y), "auto-loads", FONT_MONO_SM, GREEN)

    # Arrows from Tier 0 to Tier 1
    draw_arrow(draw, (170, tier0_y + 80), (hub_x - 120, hub_y - hub_h // 2), PURPLE, width=1, head_size=8)
    draw_arrow(draw, (430, tier0_y + 80), (hub_x, hub_y - hub_h // 2), PURPLE, width=1, head_size=8)
    text_center(draw, (680, tier0_y + 40), "loaded at", FONT_MONO_SM, TEXT_DIM)
    text_center(draw, (680, tier0_y + 58), "session start", FONT_MONO_SM, TEXT_DIM)

    # === TIER 2: STATE.md files (bottom row, spokes) ===
    tier2_y = 500
    projects = [
        ("Project A", "STATE.md", "Active"),
        ("Project B", "STATE.md", "Active"),
        ("Project C", "STATE.md", "Dormant"),
        ("Project D", "STATE.md", "Active"),
    ]

    spoke_positions = []
    for i, (name, file, status) in enumerate(projects):
        x = 120 + i * 260
        spoke_positions.append((x + 100, tier2_y + 40))

        status_color = GREEN if status == "Active" else TEXT_DIM
        rounded_rect(draw, (x, tier2_y, x + 200, tier2_y + 80), 10, fill=CARD_BG, outline=GREEN if status == "Active" else BORDER, width=2)
        text_center(draw, (x + 100, tier2_y + 22), f"{name}/", FONT_MD, GREEN if status == "Active" else TEXT_DIM)
        text_center(draw, (x + 100, tier2_y + 48), file, FONT_MONO_SM, TEXT_DIM)

        # Status dot
        dot_color = GREEN if status == "Active" else TEXT_DIM
        draw.ellipse((x + 170, tier2_y + 8, x + 184, tier2_y + 22), fill=dot_color)

    # Tier 2 label
    rounded_rect(draw, (15, tier2_y + 15, 55, tier2_y + 50), 6, fill=(15, 35, 20), outline=GREEN, width=1)
    text_center(draw, (35, tier2_y + 32), "T2", FONT_SM, GREEN)

    # On-demand badge
    badge_x2 = 1060
    rounded_rect(draw, (badge_x2, tier2_y + 12, badge_x2 + 110, tier2_y + 42), 12,
                fill=(30, 25, 10), outline=ORANGE, width=1)
    text_center(draw, (badge_x2 + 55, tier2_y + 27), "on-demand", FONT_MONO_SM, ORANGE)

    # Arrows from hub to spokes
    for sx, sy in spoke_positions:
        draw_arrow(draw, (hub_x, hub_y + hub_h // 2), (sx, tier2_y), BLUE, width=1, head_size=8)

    # Legend at bottom
    legend_y = 630
    draw.line([(40, legend_y - 10), (W - 40, legend_y - 10)], fill=BORDER, width=1)

    items = [
        (PURPLE, "Tier 0: Always loaded"),
        (BLUE, "Tier 1: Auto-loaded (survives compaction)"),
        (GREEN, "Tier 2: On-demand (per project)"),
        (ORANGE, "Read when entering project"),
    ]
    for i, (color, label) in enumerate(items):
        x = 60 + i * 280
        draw.ellipse((x, legend_y + 8, x + 12, legend_y + 20), fill=color)
        draw.text((x + 18, legend_y + 5), label, fill=TEXT_DIM, font=FONT_SM)

    img.save("assets/architecture.png", quality=95)
    print("Generated: assets/architecture.png")


def generate_lifecycle():
    """Generate the session lifecycle flow diagram."""
    W, H = 1200, 500
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    text_center(draw, (W // 2, 35), "Session Lifecycle", FONT_XL, WHITE)
    text_center(draw, (W // 2, 70), "Orient → Work → Update (every session)", FONT_SM, TEXT_DIM)

    # Flow steps
    steps = [
        ("1", "Session\nStarts", PURPLE, "CLAUDE.md +\nMEMORY.md +\nregistry load"),
        ("2", "Orient", BLUE, "Read registry\n→ see all projects\n+ connections"),
        ("3", "Enter\nProject", GREEN, "Read STATE.md\n→ detailed state\n+ file map"),
        ("4", "Work", ORANGE, "Implement,\nbrainstorm,\nreview, etc."),
        ("5", "Update\nSTATE.md", GREEN, "What was done,\nwhat's next,\nnew file map"),
        ("6", "Sync\nRegistry", BLUE, "Update row:\nstatus, date,\nnext action"),
    ]

    step_w = 150
    step_h = 90
    gap = 30
    total_w = len(steps) * step_w + (len(steps) - 1) * gap
    start_x = (W - total_w) // 2
    y = 140

    for i, (num, title, color, desc) in enumerate(steps):
        x = start_x + i * (step_w + gap)

        # Step number circle
        cx = x + step_w // 2
        cy = y - 5
        draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=color)
        text_center(draw, (cx, cy), num, FONT_MD, BG)

        # Step card
        card_y = y + 25
        rounded_rect(draw, (x, card_y, x + step_w, card_y + step_h), 10,
                    fill=CARD_BG, outline=color, width=2)
        text_center(draw, (x + step_w // 2, card_y + step_h // 2), title, FONT_MD, color)

        # Description below
        desc_y = card_y + step_h + 15
        for j, line in enumerate(desc.split("\n")):
            text_center(draw, (x + step_w // 2, desc_y + j * 18), line, FONT_MONO_SM, TEXT_DIM)

        # Arrow to next step
        if i < len(steps) - 1:
            arrow_y = card_y + step_h // 2
            draw_arrow(draw, (x + step_w + 2, arrow_y), (x + step_w + gap - 2, arrow_y), color, width=2, head_size=8)

    # Loop arrow from step 6 back to step 3 (for next project or next session)
    loop_y = y + 25 + step_h + 85
    x3 = start_x + 2 * (step_w + gap) + step_w // 2  # Center of step 3
    x6 = start_x + 5 * (step_w + gap) + step_w // 2  # Center of step 6

    # Draw the loop
    draw.line([(x6, loop_y - 15), (x6, loop_y)], fill=TEXT_DIM, width=1)
    draw.line([(x6, loop_y), (x3, loop_y)], fill=TEXT_DIM, width=1)
    draw_arrow(draw, (x3, loop_y), (x3, loop_y - 15), TEXT_DIM, width=1, head_size=8)
    text_center(draw, ((x3 + x6) // 2, loop_y + 16), "next project or next session", FONT_SM, TEXT_DIM)

    # Compaction survival note
    note_y = 420
    draw.line([(40, note_y - 15), (W - 40, note_y - 15)], fill=BORDER, width=1)

    # Compaction box
    rounded_rect(draw, (100, note_y, 550, note_y + 50), 8, fill=(30, 20, 10), outline=ORANGE, width=1)
    draw.text((115, note_y + 8), "After compaction:", fill=ORANGE, font=FONT_MD)
    draw.text((115, note_y + 28), "Registry reloads automatically → AI still knows the protocol", fill=TEXT_DIM, font=FONT_SM)

    # Abrupt end box
    rounded_rect(draw, (600, note_y, 1100, note_y + 50), 8, fill=(30, 15, 15), outline=RED, width=1)
    draw.text((615, note_y + 8), "Abrupt session end:", fill=RED, font=FONT_MD)
    draw.text((615, note_y + 28), "Next session detects stale dates → reconciles before work", fill=TEXT_DIM, font=FONT_SM)

    img.save("assets/lifecycle.png", quality=95)
    print("Generated: assets/lifecycle.png")


if __name__ == "__main__":
    import os
    os.makedirs("assets", exist_ok=True)
    os.chdir("C:/Users/aaron/Documents/c-projects/claude-discovery-system")
    generate_architecture()
    generate_lifecycle()
    print("Done!")
