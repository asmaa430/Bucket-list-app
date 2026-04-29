# ─── screens/home_screen.py ──────────────────────────────────────────────────

import tkinter as tk
import random
from theme import (
    BG, SURFACE, CARD, CARD2, ACCENT, ACCENT2, GREEN, MUTED, TEXT, BORDER,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_SMALL, FONT_BTN,
    PAD_LG, PAD_MD, PAD_SM, CATEGORY_COLORS,
)
from helpers import (
    styled_button, ghost_button, stat_box, muted_label, separator,
    scrollable_frame,
)
from data import INSPIRATION_IDEAS
from components.navbar import Navbar


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        # ── Header bar ───────────────────────────────────────────────────────
        header = tk.Frame(self, bg=SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")

        left = tk.Frame(header, bg=SURFACE, pady=PAD_MD, padx=PAD_LG)
        left.pack(side="left")
        tk.Label(left, text="✦ Bucket List", font=FONT_HEADING,
                 fg=ACCENT, bg=SURFACE).pack(anchor="w")
        self._greeting = tk.Label(left, text="", font=FONT_SMALL,
                                  fg=MUTED, bg=SURFACE)
        self._greeting.pack(anchor="w")

        styled_button(
            header, "＋ Add Goal",
            command=lambda: self.controller.show_frame("add_goal"),
            pady=10, padx=20,
        ).pack(side="right", padx=PAD_LG, pady=PAD_MD)

        # ── Scrollable body ───────────────────────────────────────────────────
        outer, inner = scrollable_frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        # Stats row
        self._stats_frame = tk.Frame(inner, bg=BG)
        self._stats_frame.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, 0))

        separator(inner)

        # Inspiration section
        insp_header = tk.Frame(inner, bg=BG)
        insp_header.pack(fill="x", padx=PAD_LG)
        tk.Label(insp_header, text="✨ Today's Inspiration",
                 font=FONT_SUBHEAD, fg=TEXT, bg=BG).pack(side="left")
        ghost_button(insp_header, "Shuffle",
                     command=self._refresh_inspiration,
                     pady=4, padx=10).pack(side="right")

        self._insp_frame = tk.Frame(inner, bg=BG)
        self._insp_frame.pack(fill="x", padx=PAD_LG, pady=PAD_SM)

        separator(inner)

        # Quick actions
        tk.Label(inner, text="Quick Actions", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w", padx=PAD_LG)

        qa = tk.Frame(inner, bg=BG)
        qa.pack(fill="x", padx=PAD_LG, pady=PAD_SM)

        actions = [
            ("📋 View All Goals", "view_goals"),
            ("✅ Completed",      "completed"),
            ("👤 My Profile",     "profile"),
        ]
        for label, screen in actions:
            ghost_button(qa, label,
                         command=lambda s=screen: self.controller.show_frame(s),
                         pady=10, padx=16).pack(side="left", padx=(0, PAD_SM))

        # Navbar
        self._navbar = Navbar(self, self.controller)
        self._navbar.pack(side="bottom", fill="x")

    # ── Public refresh ────────────────────────────────────────────────────────

    def refresh(self):
        goals = self.controller.goals
        name = self.controller.profile.get("name", "Explorer")
        self._greeting.config(text=f"Welcome back, {name} 👋")

        # Stats
        for w in self._stats_frame.winfo_children():
            w.destroy()

        total     = len(goals)
        done      = sum(1 for g in goals if g.get("done"))
        pending   = total - done
        pct       = int(done / total * 100) if total else 0

        for label, val, color in [
            ("Total Goals",  total,   ACCENT),
            ("Completed",    done,    GREEN),
            ("Pending",      pending, "#fbbf24"),
            ("Progress",     f"{pct}%", ACCENT2),
        ]:
            box = stat_box(self._stats_frame, label, val, color)
            box.pack(side="left", expand=True, fill="x", padx=4)

        self._refresh_inspiration()
        self._navbar.set_active("home")

    def _refresh_inspiration(self):
        for w in self._insp_frame.winfo_children():
            w.destroy()

        picks = random.sample(INSPIRATION_IDEAS, min(4, len(INSPIRATION_IDEAS)))
        for title, category in picks:
            color = CATEGORY_COLORS.get(category, ACCENT)
            card = tk.Frame(self._insp_frame, bg=CARD,
                            highlightthickness=1,
                            highlightbackground=BORDER,
                            padx=PAD_MD, pady=PAD_MD)
            card.pack(side="left", expand=True, fill="x", padx=4)

            tk.Label(card, text=title, font=FONT_BODY,
                     fg=TEXT, bg=CARD, wraplength=140,
                     justify="left").pack(anchor="w")

            pill_bg = CARD2
            tk.Label(card, text=f"  {category}  ",
                     font=FONT_SMALL, fg=color, bg=pill_bg,
                     highlightthickness=1,
                     highlightbackground=color,
                     pady=2).pack(anchor="w", pady=(4, 0))

            def _add_it(t=title, c=category):
                self.controller.goals.append({
                    "title": t, "category": c,
                    "notes": "", "done": False, "image": None,
                })
                self.controller.show_frame("view_goals")

            ghost_button(card, "+ Add This", _add_it,
                         pady=4, padx=8).pack(anchor="w", pady=(6, 0))
