import os


def folder_exists():
    home_dir = os.path.expanduser("~")
    downloads_english = os.path.join(home_dir, "Downloads")
    downloads_spanish = os.path.join(home_dir, "Descargas")
    default_dir = os.path.join(home_dir, "Desktop")
    if os.path.exists(downloads_english):
        downloads_folder = downloads_english
    elif os.path.exists(downloads_spanish):
        downloads_folder = downloads_spanish
    else:
        downloads_folder = default_dir
        print("Downloads folder not found.")
    if downloads_folder:
        print(f"Downloads folder: {downloads_folder}")

    return downloads_folder.replace("\\", "/")
