# ─── screens/view_goals_screen.py ────────────────────────────────────────────

import tkinter as tk
from theme import (
    BG, SURFACE, CARD, CARD2, ACCENT, ACCENT2, MUTED, TEXT, BORDER,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_SMALL, FONT_BTN,
    PAD_LG, PAD_MD, PAD_SM,
)
from helpers import (
    styled_button, ghost_button, muted_label, separator,
    scrollable_frame, styled_entry,
)
from components.navbar import Navbar
from components.ui_elements import GoalCard


class ViewGoalsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._search_var = tk.StringVar()
        self._filter_var = tk.StringVar(value="All")
        self._build()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self):
        # Header
        header = tk.Frame(self, bg=SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")

        title_row = tk.Frame(header, bg=SURFACE, pady=PAD_MD, padx=PAD_LG)
        title_row.pack(fill="x")

        ghost_button(title_row, "← Home",
                     command=lambda: self.controller.show_frame("home"),
                     pady=6).pack(side="left")
        tk.Label(title_row, text="My Goals", font=FONT_HEADING,
                 fg=ACCENT, bg=SURFACE).pack(side="left", padx=PAD_MD)

        styled_button(title_row, "＋ Add Goal",
                      command=lambda: self.controller.show_frame("add_goal"),
                      pady=8).pack(side="right")

        # Search bar
        search_row = tk.Frame(header, bg=SURFACE, padx=PAD_LG)
        search_row.pack(fill="x", pady=(0, PAD_MD))

        search_icon = tk.Label(search_row, text="🔍", bg=CARD2,
                               font=("Helvetica Neue", 13),
                               highlightthickness=1, highlightbackground=BORDER,
                               padx=8, pady=6)
        search_icon.pack(side="left")

        self._search_entry = tk.Entry(
            search_row, textvariable=self._search_var,
            font=FONT_BODY, bg=CARD2, fg=TEXT,
            insertbackground=ACCENT, relief="flat",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self._search_entry.pack(side="left", fill="x", expand=True, pady=0)
        self._search_var.trace("w", lambda *_: self._render_goals())

        # Filter pills
        self._filter_frame = tk.Frame(header, bg=SURFACE, padx=PAD_LG)
        self._filter_frame.pack(fill="x", pady=(0, PAD_SM))
        self._filter_buttons = {}
        for label in ["All", "Pending", "Completed"]:
            btn = tk.Button(
                self._filter_frame, text=label,
                font=FONT_SMALL, fg=ACCENT, bg=SURFACE,
                relief="flat", cursor="hand2",
                pady=4, padx=12, bd=0,
                highlightthickness=1, highlightbackground=BORDER,
                command=lambda l=label: self._set_filter(l),
            )
            btn.pack(side="left", padx=(0, PAD_SM))
            self._filter_buttons[label] = btn

        # ── Content area must exist BEFORE _set_filter triggers _render_goals ─
        outer, self._goals_inner = scrollable_frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        self._navbar = Navbar(self, self.controller)
        self._navbar.pack(side="bottom", fill="x")

        # Safe to call now — _goals_inner is ready
        self._set_filter("All")

    # ── Rendering ─────────────────────────────────────────────────────────────

    def refresh(self):
        self._render_goals()
        self._navbar.set_active("view_goals")

    def _set_filter(self, label):
        self._filter_var.set(label)
        for name, btn in self._filter_buttons.items():
            if name == label:
                btn.config(bg=ACCENT, fg=BG)
            else:
                btn.config(bg=SURFACE, fg=ACCENT)
        self._render_goals()

    def _render_goals(self):
        for w in self._goals_inner.winfo_children():
            w.destroy()

        query  = self._search_var.get().lower()
        filt   = self._filter_var.get()
        goals  = self.controller.goals

        filtered = []
        for i, g in enumerate(goals):
            if query and query not in g.get("title", "").lower() \
               and query not in g.get("notes", "").lower() \
               and query not in g.get("category", "").lower():
                continue
            if filt == "Pending" and g.get("done"):
                continue
            if filt == "Completed" and not g.get("done"):
                continue
            filtered.append((i, g))

        if not filtered:
            tk.Label(
                self._goals_inner,
                text="No goals match your search. 🔍",
                font=FONT_BODY, fg=MUTED, bg=BG,
            ).pack(pady=40)
            return

        # Count label
        tk.Label(
            self._goals_inner,
            text=f"  {len(filtered)} goal(s) found",
            font=FONT_SMALL, fg=MUTED, bg=BG,
        ).pack(anchor="w", padx=PAD_LG, pady=(PAD_SM, 0))

        for i, goal in filtered:
            card = GoalCard(
                self._goals_inner, goal, i,
                on_view=self._view_details,
                on_done=self._mark_done,
            )
            card.pack(fill="x", padx=PAD_LG, pady=(PAD_SM, 0))

    def _view_details(self, index):
        self.controller.current_goal_index = index
        self.controller.show_frame("details")

    def _mark_done(self, index):
        self.controller.goals[index]["done"] = True
        self._render_goals()
