import os

# Ścieżka do pulpitu
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Ścieżka do nowego folderu
new_folder_path = os.path.join(desktop_path, "test")

# Tworzenie folderu
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Folder 'test' został utworzony na pulpicie.")
else:
    print("Folder 'test' już istnieje.")
