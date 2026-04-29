# ─── helpers.py ──────────────────────────────────────────────────────────────
# Reusable UI helper functions

import tkinter as tk
from theme import (
    ACCENT, ACCENT2, BG, CARD, CARD2, TEXT, MUTED, BORDER, BORDER2,
    GREEN, RED, SURFACE,
    FONT_BTN, FONT_BODY, FONT_SMALL, FONT_SUBHEAD,
    PAD_SM, PAD_MD, PAD_LG,
)


# ── Buttons ───────────────────────────────────────────────────────────────────

def styled_button(parent, text, command, color=ACCENT, text_color=BG,
                  width=None, font=FONT_BTN, pady=10, padx=20):
    """Primary filled button."""
    cfg = dict(
        text=text, command=command, bg=color, fg=text_color,
        font=font, relief="flat", cursor="hand2",
        activebackground=ACCENT2, activeforeground=BG,
        pady=pady, padx=padx, bd=0,
    )
    if width:
        cfg["width"] = width
    btn = tk.Button(parent, **cfg)
    _add_hover(btn, color, ACCENT2, text_color, BG)
    return btn


def ghost_button(parent, text, command, color=ACCENT, font=FONT_BTN,
                 pady=8, padx=16):
    """Outlined ghost button."""
    btn = tk.Button(
        parent, text=text, command=command,
        bg=CARD, fg=color, font=font,
        relief="flat", cursor="hand2",
        activebackground=CARD2, activeforeground=ACCENT2,
        pady=pady, padx=padx, bd=0,
        highlightthickness=1, highlightbackground=color,
        highlightcolor=ACCENT2,
    )
    _add_hover(btn, CARD, CARD2, color, ACCENT2)
    return btn


def danger_button(parent, text, command, font=FONT_BTN, pady=8, padx=16):
    """Red danger button."""
    btn = tk.Button(
        parent, text=text, command=command,
        bg="#3a1a1a", fg=RED, font=font,
        relief="flat", cursor="hand2",
        activebackground="#4a2020", activeforeground=RED,
        pady=pady, padx=padx, bd=0,
        highlightthickness=1, highlightbackground=RED,
    )
    _add_hover(btn, "#3a1a1a", "#4a2020", RED, RED)
    return btn


def success_button(parent, text, command, font=FONT_BTN, pady=8, padx=16):
    """Green success button."""
    btn = tk.Button(
        parent, text=text, command=command,
        bg="#1a3a1a", fg=GREEN, font=font,
        relief="flat", cursor="hand2",
        activebackground="#2a4a2a", activeforeground=GREEN,
        pady=pady, padx=padx, bd=0,
        highlightthickness=1, highlightbackground=GREEN,
    )
    _add_hover(btn, "#1a3a1a", "#2a4a2a", GREEN, GREEN)
    return btn


def _add_hover(widget, bg_normal, bg_hover, fg_normal, fg_hover):
    widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover, fg=fg_hover))
    widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal, fg=fg_normal))


# ── Labels ────────────────────────────────────────────────────────────────────

def heading_label(parent, text, font=FONT_SUBHEAD, color=TEXT, bg=None):
    return tk.Label(
        parent, text=text, font=font, fg=color,
        bg=bg or parent.cget("bg"),
    )


def muted_label(parent, text, font=FONT_SMALL, bg=None):
    return tk.Label(
        parent, text=text, font=font, fg=MUTED,
        bg=bg or parent.cget("bg"),
    )


def body_label(parent, text, font=FONT_BODY, color=TEXT, bg=None, **kwargs):
    return tk.Label(
        parent, text=text, font=font, fg=color,
        bg=bg or parent.cget("bg"), **kwargs
    )


# ── Separators ────────────────────────────────────────────────────────────────

def separator(parent, color=BORDER, pady=8):
    frame = tk.Frame(parent, bg=parent.cget("bg"))
    line = tk.Frame(frame, bg=color, height=1)
    line.pack(fill="x")
    frame.pack(fill="x", pady=pady)
    return frame


# ── Scrollable container ──────────────────────────────────────────────────────

def scrollable_frame(parent, bg=BG):
    """Returns (outer_frame, inner_frame). Pack/grid outer_frame."""
    outer = tk.Frame(parent, bg=bg)

    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview,
                              bg=SURFACE, troughcolor=SURFACE,
                              activebackground=ACCENT)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=bg)
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_canvas_configure(event):
        canvas.itemconfig(window_id, width=event.width)

    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", _on_canvas_configure)

    # Mouse-wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    return outer, inner


# ── Card container ────────────────────────────────────────────────────────────

def card_frame(parent, bg=CARD, pady=6, padx=0):
    frame = tk.Frame(
        parent, bg=bg,
        highlightthickness=1, highlightbackground=BORDER,
    )
    return frame


# ── Category pill ─────────────────────────────────────────────────────────────

def category_pill(parent, category, color, font=FONT_SMALL, bg=None):
    bg = bg or parent.cget("bg")
    # Simulate pill with a label + border
    container = tk.Frame(parent, bg=bg)
    pill_bg = _hex_with_alpha(color, 0.15)  # fallback: use card color
    lbl = tk.Label(
        container, text=f"  {category}  ",
        font=font, fg=color,
        bg=CARD2,
        highlightthickness=1, highlightbackground=color,
        pady=2,
    )
    lbl.pack()
    return container


def _hex_with_alpha(hex_color, alpha):
    """Blend hex color with dark bg for pill effect."""
    return CARD2  # Tkinter doesn't support true RGBA; return a dark surface


# ── Input fields ──────────────────────────────────────────────────────────────

def styled_entry(parent, placeholder="", width=30, font=FONT_BODY):
    entry = tk.Entry(
        parent, font=font, bg=CARD2, fg=TEXT,
        insertbackground=ACCENT, relief="flat",
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=ACCENT, width=width,
    )
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=MUTED)

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=TEXT)

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=MUTED)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    return entry


def styled_text(parent, height=5, width=40, font=FONT_BODY):
    txt = tk.Text(
        parent, font=font, bg=CARD2, fg=TEXT,
        insertbackground=ACCENT, relief="flat",
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=ACCENT,
        height=height, width=width,
        wrap="word", pady=8, padx=8,
    )
    return txt


# ── Stat box ──────────────────────────────────────────────────────────────────

def stat_box(parent, label, value, color=ACCENT, bg=CARD):
    frame = tk.Frame(parent, bg=bg, padx=PAD_MD, pady=PAD_MD,
                     highlightthickness=1, highlightbackground=BORDER)
    tk.Label(frame, text=str(value), font=("Georgia", 28, "bold"),
             fg=color, bg=bg).pack()
    tk.Label(frame, text=label, font=FONT_SMALL,
             fg=MUTED, bg=bg).pack()
    return frame
