# ─── main.py ─────────────────────────────────────────────────────────────────
# Entry point for the Bucket List App

import sys
import os

# Ensure the project root is in the path so all imports resolve
sys.path.insert(0, os.path.dirname(__file__))

from app import BucketListApp


def main():
    app = BucketListApp()
    app.mainloop()


if __name__ == "__main__":
    main()
