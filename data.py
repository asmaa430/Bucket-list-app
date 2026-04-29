# ─── data.py ─────────────────────────────────────────────────────────────────
# Seed data and initial state

INSPIRATION_IDEAS = [
    ("See the Northern Lights", "Travel"),
    ("Learn to play guitar", "Learning"),
    ("Run a marathon", "Health"),
    ("Write a novel", "Creative"),
    ("Go skydiving", "Adventure"),
    ("Visit 10 countries", "Travel"),
    ("Learn a new language", "Learning"),
    ("Start a business", "Career"),
    ("Climb a mountain", "Adventure"),
    ("Cook a gourmet meal", "Creative"),
    ("Meditate for 30 days straight", "Health"),
    ("Go on a road trip", "Travel"),
    ("Take an improv class", "Social"),
    ("Paint a mural", "Creative"),
    ("Learn to surf", "Adventure"),
    ("Volunteer abroad", "Social"),
    ("Get a professional certification", "Career"),
    ("Build something with your hands", "Personal"),
    ("Watch a sunrise from a mountain", "Travel"),
    ("Read 50 books in a year", "Learning"),
]

DEFAULT_GOALS = [
    {
        "title": "See the Northern Lights",
        "category": "Travel",
        "notes": "Iceland or Norway in winter. Stay for at least a week to maximize chances.",
        "done": False,
        "image": None,
    },
    {
        "title": "Run a Half Marathon",
        "category": "Health",
        "notes": "Train for 3 months. Follow the Hal Higdon beginner plan.",
        "done": True,
        "image": None,
    },
    {
        "title": "Learn Spanish",
        "category": "Learning",
        "notes": "Use Duolingo daily + take a class. Goal: conversational in 1 year.",
        "done": False,
        "image": None,
    },
]

DEFAULT_PROFILE = {
    "name": "Explorer",
    "bio": "Living life to the fullest, one goal at a time ✨",
    "avatar": "🌟",
}
