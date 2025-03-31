import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
new_folder_path = os.path.join(desktop_path, "test")
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print("Folder 'test' został utworzony na pulpicie.")
else:
    print("Folder 'test' już istnieje.")
