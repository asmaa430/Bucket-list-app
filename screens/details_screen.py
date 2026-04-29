# ─── screens/details_screen.py ───────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from theme import (
    BG, SURFACE, CARD, CARD2, ACCENT, ACCENT2, GREEN, RED, MUTED, TEXT, BORDER,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_SMALL,
    CATEGORY_COLORS,
    PAD_LG, PAD_MD, PAD_SM,
)
from helpers import (
    ghost_button, styled_button, success_button, danger_button,
    separator, scrollable_frame, category_pill,
)


class DetailsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._image_ref = None

    # ── Build/refresh ─────────────────────────────────────────────────────────

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        idx = getattr(self.controller, "current_goal_index", None)
        if idx is None or idx >= len(self.controller.goals):
            tk.Label(self, text="Goal not found.", fg=MUTED, bg=BG,
                     font=FONT_BODY).pack(pady=40)
            ghost_button(self, "← Back",
                         command=lambda: self.controller.show_frame("view_goals")).pack()
            return

        goal = self.controller.goals[idx]
        cat_color = CATEGORY_COLORS.get(goal.get("category", "Other"), ACCENT)

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self, bg=SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")

        nav = tk.Frame(header, bg=SURFACE, pady=PAD_MD, padx=PAD_LG)
        nav.pack(fill="x")

        ghost_button(nav, "← Back to Goals",
                     command=lambda: self.controller.show_frame("view_goals"),
                     pady=6).pack(side="left")

        if goal.get("done"):
            tk.Label(nav, text="✦ COMPLETED", font=("Helvetica Neue", 11, "bold"),
                     fg=GREEN, bg=SURFACE).pack(side="right")

        # ── Scrollable body ───────────────────────────────────────────────────
        outer, inner = scrollable_frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        body = tk.Frame(inner, bg=BG, padx=PAD_LG, pady=PAD_LG)
        body.pack(fill="both", expand=True)

        # Category + title
        row = tk.Frame(body, bg=BG)
        row.pack(fill="x", pady=(0, PAD_SM))
        pill = category_pill(row, goal.get("category", "Other"), cat_color, bg=BG)
        pill.pack(side="left")

        title_color = GREEN if goal.get("done") else TEXT
        tk.Label(body, text=goal.get("title", "Untitled"),
                 font=FONT_HEADING, fg=title_color, bg=BG,
                 anchor="w", wraplength=500, justify="left").pack(fill="x")

        separator(body)

        # ── Image ─────────────────────────────────────────────────────────────
        img_path = goal.get("image")
        if img_path:
            try:
                img = Image.open(img_path)
                img.thumbnail((460, 280))
                self._image_ref = ImageTk.PhotoImage(img)
                img_frame = tk.Frame(body, bg=CARD,
                                     highlightthickness=1,
                                     highlightbackground=BORDER)
                img_frame.pack(fill="x", pady=(0, PAD_MD))
                tk.Label(img_frame, image=self._image_ref,
                         bg=CARD).pack(padx=2, pady=2)
            except Exception:
                tk.Label(body, text="⚠ Image could not be loaded",
                         font=FONT_SMALL, fg=RED, bg=BG).pack(anchor="w")

        # ── Notes ─────────────────────────────────────────────────────────────
        notes = goal.get("notes", "").strip()
        if notes:
            tk.Label(body, text="Notes", font=FONT_SUBHEAD,
                     fg=MUTED, bg=BG).pack(anchor="w", pady=(0, PAD_SM))
            notes_box = tk.Frame(body, bg=CARD,
                                 highlightthickness=1,
                                 highlightbackground=BORDER,
                                 padx=PAD_MD, pady=PAD_MD)
            notes_box.pack(fill="x", pady=(0, PAD_MD))
            tk.Label(notes_box, text=notes, font=FONT_BODY,
                     fg=TEXT, bg=CARD, wraplength=480,
                     justify="left", anchor="w").pack(fill="x")
        else:
            tk.Label(body, text="No notes added.",
                     font=FONT_SMALL, fg=MUTED, bg=BG).pack(anchor="w")

        separator(body)

        # ── Actions ───────────────────────────────────────────────────────────
        tk.Label(body, text="Actions", font=FONT_SUBHEAD,
                 fg=MUTED, bg=BG).pack(anchor="w", pady=(0, PAD_SM))

        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(anchor="w", pady=(0, PAD_LG))

        if not goal.get("done"):
            success_button(
                btn_row, "✓ Mark as Completed",
                command=lambda: self._mark_done(idx),
                pady=10, padx=16,
            ).pack(side="left", padx=(0, PAD_SM))

        danger_button(
            btn_row, "🗑 Delete Goal",
            command=lambda: self._delete(idx),
            pady=10, padx=16,
        ).pack(side="left")

    # ── Actions ───────────────────────────────────────────────────────────────

    def _mark_done(self, idx):
        self.controller.goals[idx]["done"] = True
        messagebox.showinfo("🎉 Congratulations!", "Goal marked as completed!")
        self.controller.show_frame("completed")

    def _delete(self, idx):
        title = self.controller.goals[idx].get("title", "this goal")
        if messagebox.askyesno("Delete Goal",
                               f"Are you sure you want to delete\n'{title}'?"):
            self.controller.goals.pop(idx)
            self.controller.show_frame("view_goals")
