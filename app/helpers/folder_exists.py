import os
from pathlib import Path


def folder_exists():
    """Detect the Downloads folder based on the operating system."""
    system_language = os.getenv("LANG", os.getenv("LANGUAGE", "")).lower()
    is_spanish = "es" in system_language

    if os.name == "nt":  # Windows
        downloads_folder = "Descargas" if is_spanish else "Downloads"
        return os.path.join(os.environ["USERPROFILE"], downloads_folder)
    else:  # macOS/Linux/Android-like systems
        downloads_folder = "Descargas" if is_spanish else "Downloads"
        return os.path.join(Path.home(), downloads_folder)
