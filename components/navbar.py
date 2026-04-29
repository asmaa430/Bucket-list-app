# ─── components/navbar.py ────────────────────────────────────────────────────

import tkinter as tk
from theme import (
    SURFACE, ACCENT, ACCENT2, MUTED, TEXT, BORDER,
    FONT_SMALL, FONT_BTN, BG,
)

NAV_ITEMS = [
    ("🏠", "Home",      "home"),
    ("📋", "Goals",     "view_goals"),
    ("✅", "Done",      "completed"),
    ("👤", "Profile",   "profile"),
]


class Navbar(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, bg=SURFACE,
                         highlightthickness=1, highlightbackground=BORDER,
                         **kwargs)
        self.controller = controller
        self._buttons = {}
        self._build()

    def _build(self):
        for icon, label, screen in NAV_ITEMS:
            col = tk.Frame(self, bg=SURFACE, cursor="hand2")
            col.pack(side="left", expand=True, fill="x")

            icon_lbl = tk.Label(col, text=icon, font=("Helvetica Neue", 18),
                                fg=MUTED, bg=SURFACE)
            icon_lbl.pack(pady=(8, 0))

            text_lbl = tk.Label(col, text=label, font=FONT_SMALL,
                                fg=MUTED, bg=SURFACE)
            text_lbl.pack(pady=(0, 8))

            indicator = tk.Frame(col, bg=SURFACE, height=3)
            indicator.pack(fill="x", side="bottom")

            self._buttons[screen] = (col, icon_lbl, text_lbl, indicator)

            # Bind click to the entire column
            for widget in (col, icon_lbl, text_lbl):
                widget.bind("<Button-1>",
                            lambda e, s=screen: self.controller.show_frame(s))
                widget.bind("<Enter>",
                            lambda e, il=icon_lbl, tl=text_lbl:
                            (il.config(fg=ACCENT2), tl.config(fg=ACCENT2)))
                widget.bind("<Leave>",
                            lambda e, il=icon_lbl, tl=text_lbl, sc=screen:
                            self._on_leave(il, tl, sc))

    def _on_leave(self, icon_lbl, text_lbl, screen):
        active = getattr(self.controller, "_active_screen", None)
        color = ACCENT if screen == active else MUTED
        icon_lbl.config(fg=color)
        text_lbl.config(fg=color)

    def set_active(self, screen_name):
        self.controller._active_screen = screen_name
        for name, (col, icon_lbl, text_lbl, indicator) in self._buttons.items():
            if name == screen_name:
                icon_lbl.config(fg=ACCENT)
                text_lbl.config(fg=ACCENT)
                indicator.config(bg=ACCENT)
            else:
                icon_lbl.config(fg=MUTED)
                text_lbl.config(fg=MUTED)
                indicator.config(bg=SURFACE)
