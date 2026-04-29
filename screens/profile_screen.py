# ─── screens/profile_screen.py ───────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox
from theme import (
    BG, SURFACE, CARD, CARD2, ACCENT, ACCENT2, GREEN, MUTED, TEXT, BORDER,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_SMALL, FONT_BTN,
    PAD_LG, PAD_MD, PAD_SM,
)
from helpers import (
    styled_button, ghost_button, styled_entry, styled_text,
    separator, stat_box, scrollable_frame,
)
from components.navbar import Navbar

AVATAR_CHOICES = ["🌟", "🚀", "🦋", "🌊", "🔥", "⚡", "🌙", "🌈", "🎯", "💎"]


class ProfileScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._selected_avatar = tk.StringVar()
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
        tk.Label(nav, text="My Profile", font=FONT_HEADING,
                 fg=ACCENT, bg=SURFACE).pack(side="left", padx=PAD_MD)

        # Scrollable body
        outer, inner = scrollable_frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        body = tk.Frame(inner, bg=BG, padx=PAD_LG, pady=PAD_LG)
        body.pack(fill="both", expand=True)

        # ── Avatar section ────────────────────────────────────────────────────
        avatar_section = tk.Frame(body, bg=CARD,
                                  highlightthickness=1,
                                  highlightbackground=BORDER,
                                  padx=PAD_LG, pady=PAD_LG)
        avatar_section.pack(fill="x", pady=(0, PAD_MD))

        # Big avatar display
        self._avatar_display = tk.Label(
            avatar_section,
            text=self.controller.profile.get("avatar", "🌟"),
            font=("Helvetica Neue", 52),
            bg=CARD,
        )
        self._avatar_display.pack()

        tk.Label(avatar_section, text="Choose your avatar:",
                 font=FONT_SMALL, fg=MUTED, bg=CARD).pack(pady=(PAD_SM, PAD_SM))

        emoji_row = tk.Frame(avatar_section, bg=CARD)
        emoji_row.pack()

        for emoji in AVATAR_CHOICES:
            btn = tk.Button(
                emoji_row, text=emoji,
                font=("Helvetica Neue", 18),
                bg=CARD2, fg=TEXT,
                relief="flat", cursor="hand2",
                pady=4, padx=6, bd=0,
                highlightthickness=1, highlightbackground=BORDER,
                command=lambda e=emoji: self._select_avatar(e),
            )
            btn.pack(side="left", padx=2)

        separator(body)

        # ── Name ──────────────────────────────────────────────────────────────
        tk.Label(body, text="Display Name", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        self._name_entry = styled_entry(body, width=40)
        self._name_entry.pack(fill="x", pady=(PAD_SM, PAD_MD))

        # ── Bio ───────────────────────────────────────────────────────────────
        tk.Label(body, text="Bio", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        self._bio_text = styled_text(body, height=3, width=40)
        self._bio_text.pack(fill="x", pady=(PAD_SM, PAD_MD))

        separator(body)

        # ── Stats display ─────────────────────────────────────────────────────
        tk.Label(body, text="Your Stats", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        self._stats_frame = tk.Frame(body, bg=BG)
        self._stats_frame.pack(fill="x", pady=PAD_SM)

        separator(body)

        # ── Save ──────────────────────────────────────────────────────────────
        styled_button(body, "  ✦ Save Profile  ",
                      command=self._save,
                      pady=12, padx=32).pack(pady=(0, PAD_LG))

        self._navbar = Navbar(self, self.controller)
        self._navbar.pack(side="bottom", fill="x")

    # ── Refresh ───────────────────────────────────────────────────────────────

    def refresh(self):
        profile = self.controller.profile
        goals   = self.controller.goals

        # Populate fields
        self._name_entry.delete(0, "end")
        self._name_entry.insert(0, profile.get("name", "Explorer"))

        self._bio_text.delete("1.0", "end")
        self._bio_text.insert("1.0", profile.get("bio", ""))

        avatar = profile.get("avatar", "🌟")
        self._selected_avatar.set(avatar)
        self._avatar_display.config(text=avatar)

        # Stats
        for w in self._stats_frame.winfo_children():
            w.destroy()

        total   = len(goals)
        done    = sum(1 for g in goals if g.get("done"))
        pending = total - done
        pct     = int(done / total * 100) if total else 0

        for label, val, color in [
            ("Total",     total,     ACCENT),
            ("Done",      done,      GREEN),
            ("Pending",   pending,   "#fbbf24"),
            ("Progress",  f"{pct}%", ACCENT2),
        ]:
            stat_box(self._stats_frame, label, val, color).pack(
                side="left", expand=True, fill="x", padx=4)

        self._navbar.set_active("profile")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _select_avatar(self, emoji):
        self._selected_avatar.set(emoji)
        self._avatar_display.config(text=emoji)

    def _save(self):
        name = self._name_entry.get().strip() or "Explorer"
        bio  = self._bio_text.get("1.0", "end").strip()
        avatar = self._selected_avatar.get() or "🌟"

        self.controller.profile["name"]   = name
        self.controller.profile["bio"]    = bio
        self.controller.profile["avatar"] = avatar

        messagebox.showinfo("Saved!", "Profile updated successfully ✦")
