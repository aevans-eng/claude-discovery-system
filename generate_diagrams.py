"""
Generate architecture diagrams for the Claude Discovery System README.
Uses Pillow with supersampling + anchor-based centering + dynamic layout.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# === RENDERING CONFIG ===
SCALE = 2  # Supersample factor — draw at 2x, downscale with Lanczos
TARGET_W, TARGET_H_ARCH = 1200, 700
TARGET_W_LIFE, TARGET_H_LIFE = 1200, 500

# Colors — dark theme matching GitHub dark mode
BG = (13, 17, 23)
CARD_BG = (22, 27, 34)
BORDER = (48, 54, 61)
TEXT = (201, 209, 217)
TEXT_DIM = (110, 118, 129)
BLUE = (88, 166, 255)
GREEN = (126, 231, 135)
PURPLE = (210, 168, 255)
ORANGE = (240, 136, 62)
RED = (248, 81, 73)
WHITE = (240, 246, 252)


def s(val):
    """Scale a value by the supersample factor."""
    return int(val * SCALE)


def load_fonts():
    """Load fonts at scaled sizes."""
    base = "C:/Windows/Fonts"
    try:
        return {
            "sm": ImageFont.truetype(f"{base}/segoeui.ttf", s(16)),
            "md": ImageFont.truetype(f"{base}/segoeuib.ttf", s(20)),
            "lg": ImageFont.truetype(f"{base}/segoeuib.ttf", s(28)),
            "xl": ImageFont.truetype(f"{base}/segoeuib.ttf", s(36)),
            "mono": ImageFont.truetype(f"{base}/consola.ttf", s(15)),
            "mono_sm": ImageFont.truetype(f"{base}/consola.ttf", s(13)),
        }
    except Exception:
        f = ImageFont.load_default()
        return {k: f for k in ["sm", "md", "lg", "xl", "mono", "mono_sm"]}


FONTS = load_fonts()


# === NODE SYSTEM ===

def make_node(x, y, w, h):
    """Create a node with named anchor points for clean line connections."""
    return {
        "rect": (s(x), s(y), s(x + w), s(y + h)),
        "top": (s(x + w / 2), s(y)),
        "bottom": (s(x + w / 2), s(y + h)),
        "left": (s(x), s(y + h / 2)),
        "right": (s(x + w), s(y + h / 2)),
        "center": (s(x + w / 2), s(y + h / 2)),
        "x": s(x), "y": s(y), "w": s(w), "h": s(h),
    }


def draw_node(draw, node, label, sublabel, font_main, font_sub, color, fill=CARD_BG):
    """Draw a rounded-rect node with centered text using anchor='mm'."""
    draw.rounded_rectangle(node["rect"], radius=s(10), fill=fill, outline=color, width=s(2))
    cx, cy = node["center"]
    if sublabel:
        draw.text((cx, cy - s(10)), label, font=font_main, fill=color, anchor="mm")
        draw.text((cx, cy + s(14)), sublabel, font=font_sub, fill=TEXT_DIM, anchor="mm")
    else:
        draw.text((cx, cy), label, font=font_main, fill=color, anchor="mm")


def draw_arrow(draw, start, end, color, width=2, head_size=10):
    """Draw an arrow from start to end with arrowhead."""
    w = s(width)
    hs = s(head_size)
    draw.line([start, end], fill=color, width=w)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    x, y = end
    for da in [2.5, -2.5]:
        ax = x - hs * math.cos(angle + da)
        ay = y - hs * math.sin(angle + da)
        draw.line([(x, y), (int(ax), int(ay))], fill=color, width=w)


def draw_badge(draw, x, y, text, color):
    """Draw a small rounded badge."""
    tw = len(text) * s(8) + s(16)
    rect = (s(x), s(y) - s(14), s(x) + tw, s(y) + s(14))
    draw.rounded_rectangle(rect, radius=s(12), fill=BG, outline=color, width=s(1))
    cx = s(x) + tw // 2
    draw.text((cx, s(y)), text, font=FONTS["mono_sm"], fill=color, anchor="mm")


def draw_tier_label(draw, x, y, tier_num, color):
    """Draw a tier label chip."""
    rect = (s(x), s(y) - s(16), s(x + 40), s(y + 16))
    bg = tuple(c // 4 for c in color)
    draw.rounded_rectangle(rect, radius=s(6), fill=bg, outline=color, width=s(1))
    draw.text((s(x + 20), s(y)), f"T{tier_num}", font=FONTS["sm"], fill=color, anchor="mm")


def finalize(img, target_w, target_h, path):
    """Downscale with Lanczos and save."""
    final = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    final.save(path, quality=95)
    print(f"Generated: {path}")


# === ARCHITECTURE DIAGRAM ===

def generate_architecture():
    W, H = s(TARGET_W), s(TARGET_H_ARCH)
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((W // 2, s(35)), "Discovery System Architecture", font=FONTS["xl"], fill=WHITE, anchor="mm")
    draw.text((W // 2, s(70)), "Hub-and-spoke with auto-loaded registry", font=FONTS["sm"], fill=TEXT_DIM, anchor="mm")

    # === TIER 0 ===
    tier0_y = 120
    claude_node = make_node(80, tier0_y, 220, 80)
    memory_node = make_node(340, tier0_y, 220, 80)

    draw_tier_label(draw, 20, tier0_y + 40, 0, PURPLE)

    # Draw lines BEFORE nodes (lines go behind)
    hub_node = make_node(360, 280, 480, 120)  # define hub early for line targets

    draw_arrow(draw, claude_node["bottom"], (hub_node["top"][0] - s(80), hub_node["top"][1]), PURPLE, width=1, head_size=8)
    draw_arrow(draw, memory_node["bottom"], hub_node["top"], PURPLE, width=1, head_size=8)

    # Now draw nodes on top
    draw_node(draw, claude_node, "CLAUDE.md", "Rules & behavior", FONTS["md"], FONTS["sm"], PURPLE)
    draw_node(draw, memory_node, "MEMORY.md", "Who the user is", FONTS["md"], FONTS["sm"], PURPLE)

    draw.text((s(630), s(tier0_y + 35)), "loaded at", font=FONTS["mono_sm"], fill=TEXT_DIM, anchor="mm")
    draw.text((s(630), s(tier0_y + 55)), "session start", font=FONTS["mono_sm"], fill=TEXT_DIM, anchor="mm")

    # === TIER 1: Hub ===
    # Glow
    for i in range(3, 0, -1):
        g = s(i * 3)
        glow = tuple(c // (4 - i) for c in BLUE)
        r = hub_node["rect"]
        draw.rounded_rectangle((r[0] - g, r[1] - g, r[2] + g, r[3] + g), radius=s(14), outline=glow, width=s(1))

    draw_node(draw, hub_node, "discovery-protocol.md", None, FONTS["lg"], FONTS["sm"], BLUE)
    # Sub-lines inside hub
    cx, cy = hub_node["center"]
    draw.text((cx, cy + s(18)), ".claude/rules/  •  auto-loaded  •  survives compaction", font=FONTS["mono_sm"], fill=TEXT_DIM, anchor="mm")
    draw.text((cx, cy + s(40)), "Project registry + orient/update protocol", font=FONTS["sm"], fill=TEXT, anchor="mm")

    draw_tier_label(draw, 310, 340, 1, BLUE)
    draw_badge(draw, 860, 340, "auto-loads", GREEN)

    # === TIER 2: Spokes (dynamic spacing) ===
    tier2_y = 500
    projects = [
        ("Project A/", True),
        ("Project B/", True),
        ("Project C/", False),  # dormant
        ("Project D/", True),
    ]
    num = len(projects)
    proj_w = 200
    total_needed = num * proj_w
    spacing = (TARGET_W - total_needed) / (num + 1)

    spoke_nodes = []
    for i, (name, active) in enumerate(projects):
        x = spacing + i * (proj_w + spacing)
        node = make_node(x, tier2_y, proj_w, 80)
        spoke_nodes.append(node)

        color = GREEN if active else BORDER
        # Lines first
        draw_arrow(draw, hub_node["bottom"], node["top"], BLUE, width=1, head_size=8)
        # Node on top
        draw_node(draw, node, name, "STATE.md", FONTS["md"], FONTS["mono_sm"], color)

        # Status dot
        dot_x = node["rect"][2] - s(20)
        dot_y = node["rect"][1] + s(10)
        draw.ellipse((dot_x, dot_y, dot_x + s(12), dot_y + s(12)), fill=GREEN if active else TEXT_DIM)

    draw_tier_label(draw, 20, tier2_y + 40, 2, GREEN)
    draw_badge(draw, 1070, tier2_y + 65, "on-demand", ORANGE)

    # === LEGEND ===
    legend_y = 640
    draw.line([(s(40), s(legend_y - 10)), (W - s(40), s(legend_y - 10))], fill=BORDER, width=s(1))

    items = [
        (PURPLE, "Tier 0: Always loaded"),
        (BLUE, "Tier 1: Auto-loaded, survives compaction"),
        (GREEN, "Tier 2: On-demand, per project"),
    ]
    total_legend_w = sum(len(label) * 8 + 40 for _, label in items)
    legend_start = (TARGET_W - total_legend_w) // 2
    lx = legend_start
    for color, label in items:
        draw.ellipse((s(lx), s(legend_y + 8), s(lx + 12), s(legend_y + 20)), fill=color)
        draw.text((s(lx + 18), s(legend_y + 14)), label, fill=TEXT_DIM, font=FONTS["sm"], anchor="lm")
        lx += len(label) * 8 + 50

    finalize(img, TARGET_W, TARGET_H_ARCH, "assets/architecture.png")


# === SESSION LIFECYCLE DIAGRAM ===

def generate_lifecycle():
    W, H = s(TARGET_W_LIFE), s(TARGET_H_LIFE)
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((W // 2, s(35)), "Session Lifecycle", font=FONTS["xl"], fill=WHITE, anchor="mm")
    draw.text((W // 2, s(70)), "Orient \u2192 Work \u2192 Update (every session)", font=FONTS["sm"], fill=TEXT_DIM, anchor="mm")

    # Steps
    steps = [
        ("1", "Session\nStarts", PURPLE, "CLAUDE.md +\nMEMORY.md +\nregistry load"),
        ("2", "Orient", BLUE, "Read registry\n\u2192 see all projects\n+ connections"),
        ("3", "Enter\nProject", GREEN, "Read STATE.md\n\u2192 detailed state\n+ file map"),
        ("4", "Work", ORANGE, "Implement,\nbrainstorm,\nreview, etc."),
        ("5", "Update\nSTATE.md", GREEN, "What was done,\nwhat's next,\nnew file map"),
        ("6", "Sync\nRegistry", BLUE, "Update row:\nstatus, date,\nnext action"),
    ]

    num_steps = len(steps)
    step_w = 150
    step_h = 90
    total_needed = num_steps * step_w
    gap = (TARGET_W_LIFE - total_needed - 80) / (num_steps - 1)  # 80px margin
    start_x = 40
    y = 140

    step_nodes = []
    for i, (num, title, color, desc) in enumerate(steps):
        x = start_x + i * (step_w + gap)
        node = make_node(x, y + 25, step_w, step_h)
        step_nodes.append(node)

        # Number circle
        cx = s(x + step_w / 2)
        cy = s(y - 5)
        r = s(16)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
        draw.text((cx, cy), num, font=FONTS["md"], fill=BG, anchor="mm")

        # Arrow to next (draw before nodes)
        if i < num_steps - 1:
            next_x = start_x + (i + 1) * (step_w + gap)
            next_node_left = (s(next_x), s(y + 25 + step_h / 2))
            draw_arrow(draw, node["right"], next_node_left, color, width=2, head_size=8)

        # Step card
        draw_node(draw, node, title, None, FONTS["md"], FONTS["sm"], color)

        # Description below
        desc_y = y + 25 + step_h + 18
        for j, line in enumerate(desc.split("\n")):
            draw.text((s(x + step_w / 2), s(desc_y + j * 18)), line, font=FONTS["mono_sm"], fill=TEXT_DIM, anchor="mm")

    # Loop arrow from step 6 back to step 3
    loop_y = y + 25 + step_h + 85
    x3_center = step_nodes[2]["center"][0]
    x6_center = step_nodes[5]["center"][0]

    draw.line([(x6_center, s(loop_y - 15)), (x6_center, s(loop_y))], fill=TEXT_DIM, width=s(1))
    draw.line([(x6_center, s(loop_y)), (x3_center, s(loop_y))], fill=TEXT_DIM, width=s(1))
    draw_arrow(draw, (x3_center, s(loop_y)), (x3_center, s(loop_y - 15)), TEXT_DIM, width=1, head_size=8)
    draw.text(((x3_center + x6_center) // 2, s(loop_y + 16)), "next project or next session", font=FONTS["sm"], fill=TEXT_DIM, anchor="mm")

    # Bottom notes
    note_y = 420
    draw.line([(s(40), s(note_y - 15)), (W - s(40), s(note_y - 15))], fill=BORDER, width=s(1))

    # Compaction note
    compact_rect = (s(80), s(note_y), s(560), s(note_y + 55))
    draw.rounded_rectangle(compact_rect, radius=s(8), fill=(30, 20, 10), outline=ORANGE, width=s(1))
    draw.text((s(95), s(note_y + 14)), "After compaction:", font=FONTS["md"], fill=ORANGE, anchor="lm")
    draw.text((s(95), s(note_y + 38)), "Registry reloads automatically \u2192 AI still knows the protocol", font=FONTS["sm"], fill=TEXT_DIM, anchor="lm")

    # Abrupt end note
    abort_rect = (s(600), s(note_y), s(1120), s(note_y + 55))
    draw.rounded_rectangle(abort_rect, radius=s(8), fill=(30, 15, 15), outline=RED, width=s(1))
    draw.text((s(615), s(note_y + 14)), "Abrupt session end:", font=FONTS["md"], fill=RED, anchor="lm")
    draw.text((s(615), s(note_y + 38)), "Next session detects stale dates \u2192 reconciles before work", font=FONTS["sm"], fill=TEXT_DIM, anchor="lm")

    finalize(img, TARGET_W_LIFE, TARGET_H_LIFE, "assets/lifecycle.png")


if __name__ == "__main__":
    import os
    os.chdir("C:/Users/aaron/Documents/c-projects/claude-discovery-system")
    os.makedirs("assets", exist_ok=True)
    generate_architecture()
    generate_lifecycle()
    print("Done!")
