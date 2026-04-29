# ─── theme.py ───────────────────────────────────────────────────────────────
# Central design tokens for the Bucket List App

# ── Colors ───────────────────────────────────────────────────────────────────
BG          = "#0f0f13"
SURFACE     = "#1a1a24"
CARD        = "#22222f"
CARD2       = "#2a2a3a"
ACCENT      = "#c084fc"
ACCENT2     = "#f0abfc"
GREEN       = "#4ade80"
RED         = "#f87171"
YELLOW      = "#fbbf24"
BLUE        = "#60a5fa"
TEXT        = "#f1f0f5"
MUTED       = "#8b8aa0"
BORDER      = "#33334a"
BORDER2     = "#44445a"

# ── Category colors ──────────────────────────────────────────────────────────
CATEGORY_COLORS = {
    "Travel":      "#60a5fa",
    "Adventure":   "#f97316",
    "Learning":    "#a78bfa",
    "Health":      "#4ade80",
    "Creative":    "#f0abfc",
    "Social":      "#fbbf24",
    "Career":      "#38bdf8",
    "Personal":    "#fb7185",
    "Other":       "#8b8aa0",
}

CATEGORIES = list(CATEGORY_COLORS.keys())

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_HEADING  = ("Georgia", 22, "bold")
FONT_SUBHEAD  = ("Georgia", 15, "bold")
FONT_BODY     = ("Helvetica Neue", 12)
FONT_SMALL    = ("Helvetica Neue", 10)
FONT_MONO     = ("Courier", 11)
FONT_BTN      = ("Helvetica Neue", 12, "bold")
FONT_TITLE    = ("Georgia", 32, "bold")
FONT_TAGLINE  = ("Georgia", 14, "italic")

# ── Spacing ───────────────────────────────────────────────────────────────────
PAD_LG  = 24
PAD_MD  = 16
PAD_SM  = 8
PAD_XS  = 4

RADIUS  = 12   # simulated border-radius via relief/border tricks
