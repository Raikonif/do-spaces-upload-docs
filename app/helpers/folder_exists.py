import os
from pathlib import Path


def folder_exists():
    """Detect the Downloads folder based on the operating system."""
    if os.name == "nt":  # Windows
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    else:  # macOS/Linux/Android-like systems
        return os.path.join(Path.home(), "Downloads")
