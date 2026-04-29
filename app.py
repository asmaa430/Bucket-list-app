# ─── app.py ──────────────────────────────────────────────────────────────────
# Main BucketListApp controller class

import tkinter as tk
from theme import BG, ACCENT, FONT_HEADING
from data import DEFAULT_GOALS, DEFAULT_PROFILE

from screens.welcome_screen   import WelcomeScreen
from screens.home_screen      import HomeScreen
from screens.add_goal_screen  import AddGoalScreen
from screens.view_goals_screen import ViewGoalsScreen
from screens.details_screen   import DetailsScreen
from screens.completed_screen import CompletedScreen
from screens.profile_screen   import ProfileScreen


class BucketListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Bucket List")
        self.geometry("680x780")
        self.minsize(560, 600)
        self.configure(bg=BG)

        # ── App state ─────────────────────────────────────────────────────────
        self.goals = list(DEFAULT_GOALS)  # copy so default isn't mutated
        self.profile = dict(DEFAULT_PROFILE)
        self.current_goal_index = None
        self._active_screen = "welcome"

        # ── Screen registry ───────────────────────────────────────────────────
        self._container = tk.Frame(self, bg=BG)
        self._container.pack(fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self._screens = {}
        for name, cls in [
            ("welcome",    WelcomeScreen),
            ("home",       HomeScreen),
            ("add_goal",   AddGoalScreen),
            ("view_goals", ViewGoalsScreen),
            ("details",    DetailsScreen),
            ("completed",  CompletedScreen),
            ("profile",    ProfileScreen),
        ]:
            frame = cls(self._container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self._screens[name] = frame

        self.show_frame("welcome")

    # ── Navigation controller ─────────────────────────────────────────────────

    def show_frame(self, name: str):
        frame = self._screens.get(name)
        if frame is None:
            raise ValueError(f"Unknown screen: '{name}'")
        frame.tkraise()
        self._active_screen = name
        # Call refresh if it exists (to reload data)
        if hasattr(frame, "refresh"):
            frame.refresh()
