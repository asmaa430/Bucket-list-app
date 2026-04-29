# ─── screens/add_goal_screen.py ──────────────────────────────────────────────

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from theme import (
    BG, SURFACE, CARD, CARD2, ACCENT, ACCENT2, GREEN, MUTED, TEXT, BORDER,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_SMALL, FONT_BTN,
    CATEGORIES, CATEGORY_COLORS,
    PAD_LG, PAD_MD, PAD_SM,
)
from helpers import (
    styled_button, ghost_button, danger_button,
    styled_entry, styled_text,
    heading_label, muted_label, separator,
)


class AddGoalScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self._selected_category = tk.StringVar(value="Travel")
        self._image_path = None
        self._image_ref = None   # prevent GC

        self._build()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self):
        # Header
        header = tk.Frame(self, bg=SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")

        nav = tk.Frame(header, bg=SURFACE, pady=PAD_MD, padx=PAD_LG)
        nav.pack(fill="x")

        ghost_button(nav, "← Back",
                     command=lambda: self.controller.show_frame("home"),
                     pady=6).pack(side="left")
        tk.Label(nav, text="Add New Goal", font=FONT_HEADING,
                 fg=ACCENT, bg=SURFACE).pack(side="left", padx=PAD_MD)

        # Scrollable body
        from helpers import scrollable_frame
        outer, inner = scrollable_frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        body = tk.Frame(inner, bg=BG, padx=PAD_LG, pady=PAD_LG)
        body.pack(fill="both", expand=True)

        # ── Title input ──────────────────────────────────────────────────────
        tk.Label(body, text="Goal Title *", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        muted_label(body, "What do you want to achieve?").pack(anchor="w", pady=(0, PAD_SM))
        self._title_entry = styled_entry(body, width=50)
        self._title_entry.pack(fill="x", pady=(0, PAD_MD))

        separator(body)

        # ── Category ─────────────────────────────────────────────────────────
        tk.Label(body, text="Category", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        muted_label(body, "Pick the bucket this goal belongs to.").pack(anchor="w", pady=(0, PAD_SM))

        self._cat_frame = tk.Frame(body, bg=BG)
        self._cat_frame.pack(fill="x", pady=(0, PAD_MD))
        self._cat_buttons = {}
        self._build_categories()

        separator(body)

        # ── Notes ─────────────────────────────────────────────────────────────
        tk.Label(body, text="Notes / Details", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        muted_label(body, "Why is this important to you? Any details?").pack(anchor="w", pady=(0, PAD_SM))
        self._notes = styled_text(body, height=5, width=50)
        self._notes.pack(fill="x", pady=(0, PAD_MD))

        separator(body)

        # ── Image upload ──────────────────────────────────────────────────────
        tk.Label(body, text="Attach Image", font=FONT_SUBHEAD,
                 fg=TEXT, bg=BG).pack(anchor="w")
        muted_label(body, "Optional: Attach an inspiring photo.").pack(anchor="w", pady=(0, PAD_SM))

        img_row = tk.Frame(body, bg=BG)
        img_row.pack(anchor="w", pady=(0, PAD_MD))

        ghost_button(img_row, "📁 Choose Image",
                     command=self._pick_image,
                     pady=8).pack(side="left")

        self._img_label = tk.Label(img_row, text="No image selected",
                                   font=FONT_SMALL, fg=MUTED, bg=BG)
        self._img_label.pack(side="left", padx=PAD_MD)

        # Image preview container
        self._preview_frame = tk.Frame(body, bg=BG)
        self._preview_frame.pack(anchor="w", pady=(0, PAD_MD))

        separator(body)

        # ── Save button ───────────────────────────────────────────────────────
        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(pady=PAD_MD)

        styled_button(btn_row, "  ✦ Save Goal  ",
                      command=self._save_goal,
                      pady=12, padx=32).pack(side="left", padx=(0, PAD_MD))

        ghost_button(btn_row, "Cancel",
                     command=self._clear_and_back,
                     pady=12, padx=20).pack(side="left")

    # ── Category buttons ──────────────────────────────────────────────────────

    def _build_categories(self):
        for w in self._cat_frame.winfo_children():
            w.destroy()
        self._cat_buttons.clear()

        row = None
        for i, cat in enumerate(CATEGORIES):
            if i % 5 == 0:
                row = tk.Frame(self._cat_frame, bg=BG)
                row.pack(anchor="w", pady=2)

            color = CATEGORY_COLORS.get(cat, ACCENT)
            is_sel = self._selected_category.get() == cat
            bg_col = CARD2 if is_sel else BG
            border_col = color

            btn = tk.Button(
                row, text=cat,
                font=("Helvetica Neue", 10, "bold"),
                fg=color, bg=bg_col,
                relief="flat", cursor="hand2",
                pady=6, padx=12, bd=0,
                highlightthickness=1, highlightbackground=border_col,
                command=lambda c=cat: self._select_category(c),
            )
            btn.pack(side="left", padx=3)
            self._cat_buttons[cat] = (btn, color)

    def _select_category(self, cat):
        self._selected_category.set(cat)
        for name, (btn, color) in self._cat_buttons.items():
            if name == cat:
                btn.config(bg=CARD2)
            else:
                btn.config(bg=BG)

    # ── Image picker ──────────────────────────────────────────────────────────

    def _pick_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                       ("All files", "*.*")]
        )
        if not path:
            return
        self._image_path = path
        short = path.split("/")[-1]
        self._img_label.config(text=f"📷 {short}", fg=ACCENT2)

        # Preview
        for w in self._preview_frame.winfo_children():
            w.destroy()
        try:
            img = Image.open(path)
            img.thumbnail((200, 150))
            self._image_ref = ImageTk.PhotoImage(img)
            lbl = tk.Label(self._preview_frame, image=self._image_ref,
                           bg=BG, cursor="hand2")
            lbl.pack()
        except Exception:
            pass

    # ── Save & clear ─────────────────────────────────────────────────────────

    def _save_goal(self):
        title = self._title_entry.get().strip()
        if not title or title == "":
            messagebox.showwarning("Required", "Please enter a goal title.")
            return

        notes = self._notes.get("1.0", "end").strip()
        category = self._selected_category.get()

        goal = {
            "title": title,
            "category": category,
            "notes": notes,
            "done": False,
            "image": self._image_path,
        }
        self.controller.goals.append(goal)
        messagebox.showinfo("Saved!", f"✦ '{title}' added to your bucket list!")
        self._clear_form()
        self.controller.show_frame("view_goals")

    def _clear_form(self):
        self._title_entry.delete(0, "end")
        self._notes.delete("1.0", "end")
        self._image_path = None
        self._image_ref = None
        self._img_label.config(text="No image selected", fg=MUTED)
        for w in self._preview_frame.winfo_children():
            w.destroy()
        self._select_category("Travel")

    def _clear_and_back(self):
        self._clear_form()
        self.controller.show_frame("home")

    def refresh(self):
        pass
