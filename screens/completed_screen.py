# ─── screens/completed_screen.py ─────────────────────────────────────────────

import tkinter as tk
from theme import (
    BG, SURFACE, CARD, GREEN, MUTED, TEXT, ACCENT, BORDER,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_SMALL,
    PAD_LG, PAD_MD, PAD_SM,
)
from helpers import ghost_button, scrollable_frame, muted_label
from components.navbar import Navbar
from components.ui_elements import CompletedCard


class CompletedScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self, bg=SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")

        nav = tk.Frame(header, bg=SURFACE, pady=PAD_MD, padx=PAD_LG)
        nav.pack(fill="x")

        ghost_button(nav, "← Home",
                     command=lambda: self.controller.show_frame("home"),
                     pady=6).pack(side="left")
        tk.Label(nav, text="✦ Completed Goals", font=FONT_HEADING,
                 fg=GREEN, bg=SURFACE).pack(side="left", padx=PAD_MD)

        # Scrollable body
        outer, self._inner = scrollable_frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        self._navbar = Navbar(self, self.controller)
        self._navbar.pack(side="bottom", fill="x")

    def refresh(self):
        for w in self._inner.winfo_children():
            w.destroy()

        completed = [g for g in self.controller.goals if g.get("done")]
        total = len(self.controller.goals)

        # Banner
        banner = tk.Frame(self._inner, bg="#1a2e1a", padx=PAD_LG, pady=PAD_MD,
                          highlightthickness=1, highlightbackground=GREEN)
        banner.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, PAD_SM))

        pct = int(len(completed) / total * 100) if total else 0
        tk.Label(banner,
                 text=f"🎉  {len(completed)} of {total} goals completed  —  {pct}% done!",
                 font=("Georgia", 14, "bold"), fg=GREEN, bg="#1a2e1a").pack()

        # Progress bar
        bar_outer = tk.Frame(self._inner, bg=CARD,
                             highlightthickness=1, highlightbackground=BORDER,
                             height=10)
        bar_outer.pack(fill="x", padx=PAD_LG, pady=(0, PAD_MD))
        bar_outer.pack_propagate(False)
        if pct > 0:
            bar_fill = tk.Frame(bar_outer, bg=GREEN, height=10)
            bar_fill.place(relx=0, rely=0, relwidth=pct/100, relheight=1)

        if not completed:
            tk.Label(self._inner,
                     text="No completed goals yet.\nKeep going! 💪",
                     font=FONT_BODY, fg=MUTED, bg=BG,
                     justify="center").pack(pady=40)
            self._navbar.set_active("completed")
            return

        tk.Label(self._inner, text="Your achievements:",
                 font=FONT_SUBHEAD, fg=TEXT, bg=BG).pack(
            anchor="w", padx=PAD_LG, pady=(0, PAD_SM))

        for goal in completed:
            card = CompletedCard(self._inner, goal)
            card.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        self._navbar.set_active("completed")
