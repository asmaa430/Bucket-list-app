# ─── components/ui_elements.py ───────────────────────────────────────────────
# Higher-level reusable UI components

import tkinter as tk
from theme import (
    CARD, CARD2, BORDER, TEXT, MUTED, ACCENT, GREEN, RED,
    CATEGORY_COLORS, FONT_BODY, FONT_SMALL, FONT_BTN, FONT_SUBHEAD,
    PAD_SM, PAD_MD,
)
from helpers import (
    styled_button, ghost_button, success_button, danger_button,
    category_pill, muted_label, body_label,
)


class GoalCard(tk.Frame):
    """A card widget representing a single goal."""

    def __init__(self, parent, goal, index, on_view, on_done, **kwargs):
        bg = CARD
        super().__init__(
            parent, bg=bg,
            highlightthickness=1,
            highlightbackground=BORDER,
            **kwargs
        )
        self.goal = goal
        self.index = index
        self._build(on_view, on_done)
        self._add_hover()

    def _build(self, on_view, on_done):
        bg = self["bg"]

        # ── Left accent strip (category color) ──────────────────────────────
        cat_color = CATEGORY_COLORS.get(self.goal.get("category", "Other"), ACCENT)
        strip = tk.Frame(self, bg=cat_color, width=4)
        strip.pack(side="left", fill="y")

        # ── Main content ─────────────────────────────────────────────────────
        content = tk.Frame(self, bg=bg, padx=PAD_MD, pady=PAD_MD)
        content.pack(side="left", fill="both", expand=True)

        # Top row: title + done badge
        top = tk.Frame(content, bg=bg)
        top.pack(fill="x")

        title_text = self.goal.get("title", "Untitled")
        if self.goal.get("done"):
            title_text = "✓ " + title_text
        title_color = GREEN if self.goal.get("done") else TEXT
        tk.Label(top, text=title_text, font=FONT_SUBHEAD,
                 fg=title_color, bg=bg, anchor="w",
                 wraplength=320).pack(side="left", fill="x", expand=True)

        # Category pill
        pill_frame = category_pill(top, self.goal.get("category", "Other"),
                                   cat_color, bg=bg)
        pill_frame.pack(side="right", padx=(PAD_SM, 0))

        # Notes preview
        notes = self.goal.get("notes", "")
        if notes:
            preview = notes[:80] + ("…" if len(notes) > 80 else "")
            tk.Label(content, text=preview, font=FONT_SMALL,
                     fg=MUTED, bg=bg, anchor="w", wraplength=380,
                     justify="left").pack(fill="x", pady=(4, 0))

        # ── Buttons ──────────────────────────────────────────────────────────
        btn_row = tk.Frame(content, bg=bg)
        btn_row.pack(fill="x", pady=(PAD_SM, 0))

        ghost_button(btn_row, "View Details",
                     command=lambda: on_view(self.index),
                     pady=5, padx=10).pack(side="left", padx=(0, PAD_SM))

        if not self.goal.get("done"):
            success_button(btn_row, "✓ Mark Done",
                           command=lambda: on_done(self.index),
                           pady=5, padx=10).pack(side="left")
        else:
            tk.Label(btn_row, text="✦ Completed", font=FONT_SMALL,
                     fg=GREEN, bg=bg).pack(side="left")

    def _add_hover(self):
        def _enter(e):
            self.config(highlightbackground=ACCENT,
                        highlightcolor=ACCENT)
        def _leave(e):
            self.config(highlightbackground=BORDER)
        self.bind("<Enter>", _enter)
        self.bind("<Leave>", _leave)


class CompletedCard(tk.Frame):
    """Styled card for completed goals."""

    def __init__(self, parent, goal, **kwargs):
        super().__init__(
            parent, bg="#1a2e1a",
            highlightthickness=1, highlightbackground=GREEN,
            **kwargs
        )
        bg = self["bg"]
        cat_color = CATEGORY_COLORS.get(goal.get("category", "Other"), ACCENT)

        inner = tk.Frame(self, bg=bg, padx=PAD_MD, pady=PAD_MD)
        inner.pack(fill="both", expand=True)

        row = tk.Frame(inner, bg=bg)
        row.pack(fill="x")

        tk.Label(row, text="✦", font=("Georgia", 20, "bold"),
                 fg=GREEN, bg=bg).pack(side="left", padx=(0, PAD_SM))

        info = tk.Frame(row, bg=bg)
        info.pack(side="left", fill="x", expand=True)

        tk.Label(info, text=goal.get("title", "Untitled"),
                 font=FONT_SUBHEAD, fg=GREEN, bg=bg, anchor="w").pack(fill="x")

        pill = category_pill(info, goal.get("category", "Other"),
                             cat_color, bg=bg)
        pill.pack(anchor="w", pady=(2, 0))
