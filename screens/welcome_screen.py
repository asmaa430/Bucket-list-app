# ─── screens/welcome_screen.py ───────────────────────────────────────────────

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from theme import (
    BG, SURFACE, ACCENT, ACCENT2, TEXT, MUTED, FONT_TITLE, FONT_TAGLINE,
    FONT_BODY, PAD_LG, PAD_MD,
)
from helpers import styled_button


def _make_gradient(width, height):
    """Create a vertical gradient image using PIL."""
    img = Image.new("RGB", (width, height), "#0f0f13")
    draw = ImageDraw.Draw(img)
    # Gradient from deep purple to dark bg
    top_color    = (40, 20, 60)     # deep violet
    bottom_color = (15, 15, 19)     # BG
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / height)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._photo = None   # keep reference to prevent GC
        self._build()

    def _build(self):
        # ── Gradient header ──────────────────────────────────────────────────
        header = tk.Canvas(self, width=600, height=320, bg=BG,
                           highlightthickness=0)
        header.pack(fill="x")

        def _draw_gradient(event=None):
            w = self.winfo_width() or 700
            img = _make_gradient(w, 320)

            # Draw decorative circles (soft glow)
            draw = ImageDraw.Draw(img)
            for cx, cy, r, opacity in [
                (w * 0.2, 80, 120, 60),
                (w * 0.8, 200, 160, 40),
                (w * 0.5, 160, 80, 80),
            ]:
                color = (192, 132, 252, opacity)
                # PIL RGBA glow circle
                glow = Image.new("RGBA", (r*2, r*2), (0, 0, 0, 0))
                gd = ImageDraw.Draw(glow)
                gd.ellipse([0, 0, r*2-1, r*2-1],
                           fill=(192, 132, 252, opacity))
                rgba_img = img.convert("RGBA")
                rgba_img.paste(glow, (int(cx - r), int(cy - r)), glow)
                img = rgba_img.convert("RGB")

            self._photo = ImageTk.PhotoImage(img)
            header.delete("all")
            header.create_image(0, 0, anchor="nw", image=self._photo)

            # Stars / sparkles
            import random
            random.seed(42)
            for _ in range(40):
                x = random.randint(0, w)
                y = random.randint(0, 320)
                s = random.choice([1, 2, 2, 1])
                header.create_oval(x, y, x+s, y+s, fill="white", outline="")

            # Title text on canvas
            cx2 = w // 2
            header.create_text(cx2, 120, text="✦ Bucket List ✦",
                               font=FONT_TITLE, fill=TEXT, anchor="center")
            header.create_text(cx2, 170,
                               text="Your dreams. Your journey. Your story.",
                               font=FONT_TAGLINE, fill=ACCENT2, anchor="center")
            header.create_text(cx2, 205,
                               text="One goal at a time.",
                               font=("Helvetica Neue", 12), fill=MUTED,
                               anchor="center")

        header.bind("<Configure>", _draw_gradient)

        # ── Body ─────────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG)
        body.pack(expand=True, fill="both", pady=PAD_LG)

        # Feature highlights
        features = [
            ("🌍", "Track life goals"),
            ("📸", "Attach memories"),
            ("✅", "Celebrate wins"),
            ("📊", "See progress"),
        ]
        row = tk.Frame(body, bg=BG)
        row.pack(pady=(0, PAD_LG))
        for icon, label in features:
            box = tk.Frame(row, bg=SURFACE, padx=16, pady=12,
                           highlightthickness=1,
                           highlightbackground="#33334a")
            box.pack(side="left", padx=8)
            tk.Label(box, text=icon, font=("Helvetica Neue", 22),
                     bg=SURFACE).pack()
            tk.Label(box, text=label, font=("Helvetica Neue", 10),
                     fg=MUTED, bg=SURFACE).pack()

        styled_button(
            body,
            text="  Start My Journey  →",
            command=lambda: self.controller.show_frame("home"),
            pady=14, padx=32,
        ).pack()

        tk.Label(body, text="Version 1.0  •  Your adventures await",
                 font=("Helvetica Neue", 9), fg=MUTED, bg=BG).pack(pady=PAD_LG)
